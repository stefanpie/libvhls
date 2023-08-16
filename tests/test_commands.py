from pathlib import Path

from rich.pretty import pprint as pp

from libvhls.commands import ListPart, OpenProject, UserTCL
from libvhls.logging_config import configure_logging
from libvhls.vitis_hls import VitisHLS

configure_logging(True)


def test_vitis_hls_init(tmp_path):
    vhls = VitisHLS(wd=tmp_path, enable_logging=True)
    assert vhls
    assert vhls.dist


def check_command_otuput_generic(wd, result):
    assert Path(wd, "vitis_hls.log").exists()
    assert result.returncode == 0


def test_command_user_tcl(tmp_path):
    vhls = VitisHLS(wd=tmp_path, enable_logging=True)
    custom_tcl = 'puts "Hello World"'
    commands = [UserTCL(custom_tcl)]
    r = vhls.run(commands)

    check_command_otuput_generic(tmp_path, r)
    assert "Hello World" in r.log


def test_command_open_project(tmp_path):
    vhls = VitisHLS(wd=tmp_path, enable_logging=True)
    commands = [OpenProject("test_project", reset=True)]
    r = vhls.run(commands)

    check_command_otuput_generic(tmp_path, r)
    assert Path(tmp_path, "test_project").exists()


def test_command_get_part(tmp_path):
    vhls = VitisHLS(wd=tmp_path, enable_logging=True)
    commands = [ListPart()]
    r = vhls.run(commands)

    check_command_otuput_generic(tmp_path, r)


def test_multi_command(tmp_path):
    vhls = VitisHLS(wd=tmp_path, enable_logging=True)
    commands = [
        OpenProject("test_project", reset=True),
        ListPart(),
        UserTCL('puts "Hello World"'),
    ]
    r = vhls.run(commands)

    check_command_otuput_generic(tmp_path, r)
    assert Path(tmp_path, "test_project").exists()
    assert "Hello World" in r.log
