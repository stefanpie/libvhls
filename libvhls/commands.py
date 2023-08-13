from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

from libvhls.dist import VitisHLSDist


class CommandStatus(Enum):
    SUCCESS = auto()
    FAIL = auto()


@dataclass(frozen=True, slots=True)
class CommandResult:
    cmd: str
    cmd_obj: "Command"
    status: CommandStatus
    returncode: int
    stdout: str | None
    stderr: str | None


class Command(ABC):
    def __init__(
        self, cmd_str: str, cmd_args: list[str] = [], cmd_kwargs: dict = {}
    ) -> None:
        self.cmd_str = cmd_str
        self.cmd_args = cmd_args
        self.cmd_kwargs = cmd_kwargs

    @abstractmethod
    def compose_command(self, dist: VitisHLSDist, cwd: Path) -> str:
        pass

    @abstractmethod
    def run(self, dist: VitisHLSDist, cwd: Path) -> CommandResult:
        pass


class CommandFailedException(Exception):
    def __init__(self, result: CommandResult):
        notes = f"""
        cmd: {result.cmd}
        returncode: {result.returncode}
        stdout:\n{result.stdout}
        stderr:\n{result.stderr}
        """
        super().__init__(f"Command {result.cmd_obj.__class__.__name__} failed" + notes)


def check_command_result(result: CommandResult) -> None:
    if result.status == CommandStatus.FAIL:
        raise CommandFailedException(result)


class OpenProject(Command):
    def __init__(
        self, project_name: str, reset: bool = False, upgrade: bool = False
    ) -> None:
        super().__init__(
            "open_project", [project_name], {"reset": reset, "upgrade": upgrade}
        )

    def compose_command(self, dist: VitisHLSDist, cwd: Path) -> str:
        raise NotImplementedError

    def run(self, dist: VitisHLSDist, cwd: Path) -> CommandResult:
        raise NotImplementedError


class Runner:
    def __init__(self, dist: VitisHLSDist, cwd: Path) -> None:
        self.dist = dist
        self.cwd = cwd

    def run_single_command(self, cmd: Command) -> None:
        cmd.run(self.dist, self.cwd)

    def run_multiple_commands(self, cmds: list[Command]) -> None:
        for cmd in cmds:
            cmd.run(self.dist, self.cwd)

    def run(self, cmd: Command | list[Command]) -> None:
        if isinstance(cmd, Command):
            self.run_single_command(cmd)
        elif isinstance(cmd, list):
            self.run_multiple_commands(cmd)
        else:
            raise TypeError("`cmd` arg must be a single Command or a list of Commands")


SUPPORTED_COMMANDS = [OpenProject]
