"""预约服务（SlotWise）线上事故：修好的预约/取消流程，加上对已有脏数据的原地修复。

设计一句话：一次请求 = 一个事务，里面按"先锁、再查、后写"的顺序做完所有事。
  1. 事务从 BEGIN IMMEDIATE 开始：先拿写锁，检查和写入之间不会被别的请求插进来（PostgreSQL 里对应 SELECT … FOR UPDATE 锁场次那一行）。
  2. 预约状态、场次的 available_slots、审计行三件事在同一个事务里提交，任何一步失败全部回滚。
  3. 取消是幂等的：只有 active 的预约才会释放名额、写审计；重复取消原样返回第一次的结果。
  4. 数据库自己拒绝坏数据：同一用户同一场次至多一条 active（部分唯一索引）；available_slots 不得大于容量（触发器，PostgreSQL 里是 CHECK）。
  5. 数据修复 upgrade_0002 先修数据、再建约束，整件事一个事务；dry_run 做完同样的事后回滚，只返回会改什么。
"""

from __future__ import annotations

import re
import sqlite3
from collections import Counter
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

REVISION_1 = "0001_initial"
REVISION_2 = "0002_repair_reservations"
STATUSES = ("active", "cancelled")


class ReservationConflict(Exception):
    """重复预约或场次已满（HTTP 409）。"""


class ReservationNotFound(Exception):
    """场次不存在、预约不存在或不属于当前用户（HTTP 404）。"""


@dataclass(frozen=True)
class Reservation:
    """一条预约的快照；字段与 API 的响应一一对应。"""

    id: int
    user_id: int
    session_id: int
    status: str
    created_at: str
    cancelled_at: str | None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> Reservation:
        return cls(**{key: row[key] for key in cls.__dataclass_fields__})

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class SlotFix:
    session_id: int
    before: int
    after: int


@dataclass(frozen=True)
class RepairReport:
    """修复做了什么（或 dry_run 时会做什么）。"""

    dry_run: bool
    cancelled: tuple[int, ...]
    slot_fixes: tuple[SlotFix, ...]
    cancelled_at: str | None

    @property
    def changed(self) -> bool:
        return bool(self.cancelled or self.slot_fixes)


# ---------------------------------------------------------------- 连接与事务 ----


def connect(path: str = ":memory:") -> sqlite3.Connection:
    """自动提交模式的连接：事务由 transaction() 显式开关，不依赖驱动的隐式行为。"""
    db = sqlite3.connect(path, timeout=30, isolation_level=None, check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


@contextmanager
def transaction(db: sqlite3.Connection, *, rollback: bool = False) -> Iterator[None]:
    """BEGIN IMMEDIATE 先拿写锁；正常结束提交（rollback=True 时回滚），异常一律回滚。"""
    db.execute("BEGIN IMMEDIATE")
    try:
        yield
    except BaseException:
        db.execute("ROLLBACK")
        raise
    db.execute("ROLLBACK" if rollback else "COMMIT")


def _stamp(moment: datetime | None) -> str:
    """统一成 UTC、定宽的 ISO 文本：按文本排序就等于按时间排序。"""
    return (moment or datetime.now(UTC)).astimezone(UTC).isoformat(timespec="microseconds")


# ------------------------------------------------------------ 建表与演示数据 ----

LEGACY_SCHEMA = (
    "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)",
    """CREATE TABLE sessions (
        id INTEGER PRIMARY KEY, title TEXT NOT NULL, starts_at TEXT NOT NULL,
        capacity INTEGER NOT NULL, available_slots INTEGER NOT NULL,
        CONSTRAINT ck_sessions_capacity_nonnegative CHECK (capacity >= 0),
        CONSTRAINT ck_sessions_slots_nonnegative CHECK (available_slots >= 0))""",
    """CREATE TABLE reservations (
        id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users (id),
        session_id INTEGER NOT NULL REFERENCES sessions (id), status TEXT NOT NULL,
        created_at TEXT NOT NULL, cancelled_at TEXT,
        CONSTRAINT ck_reservation_status CHECK (status IN ('active', 'cancelled')))""",
    """CREATE TABLE reservation_audits (
        id INTEGER PRIMARY KEY, reservation_id INTEGER NOT NULL REFERENCES reservations (id),
        action TEXT NOT NULL, actor_user_id INTEGER NOT NULL REFERENCES users (id),
        created_at TEXT NOT NULL)""",
    "CREATE TABLE alembic_version (version_num TEXT NOT NULL PRIMARY KEY)",
    f"INSERT INTO alembic_version VALUES ('{REVISION_1}')",
)

# 0002 加的约束。SQLite 不能给已有表补 CHECK，所以"available_slots 不超过容量"用触发器；
# PostgreSQL 里一条 ADD CONSTRAINT … CHECK (available_slots <= capacity) 就够。
CONSTRAINTS = (
    """CREATE UNIQUE INDEX IF NOT EXISTS uq_reservations_one_active
       ON reservations (user_id, session_id) WHERE status = 'active'""",
    """CREATE TRIGGER IF NOT EXISTS trg_slots_within_capacity_insert BEFORE INSERT ON sessions
       WHEN NEW.available_slots > NEW.capacity
       BEGIN SELECT RAISE(ABORT, 'available_slots exceeds capacity'); END""",
    """CREATE TRIGGER IF NOT EXISTS trg_slots_within_capacity_update BEFORE UPDATE ON sessions
       WHEN NEW.available_slots > NEW.capacity
       BEGIN SELECT RAISE(ABORT, 'available_slots exceeds capacity'); END""",
)


def create_legacy_schema(db: sqlite3.Connection) -> None:
    """生产库现在的样子：只有 0001 的表和 CHECK，没有 0002 的约束。"""
    for statement in LEGACY_SCHEMA:
        db.execute(statement)


def seed(db: sqlite3.Connection) -> None:
    """演示数据：三个用户、三个场次（容量 3、1、2）；已存在的 id 不重复插入。"""
    start = _stamp(datetime(2026, 12, 1, 9, tzinfo=UTC))
    db.executemany("INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)",
                   [(1, "Ada"), (2, "Lin"), (3, "Sam")])
    db.executemany(
        "INSERT OR IGNORE INTO sessions (id, title, starts_at, capacity, available_slots) VALUES (?, ?, ?, ?, ?)",
        [(1, "Morning Yoga Flow", start, 3, 3), (2, "Pottery Wheel", start, 1, 1),
         (3, "Hand-Drip Coffee", start, 2, 2)])


# ------------------------------------------------------------------ 预约流程 ----


def _holds_active(db: sqlite3.Connection, user_id: int, session_id: int) -> bool:
    row = db.execute("SELECT 1 FROM reservations WHERE user_id = ? AND session_id = ? AND status = 'active'",
                     (user_id, session_id)).fetchone()
    return row is not None


def _write_reservation(db: sqlite3.Connection, user_id: int, session_id: int, stamp: str) -> sqlite3.Row:
    """名额减一（相对更新）、插入预约、写 created 审计：三件事在调用者的事务里一起成败。"""
    db.execute("UPDATE sessions SET available_slots = available_slots - 1 WHERE id = ?", (session_id,))
    reservation_id = db.execute(
        "INSERT INTO reservations (user_id, session_id, status, created_at) VALUES (?, ?, 'active', ?)",
        (user_id, session_id, stamp)).lastrowid
    db.execute("INSERT INTO reservation_audits (reservation_id, action, actor_user_id, created_at) "
               "VALUES (?, 'created', ?, ?)", (reservation_id, user_id, stamp))
    return db.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,)).fetchone()


def reserve(db: sqlite3.Connection, *, session_id: int, user_id: int,
            now: datetime | None = None) -> Reservation:
    """预约：先锁、再查（场次在不在、是否已持有、是否满）、后写（名额、预约、审计）。"""
    stamp = _stamp(now)
    with transaction(db):
        session = db.execute("SELECT available_slots FROM sessions WHERE id = ?",
                             (session_id,)).fetchone()  # PostgreSQL：加 FOR UPDATE
        if session is None:
            raise ReservationNotFound("Session not found")
        if _holds_active(db, user_id, session_id):
            raise ReservationConflict("Already reserved")
        if session["available_slots"] <= 0:
            raise ReservationConflict("Session is full")
        row = _write_reservation(db, user_id, session_id, stamp)
    return Reservation.from_row(row)


def cancel(db: sqlite3.Connection, *, reservation_id: int, user_id: int,
           now: datetime | None = None) -> Reservation:
    """取消：别人的预约和不存在一样（404）；已取消的原样返回；只有 active 才释放名额并写审计。"""
    stamp = _stamp(now)
    with transaction(db):
        row = db.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,)).fetchone()
        if row is None or row["user_id"] != user_id:
            raise ReservationNotFound("Reservation not found")
        if row["status"] == "active":
            db.execute("UPDATE reservations SET status = 'cancelled', cancelled_at = ? WHERE id = ?",
                       (stamp, reservation_id))
            db.execute("UPDATE sessions SET available_slots = available_slots + 1 WHERE id = ?",
                       (row["session_id"],))
            db.execute("INSERT INTO reservation_audits (reservation_id, action, actor_user_id, created_at) "
                       "VALUES (?, 'cancelled', ?, ?)", (reservation_id, user_id, stamp))
            row = db.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,)).fetchone()
    return Reservation.from_row(row)


def list_reservations(db: sqlite3.Connection, *, user_id: int, status: str) -> list[Reservation]:
    """Dashboard：只看自己、只看这个状态，新的在前（同时刻按 id 倒序，结果是确定的）。"""
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}")
    rows = db.execute("SELECT * FROM reservations WHERE user_id = ? AND status = ? "
                      "ORDER BY created_at DESC, id DESC", (user_id, status))
    return [Reservation.from_row(row) for row in rows]


def list_sessions(db: sqlite3.Connection) -> list[dict[str, object]]:
    rows = db.execute("SELECT id, title, starts_at, capacity, available_slots FROM sessions ORDER BY starts_at, id")
    return [dict(row) for row in rows]


# -------------------------------------------------------------- 一致性检查 ----

CHECKS = {
    "no_duplicate_active_reservation":
        "SELECT count(*) FROM (SELECT 1 FROM reservations WHERE status = 'active' "
        "GROUP BY user_id, session_id HAVING count(*) > 1)",
    "active_within_capacity":
        "SELECT count(*) FROM sessions s WHERE (SELECT count(*) FROM reservations r "
        "WHERE r.session_id = s.id AND r.status = 'active') > s.capacity",
    "available_slots_matches_active_count":
        "SELECT count(*) FROM sessions s WHERE s.available_slots <> s.capacity - "
        "(SELECT count(*) FROM reservations r WHERE r.session_id = s.id AND r.status = 'active')",
    "available_slots_within_range":
        "SELECT count(*) FROM sessions WHERE available_slots < 0 OR available_slots > capacity",
}


def violations(db: sqlite3.Connection) -> dict[str, int]:
    """每条不变量的违反行数；空字典表示库是一致的。"""
    counts = {name: db.execute(sql).fetchone()[0] for name, sql in CHECKS.items()}
    return {name: n for name, n in counts.items() if n}


# ------------------------------------------------------------------ 数据修复 ----


def plan_repair(db: sqlite3.Connection) -> tuple[tuple[int, ...], tuple[SlotFix, ...]]:
    """只读：算出要取消的预约 id 和要改的 available_slots，不写任何东西。"""
    active = db.execute(
        "SELECT r.id, r.user_id, r.session_id, s.capacity FROM reservations r "
        "JOIN sessions s ON s.id = r.session_id WHERE r.status = 'active' "
        "ORDER BY r.created_at, r.id").fetchall()
    cancelled: list[int] = []
    holders: set[tuple[int, int]] = set()
    survivors = []
    for row in active:  # 规则 1：同一用户同一场次，最早的留下
        key = (row["user_id"], row["session_id"])
        if key in holders:
            cancelled.append(row["id"])
        else:
            holders.add(key)
            survivors.append(row)
    kept: Counter[int] = Counter()
    for row in survivors:  # 规则 2：规则 1 之后仍超容量，按同样的顺序留到容量为止
        if kept[row["session_id"]] >= row["capacity"]:
            cancelled.append(row["id"])
        else:
            kept[row["session_id"]] += 1
    fixes = tuple(SlotFix(s["id"], s["available_slots"], s["capacity"] - kept[s["id"]])
                  for s in db.execute("SELECT id, capacity, available_slots FROM sessions ORDER BY id")
                  if s["available_slots"] != s["capacity"] - kept[s["id"]])
    return tuple(sorted(cancelled)), fixes


def upgrade_0002(db: sqlite3.Connection, *, now: datetime | None = None,
                 dry_run: bool = False) -> RepairReport:
    """修数据、再建约束、再盖版本号，一个事务；幂等：干净的库上什么都不改。"""
    stamp = _stamp(now)  # 整个修复只取一次时间：所有被取消的记录 cancelled_at 相同
    with transaction(db, rollback=dry_run):
        cancelled, fixes = plan_repair(db)
        db.executemany("UPDATE reservations SET status = 'cancelled', cancelled_at = ? WHERE id = ?",
                       [(stamp, reservation_id) for reservation_id in cancelled])
        db.executemany("UPDATE sessions SET available_slots = ? WHERE id = ?",
                       [(fix.after, fix.session_id) for fix in fixes])
        for statement in CONSTRAINTS:  # 数据已干净，建唯一索引才不会失败
            db.execute(statement)
        db.execute("UPDATE alembic_version SET version_num = ?", (REVISION_2,))
    return RepairReport(dry_run, cancelled, fixes, stamp if cancelled else None)


# ------------------------------------------------------------------- HTTP 层 ----


@dataclass(frozen=True)
class Reply:
    status: int
    body: object


_ROUTES = (
    ("GET", re.compile(r"/api/sessions"), "sessions", False),
    ("POST", re.compile(r"/api/sessions/(\d+)/reservations"), "reserve", True),
    ("GET", re.compile(r"/api/reservations/me"), "mine", True),
    ("POST", re.compile(r"/api/reservations/(\d+)/cancel"), "cancel", True),
)


class Api:
    """把服务函数接到 HTTP 合同上：路径、X-User-ID、状态码和 {"detail": …} 错误体。"""

    def __init__(self, db: sqlite3.Connection) -> None:
        self._db = db

    def handle(self, method: str, path: str, headers: Mapping[str, str] | None = None) -> Reply:
        parts = urlsplit(path)
        for verb, pattern, name, needs_user in _ROUTES:
            match = pattern.fullmatch(parts.path)
            if match and verb == method:
                break
        else:
            return Reply(404, {"detail": "Not Found"})
        user_id = 0
        if needs_user:  # 鉴权先于参数校验
            failure, user_id = self._authenticate(headers or {})
            if failure is not None:
                return failure
        ids = [int(group) for group in match.groups()]
        try:
            if name == "sessions":
                return Reply(200, list_sessions(self._db))
            if name == "reserve":
                return Reply(201, reserve(self._db, session_id=ids[0], user_id=user_id).to_dict())
            if name == "cancel":
                return Reply(200, cancel(self._db, reservation_id=ids[0], user_id=user_id).to_dict())
            wanted = parse_qs(parts.query).get("status", [""])[0]
            if wanted not in STATUSES:
                return Reply(422, {"detail": "status must be active or cancelled"})
            return Reply(200, [r.to_dict() for r in list_reservations(self._db, user_id=user_id, status=wanted)])
        except ReservationNotFound as exc:
            return Reply(404, {"detail": str(exc)})
        except ReservationConflict as exc:
            return Reply(409, {"detail": str(exc)})

    def _authenticate(self, headers: Mapping[str, str]) -> tuple[Reply | None, int]:
        raw = {key.lower(): value for key, value in headers.items()}.get("x-user-id")
        if raw is None:
            return Reply(401, {"detail": "Authentication required"}), 0
        if not raw.lstrip("-").isdigit():
            return Reply(422, {"detail": "X-User-ID must be an integer"}), 0
        if self._db.execute("SELECT 1 FROM users WHERE id = ?", (int(raw),)).fetchone() is None:
            return Reply(401, {"detail": "Unknown user"}), 0
        return None, int(raw)


if __name__ == "__main__":
    demo = connect()
    create_legacy_schema(demo)
    seed(demo)
    upgrade_0002(demo)
    api = Api(demo)
    print(api.handle("POST", "/api/sessions/2/reservations", {"X-User-ID": "1"}))
    print(api.handle("POST", "/api/sessions/2/reservations", {"X-User-ID": "1"}))
    print(api.handle("POST", "/api/sessions/2/reservations", {"X-User-ID": "2"}))
