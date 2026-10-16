"""内存数据库——45 分钟面试版（Parts 2–4 的核心）。完整参考实现见 in_memory_database.py。

运行：`python3 -I in_memory_database_45min.py` → 打印 `OK in_memory_database_45min`。

这一版刻意只做面试官一定会看的东西，按讲义"45 分钟怎么写"的顺序：
    1. 存储：Table = {主键: 行字典}
    2. CRUD：create_table / insert（自增、类型检查、重复主键）/ update / delete
    3. 谓词：Eq/Ne/Lt/Le/Gt/Ge/In/IsNull/And/Or/Not，三值逻辑（NULL 用 None）
    4. select：按逻辑顺序 FROM → JOIN → WHERE → ORDER BY → LIMIT → SELECT
    5. JOIN：哈希连接（inner / left），列名限定 `t.col`
没有：SQL 文本解析、索引、聚合、事务、线程安全（面试里被追问再口头说方案，或在剩余时间里加）。
"""

from __future__ import annotations

import operator
import random
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Callable


class DBError(Exception):
    pass


# ── 谓词：对象可调用，返回 True / False / None(UNKNOWN)；WHERE 只留 `is True` 的行 ──

class Col:
    def __init__(self, name: str):
        self.name = name


class Cmp:
    def __init__(self, col: str, fn: Callable[[Any, Any], bool], right: Any):
        self.col, self.fn, self.right = col, fn, right

    def __call__(self, row: dict) -> bool | None:
        a = row[self.col]
        b = row[self.right.name] if isinstance(self.right, Col) else self.right
        return None if a is None or b is None else self.fn(a, b)   # 和 NULL 比较 → UNKNOWN


def Eq(c, v): return Cmp(c, operator.eq, v)   # noqa: E704,N802
def Ne(c, v): return Cmp(c, operator.ne, v)   # noqa: E704,N802
def Lt(c, v): return Cmp(c, operator.lt, v)   # noqa: E704,N802
def Le(c, v): return Cmp(c, operator.le, v)   # noqa: E704,N802
def Gt(c, v): return Cmp(c, operator.gt, v)   # noqa: E704,N802
def Ge(c, v): return Cmp(c, operator.ge, v)   # noqa: E704,N802


def IsNull(c: str):  # noqa: N802
    return lambda row: row[c] is None


def In(c: str, values: list):  # noqa: N802
    def pred(row: dict) -> bool | None:
        a = row[c]
        if a is None:
            return None
        if any(v is not None and a == v for v in values):
            return True
        return None if None in values else False   # 没命中但列表里有 NULL → UNKNOWN
    return pred


def And(*ps):  # noqa: N802
    def pred(row: dict) -> bool | None:
        vals = [p(row) for p in ps]
        return False if False in vals else (None if None in vals else True)
    return pred


def Or(*ps):  # noqa: N802
    def pred(row: dict) -> bool | None:
        vals = [p(row) for p in ps]
        return True if True in vals else (None if None in vals else False)
    return pred


def Not(p):  # noqa: N802
    return lambda row: None if (v := p(row)) is None else not v


# ── 存储 ──

class Table:
    def __init__(self, name: str, columns: dict[str, type], pk: str):
        if pk not in columns:
            raise DBError(f"primary key {pk!r} is not a column")
        self.name, self.columns, self.pk = name, columns, pk
        self.rows: dict[Any, dict] = {}
        self.next_id = 1


@dataclass
class Join:
    table: str
    left: str      # 已有表里的列，如 "u.id"
    right: str     # 新表里的列，如 "o.user_id"
    kind: str = "inner"
    alias: str | None = None


class Database:
    def __init__(self):
        self.tables: dict[str, Table] = {}

    def _table(self, name: str) -> Table:
        if name not in self.tables:
            raise DBError(f"no such table {name!r}")
        return self.tables[name]

    def create_table(self, name: str, columns: dict[str, type], primary_key: str) -> None:
        if name in self.tables:
            raise DBError(f"table {name!r} exists")
        self.tables[name] = Table(name, columns, primary_key)

    def _check(self, t: Table, col: str, v: Any) -> Any:
        if col not in t.columns:
            raise DBError(f"no such column {col!r}")
        if v is None:
            if col == t.pk:
                raise DBError("primary key cannot be NULL")
            return None
        if type(v) is not t.columns[col]:   # 精确比较：True 不能混进 int 列
            raise DBError(f"column {col!r} expects {t.columns[col].__name__}, got {v!r}")
        return v

    def insert(self, table: str, values: dict) -> Any:
        t = self._table(table)
        for c in values:
            if c not in t.columns:
                raise DBError(f"no such column {c!r}")
        row = {c: values.get(c) for c in t.columns}
        if row[t.pk] is None and t.columns[t.pk] is int:
            row[t.pk] = t.next_id                         # 自增
        row = {c: self._check(t, c, v) for c, v in row.items()}
        pk = row[t.pk]
        if pk in t.rows:
            raise DBError(f"duplicate primary key {pk!r}")
        t.rows[pk] = row
        if t.columns[t.pk] is int:
            t.next_id = max(t.next_id, pk + 1)            # 删除不回退
        return pk

    def _matching(self, t: Table, where) -> list[dict]:
        return [r for r in t.rows.values() if where is None or where(r) is True]

    def update(self, table: str, set_: dict, where=None) -> int:
        t = self._table(table)
        targets = self._matching(t, where)
        new_rows = [{**r, **{c: self._check(t, c, v) for c, v in set_.items()}} for r in targets]   # 先校验再动手
        if t.pk in set_:
            old = {r[t.pk] for r in targets}
            keys = [r[t.pk] for r in new_rows]
            if len(set(keys)) != len(keys) or any(k in t.rows and k not in old for k in keys):
                raise DBError("duplicate primary key")
        for r in targets:
            del t.rows[r[t.pk]]
        for r in new_rows:
            t.rows[r[t.pk]] = r
        return len(targets)

    def delete(self, table: str, where=None) -> int:
        t = self._table(table)
        targets = self._matching(t, where)
        for r in targets:
            del t.rows[r[t.pk]]
        return len(targets)

    # ── SELECT：逻辑顺序 FROM → JOIN → WHERE → ORDER BY → LIMIT → SELECT ──
    def select(self, table: str, columns: list[str] | None = None, where=None, order_by=None,
               limit: int | None = None, joins: list[Join] | None = None, alias: str | None = None) -> list[dict]:
        t = self._table(table)
        a0 = alias or table
        if not joins:
            rows = self._matching(t, where)                       # 单表：直接用存储的行（列名不带限定）
        else:
            rows = [{f"{a0}.{c}": v for c, v in r.items()} for r in t.rows.values()]   # FROM
            members = [(a0, t)]
            for j in joins:                                       # JOIN（逐个）
                rt = self._table(j.table)
                members.append((j.alias or j.table, rt))
                rows = self._hash_join(rows, rt, j.alias or j.table, j)
            counts = Counter(c for _, m in members for c in m.columns)
            for r in rows:                                        # 不重名的列也可以不限定
                for a, m in members:
                    for c in m.columns:
                        if counts[c] == 1:
                            r[c] = r[f"{a}.{c}"]
            if where is not None:                                 # WHERE 在 JOIN 之后
                rows = [r for r in rows if where(r) is True]
        try:
            for col, desc in reversed(self._norm(order_by)):     # ORDER BY：从最后一个键往前各排一遍（稳定）
                rows.sort(key=lambda r, c=col: (r[c] is not None, r[c]), reverse=desc)
            rows = rows[:limit]                                   # LIMIT
            if columns is None:
                return [dict(r) for r in rows] if not joins else [{k: v for k, v in r.items() if "." in k} for r in rows]
            return [{c: r[c] for c in columns} for r in rows]     # SELECT 投影
        except KeyError as e:
            raise DBError(f"unknown column {e.args[0]!r}") from None

    @staticmethod
    def _norm(order_by) -> list[tuple[str, bool]]:
        return [(x, False) if isinstance(x, str) else (x[0], x[1].upper() == "DESC") for x in order_by or []]

    @staticmethod
    def _hash_join(left_rows: list[dict], rt: Table, alias: str, j: Join) -> list[dict]:
        """build 右表（O(|R|)），probe 左表（O(|L| + 输出)）。NULL 键不匹配任何东西。"""
        buckets: dict[Any, list[dict]] = defaultdict(list)
        right_rows = [{f"{alias}.{c}": v for c, v in r.items()} for r in rt.rows.values()]
        for r in right_rows:
            if r[j.right] is not None:
                buckets[r[j.right]].append(r)
        nulls = {f"{alias}.{c}": None for c in rt.columns}
        out = []
        for l in left_rows:
            matches = buckets.get(l[j.left], []) if l[j.left] is not None else []
            out.extend({**l, **r} for r in matches)
            if not matches and j.kind == "left":                  # LEFT JOIN：没匹配也保留，右侧补 NULL
                out.append({**l, **nulls})
        return out


# ══════════════════════════════ 测试 ══════════════════════════════

def _raises(fn) -> None:
    try:
        fn()
    except DBError:
        return
    raise AssertionError("expected DBError")


def _company() -> Database:
    db = Database()
    db.create_table("users", {"id": int, "name": str, "age": int, "city": str}, "id")
    db.create_table("orders", {"id": int, "user_id": int, "amount": int}, "id")
    for n, a, c in [("ann", 30, "sf"), ("bob", 25, "nyc"), ("cat", 35, "sf"), ("dan", None, "nyc")]:
        db.insert("users", {"name": n, "age": a, "city": c})
    for u, amt in [(1, 50), (1, 20), (2, 70), (9, 5), (4, 40)]:
        db.insert("orders", {"user_id": u, "amount": amt})
    return db


def test_crud() -> None:
    db = _company()
    assert db.insert("users", {"name": "eve", "age": 1, "city": "la"}) == 5            # 自增
    assert db.insert("users", {"id": 10, "name": "fay"}) == 10 and db.insert("users", {"name": "gus"}) == 11
    db.delete("users", Eq("id", 11))
    assert db.insert("users", {"name": "hal"}) == 12                                   # 删除不回退
    _raises(lambda: db.insert("users", {"id": 1, "name": "dup"}))
    _raises(lambda: db.insert("users", {"name": 5}))
    _raises(lambda: db.insert("users", {"age": True}))
    _raises(lambda: db.insert("users", {"nope": 1}))
    _raises(lambda: db.insert("ghost", {}))
    _raises(lambda: db.select("ghost"))
    _raises(lambda: db.select("users", ["nope"]))
    assert db.update("users", {"age": 31}, Eq("name", "ann")) == 1
    assert db.select("users", ["age"], Eq("name", "ann")) == [{"age": 31}]
    _raises(lambda: db.update("users", {"age": "x"}))
    _raises(lambda: db.update("users", {"id": 2}, Eq("id", 1)))                        # 主键冲突
    assert db.select("users", ["name"], Eq("id", 1)) == [{"name": "ann"}]              # 失败无副作用
    assert db.update("users", {"id": 100}, Eq("id", 1)) == 1 and db.select("users", ["name"], Eq("id", 100)) == [{"name": "ann"}]
    assert db.delete("users", Eq("city", "la")) == 1
    assert db.delete("users", Eq("city", "nowhere")) == 0


def test_predicates_and_order() -> None:
    db = Database()
    db.create_table("t", {"id": int, "a": int, "b": str}, "id")
    for a, b in [(1, "x"), (2, None), (None, "y"), (4, "x"), (None, None)]:
        db.insert("t", {"a": a, "b": b})
    ids = lambda p: [r["id"] for r in db.select("t", ["id"], p)]   # noqa: E731
    assert ids(Ne("a", 2)) == [1, 4] and ids(Eq("a", None)) == [] and ids(IsNull("a")) == [3, 5]
    assert ids(Not(Eq("a", 2))) == [1, 4] and ids(Not(In("a", [1, None]))) == [] and ids(In("a", [1, None])) == [1]
    assert ids(Or(Eq("a", 2), Eq("b", "y"))) == [2, 3] and ids(And(Ge("a", 1), Eq("b", "x"))) == [1, 4]
    assert ids(Eq("a", Col("id"))) == [1, 2, 4]
    # ORDER BY：多键、混合方向、NULL 最小、稳定
    data = [("eng", 10), ("ops", 5), ("eng", 30), (None, 7), ("ops", None), ("eng", 10)]
    db.create_table("p", {"id": int, "dept": str, "sal": int}, "id")
    for d, s in data:
        db.insert("p", {"dept": d, "sal": s})
    o = lambda *keys, **kw: [r["id"] for r in db.select("p", ["id"], order_by=list(keys), **kw)]   # noqa: E731
    assert o("sal") == [5, 2, 4, 1, 6, 3] and o(("sal", "DESC")) == [3, 1, 6, 4, 2, 5]
    assert o("dept", ("sal", "DESC")) == [4, 3, 1, 6, 2, 5]
    assert o(("sal", "DESC"), limit=2) == [3, 1]
    assert o("sal", limit=0) == []


def test_join() -> None:
    db = _company()
    inner = Join("orders", "u.id", "o.user_id", "inner", "o")
    left = Join("orders", "u.id", "o.user_id", "left", "o")
    got = db.select("users", ["u.name", "o.amount"], And(Ge("o.amount", 20), Not(IsNull("u.age"))),
                    [("o.amount", "DESC")], 2, [inner], alias="u")
    assert got == [{"u.name": "bob", "o.amount": 70}, {"u.name": "ann", "o.amount": 50}]
    both = lambda j: [tuple(r.values()) for r in db.select("users", ["u.name", "o.id"], None, ["u.id", "o.id"], None, [j], alias="u")]   # noqa: E731
    assert both(inner) == [("ann", 1), ("ann", 2), ("bob", 3), ("dan", 5)]
    assert both(left) == [("ann", 1), ("ann", 2), ("bob", 3), ("cat", None), ("dan", 5)]
    assert db.select("users", ["u.name"], IsNull("o.id"), None, None, [left], alias="u") == [{"u.name": "cat"}]   # 反连接
    assert db.select("users", ["name", "amount"], None, ["amount"], 1, [Join("orders", "users.id", "orders.user_id")]) == [{"name": "ann", "amount": 20}]
    _raises(lambda: db.select("users", ["id"], None, None, None, [inner], alias="u"))                  # id 重名，必须限定
    assert list(db.select("users", None, None, None, 1, [inner], alias="u")[0]) == ["u.id", "u.name", "u.age", "u.city", "o.id", "o.user_id", "o.amount"]
    # 自连接
    db.create_table("emp", {"id": int, "name": str, "mgr": int}, "id")
    for n, m in [("root", None), ("a", 1), ("b", 1), ("c", 2)]:
        db.insert("emp", {"name": n, "mgr": m})
    sj = db.select("emp", ["e.name", "m.name"], None, ["e.id"], None, [Join("emp", "e.mgr", "m.id", "left", "m")], alias="e")
    assert [tuple(r.values()) for r in sj] == [("root", None), ("a", "root"), ("b", "root"), ("c", "a")]


def test_vs_sqlite() -> None:
    """随机表 + 随机谓词（对象和 SQL 文本同时生成），与 sqlite3 对拍。"""
    rng = random.Random(45)

    def atom() -> tuple[Any, str]:
        col = rng.choice(["age", "score"])
        v = rng.randint(0, 5)
        kind = rng.choice(["eq", "lt", "ge", "in", "null", "ne"])
        if kind == "eq": return Eq(col, v), f"{col} = {v}"
        if kind == "ne": return Ne(col, v), f"{col} <> {v}"
        if kind == "lt": return Lt(col, v), f"{col} < {v}"
        if kind == "ge": return Ge(col, v), f"{col} >= {v}"
        if kind == "in": return In(col, [v, None]), f"{col} IN ({v}, NULL)"
        return IsNull(col), f"{col} IS NULL"

    def expr(depth: int) -> tuple[Any, str]:
        if depth == 0 or rng.random() < 0.3:
            return atom()
        (p, s), (q, t) = expr(depth - 1), expr(depth - 1)
        r = rng.random()
        if r < 0.4: return And(p, q), f"({s} AND {t})"
        if r < 0.8: return Or(p, q), f"({s} OR {t})"
        return Not(p), f"NOT ({s})"

    for rnd in range(40):
        db, lite = Database(), sqlite3.connect(":memory:")
        db.create_table("u", {"id": int, "age": int, "score": int}, "id")
        db.create_table("o", {"id": int, "uid": int, "amt": int}, "id")
        lite.execute("CREATE TABLE u (id INTEGER PRIMARY KEY, age INTEGER, score INTEGER)")
        lite.execute("CREATE TABLE o (id INTEGER PRIMARY KEY, uid INTEGER, amt INTEGER)")
        pick = lambda: rng.choice([None, 0, 1, 2, 3, 4, 5])   # noqa: E731
        for i in range(1, rng.randint(1, 15)):
            vals = (i, pick(), pick())
            db.insert("u", dict(zip(["id", "age", "score"], vals)))
            lite.execute("INSERT INTO u VALUES (?,?,?)", vals)
        for i in range(1, rng.randint(1, 25)):
            vals = (i, rng.choice([None, *range(0, 16)]), pick())
            db.insert("o", dict(zip(["id", "uid", "amt"], vals)))
            lite.execute("INSERT INTO o VALUES (?,?,?)", vals)
        for _ in range(8):
            p, s = expr(3)
            order = rng.sample(["age", "score"], rng.randint(0, 2))
            dirs = [rng.choice(["ASC", "DESC"]) for _ in order]
            sql_order = ", ".join(f"{c} {d}" for c, d in zip(order, dirs)) + (", " if order else "") + "id"
            got = db.select("u", None, p, [*zip(order, dirs), "id"])
            want = lite.execute(f"SELECT * FROM u WHERE {s} ORDER BY {sql_order}").fetchall()
            assert [tuple(r.values()) for r in got] == want, s
        for kind in ("inner", "left"):
            j = Join("o", "u.id", "o.uid", kind, "o")
            got = db.select("u", ["u.id", "o.id", "o.amt"], None, ["u.id", "o.id"], None, [j], alias="u")
            want = lite.execute(f"SELECT u.id, o.id, o.amt FROM u {kind.upper()} JOIN o ON u.id = o.uid ORDER BY u.id, o.id").fetchall()
            assert [tuple(r.values()) for r in got] == want, kind


if __name__ == "__main__":
    test_crud()
    test_predicates_and_order()
    test_join()
    test_vs_sqlite()
    print("OK in_memory_database_45min")
