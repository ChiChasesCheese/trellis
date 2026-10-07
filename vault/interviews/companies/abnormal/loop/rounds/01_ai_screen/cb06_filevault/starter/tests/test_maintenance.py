from conftest import upload
from filevault.cli import main
from filevault.maintenance import fsck


def test_clean_store(app, client):
    upload(client, "a.txt", b"hello")
    assert fsck(app.service.files, app.store).clean


def test_reports_missing_and_orphaned(app, client):
    record_id = upload(client, "a.txt", b"hello").json["id"]
    blob_path = app.service.get("alice", record_id).blob_path
    app.store.delete(blob_path)
    app.store.put("stray", b"?")
    report = fsck(app.service.files, app.store)
    assert report.missing == [blob_path]
    assert report.orphaned == ["stray"]
    assert not report.clean


def test_cli_exit_code(tmp_path, capsys):
    data = str(tmp_path / "data")
    assert main(["--data-dir", data, "fsck"]) == 0
    assert capsys.readouterr().out.strip() == "ok"
