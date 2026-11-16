"""预约服务事故练习骨架（有缺陷版）：公开 API 与 `solution.py` 一致；`reserve`、`cancel`、`list_reservations`、`plan_repair`、
`upgrade_0002` 里的缺陷和真实工作区里那份服务是同一类。把它们修好，就是在真实工作区里改 `reservation_service.py` 和新增一个迁移。

真实栈与这里的区别：工作区是 FastAPI + SQLAlchemy + PostgreSQL + Alembic，这里用标准库 sqlite3；`BEGIN IMMEDIATE` 对应
`SELECT … FOR UPDATE`，触发器对应 CHECK 约束，`upgrade_0002` 对应 Alembic 的第二个迁移（修数据 → 建约束 → 盖版本号）。

产品规则（逐条都有测试）：
 1. 同一用户在同一场次至多一条 active 预约；已持有时再预约 → `ReservationConflict`（HTTP 409），什么都不改：不多一条预约、不多扣名额、不多一行审计。
 2. 任何时刻一个场次的 active 预约数不超过容量，不管多少请求同时到；已满 → `ReservationConflict`。
 3. `available_slots` 永远等于 容量 − active 预约数；取消之后同一用户可以再预约（新的预约，新的 id）。
 4. 场次不存在 → `ReservationNotFound`，HTTP 404，正文 `{"detail": "Session not found"}`，什么都不改；这一条先于重复和已满的判断。
 5. 取消：只有预约的主人能取消；别人的预约与不存在的预约一模一样（404，`Reservation not found`），而且什么都不改。
 6. 取消可以重复：每次都 200、正文与第一次相同（`cancelled_at` 保持第一次的值）；名额只释放一次，审计只写一行 `cancelled`。
 7. Dashboard：`list_reservations(user_id, status)` 只返回自己的、这个状态的预约，新的在前（同一时刻按 id 倒序）；status 只能是 active 或 cancelled。
 8. 审计：每次成功的预约或取消恰好写一行（`created` / `cancelled`，`actor_user_id` 是操作者）；失败的请求不写。
 9. 预约状态、名额、审计三者同成败：任何一步失败，这次请求什么都不留下。
10. HTTP：预约 201，取消 200，列表 200；`X-User-ID` 缺失 401 `Authentication required`，用户不存在 401 `Unknown user`；场次列表不要鉴权。
11. 历史数据修复（`upgrade_0002`）：只改状态，不删记录，id、用户、场次、`created_at` 不变。
12. 同一用户在同一场次有多条 active：`created_at` 最早的留下（相同时刻取 id 小的），其余变 cancelled。
13. 去重之后某场次的 active 仍超过容量：按同样的顺序留到容量为止，其余变 cancelled；容量为 0 的场次全部取消。
14. 被修复取消的记录 `cancelled_at` 都是这次修复的时刻（同一个值）；不为它们补写审计行；其余预约和已有审计一行不变。
15. 修复之后每个场次 `available_slots = 容量 − active 数`；数据库自己拒绝：同一用户同一场次第二条 active、`available_slots` 小于 0 或大于容量。
16. 修复整体一个事务：中途失败，数据和版本号都回到原样；成功后再跑一遍什么都不改（幂等）；`dry_run=True` 做同样的事然后回滚，返回会做什么。
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


def reserve(db: sqlite3.Connection, *, session_id: int, user_id: int,
            now: datetime | None = None) -> Reservation:
    """【有缺陷】先查再写、没有锁；场次不存在、重复预约、名额竞争、审计另起提交都没处理。"""
    stamp = _stamp(now)
    session = db.execute("SELECT available_slots FROM sessions WHERE id = ?", (session_id,)).fetchone()
    if session["available_slots"] <= 0:
        raise ReservationConflict("Session is full")
    with transaction(db):
        db.execute("UPDATE sessions SET available_slots = ? WHERE id = ?", (session["available_slots"] - 1, session_id))
        reservation_id = db.execute(
            "INSERT INTO reservations (user_id, session_id, status, created_at) VALUES (?, ?, 'active', ?)",
            (user_id, session_id, stamp)).lastrowid
    db.execute("INSERT INTO reservation_audits (reservation_id, action, actor_user_id, created_at) "
               "VALUES (?, 'created', ?, ?)", (reservation_id, user_id, stamp))
    row = db.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,)).fetchone()
    return Reservation.from_row(row)


def cancel(db: sqlite3.Connection, *, reservation_id: int, user_id: int,
           now: datetime | None = None) -> Reservation:
    """【有缺陷】不看主人；重复取消每次都释放名额、改 cancelled_at；审计另起提交。"""
    stamp = _stamp(now)
    row = db.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,)).fetchone()
    if row is None:
        raise ReservationNotFound("Reservation not found")
    with transaction(db):
        db.execute("UPDATE reservations SET status = 'cancelled', cancelled_at = ? WHERE id = ?", (stamp, reservation_id))
        db.execute("UPDATE sessions SET available_slots = available_slots + 1 WHERE id = ?", (row["session_id"],))
    db.execute("INSERT INTO reservation_audits (reservation_id, action, actor_user_id, created_at) "
               "VALUES (?, 'cancelled', ?, ?)", (reservation_id, user_id, stamp))
    row = db.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,)).fetchone()
    return Reservation.from_row(row)


def list_reservations(db: sqlite3.Connection, *, user_id: int, status: str) -> list[Reservation]:
    """【有缺陷】只在 status 是 cancelled 时才过滤，active 列表里混着已取消的。"""
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}")
    query = "SELECT * FROM reservations WHERE user_id = ?"
    if status == "cancelled":
        query += " AND status = 'cancelled'"
    return [Reservation.from_row(row) for row in db.execute(query + " ORDER BY created_at DESC", (user_id,))]


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
    """【有缺陷】重复的只留 id 最小的而不是最早的；不处理超容量；只重算被改过的场次。"""
    rows = db.execute("SELECT id, user_id, session_id FROM reservations WHERE status = 'active' ORDER BY id").fetchall()
    seen: set[tuple[int, int]] = set()
    cancelled: list[int] = []
    for row in rows:
        key = (row["user_id"], row["session_id"])
        if key in seen:
            cancelled.append(row["id"])
        seen.add(key)
    touched = {row["session_id"] for row in rows if row["id"] in cancelled}
    fixes = []
    for session_id in sorted(touched):
        capacity, available = db.execute("SELECT capacity, available_slots FROM sessions WHERE id = ?", (session_id,)).fetchone()
        left = sum(1 for row in rows if row["session_id"] == session_id and row["id"] not in cancelled)
        fixes.append(SlotFix(session_id, available, capacity - left))
    return tuple(cancelled), tuple(fixes)


def upgrade_0002(db: sqlite3.Connection, *, now: datetime | None = None,
                 dry_run: bool = False) -> RepairReport:
    """【有缺陷】不在事务里；每条记录各取一次时间；不看 dry_run；不建约束；不盖版本号。"""
    cancelled, fixes = plan_repair(db)
    for reservation_id in cancelled:
        db.execute("UPDATE reservations SET status = 'cancelled', cancelled_at = ? WHERE id = ?",
                   (_stamp(None), reservation_id))
    for fix in fixes:
        db.execute("UPDATE sessions SET available_slots = ? WHERE id = ?", (fix.after, fix.session_id))
    return RepairReport(dry_run, cancelled, fixes, _stamp(now) if cancelled else None)


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
