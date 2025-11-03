from pathlib import Path


def check_command_otuput_generic(wd, result):
    assert Path(wd, "vitis_hls.log").exists()
    assert result.returncode == 0
