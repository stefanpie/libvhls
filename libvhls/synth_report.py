from xml import ElementTree as ET


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
