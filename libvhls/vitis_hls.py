import logging
import shutil
from pathlib import Path
from typing import Sequence

from libvhls.commands.commands import Command, Runner, RunnerResult
from libvhls.dist import VitisHLSDist
from libvhls.logging_config import configure_logging

log = logging.getLogger(__name__)


def auto_find_vitis_hls() -> Path | None:
    result = shutil.which("vitis_hls")
    if result is not None:
        return Path(result).parent.parent
    else:
        return None


class VitisHLS:
    def __init__(
        self,
        tool_path: Path | None = None,
        wd: Path | None = None,
        enable_logging: bool = False,
    ) -> None:
        if enable_logging:
            configure_logging(enable_logging)
        log.info("Initializing Vitis HLS instance.")

        if tool_path is None:
            auto_find_result = VitisHLSDist.auto_find()
            if auto_find_result is None:
                raise FileNotFoundError(
                    "Could not auto find Vitis HLS installation. "
                    "Please mauanlly specify the path to the Vitis HLS installation."
                )
            self.dist = auto_find_result
        else:
            self.dist = VitisHLSDist.from_bin_path(tool_path)
        log.info(f"Using Vitis HLS dist: {str(self.dist.dist_dir)}")

        if wd is None:
            self.wd = Path.cwd()
        else:
            self.wd = wd
        log.info(f"Using working dir: {str(self.wd)}")

        self.runner = Runner(self.dist, self.wd)

    def run(self, cmd: Sequence[Command]) -> RunnerResult:
        return self.runner.run(cmd)
