from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


@dataclass
class ProjectFiles:
    name: str
    sc: str
    tb: str
    cflags: str
    csimflags: str
    blackbox: str


@dataclass
class HLSApp:
    project_type: str
    top: str
    name: str
    files: list[ProjectFiles]
    solutions: list

    @classmethod
    def parse_from_disk(cls, path: Path) -> "HLSApp":
        root = ET.fromstring(path.read_text())
        project_type = str(root.get("projectType"))
        top = str(root.get("top"))
        name = str(root.get("name"))

        files: list[ProjectFiles] = []
        if root.find("files") is not None:
            for file in root.find("files").findall("file"):
                files.append(
                    ProjectFiles(
                        name=str(file.get("name")),
                        sc=str(file.get("sc")),
                        tb=str(file.get("tb")),
                        cflags=str(file.get("cflags")),
                        csimflags=str(file.get("csimflags")),
                        blackbox=str(file.get("blackbox")),
                    )
                )

        solutions = []
        if root.find("solutions") is not None:
            for solution in root.find("solutions").findall("solution"):
                solutions.append(
                    {"name": solution.get("name"), "status": solution.get("status")}
                )

        return cls(
            project_type=project_type,
            top=top,
            name=name,
            files=files,
            solutions=solutions,
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class Project:
    dir: Path
    hls_app: HLSApp

    @classmethod
    def parse_from_disk(cls, path: Path) -> "Project":
        hls_app_fp = path / "hls.app"
        if not hls_app_fp.exists():
            raise Exception(f"Could not find hls.app in {path}")
        hls_app = HLSApp.parse_from_disk(hls_app_fp)
        return cls(dir=path, hls_app=hls_app)
