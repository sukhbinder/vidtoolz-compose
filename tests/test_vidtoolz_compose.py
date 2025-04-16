import pytest
import vidtoolz_compose as w
import os
import subprocess
from unittest.mock import mock_open, patch

from argparse import ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    result = parser.parse_args(["hello"])
    assert result.input == "hello"
    assert result.debug is False
    assert result.valid is False


def test_plugin(capsys):
    w.compose_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out


@pytest.fixture
def mock_file(tmp_path):
    content = """
# continous, howmany=3,audfile="audio1.mp3",prefix=prefix1
video1.mov
video2.mov
video3.mov
# mconcat
video4.mov
# continous, howmany=2,audio=audio2,prefix=prefix2,startat=10
video5.mov
video6.mov
"""
    input_file = tmp_path / "input.txt"
    input_file.write_text(content)
    return str(input_file)


def test_compose_video_file_creation(mock_file, tmp_path):
    w.compose_video(mock_file)
    assert os.path.exists(tmp_path / "file_0.txt")
    assert os.path.exists(tmp_path / "file_1.txt")
    assert os.path.exists(tmp_path / "file_2.txt")
    assert os.path.exists(tmp_path / "cmds.txt")

    with open(tmp_path / "file_0.txt", "r") as f:
        assert f.read() == "video1.mov\nvideo2.mov\nvideo3.mov"

    with open(tmp_path / "file_1.txt", "r") as f:
        assert f.read() == "video4.mov"

    with open(tmp_path / "file_2.txt", "r") as f:
        assert f.read() == "video5.mov\nvideo6.mov"

    with open(tmp_path / "cmds.txt", "r") as f:
        cmds = f.read().splitlines()
        assert (
            cmds[0]
            == f"continous {tmp_path / 'file_0.txt'} --howmany 3 --audfile audio1.mp3 --prefix prefix1"
        )
        assert cmds[1] == f"mconcat {tmp_path / 'file_1.txt'}"
        assert (
            cmds[2]
            == f"continous {tmp_path / 'file_2.txt'} --howmany 2 --audio audio2 --prefix prefix2 --startat 10"
        )


def test_compose_video_debug_mode(mock_file, tmp_path, capsys):
    w.compose_video(mock_file, debug=True)
    captured = capsys.readouterr()
    assert (
        f"['continous', '{tmp_path / 'file_0.txt'}', '--howmany', '3', '--audfile', 'audio1.mp3', '--prefix', 'prefix1']"
        in captured.out
    )
    assert f"['mconcat', '{tmp_path / 'file_1.txt'}']" in captured.out
    assert (
        f"['continous', '{tmp_path / 'file_2.txt'}', '--howmany', '2', '--audio', 'audio2', '--prefix', 'prefix2', '--startat', '10']"
        in captured.out
    )


def test_compose_video_valid_mode(mock_file, tmp_path, capsys):
    with patch("subprocess.check_output") as mock_check_output:
        w.compose_video(mock_file, valid=True)
        assert mock_check_output.call_count == 3
        mock_check_output.assert_any_call(
            [
                "continous",
                f"{tmp_path / 'file_0.txt'}",
                "--howmany",
                "3",
                "--audfile",
                "audio1.mp3",
                "--prefix",
                "prefix1",
                "--help",
            ],
            shell=True,
        )
        mock_check_output.assert_any_call(
            ["mconcat", f"{tmp_path / 'file_1.txt'}", "--help"], shell=True
        )
        mock_check_output.assert_any_call(
            [
                "continous",
                f"{tmp_path / 'file_2.txt'}",
                "--howmany",
                "2",
                "--audio",
                "audio2",
                "--prefix",
                "prefix2",
                "--startat",
                "10",
                "--help",
            ],
            shell=True,
        )
    captured = capsys.readouterr()
    assert "FAILED CMD" in captured.out
    assert "###" * 10 in captured.out


def test_compose_video_execution(mock_file, tmp_path, capsys):
    with patch("subprocess.call") as mock_call:
        w.compose_video(mock_file)
        assert mock_call.call_count == 3
        mock_call.assert_any_call(
            [
                "continous",
                f"{tmp_path / 'file_0.txt'}",
                "--howmany",
                "3",
                "--audfile",
                "audio1.mp3",
                "--prefix",
                "prefix1",
            ]
        )
        mock_call.assert_any_call(["mconcat", f"{tmp_path / 'file_1.txt'}"])
        mock_call.assert_any_call(
            [
                "continous",
                f"{tmp_path / 'file_2.txt'}",
                "--howmany",
                "2",
                "--audio",
                "audio2",
                "--prefix",
                "prefix2",
                "--startat",
                "10",
            ]
        )
    captured = capsys.readouterr()
    assert "FAILED CMD" in captured.out
    assert "###" * 10 in captured.out


def test_compose_video_execution_with_failure(mock_file, tmp_path, capsys):
    with patch("subprocess.call", side_effect=[0, 1, 0]):
        w.compose_video(mock_file)
        captured = capsys.readouterr()
        assert "FAILED CMD" in captured.out
        assert "###" * 10 in captured.out
        assert f"['mconcat', '{tmp_path / 'file_1.txt'}']" in captured.out


def test_empty_input_file(tmp_path):
    input_file = tmp_path / "empty.txt"
    input_file.write_text("")
    w.compose_video(str(input_file))
    assert os.path.exists(tmp_path / "cmds.txt")
    with open(tmp_path / "cmds.txt", "r") as f:
        assert f.read() == ""


def test_no_command_lines(tmp_path):
    content = """
video1.mov
video2.mov
video3.mov
"""
    input_file = tmp_path / "nocommands.txt"
    input_file.write_text(content)
    w.compose_video(str(input_file))
    assert os.path.exists(tmp_path / "cmds.txt")
    assert not os.path.exists(tmp_path / "file_0.txt")
    with open(tmp_path / "cmds.txt", "r") as f:
        assert f.read() == ""
