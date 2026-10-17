"""内存数据库（In-Memory Database）：类型化的表 → CRUD → WHERE（三值逻辑）→ ORDER BY → 哈希连接 → 迷你 SQL 解析器。

设计五行：
1. `Table` 只管存储：`{主键: 行}` 的字典 + 列类型；`Database` 管表的集合和 `select` 的流水线 FROM → JOIN → WHERE → ORDER BY → LIMIT → 投影。
2. 谓词是小对象，调用后返回 True / False / None（None 即 UNKNOWN）；WHERE 只留结果 `is True` 的行，NULL 因此不会被误选。
3. JOIN 用哈希连接：给右表建桶（O(|R|)），逐行探测左表（O(|L| + 输出)）；NULL 键永不匹配。
4. 所有写操作先校验、后动手：失败的 `insert` / `update` 不留下半成品。
5. SQL 文本是另一层：分词器 + 递归下降解析器只负责把文本翻译成上面的 Python 调用，不碰存储。
"""

from __future__ import annotations

import operator
import re
from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

Row = dict[str, Any]
Tri = bool | None                                 # 三值逻辑：True / False / None(UNKNOWN)


class DBError(Exception):
    """本模块所有可预期失败的基类。"""


class SchemaError(DBError):
    """表、列不存在或已存在，列名有歧义，类型比较不合法。"""


class ConstraintError(DBError):
    """值违反约束：类型不符、主键重复或为 NULL。"""


class SQLSyntaxError(DBError):
    """SQL 文本不合文法。"""


# ───────────────────────────── 谓词（三值逻辑） ─────────────────────────────

@dataclass(frozen=True)
class Col:
    """比较里的列引用（区别于字面量）。"""
    name: str


def _val(operand: Any, row: Row) -> Any:
    return row[operand.name] if isinstance(operand, Col) else operand


class Pred(ABC):
    """谓词：`pred(row)` 返回 True / False / None。`refs` 列出它引用的列名，供执行前统一校验。"""

    @property
    @abstractmethod
    def refs(self) -> frozenset[str]: ...

    @abstractmethod
    def __call__(self, row: Row) -> Tri: ...


_OPS: dict[str, Callable[[Any, Any], bool]] = {
    "=": operator.eq, "<>": operator.ne, "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge}


@dataclass(frozen=True)
class Cmp(Pred):
    left: Any
    op: str
    right: Any

    @property
    def refs(self) -> frozenset[str]:
        return frozenset(x.name for x in (self.left, self.right) if isinstance(x, Col))

    def __call__(self, row: Row) -> Tri:
        a, b = _val(self.left, row), _val(self.right, row)
        if a is None or b is None:
            return None                           # 和 NULL 比较永远是 UNKNOWN，包括 NULL = NULL
        try:
            return _OPS[self.op](a, b)
        except TypeError:
            raise SchemaError(f"不能比较 {a!r} {self.op} {b!r}") from None


@dataclass(frozen=True)
class In(Pred):
    col: str
    values: tuple[Any, ...]

    @property
    def refs(self) -> frozenset[str]:
        return frozenset({self.col})

    def __call__(self, row: Row) -> Tri:
        a = row[self.col]
        if a is None:
            return None
        if any(v is not None and a == v for v in self.values):
            return True
        return None if None in self.values else False    # 没命中但列表里有 NULL → UNKNOWN


@dataclass(frozen=True)
class IsNull(Pred):
    col: str

    @property
    def refs(self) -> frozenset[str]:
        return frozenset({self.col})

    def __call__(self, row: Row) -> Tri:
        return row[self.col] is None              # 唯一永远不会是 UNKNOWN 的谓词


@dataclass(frozen=True)
class And(Pred):
    parts: tuple[Pred, ...]

    @property
    def refs(self) -> frozenset[str]:
        return frozenset().union(*(p.refs for p in self.parts))

    def __call__(self, row: Row) -> Tri:
        vals = [p(row) for p in self.parts]
        return False if False in vals else (None if None in vals else True)


@dataclass(frozen=True)
class Or(Pred):
    parts: tuple[Pred, ...]

    @property
    def refs(self) -> frozenset[str]:
        return frozenset().union(*(p.refs for p in self.parts))

    def __call__(self, row: Row) -> Tri:
        vals = [p(row) for p in self.parts]
        return True if True in vals else (None if None in vals else False)


@dataclass(frozen=True)
class Not(Pred):
    part: Pred

    @property
    def refs(self) -> frozenset[str]:
        return self.part.refs

    def __call__(self, row: Row) -> Tri:
        v = self.part(row)
        return None if v is None else not v       # NOT UNKNOWN 仍是 UNKNOWN


# ───────────────────────────── 存储 ─────────────────────────────

class Table:
    """一张表：列名 → 类型、主键列、`{主键: 行}`。整数主键自增，删除不回退。"""

    def __init__(self, name: str, columns: dict[str, type], pk: str) -> None:
        if pk not in columns:
            raise SchemaError(f"主键 {pk!r} 不是表 {name!r} 的列")
        self.name, self.columns, self.pk = name, dict(columns), pk
        self.rows: dict[Any, Row] = {}
        self.next_id = 1

    def check(self, col: str, value: Any) -> Any:
        if col not in self.columns:
            raise SchemaError(f"表 {self.name!r} 没有列 {col!r}")
        if value is None:
            if col == self.pk:
                raise ConstraintError("主键不能为 NULL")
            return None
        if type(value) is not self.columns[col]:  # 精确比较：True 不能混进 int 列
            raise ConstraintError(f"列 {col!r} 需要 {self.columns[col].__name__}，得到 {value!r}")
        return value

    @property
    def row_count(self) -> int:
        return len(self.rows)


@dataclass(frozen=True)
class Join:
    table: str
    left: str                                     # 已有行里的列，如 "u.id"
    right: str                                    # 新表里的列，如 "o.user_id"
    kind: str = "inner"                           # "inner" | "left"
    alias: str | None = None


class Database:
    def __init__(self) -> None:
        self._tables: dict[str, Table] = {}

    def _table(self, name: str) -> Table:
        if name not in self._tables:
            raise SchemaError(f"没有表 {name!r}")
        return self._tables[name]

    def create_table(self, name: str, columns: dict[str, type], primary_key: str) -> None:
        if name in self._tables:
            raise SchemaError(f"表 {name!r} 已存在")
        self._tables[name] = Table(name, columns, primary_key)

    def count(self, table: str) -> int:
        return self._table(table).row_count

    def columns(self, table: str) -> list[str]:
        return list(self._table(table).columns)

    def insert(self, table: str, values: Row) -> Any:
        t = self._table(table)
        row = {c: values.get(c) for c in t.columns}
        for c in values:
            t.check(c, values[c])                 # 未知列在这里报错
        if row[t.pk] is None and t.columns[t.pk] is int:
            row[t.pk] = t.next_id                 # 自增
        row = {c: t.check(c, v) for c, v in row.items()}
        pk = row[t.pk]
        if pk in t.rows:
            raise ConstraintError(f"主键 {pk!r} 重复")
        t.rows[pk] = row
        if t.columns[t.pk] is int:
            t.next_id = max(t.next_id, pk + 1)
        return pk

    def _matching(self, t: Table, where: Pred | None) -> list[Row]:
        if where is not None:
            self._check_refs(where.refs, {c: c for c in t.columns})
        return [r for r in t.rows.values() if where is None or where(r) is True]

    def update(self, table: str, assignments: Row, where: Pred | None = None) -> int:
        t = self._table(table)
        targets = self._matching(t, where)
        changes = {c: t.check(c, v) for c, v in assignments.items()}
        new_rows = [{**r, **changes} for r in targets]             # 先在副本上改，校验全过再落盘
        if t.pk in changes:
            old = {r[t.pk] for r in targets}
            keys = [r[t.pk] for r in new_rows]
            if len(set(keys)) != len(keys) or any(k in t.rows and k not in old for k in keys):
                raise ConstraintError("主键重复")
        for r in targets:
            del t.rows[r[t.pk]]
        for r in new_rows:
            t.rows[r[t.pk]] = r
        return len(targets)

    def delete(self, table: str, where: Pred | None = None) -> int:
        t = self._table(table)
        targets = self._matching(t, where)
        for r in targets:
            del t.rows[r[t.pk]]
        return len(targets)

    # ── SELECT ──

    @staticmethod
    def _check_refs(refs: frozenset[str], scope: dict[str, Any]) -> None:
        for name in refs:
            if name not in scope:
                raise SchemaError(f"未知或有歧义的列 {name!r}")

    def select(self, table: str, columns: Sequence[str] | None = None, where: Pred | None = None,
               order_by: Sequence[str | tuple[str, str]] | None = None, limit: int | None = None,
               joins: Sequence[Join] = (), alias: str | None = None) -> list[Row]:
        """逻辑顺序：FROM → JOIN → WHERE → ORDER BY → LIMIT → 投影。`columns=None` 即 `*`。"""
        members = [(alias or table, self._table(table))]
        rows = [{f"{members[0][0]}.{c}": v for c, v in r.items()} for r in members[0][1].rows.values()]
        for j in joins:
            name, right = j.alias or j.table, self._table(j.table)
            if any(name == a for a, _ in members):
                raise SchemaError(f"别名 {name!r} 重复")
            members.append((name, right))
            scope = self._scope(members)
            self._check_refs(frozenset({j.left, j.right}), scope)
            rows = self._hash_join(rows, scope[j.left], right, name, scope[j.right], j.kind)
        scope = self._scope(members)
        for r in rows:                            # 不重名的列也可以不带限定符
            r.update({plain: r[q] for plain, q in scope.items() if "." not in plain})
        keys = [(k, False) if isinstance(k, str) else (k[0], k[1].upper() == "DESC") for k in order_by or ()]
        wanted = list(columns) if columns is not None else None
        self._check_refs(frozenset(k for k, _ in keys) | frozenset(wanted or ()), scope)
        if where is not None:
            self._check_refs(where.refs, scope)
            rows = [r for r in rows if where(r) is True]
        for col, desc in reversed(keys):          # 稳定排序：从最后一个键往前各排一遍；NULL 最小
            rows.sort(key=lambda r, c=col: (r[c] is not None, r[c]), reverse=desc)
        rows = rows[:limit]
        if wanted is None:
            wanted = [c for c in members[0][1].columns] if not joins else [
                f"{a}.{c}" for a, t in members for c in t.columns]
        return [{c: r[c] for c in wanted} for r in rows]

    @staticmethod
    def _scope(members: list[tuple[str, Table]]) -> dict[str, str]:
        """可用的列名 → 行里的限定键。不重名的列同时可以不带限定符，重名的必须限定。"""
        counts = Counter(c for _, t in members for c in t.columns)
        scope = {f"{a}.{c}": f"{a}.{c}" for a, t in members for c in t.columns}
        scope.update({c: f"{a}.{c}" for a, t in members for c in t.columns if counts[c] == 1})
        return scope

    @staticmethod
    def _hash_join(left: list[Row], left_key: str, right: Table, alias: str, right_key: str, kind: str) -> list[Row]:
        """build 右表（O(|R|)），probe 左表（O(|L| + 输出)）。NULL 键不匹配任何东西。"""
        buckets: dict[Any, list[Row]] = defaultdict(list)
        for r in right.rows.values():
            q = {f"{alias}.{c}": v for c, v in r.items()}
            if q[right_key] is not None:
                buckets[q[right_key]].append(q)
        nulls = {f"{alias}.{c}": None for c in right.columns}
        out: list[Row] = []
        for l in left:
            matches = buckets.get(l[left_key], []) if l[left_key] is not None else []
            out.extend({**l, **m} for m in matches)
            if not matches and kind == "left":    # LEFT JOIN：没匹配也保留，右侧补 NULL
                out.append({**l, **nulls})
        return out

    def execute(self, sql: str) -> list[Row] | int | None:
        """执行一条 SQL：SELECT 返回行，INSERT / UPDATE / DELETE 返回主键或影响的行数，CREATE 返回 None。"""
        return Parser(self, sql).run()


# ───────────────────────────── SQL 文本前端 ─────────────────────────────
# 文法（关键字不分大小写）：
#   select := SELECT ('*' | colref {',' colref}) FROM ident [ident] {[INNER|LEFT] JOIN ident [ident] ON colref '=' colref}
#             [WHERE expr] [ORDER BY colref [ASC|DESC] {',' ...}] [LIMIT int]
#   expr   := and {OR and};  and := not {AND not};  not := NOT not | atom
#   atom   := '(' expr ')' | operand cmp operand | colref IS [NOT] NULL | colref [NOT] IN '(' literal {',' literal} ')'

KEYWORDS = {"SELECT", "FROM", "WHERE", "JOIN", "INNER", "LEFT", "ON", "AND", "OR", "NOT", "IN", "IS", "NULL", "ORDER",
            "BY", "ASC", "DESC", "LIMIT", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE", "CREATE", "TABLE",
            "PRIMARY", "KEY", "TRUE", "FALSE"}
SQL_TYPES = {"INT": int, "TEXT": str, "REAL": float, "BOOL": bool}
_TOKEN = re.compile(r"\s*(?:(?P<num>\d+\.\d+|\d+)|(?P<str>'(?:[^']|'')*')|(?P<id>[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)?)"
                    r"|(?P<op><=|>=|<>|!=|[=<>(),*;-]))")


def tokenize(sql: str) -> list[tuple[str, Any]]:
    """文本 → [(kind, value)]，kind ∈ lit / kw / id / op / eof。"""
    out: list[tuple[str, Any]] = []
    pos = 0
    while sql[pos:].strip():
        m = _TOKEN.match(sql, pos)
        if not m:
            raise SQLSyntaxError(f"位置 {pos} 附近有无法识别的字符 {sql[pos:].strip()[0]!r}")
        kind, text = m.lastgroup or "", m.group(m.lastgroup or "")
        if kind == "num":
            out.append(("lit", float(text) if "." in text else int(text)))
        elif kind == "str":
            out.append(("lit", text[1:-1].replace("''", "'")))
        elif kind == "id":
            out.append(("kw", text.upper()) if text.upper() in KEYWORDS else ("id", text))
        else:
            out.append(("op", "<>" if text == "!=" else text))
        pos = m.end()
    return out + [("eof", None)]


class Parser:
    """递归下降：每条文法规则一个方法；优先级 OR < AND < NOT < 比较，靠方法的调用层次表达。"""

    def __init__(self, db: Database, sql: str) -> None:
        self.db, self.toks, self.i = db, tokenize(sql), 0

    def error(self, message: str) -> SQLSyntaxError:
        kind, value = self.toks[self.i]
        return SQLSyntaxError(f"{message}（遇到 {'输入结束' if kind == 'eof' else repr(value)}）")

    def accept(self, *words: str) -> str | None:
        kind, value = self.toks[self.i]
        if kind in ("kw", "op") and value in words:
            self.i += 1
            return value
        return None

    def expect(self, word: str) -> None:
        if not self.accept(word):
            raise self.error(f"需要 {word}")

    def ident(self) -> str:
        kind, value = self.toks[self.i]
        if kind != "id":
            raise self.error("需要标识符")
        self.i += 1
        return value

    def literal(self) -> Any:
        kind, value = self.toks[self.i]
        if kind == "lit":
            self.i += 1
            return value
        if self.accept("NULL", "TRUE", "FALSE"):
            return {"NULL": None, "TRUE": True, "FALSE": False}[self.toks[self.i - 1][1]]
        if self.accept("-") and self.toks[self.i][0] == "lit" and not isinstance(self.toks[self.i][1], str):
            self.i += 1
            return -self.toks[self.i - 1][1]
        raise self.error("需要字面量")

    def run(self) -> list[Row] | int | None:
        handlers = {"SELECT": self.select, "INSERT": self.insert, "UPDATE": self.update,
                    "DELETE": self.delete, "CREATE": self.create}
        word = self.accept(*handlers)
        if word is None:
            raise self.error("需要 SELECT / INSERT / UPDATE / DELETE / CREATE")
        result = handlers[word]()
        self.accept(";")
        if self.toks[self.i][0] != "eof":
            raise self.error("语句后有多余内容")
        return result

    # ── 语句 ──
    def select(self) -> list[Row]:
        cols: list[str] | None = None
        if not self.accept("*"):
            cols = [self.ident()]
            while self.accept(","):
                cols.append(self.ident())
        self.expect("FROM")
        table = self.ident()
        alias = self.ident() if self.toks[self.i][0] == "id" else None
        joins: list[Join] = []
        while (kind := self.accept("INNER", "LEFT", "JOIN")) is not None:
            if kind != "JOIN":
                self.expect("JOIN")
            name = self.ident()
            j_alias = self.ident() if self.toks[self.i][0] == "id" else None
            self.expect("ON")
            left = self.ident()
            self.expect("=")
            joins.append(Join(name, left, self.ident(), "left" if kind == "LEFT" else "inner", j_alias))
        where = self.expr() if self.accept("WHERE") else None
        order: list[tuple[str, str]] = []
        if self.accept("ORDER"):
            self.expect("BY")
            while True:
                order.append((self.ident(), self.accept("ASC", "DESC") or "ASC"))
                if not self.accept(","):
                    break
        limit = None
        if self.accept("LIMIT"):
            limit = self.literal()
            if not isinstance(limit, int) or limit < 0:
                raise self.error("LIMIT 需要非负整数")
        # 左连接的 ON 左列是“已有行”的列，右列属于新表；这与 Join 的字段含义一致
        return self.db.select(table, cols, where, order, limit, joins, alias)

    def insert(self) -> Any:
        self.expect("INTO")
        table = self.ident()
        names: list[str] = []
        if self.accept("("):
            names.append(self.ident())
            while self.accept(","):
                names.append(self.ident())
            self.expect(")")
        self.expect("VALUES")
        self.expect("(")
        values = [self.literal()]
        while self.accept(","):
            values.append(self.literal())
        self.expect(")")
        if not names:
            names = self.db.columns(table)
        if len(names) != len(values):
            raise self.error("列数和值数不一致")
        return self.db.insert(table, dict(zip(names, values)))

    def update(self) -> int:
        table = self.ident()
        self.expect("SET")
        sets: Row = {}
        while True:
            col = self.ident()
            self.expect("=")
            sets[col] = self.literal()
            if not self.accept(","):
                break
        return self.db.update(table, sets, self.expr() if self.accept("WHERE") else None)

    def delete(self) -> int:
        self.expect("FROM")
        table = self.ident()
        return self.db.delete(table, self.expr() if self.accept("WHERE") else None)

    def create(self) -> None:
        self.expect("TABLE")
        name = self.ident()
        self.expect("(")
        columns: dict[str, type] = {}
        pk: str | None = None
        while True:
            col, tname = self.ident(), self.ident().upper()
            if tname not in SQL_TYPES:
                raise self.error(f"不支持的类型 {tname}")
            columns[col] = SQL_TYPES[tname]
            if self.accept("PRIMARY"):
                self.expect("KEY")
                pk = col
            if not self.accept(","):
                break
        self.expect(")")
        if pk is None:
            raise self.error("需要 PRIMARY KEY")
        self.db.create_table(name, columns, pk)

    # ── 表达式：OR < AND < NOT < 比较 ──
    def expr(self) -> Pred:
        parts = [self.and_expr()]
        while self.accept("OR"):
            parts.append(self.and_expr())
        return parts[0] if len(parts) == 1 else Or(tuple(parts))

    def and_expr(self) -> Pred:
        parts = [self.not_expr()]
        while self.accept("AND"):
            parts.append(self.not_expr())
        return parts[0] if len(parts) == 1 else And(tuple(parts))

    def not_expr(self) -> Pred:
        return Not(self.not_expr()) if self.accept("NOT") else self.atom()

    def operand(self) -> Any:
        return Col(self.ident()) if self.toks[self.i][0] == "id" else self.literal()

    def atom(self) -> Pred:
        if self.accept("("):
            inner = self.expr()
            self.expect(")")
            return inner
        left = self.operand()
        if isinstance(left, Col):
            if self.accept("IS"):
                negate = bool(self.accept("NOT"))
                self.expect("NULL")
                return Not(IsNull(left.name)) if negate else IsNull(left.name)
            negate = bool(self.accept("NOT"))
            if self.accept("IN"):
                self.expect("(")
                values = [self.literal()]
                while self.accept(","):
                    values.append(self.literal())
                self.expect(")")
                return Not(In(left.name, tuple(values))) if negate else In(left.name, tuple(values))
            if negate:
                raise self.error("NOT 后需要 IN")
        op = self.accept("=", "<>", "<", "<=", ">", ">=")
        if op is None:
            raise self.error("需要比较运算符")
        return Cmp(left, op, self.operand())


# ───────────────────────────── 第 1 关：LeetCode 的 SQL 类 ─────────────────────────────

class SQL:
    """只有“表 + 按行号增删查”的最小接口，是上面 `Database` 的一个特例：所有列都是 str，行号就是自增主键。"""

    def __init__(self, names: list[str], columns: list[int]) -> None:
        self._db = Database()
        for name, n in zip(names, columns):
            self._db.create_table(name, {"id": int, **{f"c{i}": str for i in range(1, n + 1)}}, "id")

    def insert_row(self, name: str, row: list[str]) -> None:
        self._db.insert(name, {f"c{i}": v for i, v in enumerate(row, 1)})

    def delete_row(self, name: str, row_id: int) -> None:
        self._db.delete(name, Cmp(Col("id"), "=", row_id))

    def select_cell(self, name: str, row_id: int, column_id: int) -> str:
        rows = self._db.select(name, [f"c{column_id}"], Cmp(Col("id"), "=", row_id))
        if not rows:
            raise SchemaError(f"表 {name!r} 没有行 {row_id}")
        return rows[0][f"c{column_id}"]


if __name__ == "__main__":
    db = Database()
    db.execute("CREATE TABLE users (id INT PRIMARY KEY, name TEXT, age INT)")
    db.execute("CREATE TABLE orders (id INT PRIMARY KEY, user_id INT, amount INT)")
    for sql in ["INSERT INTO users (name, age) VALUES ('ann', 30)", "INSERT INTO users (name, age) VALUES ('bob', NULL)",
                "INSERT INTO orders (user_id, amount) VALUES (1, 50)", "INSERT INTO orders (user_id, amount) VALUES (1, 20)"]:
        db.execute(sql)
    print(db.execute("SELECT u.name, o.amount FROM users u LEFT JOIN orders o ON u.id = o.user_id ORDER BY o.amount DESC"))
