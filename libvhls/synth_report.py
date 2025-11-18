import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from libvhls.utils import unwrap


@dataclass
class RTLPort:
    name: str
    object: str
    type: str
    io_protocol: str
    dir: str
    bits: int
    attribute: str
    c_type: str
    has_ctrl: int

    @classmethod
    def from_xml_element(cls, xml_element: ET.Element) -> "RTLPort":
        name = unwrap(unwrap(xml_element.find("Name")).text)
        object = unwrap(unwrap(xml_element.find("Object")).text)
        type = unwrap(unwrap(xml_element.find("Type")).text)
        io_protocol = unwrap(unwrap(xml_element.find("IOProtocol")).text)
        dir = unwrap(unwrap(xml_element.find("Dir")).text)
        bits = int(unwrap(unwrap(xml_element.find("Bits")).text))
        attribute = unwrap(unwrap(xml_element.find("Attribute")).text)
        c_type = unwrap(unwrap(xml_element.find("CType")).text)
        has_ctrl = int(unwrap(unwrap(xml_element.find("HasCtrl")).text))
        return cls(
            name=name,
            object=object,
            type=type,
            io_protocol=io_protocol,
            dir=dir,
            bits=bits,
            attribute=attribute,
            c_type=c_type,
            has_ctrl=has_ctrl,
        )


@dataclass
class InterfaceSummary:
    rtl_ports: list[RTLPort] = field(default_factory=list)

    @classmethod
    def from_xml_element(cls, xml_element: ET.Element) -> "InterfaceSummary":
        return cls(
            rtl_ports=[
                RTLPort.from_xml_element(x) for x in xml_element.findall("RTLPorts")
            ]
        )


@dataclass
class TopLevelLatencyData:
    clock_period: float

    best_case_latency_c: int | None
    average_case_latency_c: int | None
    worst_case_latency_c: int | None

    best_case_latency_t: float | None
    average_case_latency_t: float | None
    worst_case_latency_t: float | None

    @property
    def latency_c(self):
        return self.average_case_latency_c

    @property
    def latency_t(self):
        return self.average_case_latency_t

    @property
    def is_latency_fully_estimated(self):
        b = True
        b &= self.best_case_latency_c is not None
        b &= self.average_case_latency_c is not None
        b &= self.worst_case_latency_c is not None
        return b


@dataclass
class TopLevelResourceData:
    used_abs: dict[str, int]
    available_abs: dict[str, int]
    used_percent: dict[str, float]

    def __post_init__(self):
        resource_types = ["BRAM_18K", "DSP", "FF", "LUT", "URAM"]
        for resource_type in resource_types:
            if resource_type not in self.used_abs:
                raise ValueError(f"Missing resource type {resource_type} in used_abs")
            if resource_type not in self.available_abs:
                raise ValueError(
                    f"Missing resource type {resource_type} in available_abs"
                )
            if resource_type not in self.used_percent:
                raise ValueError(
                    f"Missing resource type {resource_type} in used_percent"
                )

    @property
    def resource_types(self):
        return list(self.used_abs.keys())


def parse_latency_str(
    latency_str: str, target_clock_period: float
) -> tuple[int, float]:
    if latency_str == "undef":
        raise ValueError("Latency string is 'undef', cannot parse.")
    else:
        cycles = int(latency_str)
        return cycles, cycles * target_clock_period


def parse_report(xml_str):
    root = ET.fromstring(xml_str)

    # Gather latency data
    target_clock_period = (
        float(
            unwrap(
                unwrap(
                    unwrap(root.find("UserAssignments")).find("TargetClockPeriod")
                ).text
            )
        )
        / 1_000_000_000
    )
    performance_estimates = unwrap(root.find("PerformanceEstimates"))
    summary_of_overall_latency = unwrap(
        performance_estimates.find("SummaryOfOverallLatency")
    )
    # latency_data: dict[str, int | float] = {}

    # fmt: off
    best_case_latency_str = unwrap(unwrap(summary_of_overall_latency.find("Best-caseLatency")).text)
    average_case_latency_str = unwrap(unwrap(summary_of_overall_latency.find("Average-caseLatency")).text)
    worst_case_latency_str = unwrap(unwrap(summary_of_overall_latency.find("Worst-caseLatency")).text)

    latency_best_c, latency_best_t = parse_latency_str(best_case_latency_str, target_clock_period)
    latency_avg_c, latency_avg_t = parse_latency_str(average_case_latency_str, target_clock_period)
    latency_worst_c, latency_worst_t = parse_latency_str(worst_case_latency_str, target_clock_period)
    # fmt: on

    top_level_latency_data = TopLevelLatencyData(
        clock_period=target_clock_period,
        best_case_latency_c=latency_best_c,
        average_case_latency_c=latency_avg_c,
        worst_case_latency_c=latency_worst_c,
        best_case_latency_t=latency_best_t,
        average_case_latency_t=latency_avg_t,
        worst_case_latency_t=latency_worst_t,
    )

    # Gather resource data
    area_estimates = unwrap(root.find("AreaEstimates"))
    resources = unwrap(area_estimates.find("Resources"))
    available_resources = unwrap(area_estimates.find("AvailableResources"))

    resource_data_abs: dict[str, int] = {}
    resource_data_avail: dict[str, int] = {}
    resource_data_percent: dict[str, float] = {}

    # fmt: off
    resource_data_abs["BRAM_18K"] = int( unwrap(unwrap(resources.find("BRAM_18K")).text) )
    resource_data_abs["DSP"] = int( unwrap(unwrap(resources.find("DSP")).text) )
    resource_data_abs["FF"] = int( unwrap(unwrap(resources.find("FF")).text) )
    resource_data_abs["LUT"] = int( unwrap(unwrap(resources.find("LUT")).text) )
    resource_data_abs["URAM"] = int( unwrap(unwrap(resources.find("URAM")).text) )
    resource_data_avail["BRAM_18K"] = int( unwrap(unwrap(available_resources.find("BRAM_18K")).text) )
    resource_data_avail["DSP"] = int( unwrap(unwrap(available_resources.find("DSP")).text) )
    resource_data_avail["FF"] = int( unwrap(unwrap(available_resources.find("FF")).text) )
    resource_data_avail["LUT"] = int( unwrap(unwrap(available_resources.find("LUT")).text) )
    resource_data_avail["URAM"] = int( unwrap(unwrap(available_resources.find("URAM")).text) )
    resource_data_percent["BRAM_18K"] = float(resource_data_abs["BRAM_18K"] / resource_data_avail["BRAM_18K"])
    resource_data_percent["DSP"] = float(resource_data_abs["DSP"] / resource_data_avail["DSP"])
    resource_data_percent["FF"] = float(resource_data_abs["FF"] / resource_data_avail["FF"])
    resource_data_percent["LUT"] = float(resource_data_abs["LUT"] / resource_data_avail["LUT"])
    resource_data_percent["URAM"] = float(resource_data_abs["URAM"] / resource_data_avail["URAM"])
    # fmt: on

    top_level_resource_data = TopLevelResourceData(
        used_abs=resource_data_abs,
        available_abs=resource_data_avail,
        used_percent=resource_data_percent,
    )

    # Gather interface data
    interface_summary = InterfaceSummary.from_xml_element(
        unwrap(root.find("InterfaceSummary"))
    )

    return top_level_latency_data, top_level_resource_data, interface_summary


@dataclass
class SynthesisReport:
    top_level_latency_data: TopLevelLatencyData
    top_level_resource_data: TopLevelResourceData
    interface_summary: InterfaceSummary

    @classmethod
    def parse_from_disk(cls, path: Path) -> "SynthesisReport":
        top_level_latency_data, top_level_resource_data, interface_summary = (
            parse_report(path.read_text())
        )
        return cls(
            top_level_latency_data=top_level_latency_data,
            top_level_resource_data=top_level_resource_data,
            interface_summary=interface_summary,
        )
