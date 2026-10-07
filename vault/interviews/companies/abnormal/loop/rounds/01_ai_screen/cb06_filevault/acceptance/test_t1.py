"""t1 -- deduplication. No new endpoints: dedup is invisible; only blobs on disk and two metric names are new."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cb06_support import build_env, run_together  # noqa: E402

pytestmark = pytest.mark.t1
ROUNDS = 8  # each round is slowed by the injected store, see cb06_support.slow_local_store


@pytest.fixture
def slow_env(tmp_path):
    from filevault import metrics

    metrics.reset()
    e = build_env(tmp_path, slow_store=True)
    yield e
    e.app.close()
    metrics.reset()


@pytest.fixture
def env(tmp_path):
    from filevault import metrics

    metrics.reset()
    e = build_env(tmp_path)
    yield e
    e.app.close()
    metrics.reset()


@pytest.mark.regression
def test_single_upload_download_delete_roundtrip(env):
    fid = env.upload_ok("alice", "a.txt", b"hello", "text/plain")
    assert env.download("alice", fid) == b"hello"
    assert env.blob_count() == 1
    assert env.client("alice").delete(f"/files/{fid}").status_code == 204
    assert env.blob_count() == 0


@pytest.mark.regression
def test_different_content_is_stored_separately(env):
    env.upload_ok("alice", "a", b"one")
    env.upload_ok("alice", "b", b"two")
    assert env.blob_count() == 2


@pytest.mark.regression
def test_listing_fields_are_unchanged(env):
    env.upload_ok("alice", "a.txt", b"hello", "text/plain")
    item = env.listing("alice")[0]
    assert {"id", "filename", "content_type", "size", "created_at"} <= set(item)
    assert item["size"] == 5 and item["filename"] == "a.txt"


@pytest.mark.core
def test_same_content_twice_is_stored_once(env):
    env.upload_ok("alice", "a.txt", b"identical bytes")
    env.upload_ok("alice", "b.txt", b"identical bytes")
    assert env.blob_count() == 1


@pytest.mark.core
def test_each_upload_keeps_its_own_record(env):
    a = env.upload_ok("alice", "first.txt", b"same")
    env.clock.tick(minutes=5)
    b = env.upload_ok("alice", "second.txt", b"same")
    assert a != b
    items = {i["filename"]: i for i in env.listing("alice")}
    assert set(items) == {"first.txt", "second.txt"}
    assert items["first.txt"]["created_at"] < items["second.txt"]["created_at"]
    assert env.download("alice", a) == env.download("alice", b) == b"same"
    assert env.blob_count() == 1


@pytest.mark.core
def test_deleting_one_copy_keeps_the_other_downloadable(env):
    a = env.upload_ok("alice", "a", b"keep me")
    b = env.upload_ok("alice", "b", b"keep me")
    assert env.blob_count() == 1
    assert env.client("alice").delete(f"/files/{a}").status_code == 204
    assert env.download("alice", b) == b"keep me"
    assert env.blob_count() == 1


@pytest.mark.core
def test_deleting_the_last_copy_removes_the_blob(env):
    a = env.upload_ok("alice", "a", b"bye")
    b = env.upload_ok("alice", "b", b"bye")
    assert env.blob_count() == 1
    env.client("alice").delete(f"/files/{a}")
    env.client("alice").delete(f"/files/{b}")
    assert env.blob_count() == 0


@pytest.mark.core
def test_dedup_metrics(env):
    from filevault import metrics

    for name in ("a", "b", "c"):
        env.upload_ok("alice", name, b"12345")
    env.upload_ok("alice", "d", b"different")
    snap = metrics.snapshot()
    assert snap["dedup_hits_total"] == 2
    assert snap["bytes_saved"] == 10
    assert snap["uploads_total"] == 4


@pytest.mark.core
def test_concurrent_identical_uploads_make_one_blob(slow_env):
    env = slow_env
    for i in range(ROUNDS):
        content = f"round {i} ".encode() * 20
        errors = run_together(
            lambda: env.upload_ok("alice", f"x{i}", content), lambda: env.upload_ok("alice", f"y{i}", content)
        )
        assert errors == []
    assert env.blob_count() == ROUNDS
    assert len(env.listing("alice", limit=200)) == 2 * ROUNDS


@pytest.mark.core
def test_delete_racing_with_upload_never_loses_the_content(slow_env):
    env = slow_env
    for i in range(ROUNDS):
        content = f"race {i} ".encode() * 20
        first = env.upload_ok("alice", f"orig{i}", content)
        uploaded = []
        errors = run_together(
            lambda: env.client("alice").delete(f"/files/{first}"),
            lambda: uploaded.append(env.upload_ok("alice", f"new{i}", content)),
        )
        assert errors == []
        assert env.download("alice", uploaded[0]) == content
        again = env.upload_ok("alice", f"again{i}", content)  # must share the surviving blob
        assert env.download("alice", again) == content
    assert env.blob_count() == ROUNDS


@pytest.mark.stretch
def test_dedup_across_users_is_invisible(env):
    a = env.upload_ok("alice", "report.pdf", b"shared report")
    b = env.upload_ok("bob", "my copy.pdf", b"shared report")
    assert env.blob_count() == 1
    assert env.names("alice") == ["report.pdf"] and env.names("bob") == ["my copy.pdf"]
    assert env.client("bob").get(f"/files/{a}").status_code == 404
    env.client("alice").delete(f"/files/{a}")
    assert env.download("bob", b) == b"shared report"


@pytest.mark.stretch
def test_empty_files_and_large_files_dedup(env):
    env.upload_ok("alice", "e1", b"")
    env.upload_ok("alice", "e2", b"")
    big = b"\x00\xff" * 200_000
    env.upload_ok("alice", "b1", big)
    env.upload_ok("alice", "b2", big)
    assert env.blob_count() == 2
