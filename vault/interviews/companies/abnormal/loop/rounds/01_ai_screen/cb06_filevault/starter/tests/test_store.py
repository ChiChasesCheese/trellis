import pytest

from conftest import T0
from filevault.models import FileRecord
from filevault.store import Database, FileRepository, paginate
from filevault.store.db import MIGRATIONS_DIR


@pytest.fixture
def db(tmp_path):
    database = Database(tmp_path / "t.db")
    database.migrate()
    yield database
    database.close()


def record(file_id, owner="alice", filename="f.txt", created_at=T0, size=3):
    return FileRecord(file_id, owner, filename, "text/plain", size, created_at, f"blob-{file_id}")


def test_migrate_is_idempotent(db):
    assert db.migrate() == []
    names = [r["name"] for r in db.conn.execute("SELECT name FROM schema_migrations")]
    assert names == sorted(p.name for p in MIGRATIONS_DIR.glob("*.sql"))


def test_transaction_commits(db):
    repo = FileRepository(db)
    with db.transaction():
        repo.add(record("a"))
    assert repo.get("a", "alice") is not None


def test_transaction_rolls_back_on_error(db):
    repo = FileRepository(db)
    with pytest.raises(RuntimeError):
        with db.transaction():
            repo.add(record("a"))
            raise RuntimeError("boom")
    assert repo.get("a", "alice") is None


def test_transactions_do_not_nest(db):
    with db.transaction():
        with pytest.raises(RuntimeError):
            with db.transaction():
                pass


def test_repository_scopes_by_owner(db):
    repo = FileRepository(db)
    repo.add(record("a", owner="alice"))
    assert repo.get("a", "bob") is None
    assert repo.delete("a", "bob") is False
    assert repo.delete("a", "alice") is True


def test_list_is_newest_first(db):
    repo = FileRepository(db)
    from datetime import timedelta

    for i in range(3):
        repo.add(record(f"f{i}", created_at=T0 + timedelta(minutes=i)))
    records, nxt = repo.list_for_owner("alice", paginate(None, 10))
    assert [r.id for r in records] == ["f2", "f1", "f0"]
    assert nxt is None


def test_keyset_pagination_with_equal_timestamps(db):
    repo = FileRepository(db)
    for i in range(7):
        repo.add(record(f"f{i}"))  # all the same created_at
    seen, cursor = [], None
    while True:
        records, cursor = repo.list_for_owner("alice", paginate(cursor, 3))
        seen += [r.id for r in records]
        if cursor is None:
            break
    assert sorted(seen) == [f"f{i}" for i in range(7)]
    assert len(seen) == len(set(seen))


def test_bad_cursor_is_invalid_input():
    from filevault.errors import InvalidInput

    with pytest.raises(InvalidInput) as err:
        paginate("not-a-cursor", 10)
    assert err.value.field == "cursor"


def test_limit_bounds():
    from filevault.errors import InvalidInput

    for bad in (0, 201):
        with pytest.raises(InvalidInput):
            paginate(None, bad)


def test_get_returns_the_stored_fields(db):
    repo = FileRepository(db)
    repo.add(record("a", filename="weird name.txt", size=42))
    got = repo.get("a", "alice")
    assert (got.filename, got.size, got.created_at, got.blob_path) == ("weird name.txt", 42, T0, "blob-a")


def test_duplicate_id_is_rejected(db):
    import sqlite3

    repo = FileRepository(db)
    repo.add(record("a"))
    with pytest.raises(sqlite3.IntegrityError):
        repo.add(record("a"))


def test_negative_size_is_rejected(db):
    import sqlite3

    with pytest.raises(sqlite3.IntegrityError):
        FileRepository(db).add(record("a", size=-1))


def test_each_thread_gets_its_own_connection(db):
    import threading

    seen = []
    thread = threading.Thread(target=lambda: seen.append(db.conn))
    thread.start()
    thread.join()
    assert seen[0] is not db.conn
