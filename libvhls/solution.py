from pathlib import Path


class Solution:
    def __init__(
        self,
        dir: Path,
    ):
        self.dir = dir

    @classmethod
    def parse_from_dir(cls, dir: Path) -> "Solution":
        # check if dir is a solution dir

        return cls(dir=dir)

    @property
    def name(self) -> str:
        return self.dir.name
