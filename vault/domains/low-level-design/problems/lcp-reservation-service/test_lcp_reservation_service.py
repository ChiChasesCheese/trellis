"""预约服务事故的测试：每条产品规则、错误优先级、并发（真线程 + 屏障）、失败不留痕、数据修复（含 dry-run 与连跑两次）。"""

import importlib
import os
import random
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

T0 = datetime(2026, 11, 1, 9, 0, tzinfo=UTC)
AUTH = {"X-User-ID": "1"}


def at(minutes: int) -> datetime:
    return T0 + timedelta(minutes=minutes)


def count(db, table: str, where: str = "1=1", args: tuple = ()) -> int:
    return db.execute(f"SELECT count(*) FROM {table} WHERE {where}", args).fetchone()[0]


def slots(db, session_id: int) -> int:
    return db.execute("SELECT available_slots FROM sessions WHERE id = ?", (session_id,)).fetchone()[0]


def snapshot(db) -> tuple:
    """整个库的内容（表结构 + 每张表的全部行）：用来断言"什么都没变"。"""
    schema = tuple(tuple(r) for r in db.execute("SELECT type, name, sql FROM sqlite_master ORDER BY name"))
    tables = ("users", "sessions", "reservations", "reservation_audits", "alembic_version")
    rows = tuple(tuple(tuple(r) for r in db.execute(f"SELECT * FROM {t} ORDER BY 1")) for t in tables)
    return schema, rows


def make_db(path: str = ":memory:"):
    db = impl.connect(path)
    impl.create_legacy_schema(db)
    impl.seed(db)
    impl.upgrade_0002(db)  # 本地环境 = alembic upgrade head
    return db


@pytest.fixture
def db():
    return make_db()


@pytest.fixture
def api(db):
    return impl.Api(db)


@pytest.fixture
def db_file(tmp_path):
    path = str(tmp_path / "slotwise.sqlite")
    make_db(path).close()
    return path


# ---------- 预约 ----------

def test_reserve_takes_one_place_and_writes_one_audit_row(db):
    reservation = impl.reserve(db, session_id=1, user_id=1, now=at(0))
    assert (reservation.status, reservation.cancelled_at, reservation.user_id) == ("active", None, 1)
    assert set(reservation.to_dict()) == {"id", "user_id", "session_id", "status", "created_at", "cancelled_at"}
    assert slots(db, 1) == 2
    audit = db.execute("SELECT reservation_id, action, actor_user_id FROM reservation_audits").fetchall()
    assert [tuple(r) for r in audit] == [(reservation.id, "created", 1)]


def test_second_reserve_while_active_is_409_and_changes_nothing(db):
    impl.reserve(db, session_id=1, user_id=1)
    before = snapshot(db)
    with pytest.raises(impl.ReservationConflict):
        impl.reserve(db, session_id=1, user_id=1)
    assert snapshot(db) == before


def test_reserve_unknown_session_is_404_with_exact_body_and_changes_nothing(db, api):
    before = snapshot(db)
    reply = api.handle("POST", "/api/sessions/999999/reservations", AUTH)
    assert (reply.status, reply.body) == (404, {"detail": "Session not found"})
    assert snapshot(db) == before


def test_full_session_is_409_and_changes_nothing(db):
    impl.reserve(db, session_id=2, user_id=1)  # 场次 2 容量 1
    before = snapshot(db)
    with pytest.raises(impl.ReservationConflict):
        impl.reserve(db, session_id=2, user_id=2)
    assert snapshot(db) == before


def test_reserve_after_cancel_is_a_new_reservation(db):
    first = impl.reserve(db, session_id=1, user_id=1)
    impl.cancel(db, reservation_id=first.id, user_id=1)
    second = impl.reserve(db, session_id=1, user_id=1)
    assert second.id != first.id and second.status == "active"
    assert slots(db, 1) == 2
    assert [r.id for r in impl.list_reservations(db, user_id=1, status="cancelled")] == [first.id]


def test_missing_session_is_checked_before_the_duplicate_and_full_rules(db):
    with pytest.raises(impl.ReservationNotFound):
        impl.reserve(db, session_id=404, user_id=1)


# ---------- 取消 ----------

def test_cancel_by_another_user_looks_exactly_like_a_missing_reservation(db, api):
    rid = api.handle("POST", "/api/sessions/1/reservations", AUTH).body["id"]
    before = snapshot(db)
    other = api.handle("POST", f"/api/reservations/{rid}/cancel", {"X-User-ID": "2"})
    missing = api.handle("POST", "/api/reservations/9999/cancel", {"X-User-ID": "2"})
    assert (other.status, other.body) == (missing.status, missing.body) == (404, {"detail": "Reservation not found"})
    assert snapshot(db) == before


def test_cancel_is_safe_to_repeat_same_body_one_release_one_audit_row(db, api):
    rid = api.handle("POST", "/api/sessions/1/reservations", AUTH).body["id"]
    first = api.handle("POST", f"/api/reservations/{rid}/cancel", AUTH)
    after_first = snapshot(db)
    for _ in range(3):
        again = api.handle("POST", f"/api/reservations/{rid}/cancel", AUTH)
        assert (again.status, again.body) == (first.status, first.body)
    assert snapshot(db) == after_first
    assert slots(db, 1) == 3  # 只释放一次，没有超过容量
    actions = [r[0] for r in db.execute("SELECT action FROM reservation_audits ORDER BY id")]
    assert actions == ["created", "cancelled"]


def test_cancel_keeps_the_original_cancelled_at(db):
    rid = impl.reserve(db, session_id=1, user_id=1, now=at(0)).id
    first = impl.cancel(db, reservation_id=rid, user_id=1, now=at(5))
    again = impl.cancel(db, reservation_id=rid, user_id=1, now=at(60))
    assert first.cancelled_at == again.cancelled_at == "2026-11-01T09:05:00.000000+00:00"


# ---------- Dashboard 与鉴权 ----------

def test_dashboard_shows_only_my_reservations_in_the_asked_status(db, api):
    mine = api.handle("POST", "/api/sessions/1/reservations", AUTH).body["id"]
    gone = api.handle("POST", "/api/sessions/3/reservations", AUTH).body["id"]
    api.handle("POST", f"/api/reservations/{gone}/cancel", AUTH)
    other = api.handle("POST", "/api/sessions/1/reservations", {"X-User-ID": "2"}).body["id"]
    active = api.handle("GET", "/api/reservations/me?status=active", AUTH).body
    cancelled = api.handle("GET", "/api/reservations/me?status=cancelled", AUTH).body
    assert [r["id"] for r in active] == [mine]
    assert [r["id"] for r in cancelled] == [gone]
    assert other not in [r["id"] for r in active + cancelled]


def test_dashboard_lists_newest_first_and_breaks_ties_by_id(db):
    a = impl.reserve(db, session_id=1, user_id=1, now=at(0)).id
    b = impl.reserve(db, session_id=3, user_id=1, now=at(10)).id
    c = impl.reserve(db, session_id=2, user_id=1, now=at(10)).id
    assert [r.id for r in impl.list_reservations(db, user_id=1, status="active")] == [c, b, a]


def test_status_filter_rejects_unknown_values(api):
    assert api.handle("GET", "/api/reservations/me?status=all", AUTH).status == 422


@pytest.mark.parametrize(("method", "path"), [
    ("POST", "/api/sessions/1/reservations"), ("GET", "/api/reservations/me?status=active"),
    ("POST", "/api/reservations/1/cancel")])
def test_protected_routes_need_a_known_user(api, method, path):
    assert api.handle(method, path).status == 401
    assert api.handle(method, path, {"X-User-ID": "99"}).status == 401


def test_session_listing_is_public_and_shows_capacity_minus_active(db, api):
    api.handle("POST", "/api/sessions/1/reservations", AUTH)
    rows = api.handle("GET", "/api/sessions").body
    assert [(r["id"], r["capacity"], r["available_slots"]) for r in rows] == [(1, 3, 2), (2, 1, 1), (3, 2, 2)]


# ---------- 属性：随机操作后不变量始终成立 ----------

def test_invariants_hold_after_every_random_operation(db):
    rng = random.Random(2026)
    audit_rows = 0
    for step in range(200):
        user, session = rng.randint(1, 3), rng.randint(1, 3)
        try:
            if rng.random() < 0.6:
                impl.reserve(db, session_id=session, user_id=user, now=at(step))
            else:
                impl.cancel(db, reservation_id=rng.randint(1, 40), user_id=user, now=at(step))
            audit_rows = count(db, "reservation_audits")
        except (impl.ReservationConflict, impl.ReservationNotFound):
            assert count(db, "reservation_audits") == audit_rows  # 失败的请求不写审计
        assert impl.violations(db) == {}


# ---------- 失败不留痕 ----------

def test_a_failing_audit_write_rolls_back_the_whole_reserve(db):
    db.execute("CREATE TRIGGER boom BEFORE INSERT ON reservation_audits BEGIN SELECT RAISE(ABORT, 'boom'); END")
    before = snapshot(db)
    with pytest.raises(sqlite3.Error):
        impl.reserve(db, session_id=1, user_id=1)
    assert snapshot(db) == before and slots(db, 1) == 3


def test_a_failing_audit_write_rolls_back_the_whole_cancel(db):
    rid = impl.reserve(db, session_id=1, user_id=1).id
    db.execute("CREATE TRIGGER boom BEFORE INSERT ON reservation_audits BEGIN SELECT RAISE(ABORT, 'boom'); END")
    before = snapshot(db)
    with pytest.raises(sqlite3.Error):
        impl.cancel(db, reservation_id=rid, user_id=1)
    assert snapshot(db) == before
    assert db.execute("SELECT status FROM reservations WHERE id = ?", (rid,)).fetchone()[0] == "active"


# ---------- 并发：真线程 + 屏障，断言不变量而不是耗时 ----------

def run_together(path: str, jobs: list):
    """每个线程自己一条连接（像各自的请求）；屏障让它们同时出发。"""
    barrier = threading.Barrier(len(jobs))

    def run(job):
        conn = impl.connect(path)
        try:
            barrier.wait()
            return job(conn)
        except Exception as exc:  # noqa: BLE001 - 结果里要看到每个线程的异常类型
            return exc
        finally:
            conn.close()

    with ThreadPoolExecutor(len(jobs)) as pool:
        return list(pool.map(run, jobs))


def test_concurrent_reserves_never_oversell(db_file):
    admin = impl.connect(db_file)
    admin.executemany("INSERT INTO users (id, name) VALUES (?, ?)", [(u, f"u{u}") for u in range(4, 13)])
    jobs = [lambda c, u=u: impl.reserve(c, session_id=1, user_id=u) for u in range(1, 13)]  # 12 人抢容量 3
    results = run_together(db_file, jobs)
    assert sum(isinstance(r, impl.Reservation) for r in results) == 3
    assert all(isinstance(r, impl.ReservationConflict) for r in results if not isinstance(r, impl.Reservation))
    assert slots(admin, 1) == 0 and count(admin, "reservations", "status = 'active'") == 3
    assert count(admin, "reservation_audits") == 3 and impl.violations(admin) == {}


def test_concurrent_retries_by_one_user_create_one_reservation(db_file):
    results = run_together(db_file, [lambda c: impl.reserve(c, session_id=1, user_id=1)] * 8)
    admin = impl.connect(db_file)
    assert sum(isinstance(r, impl.Reservation) for r in results) == 1
    assert slots(admin, 1) == 2 and count(admin, "reservation_audits") == 1


def test_concurrent_cancels_release_once(db_file):
    admin = impl.connect(db_file)
    rid = impl.reserve(admin, session_id=1, user_id=1).id
    results = run_together(db_file, [lambda c: impl.cancel(c, reservation_id=rid, user_id=1)] * 8)
    assert all(isinstance(r, impl.Reservation) for r in results)
    assert len({r.cancelled_at for r in results}) == 1
    assert slots(admin, 1) == 3
    assert [r[0] for r in admin.execute("SELECT action FROM reservation_audits ORDER BY id")] == ["created", "cancelled"]


# ---------- 数据库自己拒绝坏数据 ----------

def test_database_rejects_a_second_active_reservation_and_bad_slot_counts(db):
    db.execute("INSERT INTO reservations (user_id, session_id, status, created_at) VALUES (1, 1, 'active', 'x')")
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO reservations (user_id, session_id, status, created_at) VALUES (1, 1, 'active', 'y')")
    db.execute("INSERT INTO reservations (user_id, session_id, status, created_at, cancelled_at) "
               "VALUES (1, 1, 'cancelled', 'z', 'z')")  # 已取消的不受限
    for bad in ("capacity + 1", "-1"):
        with pytest.raises(sqlite3.IntegrityError):
            db.execute(f"UPDATE sessions SET available_slots = {bad} WHERE id = 1")


# ---------- 数据修复 ----------

def legacy_db():
    """0001 状态的"生产库"：重复预约、规则 1 之后仍超容量、容量 0 的场次、计数器错位、不该动的已取消记录。"""
    db = impl.connect()
    impl.create_legacy_schema(db)
    impl.seed(db)
    db.execute("DELETE FROM sessions")
    db.execute("INSERT INTO users (id, name) VALUES (4, 'Kai')")
    db.executemany("INSERT INTO sessions VALUES (?, ?, 'x', ?, ?)", [
        (20, "Bread", 2, 7), (21, "Wreath", 0, 0), (22, "Sketch", 3, 0), (23, "Calligraphy", 2, 5),
        (24, "Knife", 1, 1), (25, "OrderOfRules", 2, 2), (26, "Tie", 1, 1)])
    db.executemany("INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?)", [
        (200, 1, 20, "active", "2026-01-01T09:02:00.000000+00:00", None),
        (201, 1, 20, "active", "2026-01-01T09:00:00.000000+00:00", None),
        (202, 2, 20, "active", "2026-01-01T09:01:00.000000+00:00", None),
        (203, 3, 20, "active", "2026-01-01T08:59:00.000000+00:00", None),
        (204, 4, 21, "active", "2026-01-01T09:00:00.000000+00:00", None),
        (205, 1, 23, "active", "2026-01-01T09:00:00.000000+00:00", None),
        (206, 2, 23, "active", "2026-01-01T09:01:00.000000+00:00", None),
        (207, 3, 24, "cancelled", "2025-12-01T09:00:00.000000+00:00", "2026-01-01T00:00:00.000000+00:00"),
        (208, 1, 25, "active", "2026-01-01T10:00:00.000000+00:00", None),
        (209, 1, 25, "active", "2026-01-01T10:01:00.000000+00:00", None),
        (210, 2, 25, "active", "2026-01-01T10:02:00.000000+00:00", None),
        (211, 1, 26, "active", "2026-01-01T11:00:00.000000+00:00", None),
        (212, 2, 26, "active", "2026-01-01T11:00:00.000000+00:00", None)])
    db.execute("INSERT INTO reservation_audits VALUES (300, 207, 'cancelled', 3, '2026-01-01T00:00:00.000000+00:00')")
    return db


REPAIR_AT = datetime(2026, 11, 16, 12, 30, tzinfo=UTC)
REPAIR_STAMP = "2026-11-16T12:30:00.000000+00:00"


def test_legacy_fixture_breaks_every_invariant_before_the_repair():
    assert impl.violations(legacy_db()) == {
        "no_duplicate_active_reservation": 2, "active_within_capacity": 4,
        "available_slots_matches_active_count": 6, "available_slots_within_range": 2}


def test_repair_cancels_the_right_reservations_and_fixes_the_counters():
    db = legacy_db()
    report = impl.upgrade_0002(db, now=REPAIR_AT)
    assert report.cancelled == (200, 202, 204, 209, 212)
    assert {(f.session_id, f.before, f.after) for f in report.slot_fixes} == {
        (20, 7, 0), (22, 0, 3), (23, 5, 0), (25, 2, 0), (26, 1, 0)}
    assert impl.violations(db) == {}
    assert db.execute("SELECT version_num FROM alembic_version").fetchone()[0] == impl.REVISION_2


def test_repair_stamps_one_time_on_every_cancelled_row_and_invents_no_audit():
    db = legacy_db()
    impl.upgrade_0002(db, now=REPAIR_AT)
    stamps = db.execute("SELECT DISTINCT cancelled_at FROM reservations WHERE id IN (200, 202, 204, 209, 212)").fetchall()
    assert [tuple(r) for r in stamps] == [(REPAIR_STAMP,)]
    assert count(db, "reservation_audits") == 1  # 只剩原来的那一行


def test_repair_touches_nothing_else():
    db = legacy_db()
    before = {r["id"]: tuple(r) for r in db.execute("SELECT * FROM reservations")}
    audits = [tuple(r) for r in db.execute("SELECT * FROM reservation_audits")]
    users = [tuple(r) for r in db.execute("SELECT * FROM users")]
    impl.upgrade_0002(db, now=REPAIR_AT)
    after = {r["id"]: tuple(r) for r in db.execute("SELECT * FROM reservations")}
    assert set(after) == set(before)  # 一条都没删
    for rid, row in before.items():
        if rid in (200, 202, 204, 209, 212):
            assert after[rid][:3] == row[:3] and after[rid][4] == row[4]  # id、用户、场次、created_at 不变
            assert after[rid][3] == "cancelled" and after[rid][5] is not None
        else:
            assert after[rid] == row
    assert [tuple(r) for r in db.execute("SELECT * FROM reservation_audits")] == audits
    assert [tuple(r) for r in db.execute("SELECT * FROM users")] == users


def test_repair_applies_the_duplicate_rule_before_the_capacity_rule():
    db = legacy_db()
    report = impl.upgrade_0002(db, now=REPAIR_AT)
    assert 210 not in report.cancelled and 209 in report.cancelled  # 先去重，用户 2 的预约才保得住
    assert db.execute("SELECT status FROM reservations WHERE id = 210").fetchone()[0] == "active"


def test_repair_breaks_a_created_at_tie_with_the_lower_id():
    db = legacy_db()
    impl.upgrade_0002(db, now=REPAIR_AT)
    statuses = dict(db.execute("SELECT id, status FROM reservations WHERE id IN (211, 212)").fetchall())
    assert statuses == {211: "active", 212: "cancelled"}


def test_repair_cancels_everything_in_a_zero_capacity_session():
    db = legacy_db()
    impl.upgrade_0002(db, now=REPAIR_AT)
    assert db.execute("SELECT status FROM reservations WHERE id = 204").fetchone()[0] == "cancelled"
    assert slots(db, 21) == 0


def test_dry_run_reports_the_same_plan_and_changes_nothing():
    db = legacy_db()
    before = snapshot(db)
    preview = impl.upgrade_0002(db, now=REPAIR_AT, dry_run=True)
    assert snapshot(db) == before  # 数据、表结构、版本号都没动
    real = impl.upgrade_0002(db, now=REPAIR_AT)
    assert preview.dry_run and not real.dry_run
    assert (preview.cancelled, preview.slot_fixes, preview.cancelled_at) == (real.cancelled, real.slot_fixes, real.cancelled_at)


def test_running_the_repair_twice_changes_nothing_the_second_time():
    db = legacy_db()
    impl.upgrade_0002(db, now=REPAIR_AT)
    after_first = snapshot(db)
    second = impl.upgrade_0002(db, now=REPAIR_AT + timedelta(days=1))
    third = impl.upgrade_0002(db, now=REPAIR_AT + timedelta(days=2), dry_run=True)
    assert not second.changed and second.cancelled == () and second.cancelled_at is None
    assert not third.changed
    assert snapshot(db) == after_first  # 连第一次的 cancelled_at 都没被覆盖


def test_a_repair_that_fails_partway_leaves_data_and_revision_as_they_were():
    db = legacy_db()
    db.execute("CREATE TRIGGER boom BEFORE UPDATE OF available_slots ON sessions WHEN NEW.id = 26 "
               "BEGIN SELECT RAISE(ABORT, 'boom'); END")
    before = snapshot(db)
    with pytest.raises(sqlite3.Error):
        impl.upgrade_0002(db, now=REPAIR_AT)
    assert snapshot(db) == before  # 前面已经取消的预约、已经改的计数、版本号全部回到原样
    assert db.execute("SELECT version_num FROM alembic_version").fetchone()[0] == impl.REVISION_1
    db.execute("DROP TRIGGER boom")
    assert impl.upgrade_0002(db, now=REPAIR_AT).changed  # 修好原因后重跑即可


def test_after_the_repair_the_database_itself_refuses_the_old_mistakes():
    db = legacy_db()
    impl.upgrade_0002(db, now=REPAIR_AT)
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO reservations (user_id, session_id, status, created_at) VALUES (1, 23, 'active', 'x')")
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("UPDATE sessions SET available_slots = 99 WHERE id = 20")


def test_migrating_a_clean_database_changes_no_rows(db):
    before = snapshot(db)
    report = impl.upgrade_0002(db)
    assert not report.changed and snapshot(db) == before
