from filevault.cli import main


def test_upload_then_ls(tmp_path, capsys):
    sample = tmp_path / "hello.txt"
    sample.write_text("hello")
    data = str(tmp_path / "data")
    assert main(["--data-dir", data, "upload", str(sample), "--user", "u1"]) == 0
    assert "hello.txt" in capsys.readouterr().out
    assert main(["--data-dir", data, "ls", "--user", "u1"]) == 0
    out = capsys.readouterr().out
    assert "hello.txt" in out and "5" in out
    assert main(["--data-dir", data, "ls", "--user", "u2"]) == 0
    assert capsys.readouterr().out == ""


def test_upload_rejects_bad_filename(tmp_path, capsys):
    nameless = tmp_path / " "
    nameless.write_text("x")
    assert main(["--data-dir", str(tmp_path / "d"), "upload", str(nameless), "--user", "u1"]) == 1
    assert "error:" in capsys.readouterr().err


def test_parser_requires_a_command():
    import pytest

    from filevault.cli import build_parser

    with pytest.raises(SystemExit):
        build_parser().parse_args([])


def test_parser_reads_serve_options():
    from filevault.cli import build_parser

    args = build_parser().parse_args(["serve", "--port", "9001"])
    assert args.command == "serve" and args.port == 9001 and args.host == "127.0.0.1"
