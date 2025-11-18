import shutil
from pathlib import Path

from rich.pretty import pprint as pp

from libvhls.commands import (
    AddFiles,
    CreateClock,
    CsynthDesign,
    ListPart,
    OpenProject,
    OpenSolution,
    SetPart,
    SetTop,
    UserTCL,
)
from libvhls.logging_config import configure_logging
from libvhls.project import Project
from libvhls.vitis_hls import VitisHLS
from tests.utils import check_command_otuput_generic

configure_logging(True)

MM_DESIGN_DIR = Path(__file__).parent / "resources" / "simple_mm_design"


def test_project_creation(tmp_path):
    vhls = VitisHLS(wd=tmp_path, enable_logging=True)
    commands = [OpenProject("test_project", reset=True)]
    r = vhls.run(commands)
    check_command_otuput_generic(tmp_path, r)

    # show all files in the working directory
    pp(list((tmp_path / "test_project").iterdir()))
    assert (tmp_path / "test_project" / "hls.app").exists()

    p = Project.parse_from_disk(tmp_path / "test_project")
    pp(p.hls_app)


def test_project_csynth(tmp_path):
    vhls = VitisHLS(wd=tmp_path, enable_logging=True)

    # copy the mm design to the working directory
    mm_design_dir = tmp_path / "mm_design"
    mm_design_dir.mkdir()
    for f in MM_DESIGN_DIR.iterdir():
        shutil.copy(f, mm_design_dir / f.name)

    commands = [
        OpenProject("test_project", reset=True),
        AddFiles(
            [
                mm_design_dir / "mm.cpp",
                mm_design_dir / "mm.h",
            ]
        ),
    ]

    r = vhls.run(commands)
    check_command_otuput_generic(tmp_path, r)

    commands = [
        OpenProject("test_project"),
        OpenSolution(
            "solution1",
            flow_target="vitis",
            reset=True,
        ),
        CreateClock("clk", "3.33"),
        SetPart("xcvu9p-flgb2104-2-i"),
        SetTop("blockmatmul"),
    ]

    r = vhls.run(commands)
    check_command_otuput_generic(tmp_path, r)

    commands = [
        OpenProject("test_project"),
        OpenSolution("solution1"),
        CsynthDesign(),
    ]

    r = vhls.run(commands)
    pp(r)
    check_command_otuput_generic(tmp_path, r)
