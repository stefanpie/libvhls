import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from string import Template
from tempfile import TemporaryDirectory
from textwrap import dedent

import matplotlib.pyplot as plt
from joblib import Parallel, delayed

from libvhls.commands import (
    AddFiles,
    CreateClock,
    CsynthDesign,
    OpenProject,
    OpenSolution,
    RunnerStatus,
    SetPart,
    SetTop,
)
from libvhls.vitis_hls import VitisHLS

header_tempate = Template(
    dedent("""
    #ifndef _BLOCK_MM_H_
    #define _BLOCK_MM_H_
    #include "hls_stream.h"
    #include <iostream>
    #include <iomanip>
    #include <vector>
    using namespace std;

    typedef int DTYPE;
    const int SIZE = 256;
    const int BLOCK_SIZE = ${BLOCK_SIZE};

    typedef struct { DTYPE a[BLOCK_SIZE]; } blockvec;

    typedef struct { DTYPE out[BLOCK_SIZE][BLOCK_SIZE]; } blockmat;

    void blockmatmul(hls::stream<blockvec> &Arows, hls::stream<blockvec> &Bcols,
                                    blockmat & ABpartial, DTYPE iteration);
    #endif
""")
)

source_tempate = Template(
    dedent("""
#include "block_mm.h"
void blockmatmul(hls::stream<blockvec> &Arows, hls::stream<blockvec> &Bcols,
        blockmat &ABpartial, int it) {
  #pragma HLS DATAFLOW
  int counter = it % (SIZE/BLOCK_SIZE);
  static DTYPE A[BLOCK_SIZE][SIZE];
  if(counter == 0){ //only load the A rows when necessary
    loadA: for(int i = 0; i < SIZE; i++) {
      blockvec tempA = Arows.read();
      for(int j = 0; j < BLOCK_SIZE; j++) {
        #pragma HLS PIPELINE II=1
        A[j][i] = tempA.a[j];
      }
    }
  }
  DTYPE AB[BLOCK_SIZE][BLOCK_SIZE] = { 0 };
  partialsum: for(int k=0; k < SIZE; k++) {
    blockvec tempB = Bcols.read();
    for(int i = 0; i < BLOCK_SIZE; i++) {
      for(int j = 0; j < BLOCK_SIZE; j++) {
        AB[i][j] = AB[i][j] +  A[i][k] * tempB.a[j];
      }
    }
  }
  writeoutput: for(int i = 0; i < BLOCK_SIZE; i++) {
    for(int j = 0; j < BLOCK_SIZE; j++) {
      ABpartial.out[i][j] = AB[i][j];
    }
  }
}
""")
)


def generate_paramaterized_design(dir: Path, block_size=8) -> list[Path]:
    header = header_tempate.substitute(BLOCK_SIZE=block_size)
    source = source_tempate.substitute()
    header_file = dir / "block_mm.h"
    source_file = dir / "block_mm.cpp"
    header_file.write_text(header)
    source_file.write_text(source)
    return [header_file, source_file]


def parse_report(xml_str):
    root = ET.fromstring(xml_str)

    # Gather latency data
    performance_estimates = root.find("PerformanceEstimates")
    summary_of_overall_latency = performance_estimates.find("SummaryOfOverallLatency")
    latency_data = {}
    # fmt: off
    latency_data["best_case_latency"] = int(summary_of_overall_latency.find("Best-caseLatency").text)
    latency_data["average_case_latency"] = int(summary_of_overall_latency.find("Average-caseLatency").text)
    latency_data["worst_case_latency"] = int(summary_of_overall_latency.find("Worst-caseLatency").text)
    latency_data["best_case_latency_t"] = float(summary_of_overall_latency.find("Best-caseRealTimeLatency").text.split()[0])
    latency_data["average_case_latency_t"] = float(summary_of_overall_latency.find("Average-caseRealTimeLatency").text.split()[0])
    latency_data["worst_case_latency_t"] = float(summary_of_overall_latency.find("Worst-caseRealTimeLatency").text.split()[0])
    # fmt: on

    # Gather resource data
    area_estimates = root.find("AreaEstimates")
    resource_data = {}
    # fmt: off
    resource_data["used_abs"] = {}
    resource_data["used_abs"]["BRAM_18K"] = int( area_estimates.find("Resources").find("BRAM_18K").text )
    resource_data["used_abs"]["DSP"] = int(area_estimates.find("Resources").find("DSP").text)
    resource_data["used_abs"]["FF"] = int(area_estimates.find("Resources").find("FF").text)
    resource_data["used_abs"]["LUT"] = int(area_estimates.find("Resources").find("LUT").text)
    resource_data["used_abs"]["URAM"] = int( area_estimates.find("Resources").find("URAM").text )
    resource_data["available_abs"] = {}
    resource_data["available_abs"]["BRAM_18K"] = int( area_estimates.find("AvailableResources").find("BRAM_18K").text )
    resource_data["available_abs"]["DSP"] = int( area_estimates.find("AvailableResources").find("DSP").text )
    resource_data["available_abs"]["FF"] = int( area_estimates.find("AvailableResources").find("FF").text )
    resource_data["available_abs"]["LUT"] = int( area_estimates.find("AvailableResources").find("LUT").text )
    resource_data["available_abs"]["URAM"] = int( area_estimates.find("AvailableResources").find("URAM").text )
    resource_data["used_percent"] = {}
    resource_data["used_percent"]["BRAM_18K"] = float(resource_data["used_abs"]["BRAM_18K"] / resource_data["available_abs"]["BRAM_18K"])
    resource_data["used_percent"]["DSP"] = float(resource_data["used_abs"]["DSP"] / resource_data["available_abs"]["DSP"])
    resource_data["used_percent"]["FF"] = float(resource_data["used_abs"]["FF"] / resource_data["available_abs"]["FF"])
    resource_data["used_percent"]["LUT"] = float(resource_data["used_abs"]["LUT"] / resource_data["available_abs"]["LUT"])
    resource_data["used_percent"]["URAM"] = float(resource_data["used_abs"]["URAM"] / resource_data["available_abs"]["URAM"])
    # fmt: on

    data = {
        "latency": latency_data,
        "resources": resource_data,
    }
    return data


# Run a single design run
def single_design_run(block_size):
    print(f"Running design run for block_size={block_size}")

    design_name = f"block_mm_{block_size}"

    # Create design directory
    design_dir = working_dir / design_name
    design_dir.mkdir(parents=True, exist_ok=True)

    # Generate source files for parameterized design
    design_files = generate_paramaterized_design(design_dir, block_size)

    # Use libvhls to build commands and run them using Vitis HLS
    vhls = VitisHLS(wd=design_dir)
    project_name = f"{design_name}_prj"
    solution_name = f"{design_name}_sol"
    commands = [
        OpenProject(project_name, reset=True),
        AddFiles(design_files),
        OpenSolution(solution_name, reset=True),
        SetPart("xcu50-fsvh2104-2-e"),  # Alveo U50
        CreateClock("default", "3.33"),  # 3.33 ns = 300 MHz
        SetTop("blockmatmul"),
        CsynthDesign(),
    ]
    r = vhls.run(commands)
    if r.status == RunnerStatus.FAIL:
        raise RuntimeError(f"Failed to run commands\n{r}")

    # Find the synthesis report file
    csynth_xml = Path(
        list(design_dir.rglob(f"{project_name}/{solution_name}/**/csynth.xml"))[0]
    )

    # Extract data from synthesis report
    synth_data = parse_report(csynth_xml.read_text())

    return design_name, {
        "block_size": block_size,
        "synth_data": synth_data,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the DSE experiment for the block matrix multiplication design."
    )
    parser.add_argument(
        "--output_figure_dir",
        type=str,
        default=None,
        help="Directory to save the output figures generated by the experiment.",
    )
    args = parser.parse_args()

    # Setup a temporary working directory for the DSE experiment
    print("Setting up working directory...")
    working_dir_obj = TemporaryDirectory()
    working_dir = Path(working_dir_obj.name)
    print("Using working directory:", str(working_dir))

    # Define the design space
    BLOCK_SIZE_VALUES = [1, 2, 4, 8, 16, 32, 64, 128]

    # Run design runs in parallel
    print("Running design runs...")
    N_JOBS = 8
    run_data = Parallel(n_jobs=N_JOBS, backend="multiprocessing")(
        delayed(single_design_run)(block_size) for block_size in BLOCK_SIZE_VALUES
    )
    dse_data = {design_name: design_data for design_name, design_data in run_data}

    # Cleanup working directory since we are done with it
    working_dir_obj.cleanup()

    # Gather data neeed for figures
    print("Gathering data...")
    index = []
    block_sizes = []
    avg_latency_ts = []
    percent_used_bram = []
    percent_used_dsp = []
    percent_used_ff = []
    percent_used_lut = []
    for i, design in enumerate(dse_data.values()):
        index.append(i)
        block_sizes.append(design["block_size"])
        # fmt: off
        avg_latency_ts.append(design["synth_data"]["latency"]["average_case_latency_t"])
        percent_used_bram.append(design["synth_data"]["resources"]["used_percent"]["BRAM_18K"])
        percent_used_dsp.append(design["synth_data"]["resources"]["used_percent"]["DSP"])
        percent_used_ff.append(design["synth_data"]["resources"]["used_percent"]["FF"])
        percent_used_lut.append(design["synth_data"]["resources"]["used_percent"]["LUT"])
        # fmt: on

    # Create figures
    print("Creating figures...")
    fig, axs = plt.subplots(5, 1, figsize=(10, 12))

    axs[0].bar(index, avg_latency_ts)
    axs[0].set_xticks(index)
    axs[0].set_xticklabels(block_sizes)
    axs[0].set_xlabel("Block Size")
    axs[0].set_ylabel("Average Latency (s)")
    axs[0].set_title("Average Latency vs. Block Size")

    axs[1].bar(index, percent_used_dsp)
    axs[1].set_xticks(index)
    axs[1].set_xticklabels(block_sizes)
    axs[1].yaxis.set_major_formatter("{x:.0%}")
    axs[1].set_xlabel("Block Size")
    axs[1].set_ylabel("Percent Used")
    axs[1].set_title("DSP Resources Usage")

    axs[2].bar(index, percent_used_bram)
    axs[2].set_xticks(index)
    axs[2].set_xticklabels(block_sizes)
    axs[2].yaxis.set_major_formatter("{x:.0%}")
    axs[2].set_xlabel("Block Size")
    axs[2].set_ylabel("Percent Used")
    axs[2].set_title("BRAM Resources Usage")

    axs[3].bar(index, percent_used_ff)
    axs[3].set_xticks(index)
    axs[3].set_xticklabels(block_sizes)
    axs[3].yaxis.set_major_formatter("{x:.0%}")
    axs[3].set_xlabel("Block Size")
    axs[3].set_ylabel("Percent Used")
    axs[3].set_title("FF Resources Usage")

    axs[4].bar(index, percent_used_lut)
    axs[4].set_xticks(index)
    axs[4].set_xticklabels(block_sizes)
    axs[4].yaxis.set_major_formatter("{x:.0%}")
    axs[4].set_xlabel("Block Size")
    axs[4].set_ylabel("Percent Used")
    axs[4].set_title("LUT Resources Usage")

    plt.tight_layout()

    if args.output_figure_dir is None:
        fig_path = Path(".")
    else:
        fig_path = Path(args.output_figure_dir)
    plt.savefig(str(fig_path / "fig_dse_results.png"), dpi=600)

    # We are done!
    print("Done!")
