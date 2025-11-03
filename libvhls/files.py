from enum import Enum, auto
from pathlib import Path


class FileType(Enum):
    SOURCE = auto()
    HEADER = auto()
    BINARY = auto()
    CONFIG = auto()
    IR = auto()
    OTHER = auto()


class File:
    def __init__(self, path: Path, type: FileType | None = None):
        self.path = path

        if type is None:
            auto_result = File.auto_type(path)
            if auto_result is None:
                raise ValueError(
                    f"Could not auto detect the file type of {path}. Please specify it"
                    " manually."
                )
            self.type = auto_result
        else:
            self.type = type

    @staticmethod
    def auto_type(fp: Path) -> FileType | None:
        if fp.suffix.lower() in (".c", ".cpp", ".cc", ".cxx"):
            return FileType.SOURCE
        elif fp.suffix.lower() in (".h", ".hpp", ".hh", ".hxx"):
            return FileType.HEADER
        else:
            return None
