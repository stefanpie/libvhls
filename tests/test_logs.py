from pathlib import Path

import pytest

from libvhls.hls_logs import HLSLog, RuntimeInfo

LOG_GOOD_PATH = Path(__file__).parent / "resources" / "logs" / "log_good.txt"


@pytest.fixture
def log_good():
    """Load the good log file for testing."""
    with open(LOG_GOOD_PATH) as f:
        return f.read()


@pytest.fixture
def hls_log(log_good):
    """Create an HLSLog instance from the good log."""
    return HLSLog(log_good)


def test_hls_log_init(log_good):
    """Test HLSLog initialization."""
    log = HLSLog(log_good)
    assert log.txt == log_good
    assert isinstance(log, HLSLog)


def test_hls_log_lines(hls_log):
    """Test that lines() returns a list of lines."""
    lines = hls_log.lines()
    assert isinstance(lines, list)
    assert len(lines) > 0
    # Check that the first line matches expected content
    assert lines[0].startswith("****** Vitis HLS")


def test_hls_log_warnings(hls_log):
    """Test that warnings() extracts all WARNING lines."""
    warnings = hls_log.warnings()
    assert isinstance(warnings, list)
    # From the log file, we can see several warnings
    assert len(warnings) > 0
    # All returned lines should contain WARNING:
    for warning in warnings:
        assert "WARNING:" in warning
    # Check for specific warnings we know are in the log
    warning_texts = " ".join(warnings)
    assert "HLS 200-2053" in warning_texts
    assert "HLS 214-111" in warning_texts


def test_hls_log_errors(hls_log):
    """Test that errors() extracts all ERROR lines."""
    errors = hls_log.errors()
    assert isinstance(errors, list)
    # The good log should not have any errors
    assert len(errors) == 0


def test_hls_log_infos(hls_log):
    """Test that infos() extracts all INFO lines."""
    infos = hls_log.infos()
    assert isinstance(infos, list)
    assert len(infos) > 0
    # All returned lines should contain INFO:
    for info in infos:
        assert "INFO:" in info
    # Check for specific info messages we know are in the log
    info_texts = " ".join(infos)
    assert "HLS 200-10" in info_texts
    assert "Opening project" in info_texts


def test_hls_log_runtimes(hls_log):
    """Test that runtimes() extracts all runtime information."""
    runtimes = hls_log.runtimes()
    assert isinstance(runtimes, list)
    assert len(runtimes) > 0

    # All items should be RuntimeInfo instances
    for runtime in runtimes:
        assert isinstance(runtime, RuntimeInfo)
        assert isinstance(runtime.phase, str)
        assert isinstance(runtime.cpu_user, float)
        assert isinstance(runtime.cpu_sys, float)
        assert isinstance(runtime.elapsed, float)
        # Times should be non-negative
        assert runtime.cpu_user >= 0
        assert runtime.cpu_sys >= 0
        assert runtime.elapsed >= 0

    # Check for specific phases we know are in the log
    phases = [r.phase for r in runtimes]
    assert "File checks and directory preparation" in phases
    assert "Source Code Analysis and Preprocessing" in phases
    assert "Compiling Optimization and Transform" in phases


def test_runtime_info_dataclass():
    """Test RuntimeInfo dataclass."""
    runtime = RuntimeInfo(phase="Test Phase", cpu_user=1.5, cpu_sys=0.5, elapsed=2.0)
    assert runtime.phase == "Test Phase"
    assert runtime.cpu_user == 1.5
    assert runtime.cpu_sys == 0.5
    assert runtime.elapsed == 2.0


def test_hls_log_with_empty_string():
    """Test HLSLog with an empty string."""
    log = HLSLog("")
    assert log.lines() == []
    assert log.warnings() == []
    assert log.errors() == []
    assert log.infos() == []
    assert log.runtimes() == []


def test_hls_log_warnings_count(hls_log):
    """Test that we get the expected number of warnings from the good log."""
    warnings = hls_log.warnings()
    # From the log file, count the number of WARNING: occurrences
    # Lines: 12, 31, 33, 35, 68, 90, 94, 95, 114, 116, 255
    assert len(warnings) >= 10  # At least 10 warnings in the file


def test_hls_log_infos_count(hls_log):
    """Test that we get a reasonable number of info messages."""
    infos = hls_log.infos()
    # The log file has many INFO messages
    assert len(infos) > 50  # Should have many info messages


def test_hls_log_specific_runtime_values(hls_log):
    """Test specific runtime values from the log."""
    runtimes = hls_log.runtimes()

    # Find the first runtime entry
    if len(runtimes) > 0:
        first_runtime = runtimes[0]
        assert first_runtime.phase == "File checks and directory preparation"
        assert first_runtime.cpu_user == 0.04
        assert first_runtime.cpu_sys == 0.0
        assert first_runtime.elapsed == 0.05

    # Find another specific entry
    phase_names = {r.phase: r for r in runtimes}
    if "Source Code Analysis and Preprocessing" in phase_names:
        runtime = phase_names["Source Code Analysis and Preprocessing"]
        assert runtime.cpu_user == 0.28
        assert runtime.cpu_sys == 0.39
        assert runtime.elapsed == 0.69


def test_hls_log_regex_pattern():
    """Test the regex pattern directly."""
    test_line = "INFO: [HLS 200-111] Finished Test Phase: CPU user time: 1.23 seconds. CPU system time: 0.45 seconds. Elapsed time: 1.68 seconds; current allocated memory: 0.000 MB."
    log = HLSLog(test_line)
    runtimes = log.runtimes()

    assert len(runtimes) == 1
    assert runtimes[0].phase == "Test Phase"
    assert runtimes[0].cpu_user == 1.23
    assert runtimes[0].cpu_sys == 0.45
    assert runtimes[0].elapsed == 1.68
