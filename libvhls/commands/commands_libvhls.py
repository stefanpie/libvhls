import logging
from dataclasses import dataclass
from pathlib import Path

from libvhls.commands.commands import Command
from libvhls.dist import VitisHLSDist

log = logging.getLogger(__name__)


@dataclass
class UserTCL(Command):
    tcl: str

    def __post_init__(self) -> None:
        super().__init__("libvhls_user_tcl")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        return self.tcl


@dataclass
class ExexInTCL(Command):
    exec_command: str

    def __post_init__(self) -> None:
        super().__init__("libvhls_exec_in_tcl")

    def compose(self, dist: VitisHLSDist, wd: Path) -> str:
        return f"exec {self.exec_command}"


COMMANDS_LIBVHLS = [UserTCL, ExexInTCL]
# __all__ = [cls.__name__ for cls in COMMANDS_LIBVHLS]
