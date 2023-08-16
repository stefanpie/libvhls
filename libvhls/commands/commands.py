import logging
import subprocess
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Sequence

from libvhls.dist import VitisHLSDist

log = logging.getLogger(__name__)


class RunnerStatus(Enum):
    SUCCESS = auto()
    FAIL = auto()


@dataclass(frozen=True, slots=True)
class RunnerResult:
    commands: Sequence["Command"]
    script: str
    returncode: int
    stdout: str
    stderr: str
    log: str

    @property
    def status(self) -> RunnerStatus:
        if self.returncode == 0:
            return RunnerStatus.SUCCESS
        else:
            return RunnerStatus.FAIL


class Command(ABC):
    def __init__(self, command_str: str) -> None:
        self.command_str = command_str

    @abstractmethod
    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        pass


class Runner:
    def __init__(self, dist: VitisHLSDist, wd: Path) -> None:
        self.dist = dist
        self.wd = wd

    def build_script(self, commands: Sequence[Command]) -> str:
        script = ""
        for cmd in commands:
            script += cmd.compose(self.dist, self.wd)
            script += "\n"
        return script

    def run(self, commands: Sequence[Command]) -> RunnerResult:
        script = self.build_script(commands)
        script_file = tempfile.NamedTemporaryFile(mode="w", suffix=".tcl", delete=False)
        script_fp = Path(script_file.name)
        script_fp.write_text(script)

        s = subprocess.run(
            [str(self.dist.vitis_hls_bin), str(script_fp)],
            cwd=self.wd,
            capture_output=True,
            text=True,
        )

        script_file.close()

        # capture log file
        log_path = self.wd / "vitis_hls.log"
        if not log_path.exists():
            raise RuntimeError(f"Log file {log_path} does not exist")
        log_text = log_path.read_text()

        result = RunnerResult(
            commands=commands,
            script=script,
            returncode=s.returncode,
            stdout=s.stdout,
            stderr=s.stderr,
            log=log_text,
        )

        return result
