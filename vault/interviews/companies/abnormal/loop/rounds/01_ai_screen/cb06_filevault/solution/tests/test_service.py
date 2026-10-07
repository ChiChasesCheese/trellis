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


# ---- deduplication

def test_same_content_is_stored_once(app):
    a = app.service.upload("alice", "a.txt", "text/plain", b"same bytes")
    b = app.service.upload("alice", "copy of a.txt", "text/plain", b"same bytes")
    assert a.id != b.id and a.filename != b.filename
    assert len(app.store.paths()) == 1
    assert app.service.read("alice", a.id)[1] == app.service.read("alice", b.id)[1] == b"same bytes"


def test_dedup_spans_users_but_records_stay_separate(app):
    a = app.service.upload("alice", "r.pdf", "application/pdf", b"report")
    b = app.service.upload("bob", "r.pdf", "application/pdf", b"report")
    assert len(app.store.paths()) == 1
    assert app.service.get("alice", a.id).owner == "alice"
    assert app.service.get("bob", b.id).owner == "bob"


def test_blob_survives_until_the_last_reference_is_deleted(app):
    a = app.service.upload("alice", "a", "x/y", b"data")
    b = app.service.upload("bob", "b", "x/y", b"data")
    app.service.delete("alice", a.id)
    assert app.service.read("bob", b.id)[1] == b"data"
    app.service.delete("bob", b.id)
    assert app.store.paths() == []


def test_different_content_gets_different_blobs(app):
    app.service.upload("alice", "a", "x/y", b"one")
    app.service.upload("alice", "b", "x/y", b"two")
    assert len(app.store.paths()) == 2


def test_dedup_metrics(app):
    from filevault import metrics

    app.service.upload("alice", "a", "x/y", b"12345")
    app.service.upload("alice", "b", "x/y", b"12345")
    app.service.upload("alice", "c", "x/y", b"other")
    snap = metrics.snapshot()
    assert snap["uploads_total"] == 3
    assert snap["dedup_hits_total"] == 1
    assert snap["bytes_saved"] == 5


def test_files_without_a_hash_keep_their_own_blob(app):
    """Rows from before the dedup migration have sha256 NULL: delete removes their private blob."""
    from dataclasses import replace

    record = app.service.upload("alice", "old.txt", "text/plain", b"legacy")
    app.service.delete("alice", record.id)
    legacy = replace(record, id="legacy1", blob_path="legacy1", sha256=None)
    app.store.put("legacy1", b"legacy")
    app.service.files.add(legacy)
    app.service.delete("alice", "legacy1")
    assert app.store.paths() == []


def test_quota_check_is_atomic_with_the_insert(app):
    import threading

    from filevault.errors import QuotaExceeded

    app.settings = app.service.settings = __import__("dataclasses").replace(
        app.settings, quota_bytes_per_user=100
    )
    barrier, outcomes = threading.Barrier(2), []

    def worker(i):
        barrier.wait()
        try:
            app.service.upload("alice", f"f{i}", "x/y", bytes([i]) * 60)
            outcomes.append("ok")
        except QuotaExceeded:
            outcomes.append("quota")

    threads = [threading.Thread(target=worker, args=(i,)) for i in (1, 2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert sorted(outcomes) == ["ok", "quota"]
