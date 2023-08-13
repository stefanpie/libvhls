import shutil
from pathlib import Path

from libvhls.commands import Command, Runner
from libvhls.dist import VitisHLSDist
from libvhls.project import Project


def auto_find_vitis_hls() -> Path | None:
    result = shutil.which("vitis_hls")
    if result is not None:
        return Path(result).parent.parent
    else:
        return None


class VitisHLS:
    def __init__(self, tool_path: Path | None = None, cwd: Path | None = None) -> None:
        if tool_path is None:
            self.dist = VitisHLSDist.auto_find()
        else:
            self.dist = VitisHLSDist.from_bin_path(tool_path)

        if cwd is None:
            self.cwd = Path.cwd()
        else:
            self.cwd = cwd

        self.runner = Runner(self.dist, self.cwd)
        # TODO: look into passing in a refrence of the app to the runner
        # for example, open_project may want to update the
        # project vaiable in the app instance
        self.project: Project | None = None

    def run(self, cmd: Command | list[Command]) -> None:
        self.runner.run(cmd)
