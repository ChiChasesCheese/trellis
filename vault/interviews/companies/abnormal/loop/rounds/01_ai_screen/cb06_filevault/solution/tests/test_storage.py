import pytest

from filevault.errors import BlobNotFound
from filevault.storage import InMemoryStore, LocalDiskStore


@pytest.fixture(params=["memory", "disk"])
def store(request, tmp_path):
    return InMemoryStore() if request.param == "memory" else LocalDiskStore(tmp_path / "blobs")


def test_put_get_roundtrip(store):
    store.put("a/b", b"hello")
    assert store.get("a/b") == b"hello"
    assert store.exists("a/b")


def test_put_replaces(store):
    store.put("k", b"one")
    store.put("k", b"two")
    assert store.get("k") == b"two"
    assert store.paths() == ["k"]


def test_get_missing_raises(store):
    with pytest.raises(BlobNotFound):
        store.get("nope")


def test_delete_is_idempotent(store):
    store.put("k", b"x")
    store.delete("k")
    store.delete("k")
    assert not store.exists("k")


def test_paths_are_sorted(store):
    for name in ("b", "a/z", "a/y"):
        store.put(name, b"x")
    assert store.paths() == ["a/y", "a/z", "b"]


def test_local_store_rejects_escape(tmp_path):
    store = LocalDiskStore(tmp_path / "blobs")
    with pytest.raises(ValueError):
        store.put("../outside", b"x")


def test_local_store_leaves_no_partial_files(tmp_path):
    store = LocalDiskStore(tmp_path / "blobs")
    store.put("k", b"x" * 1000)
    assert sorted(p.name for p in (tmp_path / "blobs").iterdir()) == ["k"]
