import importlib
import os
import random
import sqlite3

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
DB = impl.DBError


def company():
    db = impl.Database()
    db.create_table("users", {"id": int, "name": str, "age": int, "city": str}, "id")
    db.create_table("orders", {"id": int, "user_id": int, "amount": int}, "id")
    for n, a, c in [("ann", 30, "sf"), ("bob", 25, "nyc"), ("cat", 35, "sf"), ("dan", None, "nyc")]:
        db.insert("users", {"name": n, "age": a, "city": c})
    for u, amt in [(1, 50), (1, 20), (2, 70), (9, 5), (4, 40)]:
        db.insert("orders", {"user_id": u, "amount": amt})
    return db


# ── 第 1 关：LeetCode 的 SQL 类 ──

def test_sql_class_insert_select_delete():
    sql = impl.SQL(["one", "two"], [2, 3])
    sql.insert_row("two", ["first", "second", "third"])
    sql.insert_row("two", ["a", "b", "c"])
    assert sql.select_cell("two", 1, 3) == "third"
    sql.delete_row("two", 1)
    sql.insert_row("two", ["x", "y", "z"])
    assert sql.select_cell("two", 3, 1) == "x"              # 行号不回退
    with pytest.raises(DB):
        sql.select_cell("two", 1, 1)                        # 已删除


# ── 第 2 关：类型化的表与 CRUD ──

def test_autoincrement_and_explicit_keys():
    db = company()
    assert db.insert("users", {"name": "eve"}) == 5
    assert db.insert("users", {"id": 10, "name": "fay"}) == 10
    assert db.insert("users", {"name": "gus"}) == 11
    db.delete("users", impl.Cmp(impl.Col("id"), "=", 11))
    assert db.insert("users", {"name": "hal"}) == 12        # 删除不回退


@pytest.mark.parametrize("values", [{"id": 1, "name": "dup"}, {"name": 5}, {"age": True}, {"nope": 1}])
def test_insert_rejects_bad_rows_without_side_effects(values):
    db = company()
    with pytest.raises(DB):
        db.insert("users", values)
    assert db.count("users") == 4


def test_unknown_table_and_column():
    db = company()
    for call in (lambda: db.insert("ghost", {}), lambda: db.select("ghost"), lambda: db.select("users", ["nope"]),
                 lambda: db.select("users", where=impl.IsNull("nope")), lambda: db.select("users", order_by=["nope"])):
        with pytest.raises(impl.SchemaError):
            call()
    with pytest.raises(impl.SchemaError):
        db.create_table("users", {"id": int}, "id")


def test_update_is_atomic():
    db = company()
    assert db.update("users", {"age": 31}, impl.Cmp(impl.Col("name"), "=", "ann")) == 1
    assert db.select("users", ["age"], impl.Cmp(impl.Col("name"), "=", "ann")) == [{"age": 31}]
    with pytest.raises(impl.ConstraintError):
        db.update("users", {"age": "x"})
    with pytest.raises(impl.ConstraintError):
        db.update("users", {"id": 2}, impl.Cmp(impl.Col("id"), "=", 1))
    assert db.select("users", ["name"], impl.Cmp(impl.Col("id"), "=", 1)) == [{"name": "ann"}]
    with pytest.raises(impl.ConstraintError):               # 两行同时改成同一个主键
        db.update("users", {"id": 50}, impl.Cmp(impl.Col("city"), "=", "sf"))
    assert db.count("users") == 4
    assert db.update("users", {"id": 100}, impl.Cmp(impl.Col("id"), "=", 1)) == 1
    assert db.delete("users", impl.Cmp(impl.Col("city"), "=", "nowhere")) == 0


# ── 第 2 关：WHERE 的三值逻辑与 ORDER BY ──

def ids(db, pred, table="t"):
    return [r["id"] for r in db.select(table, ["id"], pred)]


def nulls_db():
    db = impl.Database()
    db.create_table("t", {"id": int, "a": int, "b": str}, "id")
    for a, b in [(1, "x"), (2, None), (None, "y"), (4, "x"), (None, None)]:
        db.insert("t", {"a": a, "b": b})
    return db


def test_null_never_matches_comparisons():
    db = nulls_db()
    C, V = impl.Col, impl.Cmp
    assert ids(db, V(C("a"), "<>", 2)) == [1, 4]              # NULL 行不在 <> 的结果里
    assert ids(db, V(C("a"), "=", None)) == []                # = NULL 永远没有行
    assert ids(db, impl.IsNull("a")) == [3, 5]
    assert ids(db, impl.Not(V(C("a"), "=", 2))) == [1, 4]     # NOT UNKNOWN 仍是 UNKNOWN


def test_in_with_null_and_boolean_combinators():
    db = nulls_db()
    C, V = impl.Col, impl.Cmp
    assert ids(db, impl.In("a", (1, None))) == [1]
    assert ids(db, impl.Not(impl.In("a", (1, None)))) == []   # NOT IN 遇到 NULL：什么都不选
    assert ids(db, impl.Or((V(C("a"), "=", 2), V(C("b"), "=", "y")))) == [2, 3]
    assert ids(db, impl.And((V(C("a"), ">=", 1), V(C("b"), "=", "x")))) == [1, 4]
    assert ids(db, V(C("a"), "=", C("id"))) == [1, 2, 4]      # 列和列比较
    assert ids(db, impl.Or((V(C("a"), "=", 2), impl.IsNull("a")))) == [2, 3, 5]


def test_comparing_incompatible_types_raises():
    db = nulls_db()
    with pytest.raises(impl.SchemaError):
        db.select("t", where=impl.Cmp(impl.Col("b"), "<", 3))


def test_order_by_multi_key_nulls_first_and_stable():
    db = impl.Database()
    db.create_table("p", {"id": int, "dept": str, "sal": int}, "id")
    for d, s in [("eng", 10), ("ops", 5), ("eng", 30), (None, 7), ("ops", None), ("eng", 10)]:
        db.insert("p", {"dept": d, "sal": s})
    order = lambda *keys, **kw: [r["id"] for r in db.select("p", ["id"], order_by=list(keys), **kw)]   # noqa: E731
    assert order("sal") == [5, 2, 4, 1, 6, 3]                 # NULL 最小，相等的保持插入顺序
    assert order(("sal", "DESC")) == [3, 1, 6, 4, 2, 5]
    assert order("dept", ("sal", "DESC")) == [4, 3, 1, 6, 2, 5]
    assert order(("sal", "DESC"), limit=2) == [3, 1] and order("sal", limit=0) == []


# ── 第 3 关：JOIN ──

def test_inner_and_left_join_with_alias_and_where():
    db = company()
    inner, left = impl.Join("orders", "u.id", "o.user_id", "inner", "o"), impl.Join("orders", "u.id", "o.user_id", "left", "o")
    where = impl.And((impl.Cmp(impl.Col("o.amount"), ">=", 20), impl.Not(impl.IsNull("u.age"))))
    got = db.select("users", ["u.name", "o.amount"], where, [("o.amount", "DESC")], 2, [inner], alias="u")
    assert got == [{"u.name": "bob", "o.amount": 70}, {"u.name": "ann", "o.amount": 50}]
    pairs = lambda j: [tuple(r.values()) for r in db.select("users", ["u.name", "o.id"], None, ["u.id", "o.id"], None, [j], alias="u")]   # noqa: E731
    assert pairs(inner) == [("ann", 1), ("ann", 2), ("bob", 3), ("dan", 5)]
    assert pairs(left) == [("ann", 1), ("ann", 2), ("bob", 3), ("cat", None), ("dan", 5)]
    assert db.select("users", ["u.name"], impl.IsNull("o.id"), None, None, [left], alias="u") == [{"u.name": "cat"}]


def test_join_column_resolution_and_star():
    db = company()
    join = impl.Join("orders", "users.id", "orders.user_id")
    assert db.select("users", ["name", "amount"], None, ["amount"], 1, [join]) == [{"name": "ann", "amount": 20}]
    with pytest.raises(impl.SchemaError):                     # id 在两张表里都有，必须限定
        db.select("users", ["id"], None, None, None, [join])
    first = db.select("users", None, None, None, 1, [join])[0]
    assert list(first) == ["users.id", "users.name", "users.age", "users.city", "orders.id", "orders.user_id", "orders.amount"]


def test_self_join_and_null_keys_never_match():
    db = impl.Database()
    db.create_table("emp", {"id": int, "name": str, "mgr": int}, "id")
    for n, m in [("root", None), ("a", 1), ("b", 1), ("c", 2)]:
        db.insert("emp", {"name": n, "mgr": m})
    rows = db.select("emp", ["e.name", "m.name"], None, ["e.id"], None, [impl.Join("emp", "e.mgr", "m.id", "left", "m")], alias="e")
    assert [tuple(r.values()) for r in rows] == [("root", None), ("a", "root"), ("b", "root"), ("c", "a")]


# ── 第 4 关：SQL 文本 ──

def test_sql_text_end_to_end():
    db = impl.Database()
    db.execute("CREATE TABLE users (id INT PRIMARY KEY, name TEXT, age INT)")
    db.execute("create table orders (id int primary key, user_id int, amount int);")
    assert db.execute("INSERT INTO users (name, age) VALUES ('ann', 30)") == 1
    assert db.execute("INSERT INTO users (id, name, age) VALUES (7, 'o''neil', NULL)") == 7
    db.execute("INSERT INTO orders (user_id, amount) VALUES (1, 50)")
    db.execute("INSERT INTO orders (user_id, amount) VALUES (1, -20)")
    assert db.execute("SELECT name FROM users WHERE age IS NULL") == [{"name": "o'neil"}]
    assert db.execute("SELECT name FROM users WHERE age IS NOT NULL OR name = 'x'") == [{"name": "ann"}]
    got = db.execute("SELECT u.name, o.amount FROM users u LEFT JOIN orders o ON u.id = o.user_id ORDER BY o.amount DESC LIMIT 2")
    assert got == [{"u.name": "ann", "o.amount": 50}, {"u.name": "ann", "o.amount": -20}]
    assert db.execute("UPDATE users SET age = 31 WHERE name = 'ann'") == 1
    assert db.execute("SELECT * FROM users WHERE age IN (31, 99) AND NOT name = 'z'") == [{"id": 1, "name": "ann", "age": 31}]
    assert db.execute("SELECT name FROM users WHERE age NOT IN (1, 2)") == [{"name": "ann"}]
    assert db.execute("DELETE FROM orders WHERE amount < 0") == 1
    assert db.execute("DELETE FROM orders") == 1 and db.count("orders") == 0


def test_operator_precedence_not_binds_tighter_than_and_than_or():
    db = nulls_db()
    # a = 1 OR a = 2 AND b = 'y'  ==  a = 1 OR (a = 2 AND b = 'y')  →  只有 id 1
    assert [r["id"] for r in db.execute("SELECT id FROM t WHERE a = 1 OR a = 2 AND b = 'y'")] == [1]
    assert [r["id"] for r in db.execute("SELECT id FROM t WHERE (a = 1 OR a = 2) AND b = 'y'")] == []
    assert [r["id"] for r in db.execute("SELECT id FROM t WHERE NOT a = 1 AND b = 'x'")] == [4]
    assert [r["id"] for r in db.execute("SELECT id FROM t WHERE 2 < a")] == [4]


@pytest.mark.parametrize("sql", [
    "", "SELEKT * FROM t", "SELECT FROM t", "SELECT * FROM", "SELECT * FROM t WHERE", "SELECT * FROM t WHERE a =",
    "SELECT * FROM t ORDER a", "SELECT * FROM t LIMIT -1", "SELECT * FROM t LIMIT 'x'", "SELECT * FROM t extra stuff",
    "INSERT INTO t (a) VALUES (1, 2)", "INSERT INTO t VALUES", "UPDATE t SET WHERE a = 1", "SELECT * FROM t WHERE a @ 1",
    "SELECT * FROM t WHERE a NOT 1", "CREATE TABLE z (a INT)", "CREATE TABLE z (a BLOB PRIMARY KEY)",
])
def test_bad_sql_raises_dberror_not_a_crash(sql):
    db = nulls_db()
    with pytest.raises(DB):
        db.execute(sql)


# ── 与 SQLite 对拍 ──

def test_matches_sqlite_on_random_queries():
    rng = random.Random(45)

    def atom():
        col, v = rng.choice(["age", "score"]), rng.randint(0, 5)
        kind = rng.choice(["eq", "ne", "lt", "ge", "in", "notin", "null", "notnull"])
        return {"eq": f"{col} = {v}", "ne": f"{col} <> {v}", "lt": f"{col} < {v}", "ge": f"{col} >= {v}",
                "in": f"{col} IN ({v}, NULL)", "notin": f"{col} NOT IN ({v}, {v + 1})", "null": f"{col} IS NULL",
                "notnull": f"{col} IS NOT NULL"}[kind]

    def expr(depth):
        if depth == 0 or rng.random() < 0.3:
            return atom()
        a, b = expr(depth - 1), expr(depth - 1)
        r = rng.random()
        return f"({a} AND {b})" if r < 0.4 else f"({a} OR {b})" if r < 0.8 else f"NOT ({a})"

    for _ in range(40):
        db, lite = impl.Database(), sqlite3.connect(":memory:")
        db.execute("CREATE TABLE u (id INT PRIMARY KEY, age INT, score INT)")
        db.execute("CREATE TABLE o (id INT PRIMARY KEY, uid INT, amt INT)")
        lite.execute("CREATE TABLE u (id INTEGER PRIMARY KEY, age INTEGER, score INTEGER)")
        lite.execute("CREATE TABLE o (id INTEGER PRIMARY KEY, uid INTEGER, amt INTEGER)")
        pick = lambda: rng.choice([None, 0, 1, 2, 3, 4, 5])    # noqa: E731
        for i in range(1, rng.randint(1, 15)):
            vals = (i, pick(), pick())
            db.insert("u", dict(zip(["id", "age", "score"], vals)))
            lite.execute("INSERT INTO u VALUES (?,?,?)", vals)
        for i in range(1, rng.randint(1, 25)):
            vals = (i, rng.choice([None, *range(0, 16)]), pick())
            db.insert("o", dict(zip(["id", "uid", "amt"], vals)))
            lite.execute("INSERT INTO o VALUES (?,?,?)", vals)
        for _ in range(8):
            where = expr(3)
            order = rng.sample(["age", "score"], rng.randint(0, 2))
            order_sql = ", ".join([f"{c} {rng.choice(['ASC', 'DESC'])}" for c in order] + ["id"])
            got = db.execute(f"SELECT * FROM u WHERE {where} ORDER BY {order_sql}")
            want = lite.execute(f"SELECT * FROM u WHERE {where} ORDER BY {order_sql}").fetchall()
            assert [tuple(r.values()) for r in got] == want, where
        for kind in ("INNER", "LEFT"):
            q = f"SELECT u.id, o.id, o.amt FROM u {kind} JOIN o ON u.id = o.uid ORDER BY u.id, o.id"
            assert [tuple(r.values()) for r in db.execute(q)] == lite.execute(q).fetchall(), kind


def test_hash_join_agrees_with_nested_loop_on_random_data():
    rng = random.Random(3)
    for _ in range(30):
        db = impl.Database()
        db.create_table("l", {"id": int, "k": int}, "id")
        db.create_table("r", {"id": int, "k": int}, "id")
        left = [rng.choice([None, 1, 2, 3]) for _ in range(rng.randint(0, 12))]
        right = [rng.choice([None, 1, 2, 3, 4]) for _ in range(rng.randint(0, 12))]
        for k in left:
            db.insert("l", {"k": k})
        for k in right:
            db.insert("r", {"k": k})
        j = impl.Join("r", "l.k", "r.k", "left")
        got = [(r["l.id"], r["r.id"]) for r in db.select("l", ["l.id", "r.id"], order_by=["l.id", "r.id"], joins=[j])]
        want = []
        for i, a in enumerate(left, 1):
            hits = [j2 for j2, b in enumerate(right, 1) if a is not None and b is not None and a == b]
            want += [(i, h) for h in hits] or [(i, None)]
        assert got == want
