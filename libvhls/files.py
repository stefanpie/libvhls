from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path


class FileType(Enum):
    SOURCE = auto()
    HEADER = auto()
    BINARY = auto()


@dataclass(frozen=True, slots=True)
class File:
    path: Path

    @property
    def type(self):
        if self.path.suffix.lower() in (".c", ".cpp", ".cc", ".cxx"):
            return FileType.SOURCE
        if self.path.suffix.lower() in (".h", ".hpp", ".hh", ".hxx"):
            return FileType.HEADER
        return FileType.BINARY
