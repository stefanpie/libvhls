import shutil
from pathlib import Path


class VitisHLSDist:
    def __init__(self, dist_dir: Path):
        self.dist_dir = dist_dir

    @classmethod
    def from_bin_path(cls, bin_path: Path):
        return cls(bin_path.parent.parent)

    @classmethod
    def auto_find(cls):
        vitis_hls_path = shutil.which("vitis_hls")
        if vitis_hls_path is None:
            raise RuntimeError(
                "Could not find vitis_hls automatically, please specify the path"
                " manually."
            )
        return cls.from_bin_path(Path(vitis_hls_path))

    @property
    def bin_dir(self) -> Path:
        return self.dist_dir / "bin"

    @property
    def vitis_hls_bin(self) -> Path:
        return self.bin_dir / "vitis_hls"

    @property
    def include_dir(self) -> Path:
        return self.dist_dir / "include"

    @property
    def all_include_dirs(self) -> dict[str, Path]:
        dirs = {}
        dirs["include"] = self.include_dir
        for path in self.include_dir.glob("**/"):
            dirs[path.name] = path
        return dirs

    @property
    def includes(self) -> dict[str, Path]:
        includes = {}
        for path in self.include_dir.glob("**/*.h"):
            includes[path.name] = path
        return includes
