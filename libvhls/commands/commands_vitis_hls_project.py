import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from libvhls.commands.commands import Command
from libvhls.dist import VitisHLSDist

log = logging.getLogger(__name__)


@dataclass
class AddFiles(Command):
    src_files: Sequence[Path] | Path
    blackbox: str | None = None
    cflags: str | None = None
    csimflags: str | None = None
    tb: bool | None = False

    def __post_init__(self) -> None:
        super().__init__("add_files")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = ""
        c += f"{self.command_str}"
        if self.blackbox:
            c += f" -blackbox {self.blackbox}"
        if self.cflags:
            c += f" -cflags {self.cflags}"
        if self.csimflags:
            c += f" -csimflags {self.csimflags}"
        if self.tb:
            c += " -tb"

        if isinstance(self.src_files, Path):
            c += f" {str(self.src_files)}"
        elif isinstance(self.src_files, Sequence):
            c += f' "{" ".join([str(f) for f in self.src_files])}"'

        return c


class CloseProject(Command):
    def __init__(self) -> None:
        super().__init__("close_project")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        return self.command_str


class CloseSolution(Command):
    def __init__(self) -> None:
        super().__init__("close_solution")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        return self.command_str


@dataclass
class CosimDesign(Command):
    O: bool | None = None  # noqa: E741
    argv: str | None = None
    compiled_library_dir: str | None = None
    coverage: bool | None = None
    disable_binary_tv: bool | None = None
    disable_deadlock_detection: bool | None = None
    disable_dependency_check: bool | None = None
    enable_dataflow_profiling: bool | None = None
    enable_fifo_sizing: bool | None = None
    hwemu_trace_dir: str | None = None
    ldflags: str | None = None
    mflags: str | None = None
    random_stall: bool | None = None
    rtl: str | None = None
    setup: bool | None = None
    stable_axilite_update: bool | None = None
    trace_level: str | None = None
    user_stall: str | None = None
    wave_debug: bool | None = None

    def __post_init__(self) -> None:
        super().__init__("cosim_design")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "cosim_design"
        if self.O:
            c += " -O"
        if self.argv:
            c += f" -argv {self.argv}"
        if self.compiled_library_dir:
            c += f" -compiled_library_dir {self.compiled_library_dir}"
        if self.coverage:
            c += " -coverage"
        if self.disable_deadlock_detection:
            c += " -disable_deadlock_detection"
        if self.disable_dependency_check:
            c += " -disable_dependency_check"
        if self.enable_dataflow_profiling:
            c += " -enable_dataflow_profiling"
        if self.enable_fifo_sizing:
            c += " -enable_fifo_sizing"
        if self.hwemu_trace_dir:
            c += f" -hwemu_trace_dir {self.hwemu_trace_dir}"
        if self.ldflags:
            c += f" -ldflags {self.ldflags}"
        if self.mflags:
            c += f" -mflags {self.mflags}"
        if self.random_stall:
            c += " -random_stall"
        if self.rtl:
            c += f" -rtl {self.rtl}"
        if self.setup:
            c += " -setup"
        if self.stable_axilite_update:
            c += " -stable_axilite_update"
        if self.trace_level:
            c += f" -trace_level {self.trace_level}"
        if self.user_stall:
            c += f" -user_stall {self.user_stall}"
        if self.wave_debug:
            c += " -wave_debug"
        return c


@dataclass
class CosimStall(Command):
    check: str | None = None
    generate: str | None = None
    list: bool | None = None

    def __post_init__(self) -> None:
        super().__init__("cosim_stall")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "cosim_stall"
        if self.check:
            c += f" -check {self.check}"
        if self.generate:
            c += f" -generate {self.generate}"
        if self.list:
            c += " -list"
        return c


@dataclass
class CreateClock(Command):
    name: str | None = None
    period: str | None = None

    def __post_init__(self) -> None:
        super().__init__("create_clock")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "create_clock"
        if self.name:
            c += f" -name {self.name}"
        if self.period:
            c += f" -period {self.period}"
        return c


@dataclass
class CsimDesign(Command):
    O: bool | None = None  # noqa: E741
    argv: str | None = None
    clean: bool | None = None
    ldflags: str | None = None
    mflags: str | None = None
    profile: bool | None = None
    setup: bool | None = None

    def __post_init__(self) -> None:
        super().__init__("csim_design")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "csim_design"
        if self.O:
            c += " -O"
        if self.argv:
            c += f" -argv {self.argv}"
        if self.clean:
            c += " -clean"
        if self.ldflags:
            c += f" -ldflags {self.ldflags}"
        if self.mflags:
            c += f" -mflags {self.mflags}"
        if self.profile:
            c += " -profile"
        if self.setup:
            c += " -setup"
        return c


@dataclass
class CsynthDesign(Command):
    dump_cfg: bool | None = None
    dump_post_cfg: bool | None = None
    synthesis_check: bool | None = None

    def __post_init__(self) -> None:
        super().__init__("csynth_design")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "csynth_design"
        if self.dump_cfg:
            c += " -dump_cfg"
        if self.dump_post_cfg:
            c += " -dump_post_cfg"
        if self.synthesis_check:
            c += " -synthesis_check"
        return c


@dataclass
class DeleteProject(Command):
    project_name: str

    def __post_init__(self) -> None:
        super().__init__("delete_project")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = f"delete_project {self.project_name}"
        return c


@dataclass
class DeleteSolution(Command):
    solution_name: str

    def __post_init__(self) -> None:
        super().__init__("delete_solution")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = f"delete_solution {self.solution_name}"
        return c


@dataclass
class EnableBetaDevice(Command):
    pattern: str

    def __post_init__(self) -> None:
        super().__init__("enable_beta_device")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = f"enable_beta_device {self.pattern}"
        return c


@dataclass
class ExportDesign(Command):
    description: str
    display_name: str
    flow: str
    format: str
    ipname: str
    library: str
    output: str
    rtl: str
    taxonomy: str
    vendor: str
    version: str

    VALID_FLOWS = ["syn", "impl"]
    VALID_FORMATS = ["ip_catalog", "xo", "syn_dcp", "sysgen"]
    VALID_RTL = ["verilog", "VHDL"]

    def __post_init__(self) -> None:
        super().__init__("export_design")

        if self.flow not in self.VALID_FLOWS:
            raise ValueError(f"Invalid flow {self.flow}")
        if self.format not in self.VALID_FORMATS:
            raise ValueError(f"Invalid format {self.format}")
        if self.rtl not in self.VALID_RTL:
            raise ValueError(f"Invalid rtl {self.rtl}")


@dataclass
class GetClockPeriod(Command):
    default: bool | None = None
    name: str | None = None
    ns: bool | None = None

    def __post_init__(self) -> None:
        super().__init__("get_clock_period")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "get_clock_period"
        if self.default:
            c += " -default"
        if self.name:
            c += f" -name {self.name}"
        if self.ns:
            c += " -ns"
        return c


@dataclass
class GetClockUncertainty(Command):
    clock_name: str | None = None

    def __post_init__(self) -> None:
        super().__init__("get_clock_uncertainty")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "get_clock_uncertainty"
        if self.clock_name:
            c += f" {self.clock_name}"
        return c


@dataclass
class GetFiles(Command):
    cflags: bool | None = None
    fullpath: bool | None = None
    tb: bool | None = None

    def __post_init__(self) -> None:
        super().__init__("get_files")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "get_files"
        if self.cflags:
            c += " -cflags"
        if self.fullpath:
            c += " -fullpath"
        if self.tb:
            c += " -tb"
        return c


# get_part
@dataclass
class GetPart(Command):
    def __post_init__(self) -> None:
        super().__init__("get_part")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        return self.command_str


@dataclass
class GetProject(Command):
    directory: bool | None = None
    name: bool | None = None
    solutions: bool | None = None

    def __post_init__(self) -> None:
        super().__init__("get_project")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "get_project"
        if self.directory:
            c += " -directory"
        if self.name:
            c += " -name"
        if self.solutions:
            c += " -solutions"
        return c


@dataclass
class GetSolution(Command):
    directory: bool | None = None
    flow_target: bool | None = None
    json: bool | None = None
    name: bool | None = None

    def __post_init__(self) -> None:
        super().__init__("get_solution")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "get_solution"
        if self.directory:
            c += " -directory"
        if self.flow_target:
            c += " -flow_target"
        if self.json:
            c += " -json"
        if self.name:
            c += " -name"
        return c


@dataclass
class GetTop(Command):
    def __post_init__(self) -> None:
        super().__init__("get_top")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        return self.command_str


@dataclass
class Help(Command):
    lookup_command: str | None = None

    def __post_init__(self) -> None:
        super().__init__("help")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = "help"
        if self.lookup_command:
            c += f" {self.lookup_command}"
        return c


@dataclass
class ListPart(Command):
    family: str | None = None
    name: str | None = None
    board: bool | None = False
    clock_regions: bool | None = False
    slr_pblocks: bool | None = False

    def __post_init__(self) -> None:
        super().__init__("list_part")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = ""
        c += f"{self.command_str}"
        if self.family:
            c += f" {self.family}"
        if self.name:
            c += f" -name {self.name}"
        if self.board:
            c += " -board"
        if self.clock_regions:
            c += " -clock_regions"
        if self.slr_pblocks:
            c += " -slr_pblocks"
        return c


@dataclass
class OpenProject(Command):
    project_name: str
    reset: bool | None = None
    upgrade: bool | None = None

    def __post_init__(self) -> None:
        super().__init__("open_project")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = ""
        c += f"{self.command_str}"
        if self.reset:
            c += " -reset"
        if self.upgrade:
            c += " -upgrade"
        c += f" {self.project_name}"
        return c


@dataclass
class OpenSolution(Command):
    name: str
    flow_target: str | None = None
    reset: bool | None = None

    VALID_FLOW_TARGETS = ["vitis", "vivado"]

    def __post_init__(self) -> None:
        super().__init__("open_solution")

        if self.flow_target and self.flow_target not in self.VALID_FLOW_TARGETS:
            raise ValueError(f"Invalid flow target {self.flow_target}")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = ""
        c += f"{self.command_str}"
        if self.flow_target:
            c += f" -flow_target {self.flow_target}"
        if self.reset:
            c += " -reset"
        c += f" {self.name}"
        return c


@dataclass
class OpenTCLProject(Command):
    tclfile: Path

    def __post_init__(self) -> None:
        super().__init__("open_tcl_project")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = f"{self.command_str} {str(self.tclfile)}"
        return c


@dataclass
class SetClockUncertainty(Command):
    uncertainty: str
    clock_list: list[str]

    def __post_init__(self) -> None:
        super().__init__("set_clock_uncertainty")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        c = f"{self.command_str} {self.uncertainty} {' '.join(self.clock_list)}"
        return c


@dataclass
class SetPart(Command):
    device_specification: str

    def __post_init__(self) -> None:
        super().__init__("set_part")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        return f"{self.command_str} {self.device_specification}"


@dataclass
class SetTop(Command):
    name: str

    def __post_init__(self) -> None:
        super().__init__("set_top")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        return f"{self.command_str} {self.name}"


# Project Commands
COMMANDS_VITIS_HLS_PROJECT = [
    AddFiles,
    CloseProject,
    CloseSolution,
    CosimDesign,
    CosimStall,
    CreateClock,
    CsimDesign,
    CsynthDesign,
    DeleteProject,
    DeleteSolution,
    EnableBetaDevice,
    ExportDesign,
    GetClockPeriod,
    GetClockUncertainty,
    GetFiles,
    GetPart,
    GetProject,
    GetSolution,
    GetTop,
    Help,
    ListPart,
    OpenProject,
    OpenSolution,
    OpenTCLProject,
    SetClockUncertainty,
    SetPart,
    SetTop,
]
# __all__ = [cls.__name__ for cls in COMMANDS_VITIS_HLS_PROJECT]
