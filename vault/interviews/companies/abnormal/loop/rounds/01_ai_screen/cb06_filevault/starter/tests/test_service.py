import pytest

from filevault.errors import FileNotFound, FileTooLarge, InvalidInput


def test_upload_and_read(app):
    record = app.service.upload("alice", "a.txt", "text/plain", b"hello")
    got, data = app.service.read("alice", record.id)
    assert data == b"hello" and got.filename == "a.txt"


def test_filename_is_validated(app):
    for bad in ("", "   ", "a/b", "x" * 256):
        with pytest.raises(InvalidInput) as err:
            app.service.upload("alice", bad, "text/plain", b"")
        assert err.value.field == "filename"


def test_size_limit(app):
    with pytest.raises(FileTooLarge):
        app.service.upload("alice", "a", "x/y", b"x" * (app.settings.max_upload_bytes + 1))


def test_get_for_other_user_is_not_found(app):
    record = app.service.upload("alice", "a.txt", "text/plain", b"hello")
    with pytest.raises(FileNotFound):
        app.service.get("bob", record.id)


def test_created_at_comes_from_the_injected_clock(app, clock):
    record = app.service.upload("alice", "a.txt", "text/plain", b"x")
    assert record.created_at == clock.now


def test_delete_removes_record_and_blob(app):
    record = app.service.upload("alice", "a.txt", "text/plain", b"hello")
    assert app.store.exists(record.blob_path)
    app.service.delete("alice", record.id)
    assert not app.store.exists(record.blob_path)
    with pytest.raises(FileNotFound):
        app.service.get("alice", record.id)


def test_delete_twice_is_not_found(app):
    record = app.service.upload("alice", "a.txt", "text/plain", b"hello")
    app.service.delete("alice", record.id)
    with pytest.raises(FileNotFound):
        app.service.delete("alice", record.id)


def test_other_user_cannot_delete(app):
    record = app.service.upload("alice", "a.txt", "text/plain", b"hello")
    with pytest.raises(FileNotFound):
        app.service.delete("bob", record.id)
    assert app.store.exists(record.blob_path)


def test_read_reports_a_missing_blob(app):
    from filevault.errors import BlobNotFound

    record = app.service.upload("alice", "a.txt", "text/plain", b"hello")
    app.store.delete(record.blob_path)
    with pytest.raises(BlobNotFound):
        app.service.read("alice", record.id)


def test_list_files_uses_default_page_size(app):
    for i in range(app.settings.default_page_size + 3):
        app.service.upload("alice", f"f{i}.txt", "text/plain", b"x")
    records, cursor = app.service.list_files("alice")
    assert len(records) == app.settings.default_page_size
    assert cursor is not None
    rest, cursor = app.service.list_files("alice", cursor)
    assert len(rest) == 3 and cursor is None


def test_empty_content_type_becomes_binary(app):
    record = app.service.upload("alice", "a", "", b"x")
    assert record.content_type == "application/octet-stream"


def test_empty_file_is_allowed(app):
    record = app.service.upload("alice", "empty", "text/plain", b"")
    assert record.size == 0
    assert app.service.read("alice", record.id)[1] == b""
