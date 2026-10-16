"""内存数据库（Chi 亲历：Amazon 面试被问 "design an in-memory database：CRUD，并用 Python 模拟 SELECT … FROM … JOIN … WHERE … ORDER BY"）。

运行：`python3 -I in_memory_database.py`（全部 assert 通过打印 `OK in_memory_database`）。讲解见上一级 `in_memory_database.md`。

LeetCode 近亲：LC 2408 Design SQL（`SQL` 类，API 是 ins / rmv / sel / exp），见 Part 1。

文件结构（和讲义的 Part 对应）：
    Part 1  LC 2408 `SQL`
    Part 2  类型化的表与 CRUD：Column / Table / Database
    Part 3  谓词对象（三值逻辑）+ 多键、混合方向、稳定的 ORDER BY
    Part 4  JOIN：嵌套循环、哈希连接、LEFT JOIN、限定列名
    Part 5  迷你 SQL 前端：tokenizer + 递归下降 parser
    Part 6  索引与规划器、GROUP BY 聚合、事务（undo log）、线程安全

三条贯穿全文的设计决定：
1. **SQL 的执行顺序是逻辑顺序** FROM → JOIN → WHERE → GROUP BY → SELECT → ORDER BY → LIMIT，不是书写顺序；`select()` 的代码就按这个顺序写。
2. **NULL 用 None，比较是三值逻辑**（True / False / None=UNKNOWN）；WHERE 只保留结果恰好为 True 的行。
3. **所有改动都经过两个原语 `_add` / `_drop`**；索引维护、undo log、事务回滚都只需要挂在这两个原语上。
"""

from __future__ import annotations

import bisect
import functools
import operator
import random
import re
import sqlite3
import threading
import time
from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

Row = dict[str, Any]


# ═══════════════════════ Part 1：LC 2408 Design SQL ═══════════════════════

class SQL:
    """LC 2408。表 = {rowId: 行}；dict 保持插入顺序，而 id 单调递增，所以 exp 的顺序天然是 id 升序。

    删除不会让 next_id 回退（题面："even if the last row was removed"）。
    """

    def __init__(self, names: list[str], columns: list[int]):
        self._width = dict(zip(names, columns))
        self._rows: dict[str, dict[int, list[str]]] = {n: {} for n in names}
        self._next_id = dict.fromkeys(names, 1)

    def ins(self, name: str, row: list[str]) -> bool:
        if name not in self._rows or len(row) != self._width[name]:
            return False
        row_id = self._next_id[name]
        self._next_id[name] = row_id + 1
        self._rows[name][row_id] = list(row)
        return True

    def rmv(self, name: str, rowId: int) -> None:  # noqa: N803 - 名字与 LeetCode 签名一致
        table = self._rows.get(name)
        if table is not None:
            table.pop(rowId, None)

    def sel(self, name: str, rowId: int, columnId: int) -> str:  # noqa: N803
        row = self._rows.get(name, {}).get(rowId)
        if row is None or not 1 <= columnId <= len(row):
            return "<null>"
        return row[columnId - 1]

    def exp(self, name: str) -> list[str]:
        return [",".join([str(row_id), *row]) for row_id, row in self._rows.get(name, {}).items()]


# ═══════════════════════ Part 2：类型化的表与 CRUD ═══════════════════════

class DBError(Exception):
    """所有数据库错误的基类。调用方 `except DBError` 能接住全部。"""


class TableExists(DBError): pass
class NoSuchTable(DBError): pass
class NoSuchColumn(DBError): pass
class AmbiguousColumn(DBError): pass
class DuplicateKey(DBError): pass
class TypeMismatch(DBError): pass
class NotNullViolation(DBError): pass
class TransactionError(DBError): pass
class SQLSyntaxError(DBError): pass


@dataclass(frozen=True)
class Column:
    name: str
    type: type = str
    nullable: bool = True


def coerce(column: Column, value: Any) -> Any:
    """存入前的类型检查。精确比较 `type(v) is t`：这样 True 不会混进 int 列（bool 是 int 的子类）。
    唯一的隐式转换：int 可以存进 float 列。"""
    if value is None:
        if not column.nullable:
            raise NotNullViolation(f"column {column.name!r} is NOT NULL")
        return None
    if column.type is float and type(value) is int:
        return float(value)
    if type(value) is not column.type:
        raise TypeMismatch(f"column {column.name!r} expects {column.type.__name__}, got {value!r}")
    return value


def _numeric(t: type | None) -> bool:
    return t in (int, float)


def _literal_ok(ctype: type | None, value: Any) -> bool:
    """比较时字面量和列类型是否可比：数值互通，其余必须同类型；NULL 与谁都可比（结果 UNKNOWN）。"""
    if value is None or ctype is None:
        return True
    return _numeric(ctype) and type(value) in (int, float) or type(value) is ctype


def _types_ok(a: type | None, b: type | None) -> bool:
    return a is None or b is None or (_numeric(a) and _numeric(b)) or a is b


# ───────────────────────── 名字解析：Scope ─────────────────────────

class Scope:
    """把用户写的名字（'age' 或 'u.age'）解析成行字典里的 key，并报告重名 / 不存在。

    单表查询：行字典沿用存储的 {列名: 值}，key 是裸列名（零拷贝）。
    有 JOIN：行字典的 key 是 'alias.列名'（保证不同表同名列不会互相覆盖）。
    """

    def __init__(self, qualified: bool):
        self.qualified = qualified
        self.tables: list[tuple[str, Table]] = []

    def add(self, alias: str, table: Table) -> None:
        if any(a == alias for a, _ in self.tables):
            raise DBError(f"duplicate table alias {alias!r} (self-join needs an alias)")
        self.tables.append((alias, table))

    def key(self, alias: str, col: str) -> str:
        return f"{alias}.{col}" if self.qualified else col

    def lookup(self, name: str) -> tuple[str, Column]:
        if "." in name:
            alias, col = name.split(".", 1)
            for a, t in self.tables:
                if a == alias:
                    if col not in t.col:
                        raise NoSuchColumn(name)
                    return self.key(a, col), t.col[col]
            raise NoSuchColumn(name)
        hits = [(a, t.col[name]) for a, t in self.tables if name in t.col]
        if not hits:
            raise NoSuchColumn(name)
        if len(hits) > 1:
            raise AmbiguousColumn(f"column {name!r} is ambiguous: {[a for a, _ in hits]}")
        return self.key(hits[0][0], name), hits[0][1]

    def star(self) -> list[str]:
        return [self.key(a, c.name) for a, t in self.tables for c in t.columns]


# ═══════════════ Part 3：谓词（三值逻辑）与 ORDER BY ═══════════════

class Col:
    """列引用。未 bind 时 name 是用户写的名字；bind 之后 name 是行字典里的 key，ctype 是列类型。"""

    def __init__(self, name: str, ctype: type | None = None):
        self.name = name
        self.ctype = ctype

    def get(self, row: Mapping[str, Any]) -> Any:
        return row[self.name]

    def bind(self, scope: Scope) -> Col:
        key, column = scope.lookup(self.name)
        return Col(key, column.type)

    def __repr__(self) -> str:
        return self.name


class Pred:
    """谓词基类。eval 返回 True / False / None（UNKNOWN）；WHERE 只保留 `is True` 的行。"""

    def eval(self, row: Mapping[str, Any]) -> bool | None:
        raise NotImplementedError

    def bind(self, scope: Scope) -> Pred:
        raise NotImplementedError

    def conjuncts(self) -> list[Pred]:
        return [self]

    def __and__(self, other: Pred) -> Pred:
        return And(self, other)

    def __or__(self, other: Pred) -> Pred:
        return Or(self, other)

    def __invert__(self) -> Pred:
        return Not(self)


class Compare(Pred):
    """col <op> (字面量 | 另一列)。第一个参数永远是列；第二个参数是字面量，除非它是 Col(...)。"""

    sym = "?"
    fn: Callable[[Any, Any], bool]

    def __init__(self, left: str | Col, right: Any):
        self.left = left if isinstance(left, Col) else Col(left)
        self.right = right

    def eval(self, row):
        a = self.left.get(row)
        b = self.right.get(row) if isinstance(self.right, Col) else self.right
        if a is None or b is None:
            return None  # 任何和 NULL 的比较都是 UNKNOWN，包括 NULL = NULL
        return self.fn(a, b)

    def bind(self, scope):
        left = self.left.bind(scope)
        if isinstance(self.right, Col):
            right = self.right.bind(scope)
            if not _types_ok(left.ctype, right.ctype):
                raise TypeMismatch(f"cannot compare {left} with {right}")
        else:
            right = self.right
            if not _literal_ok(left.ctype, right):
                raise TypeMismatch(f"cannot compare {left} ({left.ctype.__name__}) with {right!r}")
        return type(self)(left, right)

    def __repr__(self):
        return f"{self.left} {self.sym} {self.right!r}"


class Eq(Compare): sym, fn = "=", staticmethod(operator.eq)
class Ne(Compare): sym, fn = "<>", staticmethod(operator.ne)
class Lt(Compare): sym, fn = "<", staticmethod(operator.lt)
class Le(Compare): sym, fn = "<=", staticmethod(operator.le)
class Gt(Compare): sym, fn = ">", staticmethod(operator.gt)
class Ge(Compare): sym, fn = ">=", staticmethod(operator.ge)


class In(Pred):
    """col IN (v1, v2, …)。三值：命中 → True；没命中但列表里有 NULL → UNKNOWN；否则 False。"""

    def __init__(self, left: str | Col, values: Iterable[Any]):
        self.left = left if isinstance(left, Col) else Col(left)
        self.values = list(values)

    def eval(self, row):
        a = self.left.get(row)
        if a is None:
            return None
        saw_null = False
        for v in self.values:
            if v is None:
                saw_null = True
            elif a == v:
                return True
        return None if saw_null else False

    def bind(self, scope):
        left = self.left.bind(scope)
        for v in self.values:
            if not _literal_ok(left.ctype, v):
                raise TypeMismatch(f"cannot compare {left} with {v!r}")
        return In(left, self.values)

    def __repr__(self):
        return f"{self.left} IN {self.values!r}"


class IsNull(Pred):
    """col IS NULL。这是唯一能"看见" NULL 的谓词：永远返回 True / False，不会 UNKNOWN。"""

    def __init__(self, left: str | Col):
        self.left = left if isinstance(left, Col) else Col(left)

    def eval(self, row):
        return self.left.get(row) is None

    def bind(self, scope):
        return IsNull(self.left.bind(scope))

    def __repr__(self):
        return f"{self.left} IS NULL"


class Const(Pred):
    """常量谓词，供 `WHERE 1 = 1` 这类写法使用。"""

    def __init__(self, value: bool | None):
        self.value = value

    def eval(self, row):
        return self.value

    def bind(self, scope):
        return self


class And(Pred):
    """任一为 False → False；否则任一为 UNKNOWN → UNKNOWN；否则 True。"""

    def __init__(self, *parts: Pred):
        self.parts = parts

    def eval(self, row):
        result: bool | None = True
        for p in self.parts:
            v = p.eval(row)
            if v is False:
                return False
            if v is None:
                result = None
        return result

    def bind(self, scope):
        return And(*(p.bind(scope) for p in self.parts))

    def conjuncts(self):
        return [c for p in self.parts for c in p.conjuncts()]

    def __repr__(self):
        return "(" + " AND ".join(map(repr, self.parts)) + ")"


class Or(Pred):
    """任一为 True → True；否则任一为 UNKNOWN → UNKNOWN；否则 False。"""

    def __init__(self, *parts: Pred):
        self.parts = parts

    def eval(self, row):
        result: bool | None = False
        for p in self.parts:
            v = p.eval(row)
            if v is True:
                return True
            if v is None:
                result = None
        return result

    def bind(self, scope):
        return Or(*(p.bind(scope) for p in self.parts))

    def __repr__(self):
        return "(" + " OR ".join(map(repr, self.parts)) + ")"


class Not(Pred):
    """NOT UNKNOWN 仍然是 UNKNOWN，所以 `NOT (x = 1)` 不会选中 x 为 NULL 的行。"""

    def __init__(self, part: Pred):
        self.part = part

    def eval(self, row):
        v = self.part.eval(row)
        return None if v is None else not v

    def bind(self, scope):
        return Not(self.part.bind(scope))

    def __repr__(self):
        return f"NOT {self.part!r}"


def as_pred(where: Pred | Mapping[str, Any] | None) -> Pred | None:
    """where 可以是 None、Pred，或 {列: 值} 字典（等值条件的 AND；值为 None 表示 IS NULL）。"""
    if where is None or isinstance(where, Pred):
        return where
    return And(*(IsNull(k) if v is None else Eq(k, v) for k, v in where.items()))


def _null_first(value: Any) -> tuple[bool, Any]:
    """排序键：NULL 比任何值都小（SQLite 的规则）。元组比较先比第一个分量，
    两个 None 比较时 None == None 成立，不会触发 None < None 的 TypeError。"""
    return (value is not None, value)


def sort_rows(rows: list[Row], keys: Sequence[tuple[str, bool]]) -> list[Row]:
    """多键、混合方向、稳定。keys = [(行字典 key, 是否 DESC), …]，第一个是最主要的键。
    做法：从最后一个键往前，各排一遍。list.sort 是稳定的，reverse=True 也保持稳定，
    所以后排的主键不会打乱先排的次键。"""
    for key, desc in reversed(keys):
        rows.sort(key=lambda r, k=key: _null_first(r[k]), reverse=desc)
    return rows


def _norm_order(order_by: Sequence[Any] | None) -> list[tuple[str, bool]]:
    """接受 'col' / ('col', 'DESC') / Agg；统一成 [(名字, 是否 DESC)]。"""
    out = []
    for item in order_by or []:
        name, direction = (item, "ASC") if isinstance(item, (str, Agg)) else item
        if isinstance(name, Agg):
            name = name.label
        if direction.upper() not in ("ASC", "DESC"):
            raise DBError(f"bad ORDER BY direction {direction!r}")
        out.append((name, direction.upper() == "DESC"))
    return out


# ───────────────────────── 索引（Part 6 详解，Table 要用到）─────────────────────────

class HashIndex:
    """value → {pk}。只能回答 '=' 和 IN。NULL 不进索引（`= NULL` 永远不是 True）。"""

    kind = "hash"

    def __init__(self, column: str):
        self.column = column
        self.map: dict[Any, set] = {}

    def add(self, value: Any, pk: Any) -> None:
        if value is not None:
            self.map.setdefault(value, set()).add(pk)

    def remove(self, value: Any, pk: Any) -> None:
        if value is None:
            return
        bucket = self.map[value]
        bucket.discard(pk)
        if not bucket:
            del self.map[value]

    def eq(self, value: Any) -> list:
        return list(self.map.get(value, ()))


class SortedIndex:
    """两个平行的有序列表 keys / pks，按 key 排序；用 bisect 回答 '=' 和范围查询。
    插入 / 删除是 O(n)（list 搬移，常数很小）；查询是 O(log n + 命中数)。"""

    kind = "sorted"

    def __init__(self, column: str):
        self.column = column
        self.keys: list[Any] = []
        self.pks: list[Any] = []

    def add(self, value: Any, pk: Any) -> None:
        if value is None:
            return
        i = bisect.bisect_right(self.keys, value)
        self.keys.insert(i, value)
        self.pks.insert(i, pk)

    def remove(self, value: Any, pk: Any) -> None:
        if value is None:
            return
        i = bisect.bisect_left(self.keys, value)
        while self.pks[i] != pk:  # 同值的多个 pk 排在一起，线性找到那一个
            i += 1
        del self.keys[i]
        del self.pks[i]

    def range(self, lo: Any = None, lo_incl: bool = True, hi: Any = None, hi_incl: bool = True) -> tuple[int, int]:
        """返回命中区间 [i, j)（只是下标，不拷贝），None 表示无界。j - i 就是命中数，规划器用它估代价。"""
        i = 0 if lo is None else (bisect.bisect_left(self.keys, lo) if lo_incl else bisect.bisect_right(self.keys, lo))
        j = len(self.keys) if hi is None else (bisect.bisect_right(self.keys, hi) if hi_incl else bisect.bisect_left(self.keys, hi))
        return i, max(i, j)

    def eq(self, value: Any) -> list:
        i, j = self.range(value, True, value, True)
        return self.pks[i:j]


# ───────────────────────── 聚合函数（Part 6）─────────────────────────

class Agg:
    """COUNT / SUM / AVG / MIN / MAX。NULL 被忽略（COUNT(*) 数行，不看值）；
    没有非 NULL 值时 SUM / AVG / MIN / MAX 是 NULL，COUNT 是 0。"""

    FUNCS = ("count", "sum", "avg", "min", "max")

    def __init__(self, func: str, column: str = "*", label: str | None = None):
        func = func.lower()
        if func not in self.FUNCS:
            raise DBError(f"unknown aggregate {func!r}")
        if column == "*" and func != "count":
            raise DBError(f"{func}(*) is not allowed")
        self.func, self.column = func, column
        self.label = label or f"{func}({column})"

    def bind(self, scope: Scope) -> str | None:
        """返回行字典里的 key（COUNT(*) 返回 None）；SUM / AVG 要求数值列。"""
        if self.column == "*":
            return None
        key, column = scope.lookup(self.column)
        if self.func in ("sum", "avg") and not _numeric(column.type):
            raise TypeMismatch(f"{self.func}() needs a numeric column, got {column.name!r}")
        return key

    def compute(self, rows: list[Row], key: str | None) -> Any:
        if key is None:
            return len(rows)
        values = [r[key] for r in rows if r[key] is not None]
        if self.func == "count":
            return len(values)
        if not values:
            return None
        if self.func == "sum":
            return sum(values)
        if self.func == "avg":
            return sum(values) / len(values)
        return min(values) if self.func == "min" else max(values)


@dataclass
class Join:
    table: str
    on: Pred
    kind: str = "inner"  # "inner" | "left"
    alias: str | None = None


# ───────────────────────── Table ─────────────────────────

class Table:
    """一张表：rows 是 {主键: 行字典}；seq 记录每行的插入序号，让"没有 ORDER BY 时的结果顺序"
    与走不走索引无关（总是按插入顺序）。改动只有 `_add` / `_drop` 两个原语，各自把逆操作写进 journal。"""

    def __init__(self, name: str, columns: Sequence[Column], primary_key: str, journal: list[Callable[[], None]]):
        if not columns:
            raise DBError("a table needs at least one column")
        names = [c.name for c in columns]
        if len(set(names)) != len(names):
            raise DBError(f"duplicate column names in {name!r}")
        if any("." in n or not n for n in names):
            raise DBError("column names must be non-empty and contain no '.'")
        if primary_key not in names:
            raise NoSuchColumn(f"primary key {primary_key!r} is not a column of {name!r}")
        self.name = name
        self.columns = [Column(c.name, c.type, False if c.name == primary_key else c.nullable) for c in columns]
        self.col = {c.name: c for c in self.columns}
        self.pk = primary_key
        self.rows: dict[Any, Row] = {}
        self.seq: dict[Any, int] = {}
        self.indexes: dict[str, HashIndex | SortedIndex] = {}
        self._next_seq = 0
        self._next_auto = 1
        self._journal = journal

    # ── 两个原语（带 journal）与它们的 raw 版本（undo 时用，不再记 journal）──
    def _add_raw(self, pk: Any, row: Row, seq: int) -> None:
        self.rows[pk] = row
        self.seq[pk] = seq
        for ix in self.indexes.values():
            ix.add(row[ix.column], pk)

    def _drop_raw(self, pk: Any) -> Row:
        row = self.rows.pop(pk)
        del self.seq[pk]
        for ix in self.indexes.values():
            ix.remove(row[ix.column], pk)
        return row

    def _add(self, pk: Any, row: Row, seq: int) -> None:
        self._add_raw(pk, row, seq)
        self._journal.append(lambda: self._drop_raw(pk))

    def _drop(self, pk: Any) -> None:
        seq = self.seq[pk]
        row = self._drop_raw(pk)
        self._journal.append(lambda: self._add_raw(pk, row, seq))

    def _set_counters(self, next_auto: int, next_seq: int) -> None:
        self._next_auto, self._next_seq = next_auto, next_seq

    # ── CRUD ──
    def insert(self, values: Mapping[str, Any]) -> Any:
        for name in values:
            if name not in self.col:
                raise NoSuchColumn(name)
        row: Row = {}
        for c in self.columns:
            v = values.get(c.name)
            if v is None and c.name == self.pk and c.type is int:
                v = self._next_auto  # 主键省略 → 自增
            row[c.name] = coerce(c, v)
        pk = row[self.pk]
        if pk in self.rows:
            raise DuplicateKey(f"duplicate primary key {pk!r} in {self.name!r}")
        old_counters = (self._next_auto, self._next_seq)
        self._add(pk, row, self._next_seq)
        self._next_seq += 1
        if self.col[self.pk].type is int:
            self._next_auto = max(self._next_auto, pk + 1)  # 显式给的大主键也要推进计数器；删除不会让它回退
        self._journal.append(lambda: self._set_counters(*old_counters))
        return pk

    def update(self, set_: Mapping[str, Any], pred: Pred | None) -> int:
        """set_ 的值可以是常量，也可以是 callable(旧行) → 新值（例如 lambda r: r["age"] + 1）。
        先算出全部新行并校验（类型、NOT NULL、主键冲突），全部通过才动手，所以失败不会留下半截。"""
        for name in set_:
            if name not in self.col:
                raise NoSuchColumn(name)
        targets = self.matching(pred)
        new_rows = []
        for row in targets:
            new = dict(row)
            for name, v in set_.items():
                new[name] = coerce(self.col[name], v(row) if callable(v) else v)
            new_rows.append(new)
        if self.pk in set_:
            old_keys = {r[self.pk] for r in targets}
            new_keys = [r[self.pk] for r in new_rows]
            if len(set(new_keys)) != len(new_keys) or any(k in self.rows and k not in old_keys for k in new_keys):
                raise DuplicateKey(f"update would duplicate primary key in {self.name!r}")
        seqs = [self.seq[r[self.pk]] for r in targets]
        for r in targets:  # 先全删再全加：主键互换（1→2, 2→1）也正确；沿用旧 seq 保持位置
            self._drop(r[self.pk])
        for new, seq in zip(new_rows, seqs):
            self._add(new[self.pk], new, seq)
        return len(targets)

    def delete(self, pred: Pred | None) -> int:
        targets = self.matching(pred)
        for r in targets:
            self._drop(r[self.pk])
        return len(targets)

    # ── 读：规划 + 执行 ──
    def plan(self, pred: Pred | None) -> tuple[str, list | None]:
        """极简规划器：从 WHERE 的顶层 AND 合取项里找能用索引的（'=' / IN / 范围），
        挑候选行数最少的那条路径；没有就全表扫描。返回 (说明, 候选主键列表 | None=全表)。
        规划器只负责"缩小候选集"，之后仍用完整 WHERE 过滤，所以它永远不会改变结果。"""
        total = len(self.rows)
        best: tuple[int, str, list | None] = (total, f"SCAN {self.name} ({total} rows)", None)
        if pred is None:
            return best[1], best[2]
        bounds: dict[str, list] = {}  # 列 → [lo, lo_incl, hi, hi_incl]

        def consider(cost: int, text: str, pks: Callable[[], list]) -> None:
            nonlocal best
            if cost < best[0]:
                best = (cost, text, pks())

        for c in pred.conjuncts():
            if isinstance(c, Compare) and not isinstance(c.right, Col) and c.right is not None:
                col, v = c.left.name, c.right
                if isinstance(c, Eq):
                    found = self._lookup_eq(col, [v])
                    if found is not None:
                        consider(len(found[1]), f"INDEX {found[0]} {self.name}.{col} = {v!r} ({len(found[1])} of {total})", lambda f=found: f[1])
                elif isinstance(c, (Lt, Le, Gt, Ge)) and isinstance(self.indexes.get(col), SortedIndex):
                    b = bounds.setdefault(col, [None, True, None, True])
                    if isinstance(c, (Gt, Ge)):  # 取更紧的下界（同值时开区间更紧）
                        if b[0] is None or v > b[0] or (v == b[0] and isinstance(c, Gt)):
                            b[0], b[1] = v, isinstance(c, Ge)
                    elif b[2] is None or v < b[2] or (v == b[2] and isinstance(c, Lt)):
                        b[2], b[3] = v, isinstance(c, Le)
            elif isinstance(c, In) and None not in c.values:
                found = self._lookup_eq(c.left.name, c.values)
                if found is not None:
                    consider(len(found[1]), f"INDEX {found[0]} {self.name}.{c.left.name} IN (…{len(c.values)}) ({len(found[1])} of {total})", lambda f=found: f[1])
        for col, (lo, lo_incl, hi, hi_incl) in bounds.items():
            ix = self.indexes[col]
            i, j = ix.range(lo, lo_incl, hi, hi_incl)
            consider(j - i, f"INDEX sorted {self.name}.{col} range {lo!r}..{hi!r} ({j - i} of {total})", lambda ix=ix, i=i, j=j: ix.pks[i:j])
        return best[1], best[2]

    def _lookup_eq(self, col: str, values: Iterable[Any]) -> tuple[str, list] | None:
        """用主键字典或该列的索引取等值候选；没有可用的就返回 None。"""
        if col == self.pk:
            return "pk", [v for v in dict.fromkeys(values) if v in self.rows]
        ix = self.indexes.get(col)
        if ix is None:
            return None
        pks: dict[Any, None] = {}
        for v in values:
            for pk in ix.eq(v):
                pks[pk] = None
        return ix.kind, list(pks)

    def matching(self, pred: Pred | None) -> list[Row]:
        """满足 WHERE 的行（存储的行字典本身，调用者不得修改），按插入顺序。"""
        _, pks = self.plan(pred)
        pool = self.rows.values() if pks is None else (self.rows[pk] for pk in pks)
        out = [r for r in pool if pred is None or pred.eval(r) is True]
        out.sort(key=lambda r: self.seq[r[self.pk]])
        return out

    def add_index(self, column: str, kind: str) -> None:
        if column not in self.col:
            raise NoSuchColumn(column)
        if column in self.indexes:
            raise DBError(f"index on {self.name}.{column} already exists")
        ix = {"hash": HashIndex, "sorted": SortedIndex}[kind](column)
        for pk, row in self.rows.items():
            ix.add(row[column], pk)
        self.indexes[column] = ix

    def check_invariants(self) -> None:
        """测试用：索引内容必须等于"从行数据重建"的结果。"""
        assert set(self.rows) == set(self.seq)
        for pk, row in self.rows.items():
            assert row[self.pk] == pk
        for col, ix in self.indexes.items():
            fresh = type(ix)(col)
            for pk, row in self.rows.items():
                fresh.add(row[col], pk)
            if isinstance(ix, HashIndex):
                assert ix.map == fresh.map, (self.name, col)
            else:
                assert ix.keys == sorted(ix.keys)
                assert sorted(zip(ix.keys, ix.pks)) == sorted(zip(fresh.keys, fresh.pks)), (self.name, col)


# ═══════════════ Database：select 的流水线、JOIN、事务 ═══════════════

class Database:
    def __init__(self):
        self.tables: dict[str, Table] = {}
        self._journal: list[Callable[[], None]] = []  # undo log：逆操作闭包栈
        self._in_txn = False
        self.join_strategy = "auto"  # "auto" | "nested"（测试用：强制嵌套循环，与哈希连接对拍）

    # ── 事务与语句原子性 ──
    def _undo_to(self, mark: int) -> None:
        while len(self._journal) > mark:
            self._journal.pop()()

    @contextmanager
    def _statement(self):
        """每条语句要么全做要么全不做：出错就把 journal 撤销回语句开始处。
        没有显式事务时语句结束即"自动提交"（清空 journal）。"""
        mark = len(self._journal)
        try:
            yield
        except BaseException:
            self._undo_to(mark)
            raise
        else:
            if not self._in_txn:
                self._journal.clear()

    def begin(self) -> None:
        if self._in_txn:
            raise TransactionError("transaction already active (savepoints are not supported)")
        self._in_txn = True

    def commit(self) -> None:
        if not self._in_txn:
            raise TransactionError("no active transaction")
        self._journal.clear()
        self._in_txn = False

    def rollback(self) -> None:
        if not self._in_txn:
            raise TransactionError("no active transaction")
        self._undo_to(0)
        self._in_txn = False

    @contextmanager
    def transaction(self):
        self.begin()
        try:
            yield self
        except BaseException:
            self.rollback()
            raise
        else:
            self.commit()

    # ── DDL ──
    def _table(self, name: str) -> Table:
        try:
            return self.tables[name]
        except KeyError:
            raise NoSuchTable(name) from None

    def create_table(self, name: str, columns: Sequence[Column | tuple], primary_key: str) -> None:
        if name in self.tables:
            raise TableExists(name)
        cols = [c if isinstance(c, Column) else Column(*c) for c in columns]
        with self._statement():
            self.tables[name] = Table(name, cols, primary_key, self._journal)
            self._journal.append(lambda: self.tables.pop(name))

    def create_index(self, table: str, column: str, kind: str = "hash") -> None:
        t = self._table(table)
        with self._statement():
            t.add_index(column, kind)
            self._journal.append(lambda: t.indexes.pop(column))

    # ── DML ──
    def insert(self, table: str, values: Mapping[str, Any]) -> Any:
        t = self._table(table)
        with self._statement():
            return t.insert(values)

    def update(self, table: str, set_: Mapping[str, Any], where: Pred | Mapping | None = None) -> int:
        t = self._table(table)
        scope = Scope(qualified=False)
        scope.add(table, t)
        pred = as_pred(where)
        bound = pred.bind(scope) if pred else None
        for name in set_:  # `u.age` 形式也接受
            scope.lookup(name)
        with self._statement():
            return t.update({scope.lookup(k)[0]: v for k, v in set_.items()}, bound)

    def delete(self, table: str, where: Pred | Mapping | None = None) -> int:
        t = self._table(table)
        scope = Scope(qualified=False)
        scope.add(table, t)
        pred = as_pred(where)
        bound = pred.bind(scope) if pred else None
        with self._statement():
            return t.delete(bound)

    # ── SELECT：按逻辑顺序 FROM → JOIN → WHERE → GROUP BY/聚合 → SELECT → ORDER BY → LIMIT ──
    def select(self, table: str, columns: Sequence[str | Agg] | None = None, where: Pred | Mapping | None = None,
               order_by: Sequence[Any] | None = None, limit: int | None = None, joins: Sequence[Join] = (),
               group_by: Sequence[str] = (), alias: str | None = None) -> list[Row]:
        if limit is not None and (type(limit) is not int or limit < 0):
            raise DBError(f"bad LIMIT {limit!r}")
        t = self._table(table)
        scope = Scope(qualified=bool(joins))
        from_alias = alias or table
        scope.add(from_alias, t)
        where = as_pred(where)

        # 1) FROM / 2) JOIN / 3) WHERE
        if not joins:
            rows = t.matching(where.bind(scope) if where else None)  # 单表：WHERE 可以走索引
        else:
            rows = [self._qualify(from_alias, r) for r in t.matching(None)]
            for j in joins:
                right = self._table(j.table)
                right_alias = j.alias or j.table
                scope.add(right_alias, right)
                rows = self._join(rows, right, right_alias, j.on.bind(scope), j.kind)
            if where:
                bound = where.bind(scope)
                rows = [r for r in rows if bound.eval(r) is True]

        # 4) GROUP BY + 聚合 / 5) SELECT / 6) ORDER BY / 7) LIMIT
        items = list(columns) if columns else ["*"]
        order = _norm_order(order_by)
        if group_by or any(isinstance(c, Agg) for c in items):
            out, labels = self._aggregate(scope, rows, items, group_by)
            for name, _ in order:
                if name not in labels:
                    raise NoSuchColumn(f"ORDER BY {name!r}: must be one of the selected columns {labels}")
            sort_rows(out, order)
            return out[:limit]
        sort_rows(rows, [(scope.lookup(name)[0], desc) for name, desc in order])  # 先排序再投影：ORDER BY 可以用没选出来的列
        rows = rows[:limit]
        projection: list[tuple[str, str]] = []  # (输出标签, 行字典 key)
        for c in items:
            if c == "*":
                projection.extend((k, k) for k in scope.star())
            else:
                projection.append((c, scope.lookup(c)[0]))
        return [{label: r[key] for label, key in projection} for r in rows]

    @staticmethod
    def _qualify(alias: str, row: Row) -> Row:
        return {f"{alias}.{k}": v for k, v in row.items()}

    def _aggregate(self, scope: Scope, rows: list[Row], items: list, group_by: Sequence[str]) -> tuple[list[Row], list[str]]:
        gkeys = [scope.lookup(g)[0] for g in group_by]
        plan: list[tuple[str, Agg | None, str | None]] = []
        for it in items:
            if isinstance(it, Agg):
                plan.append((it.label, it, it.bind(scope)))
            elif it == "*":
                raise DBError("SELECT * cannot be combined with GROUP BY / aggregates")
            else:
                key = scope.lookup(it)[0]
                if key not in gkeys:
                    raise DBError(f"column {it!r} must appear in GROUP BY or inside an aggregate")
                plan.append((it, None, key))
        groups: dict[tuple, list[Row]] = {}
        for r in rows:
            groups.setdefault(tuple(r[k] for k in gkeys), []).append(r)  # NULL 会分到同一组（None 可哈希）
        if not gkeys and not groups:
            groups[()] = []  # 没有 GROUP BY 的聚合：空表也输出一行（COUNT=0，其余 NULL）
        out = [{label: agg.compute(grp, key) if agg else grp[0][key] for label, agg, key in plan} for grp in groups.values()]
        return out, [label for label, _, _ in plan]

    # ── JOIN ──
    def _join(self, left_rows: list[Row], right: Table, alias: str, on: Pred, kind: str) -> list[Row]:
        if kind not in ("inner", "left"):
            raise DBError(f"unsupported join kind {kind!r}")
        right_rows = [self._qualify(alias, r) for r in right.matching(None)]
        nulls = {f"{alias}.{c.name}": None for c in right.columns}  # LEFT JOIN 没匹配时右侧补 NULL
        equi = None if self.join_strategy == "nested" else self._split_equi(on, set(nulls))
        if equi is None:
            return self._nested_loop_join(left_rows, right_rows, on, kind, nulls)
        return self._hash_join(left_rows, right_rows, equi, kind, nulls)

    @staticmethod
    def _split_equi(on: Pred, right_keys: set[str]) -> tuple[str, str, Pred | None] | None:
        """从 ON 的顶层合取项里找一条 '左侧列 = 右侧列'，它就是哈希连接的键；其余条件作为 residual 继续检查。"""
        conjuncts = on.conjuncts()
        for i, c in enumerate(conjuncts):
            if isinstance(c, Eq) and isinstance(c.right, Col) and (c.left.name in right_keys) != (c.right.name in right_keys):
                lkey, rkey = (c.right.name, c.left.name) if c.left.name in right_keys else (c.left.name, c.right.name)
                rest = conjuncts[:i] + conjuncts[i + 1:]
                return lkey, rkey, (And(*rest) if rest else None)
        return None

    @staticmethod
    def _nested_loop_join(left_rows, right_rows, on: Pred, kind: str, nulls: Row) -> list[Row]:
        """O(|L|·|R|)。任意 ON 条件都能用。"""
        out = []
        for lrow in left_rows:
            matched = False
            for rrow in right_rows:
                merged = {**lrow, **rrow}
                if on.eval(merged) is True:
                    matched = True
                    out.append(merged)
            if not matched and kind == "left":
                out.append({**lrow, **nulls})
        return out

    @staticmethod
    def _hash_join(left_rows, right_rows, equi, kind: str, nulls: Row) -> list[Row]:
        """build：把右表按连接键放进 dict（O(|R|)）；probe：左表每行 O(1) 取候选（O(|L| + 输出)）。
        NULL 键永远不匹配（NULL = NULL 是 UNKNOWN），所以不进桶、也不去探测。"""
        lkey, rkey, residual = equi
        buckets: dict[Any, list[Row]] = defaultdict(list)
        for rrow in right_rows:
            if rrow[rkey] is not None:
                buckets[rrow[rkey]].append(rrow)
        out = []
        for lrow in left_rows:
            matched = False
            k = lrow[lkey]
            if k is not None:
                for rrow in buckets.get(k, ()):
                    merged = {**lrow, **rrow}
                    if residual is None or residual.eval(merged) is True:  # LEFT JOIN：residual 属于"匹配条件"，不是事后过滤
                        matched = True
                        out.append(merged)
            if not matched and kind == "left":
                out.append({**lrow, **nulls})
        return out

    def explain(self, table: str, where: Pred | Mapping | None = None) -> str:
        t = self._table(table)
        scope = Scope(qualified=False)
        scope.add(table, t)
        pred = as_pred(where)
        return t.plan(pred.bind(scope) if pred else None)[0]

    # ── SQL 文本入口（Part 5）──
    def execute(self, sql: str, params: Sequence[Any] = ()) -> Any:
        """SELECT → list[dict]；INSERT / UPDATE / DELETE → 受影响行数；其余 → None。"""
        kind, a = Parser(sql, params).statement()
        if kind == "select":
            return self.select(**a)
        if kind == "insert":
            t = self._table(a["table"])
            cols = a["columns"] or [c.name for c in t.columns]
            with self._statement():  # 多行 VALUES 要么全进要么全不进
                for values in a["rows"]:
                    if len(values) != len(cols):
                        raise DBError(f"INSERT has {len(cols)} columns but {len(values)} values")
                    t.insert(dict(zip(cols, values)))
            return len(a["rows"])
        if kind == "update":
            return self.update(a["table"], a["set_"], a["where"])
        if kind == "delete":
            return self.delete(a["table"], a["where"])
        if kind == "create":
            return self.create_table(a["table"], a["columns"], a["primary_key"])
        return {"begin": self.begin, "commit": self.commit, "rollback": self.rollback}[kind]()


# ═══════════════ Part 5：迷你 SQL 前端（tokenizer + 递归下降）═══════════════
#
# 文法（EBNF；大写是关键字，不区分大小写；标识符区分大小写）：
#
#   statement  := ( select | insert | update | delete | create | BEGIN | COMMIT | ROLLBACK ) [ ';' ] EOF
#   select     := SELECT ( '*' | item { ',' item } )
#                 FROM table_ref { join }
#                 [ WHERE expr ] [ GROUP BY colref { ',' colref } ]
#                 [ ORDER BY order_item { ',' order_item } ] [ LIMIT int ]
#   item       := colref | agg
#   agg        := ( COUNT | SUM | AVG | MIN | MAX ) '(' ( '*' | colref ) ')'
#   table_ref  := ident [ [ AS ] ident ]
#   join       := [ INNER | LEFT [ OUTER ] ] JOIN table_ref ON expr
#   order_item := ( colref | agg ) [ ASC | DESC ]
#   insert     := INSERT INTO ident [ '(' ident { ',' ident } ')' ] VALUES row { ',' row }
#   row        := '(' literal { ',' literal } ')'
#   update     := UPDATE ident SET ident '=' literal { ',' ident '=' literal } [ WHERE expr ]
#   delete     := DELETE FROM ident [ WHERE expr ]
#   create     := CREATE TABLE ident '(' coldef { ',' coldef } ')'
#   coldef     := ident ident [ PRIMARY KEY ] [ NOT NULL ]
#
#   expr       := or_expr
#   or_expr    := and_expr { OR and_expr }              -- 优先级最低
#   and_expr   := not_expr { AND not_expr }
#   not_expr   := NOT not_expr | predicate               -- NOT 比 AND 紧
#   predicate  := '(' expr ')'
#               | operand cmp operand                    -- cmp: = <> != < <= > >=
#               | colref [ NOT ] IN '(' literal { ',' literal } ')'
#               | colref [ NOT ] BETWEEN literal AND literal
#               | colref IS [ NOT ] NULL
#   operand    := colref | literal
#   literal    := int | float | 'string' | TRUE | FALSE | NULL | '-' number | '?'
#   colref     := ident | ident '.' ident                -- tokenizer 把 t.col 作为一个 token

KEYWORDS = {
    "SELECT", "FROM", "WHERE", "JOIN", "INNER", "LEFT", "OUTER", "ON", "AND", "OR", "NOT", "IN", "IS", "NULL",
    "ORDER", "BY", "GROUP", "ASC", "DESC", "LIMIT", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE",
    "CREATE", "TABLE", "PRIMARY", "KEY", "TRUE", "FALSE", "BETWEEN", "AS", "BEGIN", "COMMIT", "ROLLBACK",
}
SQL_TYPES = {"INT": int, "INTEGER": int, "TEXT": str, "VARCHAR": str, "REAL": float, "FLOAT": float, "BOOL": bool, "BOOLEAN": bool}
_TOKEN = re.compile(
    r"""\s*(?:(?P<num>\d+\.\d+|\d+)|(?P<str>'(?:[^']|'')*')|(?P<id>[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)?)|(?P<op><=|>=|<>|!=|[=<>(),*?;-]))"""
)
_CMP = {"=": Eq, "<>": Ne, "!=": Ne, "<": Lt, "<=": Le, ">": Gt, ">=": Ge}
_FLIP = {"=": Eq, "<>": Ne, "!=": Ne, "<": Gt, "<=": Ge, ">": Lt, ">=": Le}  # `5 < age` ≡ `age > 5`


def tokenize(sql: str) -> list[tuple[str, Any, int]]:
    """返回 [(kind, value, 位置)]，kind ∈ lit / kw / id / op / eof。"""
    out: list[tuple[str, Any, int]] = []
    pos = 0
    while True:
        m = _TOKEN.match(sql, pos)
        if not m:
            rest = sql[pos:].strip()
            if rest:
                raise SQLSyntaxError(f"unexpected character {rest[0]!r} at position {sql.index(rest[0], pos)}")
            break
        kind, text = m.lastgroup, m.group(m.lastgroup)
        if kind == "num":
            out.append(("lit", float(text) if "." in text else int(text), m.start(kind)))
        elif kind == "str":
            out.append(("lit", text[1:-1].replace("''", "'"), m.start(kind)))
        elif kind == "id":
            out.append(("kw", text.upper(), m.start(kind)) if text.upper() in KEYWORDS else ("id", text, m.start(kind)))
        else:
            out.append(("op", text, m.start(kind)))
        pos = m.end()
    out.append(("eof", None, len(sql)))
    return out


class Parser:
    def __init__(self, sql: str, params: Sequence[Any] = ()):
        self.toks = tokenize(sql)
        self.i = 0
        self.params = list(params)
        self.next_param = 0

    # ── token 工具 ──
    def peek(self) -> tuple[str, Any, int]:
        return self.toks[self.i]

    def advance(self) -> tuple[str, Any, int]:
        tok = self.toks[self.i]
        if tok[0] != "eof":
            self.i += 1
        return tok

    def error(self, message: str) -> SQLSyntaxError:
        kind, value, pos = self.peek()
        got = "end of input" if kind == "eof" else repr(value)
        return SQLSyntaxError(f"{message} at position {pos} (got {got})")

    def accept_kw(self, *names: str) -> str | None:
        kind, value, _ = self.peek()
        if kind == "kw" and value in names:
            self.i += 1
            return value
        return None

    def expect_kw(self, name: str) -> None:
        if not self.accept_kw(name):
            raise self.error(f"expected {name}")

    def accept_op(self, op: str) -> bool:
        kind, value, _ = self.peek()
        if kind == "op" and value == op:
            self.i += 1
            return True
        return False

    def expect_op(self, op: str) -> None:
        if not self.accept_op(op):
            raise self.error(f"expected {op!r}")

    def ident(self) -> str:
        kind, value, _ = self.peek()
        if kind != "id":
            raise self.error("expected an identifier")
        self.i += 1
        return value

    def literal(self) -> Any:
        kind, value, _ = self.peek()
        if kind == "lit":
            self.i += 1
            return value
        if self.accept_kw("NULL"):
            return None
        if self.accept_kw("TRUE"):
            return True
        if self.accept_kw("FALSE"):
            return False
        if self.accept_op("-"):
            kind, value, _ = self.peek()
            if kind != "lit" or isinstance(value, str):
                raise self.error("expected a number after '-'")
            self.i += 1
            return -value
        if self.accept_op("?"):  # 参数占位符：值不经过 SQL 文本，天然没有注入问题
            if self.next_param >= len(self.params):
                raise self.error("not enough parameters for '?'")
            self.next_param += 1
            return self.params[self.next_param - 1]
        raise self.error("expected a literal")

    # ── 语句 ──
    def statement(self) -> tuple[str, dict]:
        word = self.accept_kw("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "BEGIN", "COMMIT", "ROLLBACK")
        if word is None:
            raise self.error("expected a statement")
        if word in ("BEGIN", "COMMIT", "ROLLBACK"):
            result: tuple[str, dict] = (word.lower(), {})
        else:
            result = (word.lower(), getattr(self, f"parse_{word.lower()}")())
        self.accept_op(";")
        if self.peek()[0] != "eof":
            raise self.error("unexpected trailing input")
        return result

    def table_ref(self) -> tuple[str, str | None]:
        name = self.ident()
        self.accept_kw("AS")
        alias = self.ident() if self.peek()[0] == "id" else None
        return name, alias

    def aggregate_ahead(self) -> bool:
        kind, value, _ = self.peek()
        nxt = self.toks[self.i + 1]
        return kind == "id" and value.lower() in Agg.FUNCS and nxt[0] == "op" and nxt[1] == "("

    def aggregate(self) -> Agg:
        func = self.ident()
        self.expect_op("(")
        column = "*" if self.accept_op("*") else self.ident()
        self.expect_op(")")
        try:
            return Agg(func, column)
        except DBError as e:
            raise SQLSyntaxError(str(e)) from None

    def parse_select(self) -> dict:
        columns: list[str | Agg] | None = None
        if not self.accept_op("*"):
            columns = []
            while True:
                columns.append(self.aggregate() if self.aggregate_ahead() else self.ident())
                if not self.accept_op(","):
                    break
        self.expect_kw("FROM")
        table, alias = self.table_ref()
        joins: list[Join] = []
        while True:
            kind = "inner"
            if self.accept_kw("LEFT"):
                kind = "left"
                self.accept_kw("OUTER")
            elif self.accept_kw("INNER"):
                pass
            elif self.peek() != ("kw", "JOIN", self.peek()[2]):
                break
            self.expect_kw("JOIN")
            jt, ja = self.table_ref()
            self.expect_kw("ON")
            joins.append(Join(jt, self.expr(), kind, ja))
        where = self.expr() if self.accept_kw("WHERE") else None
        group_by: list[str] = []
        if self.accept_kw("GROUP"):
            self.expect_kw("BY")
            group_by.append(self.ident())
            while self.accept_op(","):
                group_by.append(self.ident())
        order_by: list[tuple[Any, str]] = []
        if self.accept_kw("ORDER"):
            self.expect_kw("BY")
            while True:
                key = self.aggregate() if self.aggregate_ahead() else self.ident()
                order_by.append((key, self.accept_kw("ASC", "DESC") or "ASC"))
                if not self.accept_op(","):
                    break
        limit = None
        if self.accept_kw("LIMIT"):
            kind, value, _ = self.peek()
            if kind != "lit" or type(value) is not int:
                raise self.error("LIMIT needs an integer")
            self.i += 1
            limit = value
        return dict(table=table, columns=columns, where=where, order_by=order_by, limit=limit,
                    joins=joins, group_by=group_by, alias=alias)

    def parse_insert(self) -> dict:
        self.expect_kw("INTO")
        table = self.ident()
        columns = None
        if self.accept_op("("):
            columns = [self.ident()]
            while self.accept_op(","):
                columns.append(self.ident())
            self.expect_op(")")
        self.expect_kw("VALUES")
        rows = []
        while True:
            self.expect_op("(")
            values = [self.literal()]
            while self.accept_op(","):
                values.append(self.literal())
            self.expect_op(")")
            rows.append(values)
            if not self.accept_op(","):
                break
        return dict(table=table, columns=columns, rows=rows)

    def parse_update(self) -> dict:
        table = self.ident()
        self.expect_kw("SET")
        set_: dict[str, Any] = {}
        while True:
            col = self.ident()
            self.expect_op("=")
            set_[col] = self.literal()
            if not self.accept_op(","):
                break
        return dict(table=table, set_=set_, where=self.expr() if self.accept_kw("WHERE") else None)

    def parse_delete(self) -> dict:
        self.expect_kw("FROM")
        table = self.ident()
        return dict(table=table, where=self.expr() if self.accept_kw("WHERE") else None)

    def parse_create(self) -> dict:
        self.expect_kw("TABLE")
        table = self.ident()
        self.expect_op("(")
        columns: list[Column] = []
        primary_key = None
        while True:
            name, type_name = self.ident(), self.ident()
            if type_name.upper() not in SQL_TYPES:
                raise self.error(f"unknown type {type_name!r}")
            nullable = True
            while True:
                if self.accept_kw("PRIMARY"):
                    self.expect_kw("KEY")
                    primary_key = name
                elif self.accept_kw("NOT"):
                    self.expect_kw("NULL")
                    nullable = False
                else:
                    break
            columns.append(Column(name, SQL_TYPES[type_name.upper()], nullable))
            if not self.accept_op(","):
                break
        self.expect_op(")")
        if primary_key is None:
            raise self.error("table needs a PRIMARY KEY column")
        return dict(table=table, columns=columns, primary_key=primary_key)

    # ── 表达式：每一层文法对应一个函数，优先级就是调用层次 ──
    def expr(self) -> Pred:
        parts = [self.and_expr()]
        while self.accept_kw("OR"):
            parts.append(self.and_expr())
        return parts[0] if len(parts) == 1 else Or(*parts)

    def and_expr(self) -> Pred:
        parts = [self.not_expr()]
        while self.accept_kw("AND"):
            parts.append(self.not_expr())
        return parts[0] if len(parts) == 1 else And(*parts)

    def not_expr(self) -> Pred:
        if self.accept_kw("NOT"):
            return Not(self.not_expr())
        return self.predicate()

    def operand(self) -> Col | Any:
        if self.peek()[0] == "id":
            return Col(self.ident())
        return self.literal()

    def predicate(self) -> Pred:
        if self.accept_op("("):
            inner = self.expr()
            self.expect_op(")")
            return inner
        left = self.operand()
        kind, value, _ = self.peek()
        if kind == "op" and value in _CMP:
            self.i += 1
            right = self.operand()
            if isinstance(left, Col):
                return _CMP[value](left, right)
            if isinstance(right, Col):
                return _FLIP[value](right, left)
            if left is None or right is None:
                return Const(None)
            return Const(_CMP[value].fn(left, right))
        if not isinstance(left, Col):
            raise self.error("expected a comparison operator")
        if self.accept_kw("IS"):
            negate = bool(self.accept_kw("NOT"))
            self.expect_kw("NULL")
            return Not(IsNull(left)) if negate else IsNull(left)
        negate = bool(self.accept_kw("NOT"))
        if self.accept_kw("IN"):
            self.expect_op("(")
            values = [self.literal()]
            while self.accept_op(","):
                values.append(self.literal())
            self.expect_op(")")
            p: Pred = In(left, values)
        elif self.accept_kw("BETWEEN"):
            lo = self.literal()
            self.expect_kw("AND")
            p = And(Ge(left, lo), Le(left, self.literal()))
        else:
            raise self.error("expected a comparison operator, IN, BETWEEN or IS")
        return Not(p) if negate else p


# ═══════════════ Part 6：线程安全（最简单的正确方案：一把粗粒度可重入锁）═══════════════

def _synchronized(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return wrapper


class ThreadSafeDatabase(Database):
    """每个公开方法都在同一把 RLock 里执行；`begin()` 拿到锁后一直持有到 commit / rollback，
    于是一个事务内的"读-改-写"不会被别的线程插队（等价于串行执行，隔离级别是 serializable）。
    RLock 可重入：持锁线程在事务内再调用 select / update 不会死锁。"""

    def __init__(self):
        super().__init__()
        self._lock = threading.RLock()

    create_table = _synchronized(Database.create_table)
    create_index = _synchronized(Database.create_index)
    insert = _synchronized(Database.insert)
    update = _synchronized(Database.update)
    delete = _synchronized(Database.delete)
    select = _synchronized(Database.select)
    explain = _synchronized(Database.explain)
    execute = _synchronized(Database.execute)

    def begin(self) -> None:
        self._lock.acquire()
        try:
            super().begin()
        except BaseException:
            self._lock.release()
            raise

    def commit(self) -> None:
        super().commit()  # 没有事务时这里抛错，锁不会被多释放
        self._lock.release()

    def rollback(self) -> None:
        super().rollback()
        self._lock.release()


# ══════════════════════════════ 测试 ══════════════════════════════

def _raises(exc: type[BaseException], fn: Callable[[], Any]) -> None:
    try:
        fn()
    except exc:
        return
    raise AssertionError(f"expected {exc.__name__}")


def _tuples(rows: list[Row]) -> list[tuple]:
    return [tuple(r.values()) for r in rows]


def _make_company() -> Database:
    """讲义里的手算例子用的数据。"""
    db = Database()
    db.create_table("users", [("id", int), ("name", str), ("age", int), ("city", str)], primary_key="id")
    db.create_table("orders", [("id", int), ("user_id", int), ("amount", int)], primary_key="id")
    for row in [(1, "ann", 30, "sf"), (2, "bob", 25, "nyc"), (3, "cat", 35, "sf"), (4, "dan", None, "nyc")]:
        db.insert("users", dict(zip(["id", "name", "age", "city"], row)))
    for row in [(10, 1, 50), (11, 1, 20), (12, 2, 70), (13, 9, 5), (14, 4, 40)]:
        db.insert("orders", dict(zip(["id", "user_id", "amount"], row)))
    return db


def test_lc2408() -> None:
    # 题面 Example 1
    sql = SQL(["one", "two", "three"], [2, 3, 1])
    assert sql.ins("two", ["first", "second", "third"]) is True
    assert sql.sel("two", 1, 3) == "third"
    assert sql.ins("two", ["fourth", "fifth", "sixth"]) is True
    assert sql.exp("two") == ["1,first,second,third", "2,fourth,fifth,sixth"]
    sql.rmv("two", 1)
    assert sql.sel("two", 2, 2) == "fifth"
    assert sql.exp("two") == ["2,fourth,fifth,sixth"]
    # 题面 Example 2
    sql = SQL(["one", "two", "three"], [2, 3, 1])
    assert sql.ins("two", ["first", "second", "third"])
    assert sql.sel("two", 1, 3) == "third"
    sql.rmv("two", 1)
    assert sql.sel("two", 1, 2) == "<null>"
    assert sql.ins("two", ["fourth", "fifth"]) is False
    assert sql.ins("two", ["fourth", "fifth", "sixth"]) is True
    assert sql.sel("two", 2, 1) == "fourth"        # 失败的 ins 没有消耗 id：这行是 id 2
    # 边界
    assert sql.ins("nope", ["a"]) is False
    assert sql.sel("nope", 1, 1) == "<null>"
    assert sql.sel("two", 2, 0) == "<null>" and sql.sel("two", 2, 4) == "<null>"
    assert sql.sel("two", 99, 1) == "<null>"
    sql.rmv("nope", 1)
    sql.rmv("two", 99)                              # 都是 no-op
    assert sql.exp("nope") == []
    assert sql.exp("one") == []
    sql.rmv("two", 2)
    assert sql.ins("two", ["x", "y", "z"]) and sql.exp("two") == ["3,x,y,z"]   # 删光后 id 继续增长


def test_crud() -> None:
    db = Database()
    db.create_table("users", [("id", int), ("name", str), Column("age", int), Column("email", str, nullable=False)], primary_key="id")
    assert db.insert("users", {"name": "ann", "age": 30, "email": "a@x"}) == 1       # 自增
    assert db.insert("users", {"name": "bob", "age": 25, "email": "b@x"}) == 2
    assert db.insert("users", {"id": 10, "name": "cat", "email": "c@x"}) == 10        # 显式主键，age 缺省 = NULL
    assert db.insert("users", {"name": "dan", "age": None, "email": "d@x"}) == 11     # 计数器跟着推进
    db.delete("users", {"id": 11})
    assert db.insert("users", {"name": "eve", "email": "e@x"}) == 12                  # 删除不让计数器回退

    # 错误
    _raises(NoSuchTable, lambda: db.insert("ghost", {"x": 1}))
    _raises(NoSuchTable, lambda: db.select("ghost"))
    _raises(NoSuchColumn, lambda: db.insert("users", {"nope": 1, "email": "z"}))
    _raises(NoSuchColumn, lambda: db.select("users", ["nope"]))
    _raises(NoSuchColumn, lambda: db.select("users", where=Eq("nope", 1)))
    _raises(NoSuchColumn, lambda: db.update("users", {"nope": 1}))
    _raises(DuplicateKey, lambda: db.insert("users", {"id": 1, "email": "z"}))
    _raises(TypeMismatch, lambda: db.insert("users", {"name": 5, "email": "z"}))
    _raises(TypeMismatch, lambda: db.insert("users", {"age": "30", "email": "z"}))
    _raises(TypeMismatch, lambda: db.insert("users", {"age": True, "email": "z"}))    # bool 不能混进 int 列
    _raises(NotNullViolation, lambda: db.insert("users", {"name": "z"}))              # email NOT NULL
    _raises(TableExists, lambda: db.create_table("users", [("id", int)], "id"))
    _raises(NoSuchColumn, lambda: db.create_table("t", [("id", int)], "zzz"))
    _raises(DBError, lambda: db.create_table("t", [("id", int), ("id", str)], "id"))
    _raises(DBError, lambda: db.create_table("t", [], "id"))
    assert [r["id"] for r in db.select("users")] == [1, 2, 10, 12]                    # 出错的插入没有留下痕迹

    # update：常量、callable、where 字典；返回行数
    assert db.update("users", {"age": 31}, {"id": 1}) == 1
    assert db.update("users", {"age": lambda r: r["age"] + 1}, Gt("age", 25)) == 1     # ann: 31 → 32；cat 的 age 是 NULL（UNKNOWN，不匹配）
    assert db.select("users", ["age"], where={"id": 1}) == [{"age": 32}]
    assert db.update("users", {"age": None}, {"name": "bob"}) == 1
    assert db.update("users", {"age": 1}, {"name": "nobody"}) == 0
    _raises(TypeMismatch, lambda: db.update("users", {"age": "x"}, {"id": 1}))
    _raises(NotNullViolation, lambda: db.update("users", {"email": None}, {"id": 1}))
    # 主键更新：冲突整条语句失败且无副作用；互换主键合法
    _raises(DuplicateKey, lambda: db.update("users", {"id": 2}, {"id": 1}))
    _raises(DuplicateKey, lambda: db.update("users", {"id": 5}, Gt("id", 0)))         # 多行被设成同一个主键
    assert db.update("users", {"id": lambda r: 3 - r["id"]}, In("id", [1, 2])) == 2     # 1↔2 互换
    assert db.select("users", ["name"], where={"id": 1}) == [{"name": "bob"}]
    assert db.select("users", ["name"], where={"id": 2}) == [{"name": "ann"}]
    db.tables["users"].check_invariants()

    # delete
    assert db.delete("users", Eq("name", "nobody")) == 0
    assert db.delete("users", {"name": "bob"}) == 1
    assert db.delete("users") == 3 and db.select("users") == []                        # 无 WHERE = 全删
    # float 列接受 int 并转成 float；str 主键不自增
    db.create_table("m", [("k", str), ("x", float)], "k")
    db.insert("m", {"k": "a", "x": 3})
    assert db.select("m")[0]["x"] == 3.0 and type(db.select("m")[0]["x"]) is float
    _raises(NotNullViolation, lambda: db.insert("m", {"x": 1.0}))                      # 非 int 主键不能省略
    # select 返回的是拷贝：改结果不影响库
    got = db.select("m")
    got[0]["x"] = 99.0
    assert db.select("m")[0]["x"] == 3.0


def test_predicates() -> None:
    db = Database()
    db.create_table("t", [("id", int), ("a", int), ("b", str)], "id")
    for i, (a, b) in enumerate([(1, "x"), (2, None), (None, "y"), (4, "x"), (None, None)], start=1):
        db.insert("t", {"a": a, "b": b})

    def ids(pred: Pred | None) -> list[int]:
        return [r["id"] for r in db.select("t", ["id"], where=pred)]

    assert ids(Eq("a", 2)) == [2]
    assert ids(Ne("a", 2)) == [1, 4]                                   # NULL 行不在里面！
    assert ids(Lt("a", 4)) == [1, 2] and ids(Le("a", 4)) == [1, 2, 4]
    assert ids(Gt("a", 1)) == [2, 4] and ids(Ge("a", 1)) == [1, 2, 4]
    assert ids(Eq("a", None)) == []                                    # = NULL 永远不成立
    assert ids(IsNull("a")) == [3, 5] and ids(Not(IsNull("a"))) == [1, 2, 4]
    assert ids(In("a", [1, 4, 9])) == [1, 4]
    assert ids(In("a", [1, None])) == [1]                              # 列表含 NULL：没命中 → UNKNOWN，不是 False
    assert ids(Not(In("a", [1, None]))) == []                          # NOT IN 含 NULL 的经典陷阱：一行都选不出
    assert ids(Not(In("a", [1]))) == [2, 4]
    assert ids(Not(Eq("a", 2))) == [1, 4]                              # NOT UNKNOWN = UNKNOWN
    assert ids(And(Eq("a", 1), Eq("b", "x"))) == [1]
    assert ids(Or(Eq("a", 2), Eq("b", "y"))) == [2, 3]
    assert ids(Eq("a", 1) | Eq("a", 4)) == [1, 4]                      # 运算符糖
    assert ids((Gt("a", 0) & Eq("b", "x")) | IsNull("b")) == [1, 2, 4, 5]
    assert ids(~Eq("b", "x")) == [3]                                   # b 为 NULL 的行 NOT UNKNOWN = UNKNOWN，也不在
    assert ids({"b": "x"}) == [1, 4] and ids({"b": None}) == [2, 5]    # 字典糖
    assert ids(Eq("a", Col("id"))) == [1, 2, 4]                        # 列与列比较
    # 三值逻辑真值表
    T, F, U = True, False, None
    row = {"p": None}

    class K(Pred):
        def __init__(self, v): self.v = v
        def eval(self, row): return self.v

    for x in (T, F, U):
        for y in (T, F, U):
            expect_and = F if F in (x, y) else (U if U in (x, y) else T)
            expect_or = T if T in (x, y) else (U if U in (x, y) else F)
            assert And(K(x), K(y)).eval(row) is expect_and, (x, y)
            assert Or(K(x), K(y)).eval(row) is expect_or, (x, y)
        assert Not(K(x)).eval(row) is (U if x is U else (not x))
    assert And().eval({}) is True and Or().eval({}) is False
    # 类型检查发生在 bind（执行前），空表也一样
    _raises(TypeMismatch, lambda: db.select("t", where=Eq("a", "one")))
    _raises(TypeMismatch, lambda: db.select("t", where=In("a", [1, "x"])))
    _raises(TypeMismatch, lambda: db.select("t", where=Eq("a", Col("b"))))
    _raises(TypeMismatch, lambda: db.select("t", where=Eq("a", True)))
    assert db.select("t", where=Gt("a", 1.5), columns=["id"]) == [{"id": 2}, {"id": 4}]   # int 列和 float 字面量可比


def test_order_by() -> None:
    db = Database()
    db.create_table("p", [("id", int), ("dept", str), ("sal", int)], "id")
    data = [("eng", 10), ("ops", 5), ("eng", 30), (None, 7), ("ops", None), ("eng", 10), (None, None), ("ops", 5)]
    for dept, sal in data:
        db.insert("p", {"dept": dept, "sal": sal})
    ids = lambda **kw: [r["id"] for r in db.select("p", ["id"], **kw)]   # noqa: E731
    # NULL 最小：ASC 时在最前，DESC 时在最后
    assert ids(order_by=["sal"]) == [5, 7, 2, 8, 4, 1, 6, 3]
    assert ids(order_by=[("sal", "DESC")]) == [3, 1, 6, 4, 2, 8, 5, 7]
    # 多键、混合方向：dept ASC（NULL 在前），sal DESC（同 dept 内）
    assert ids(order_by=["dept", ("sal", "DESC")]) == [4, 7, 3, 1, 6, 2, 8, 5]
    # 稳定：键相同的行保持插入顺序（id 2 与 8 同为 ('ops',5)；1 与 6 同为 ('eng',10)）
    got = ids(order_by=["dept", ("sal", "DESC")])
    assert got.index(1) < got.index(6) and got.index(2) < got.index(8)
    assert ids(order_by=[("dept", "DESC"), "sal"]) == [5, 2, 8, 1, 6, 3, 7, 4]   # ops(NULL,5,5) eng(10,10,30) NULL(NULL,7)
    # 与 Python 的参考实现对拍（NULL 最小、其余同方向）
    def reference(keys):
        rows = [dict(id=i + 1, dept=d, sal=s) for i, (d, s) in enumerate(data)]
        for k, desc in reversed(keys):
            rows.sort(key=lambda r: (r[k] is not None, r[k] if r[k] is not None else 0), reverse=desc)
        return [r["id"] for r in rows]
    for keys in ([("dept", False), ("sal", True)], [("dept", True), ("sal", False)], [("sal", True), ("dept", True)], [("sal", False)]):
        assert ids(order_by=[(k, "DESC" if d else "ASC") for k, d in keys]) == reference(keys), keys
    # LIMIT 在排序之后
    assert ids(order_by=[("sal", "DESC")], limit=2) == [3, 1]
    assert ids(order_by=["sal"], limit=0) == [] and ids(limit=100) == list(range(1, 9))
    _raises(DBError, lambda: ids(limit=-1))
    _raises(DBError, lambda: ids(order_by=[("sal", "SIDEWAYS")]))
    _raises(NoSuchColumn, lambda: ids(order_by=["nope"]))
    # ORDER BY 可以用没有被选出来的列
    assert db.select("p", ["dept"], order_by=[("id", "DESC")], limit=1) == [{"dept": "ops"}]


def test_join() -> None:
    db = _make_company()
    q = dict(columns=["u.name", "o.amount"], alias="u")
    inner = Join("orders", Eq("u.id", Col("o.user_id")), "inner", "o")
    # 讲义里手算的例子
    rows = db.select("users", ["u.name", "o.amount"], where=And(Ge("o.amount", 20), Not(IsNull("u.age"))),
                     order_by=[("o.amount", "DESC")], limit=2, joins=[inner], alias="u")
    assert rows == [{"u.name": "bob", "o.amount": 70}, {"u.name": "ann", "o.amount": 50}]
    # JOIN 的中间结果（还没 WHERE）：dan 有订单、cat 没订单、订单 13 没有用户
    all_inner = db.select("users", ["u.name", "o.id"], order_by=["o.id"], joins=[inner], alias="u")
    assert _tuples(all_inner) == [("ann", 10), ("ann", 11), ("bob", 12), ("dan", 14)]
    left = Join("orders", Eq("u.id", Col("o.user_id")), "left", "o")
    all_left = db.select("users", ["u.name", "o.id"], order_by=["u.id", "o.id"], joins=[left], alias="u")
    assert _tuples(all_left) == [("ann", 10), ("ann", 11), ("bob", 12), ("cat", None), ("dan", 14)]
    # LEFT JOIN 的反连接：没有订单的用户
    anti = db.select("users", ["u.name"], where=IsNull("o.id"), joins=[left], alias="u")
    assert anti == [{"u.name": "cat"}]
    # WHERE 过滤 LEFT JOIN 右表的非 NULL 条件，会把补 NULL 的行也滤掉（等价于 inner）；ON 里的条件则不会
    assert _tuples(db.select("users", ["u.name", "o.id"], where=Gt("o.amount", 0), joins=[left], alias="u", order_by=["o.id"])) == \
        [("ann", 10), ("ann", 11), ("bob", 12), ("dan", 14)]
    left_big = Join("orders", And(Eq("u.id", Col("o.user_id")), Gt("o.amount", 45)), "left", "o")
    assert _tuples(db.select("users", ["u.name", "o.id"], joins=[left_big], alias="u", order_by=["u.id"])) == \
        [("ann", 10), ("bob", 12), ("cat", None), ("dan", None)]
    # 限定列名与重名：id 两边都有
    _raises(AmbiguousColumn, lambda: db.select("users", ["id"], joins=[inner], alias="u"))
    _raises(NoSuchColumn, lambda: db.select("users", ["x.id"], joins=[inner], alias="u"))
    _raises(NoSuchColumn, lambda: db.select("users", ["users.id"], joins=[inner], alias="u"))   # 起了别名就必须用别名
    assert db.select("users", ["name", "amount"], joins=[Join("orders", Eq("users.id", Col("user_id")))], order_by=["amount"], limit=1) == \
        [{"name": "ann", "amount": 20}]                                                          # 不重名的列可以不限定
    # SELECT *：连接后列名带限定
    star = db.select("users", None, joins=[inner], alias="u", order_by=["o.id"], limit=1)
    assert list(star[0]) == ["u.id", "u.name", "u.age", "u.city", "o.id", "o.user_id", "o.amount"]
    # 自连接：必须起别名（员工 → 经理）
    db.create_table("emp", [("id", int), ("name", str), ("mgr", int)], "id")
    for i, (n, m) in enumerate([("root", None), ("a", 1), ("b", 1), ("c", 2)], start=1):
        db.insert("emp", {"name": n, "mgr": m})
    self_join = Join("emp", Eq("e.mgr", Col("m.id")), "left", "m")
    got = db.select("emp", ["e.name", "m.name"], joins=[self_join], alias="e", order_by=["e.id"])
    assert _tuples(got) == [("root", None), ("a", "root"), ("b", "root"), ("c", "a")]
    _raises(DBError, lambda: db.select("emp", ["name"], joins=[Join("emp", Eq("emp.mgr", Col("emp.id")))]))   # 没起别名
    # 三表连接 + 类型检查
    db.create_table("city", [("name", str), ("state", str)], "name")
    db.insert("city", {"name": "sf", "state": "CA"})
    db.insert("city", {"name": "nyc", "state": "NY"})
    three = db.select("users", ["u.name", "o.amount", "c.state"], alias="u", order_by=["o.id"],
                      joins=[inner, Join("city", Eq("u.city", Col("c.name")), "inner", "c")])
    assert _tuples(three) == [("ann", 50, "CA"), ("ann", 20, "CA"), ("bob", 70, "NY"), ("dan", 40, "NY")]
    _raises(TypeMismatch, lambda: db.select("users", alias="u", joins=[Join("orders", Eq("u.name", Col("o.user_id")), "inner", "o")]))
    # 非等值 ON → 嵌套循环（哈希连接用不了）；两种策略必须给出同一结果
    theta = Join("orders", Lt("u.age", Col("o.amount")), "inner", "o")
    base = db.select("users", ["u.id", "o.id"], alias="u", joins=[theta], order_by=["u.id", "o.id"])
    assert len(base) > 0
    # 哈希连接 vs 嵌套循环（等值 + residual、NULL 键、重复键、inner / left）
    for kind in ("inner", "left"):
        for on in (Eq("u.id", Col("o.user_id")),
                   And(Eq("u.id", Col("o.user_id")), Gt("o.amount", 30)),
                   And(Gt("o.amount", 30), Eq("o.user_id", Col("u.id")))):     # 等号两边的顺序不影响
            j = Join("orders", on, kind, "o")
            db.join_strategy = "auto"
            fast = db.select("users", None, alias="u", joins=[j])
            db.join_strategy = "nested"
            slow = db.select("users", None, alias="u", joins=[j])
            db.join_strategy = "auto"
            assert fast == slow, (kind, on)
    # 键为 NULL 的行不匹配任何东西（包括另一个 NULL）
    db.create_table("l", [("id", int), ("k", int)], "id")
    db.create_table("r", [("id", int), ("k", int)], "id")
    for k in (1, None, 1):
        db.insert("l", {"k": k})
    for k in (1, None, 1):
        db.insert("r", {"k": k})
    nn = db.select("l", ["l.id", "r.id"], alias="l", joins=[Join("r", Eq("l.k", Col("r.k")), "inner", "r")], order_by=["l.id", "r.id"])
    assert _tuples(nn) == [(1, 1), (1, 3), (3, 1), (3, 3)]                        # 重复键 → 笛卡尔积 2×2；NULL 行没有出现
    nl = db.select("l", ["l.id", "r.id"], alias="l", joins=[Join("r", Eq("l.k", Col("r.k")), "left", "r")], order_by=["l.id", "r.id"])
    assert _tuples(nl) == [(1, 1), (1, 3), (2, None), (3, 1), (3, 3)]


def test_parser() -> None:
    db = _make_company()
    # 手算例子，字符串版
    sql = ("SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id "
           "WHERE o.amount >= 20 AND u.age IS NOT NULL ORDER BY o.amount DESC LIMIT 2;")
    assert db.execute(sql) == [{"u.name": "bob", "o.amount": 70}, {"u.name": "ann", "o.amount": 50}]
    assert db.execute("select name from users where city = 'sf' order by name desc") == [{"name": "cat"}, {"name": "ann"}]
    assert db.execute("SELECT * FROM users WHERE id = ?", [2]) == [{"id": 2, "name": "bob", "age": 25, "city": "nyc"}]
    assert db.execute("SELECT name FROM users WHERE name = ?", ["x' OR '1'='1"]) == []          # 参数化：不是注入
    # 优先级：NOT > AND > OR
    assert db.execute("SELECT id FROM users WHERE id = 1 OR id = 2 AND id = 3") == [{"id": 1}]          # = 1 OR (2 AND 3)
    assert db.execute("SELECT id FROM users WHERE (id = 1 OR id = 2) AND id = 3") == []
    assert db.execute("SELECT id FROM users WHERE NOT id = 1 AND id < 3") == [{"id": 2}]               # (NOT id=1) AND id<3
    assert db.execute("SELECT id FROM users WHERE NOT (id = 1 AND id < 3) AND id < 3") == [{"id": 2}]
    assert db.execute("SELECT id FROM users WHERE id IN (1, 3) AND NOT age > 30") == [{"id": 1}]
    assert db.execute("SELECT id FROM users WHERE id NOT IN (1, 2, 3)") == [{"id": 4}]
    assert db.execute("SELECT id FROM users WHERE age BETWEEN 25 AND 30") == [{"id": 1}, {"id": 2}]
    assert db.execute("SELECT id FROM users WHERE age NOT BETWEEN 25 AND 30") == [{"id": 3}]
    assert db.execute("SELECT id FROM users WHERE 28 < age") == [{"id": 1}, {"id": 3}]                 # 字面量在左边：翻转
    assert db.execute("SELECT id FROM users WHERE 1 = 1 AND id <> 1 AND id != 2") == [{"id": 3}, {"id": 4}]
    assert db.execute("SELECT id FROM users WHERE age = NULL") == []
    assert db.execute("SELECT id FROM users WHERE age > -1 ORDER BY id LIMIT 1") == [{"id": 1}]         # 负数
    assert db.execute("SELECT users.id FROM users LEFT OUTER JOIN orders ON users.id = orders.user_id WHERE orders.id IS NULL") == [{"users.id": 3}]
    # 聚合
    assert db.execute("SELECT city, COUNT(*), AVG(age) FROM users GROUP BY city ORDER BY city") == \
        [{"city": "nyc", "count(*)": 2, "avg(age)": 25.0}, {"city": "sf", "count(*)": 2, "avg(age)": 32.5}]
    _raises(NoSuchColumn, lambda: db.execute("SELECT city FROM users GROUP BY city ORDER BY COUNT(*) DESC"))   # 排序用的聚合必须在 SELECT 列表里
    assert db.execute("SELECT city, COUNT(*) FROM users GROUP BY city ORDER BY COUNT(*) DESC, city") == \
        [{"city": "nyc", "count(*)": 2}, {"city": "sf", "count(*)": 2}]
    # DML
    assert db.execute("INSERT INTO users (name, age, city) VALUES ('eve', 41, 'la'), ('it''s', NULL, 'la')") == 2
    assert db.execute("SELECT name FROM users WHERE id > 4 ORDER BY id") == [{"name": "eve"}, {"name": "it's"}]    # '' 转义
    assert db.execute("UPDATE users SET age = 42, city = 'sea' WHERE name = 'eve'") == 1
    assert db.execute("SELECT age, city FROM users WHERE name = 'eve'") == [{"age": 42, "city": "sea"}]
    assert db.execute("DELETE FROM users WHERE city = 'la'") == 1
    assert db.execute("DELETE FROM users") == 5 and db.execute("SELECT * FROM users") == []
    db.execute("CREATE TABLE z (k TEXT PRIMARY KEY, v REAL NOT NULL, ok BOOL)")
    assert db.execute("INSERT INTO z VALUES ('a', 1.5, TRUE)") == 1
    assert db.execute("SELECT * FROM z") == [{"k": "a", "v": 1.5, "ok": True}]
    # INSERT 多行是原子的：第二行重复主键 → 第一行也不留
    _raises(DuplicateKey, lambda: db.execute("INSERT INTO z VALUES ('b', 2.0, NULL), ('a', 3.0, NULL)"))
    assert db.execute("SELECT k FROM z") == [{"k": "a"}]
    # 事务语句
    db.execute("BEGIN")
    db.execute("INSERT INTO z VALUES ('t', 0.5, NULL)")
    db.execute("ROLLBACK")
    assert db.execute("SELECT k FROM z") == [{"k": "a"}]
    # 语法错误
    for bad in ["", "SELEC * FROM users", "SELECT FROM users", "SELECT * users", "SELECT * FROM",
                "SELECT * FROM users WHERE", "SELECT * FROM users WHERE id =", "SELECT * FROM users WHERE (id = 1",
                "SELECT * FROM users WHERE id = 1 junk", "SELECT * FROM users LIMIT x", "SELECT * FROM users ORDER id",
                "SELECT * FROM users WHERE name = 'unterminated", "SELECT * FROM users WHERE id = $1",
                "INSERT INTO users VALUES 1", "UPDATE users SET WHERE id = 1", "DELETE users",
                "SELECT * FROM users WHERE id = ?", "SELECT SUM(*) FROM users", "CREATE TABLE q (a INT)",
                "SELECT * FROM users WHERE 1 2", "SELECT * FROM users WHERE id IN ()"]:
        _raises(SQLSyntaxError, lambda bad=bad: db.execute(bad))
    # 语义错误走 DBError 家族
    _raises(NoSuchTable, lambda: db.execute("SELECT * FROM nope"))
    _raises(NoSuchColumn, lambda: db.execute("SELECT nope FROM z"))
    _raises(TypeMismatch, lambda: db.execute("SELECT * FROM z WHERE k = 1"))
    # tokenizer
    assert [t[:2] for t in tokenize("a.b>=-1.5")][:-1] == [("id", "a.b"), ("op", ">="), ("op", "-"), ("lit", 1.5)]
    assert tokenize("x")[-1][0] == "eof"


def test_indexes_and_planner() -> None:
    db = Database()
    db.create_table("e", [("id", int), ("uid", int), ("ts", int), ("kind", str)], "id")
    rng = random.Random(7)
    for _ in range(300):
        db.insert("e", {"uid": rng.randint(0, 29), "ts": rng.randint(0, 999), "kind": rng.choice(["a", "b", "c", None])})
    plain = [r["id"] for r in db.select("e", ["id"], where=And(Eq("uid", 3), Ge("ts", 100), Lt("ts", 500)))]
    assert "SCAN" in db.explain("e", Eq("uid", 3))
    db.create_index("e", "uid", "hash")
    db.create_index("e", "ts", "sorted")
    assert db.explain("e", Eq("uid", 3)).startswith("INDEX hash e.uid = 3")
    assert db.explain("e", {"id": 5}).startswith("INDEX pk e.id")                           # 主键天然有哈希
    assert db.explain("e", And(Ge("ts", 100), Lt("ts", 120))).startswith("INDEX sorted e.ts range 100..120")
    assert db.explain("e", Eq("kind", "a")).startswith("SCAN")                              # 没有索引的列
    assert db.explain("e", Or(Eq("uid", 3), Eq("ts", 4))).startswith("SCAN")                # OR 不拆（保守）
    assert db.explain("e", In("uid", [1, 2, 3])).startswith("INDEX hash e.uid IN")
    assert db.explain("e", Ne("uid", 3)).startswith("SCAN")
    assert db.explain("e", Eq("uid", None)).startswith("SCAN")                              # = NULL 不走索引（也永远无结果）
    # 同时有两个可用索引时选命中数少的
    assert "e.ts" in db.explain("e", And(Eq("uid", 3), Eq("ts", 5)))
    # 结果和不走索引时一致，顺序也一致（都是插入顺序）
    with_ix = [r["id"] for r in db.select("e", ["id"], where=And(Eq("uid", 3), Ge("ts", 100), Lt("ts", 500)))]
    assert with_ix == plain and len(plain) > 0
    # 范围边界：开 / 闭、同列多个条件取交集、空区间
    ref = lambda f: [r["id"] for r in db.tables["e"].matching(None) if f(r)]   # noqa: E731  # 全表扫描参考答案
    for pred, f in [(Gt("ts", 500), lambda r: r["ts"] > 500), (Ge("ts", 500), lambda r: r["ts"] >= 500),
                    (Lt("ts", 3), lambda r: r["ts"] < 3), (Le("ts", 3), lambda r: r["ts"] <= 3),
                    (And(Gt("ts", 10), Gt("ts", 20), Le("ts", 40), Lt("ts", 60)), lambda r: 20 < r["ts"] <= 40),
                    (And(Ge("ts", 20), Gt("ts", 20)), lambda r: r["ts"] > 20),
                    (And(Gt("ts", 50), Lt("ts", 50)), lambda r: False),
                    (And(Ge("ts", 50), Le("ts", 50)), lambda r: r["ts"] == 50),
                    (In("uid", [1, 1, 2, 99]), lambda r: r["uid"] in (1, 2)),
                    (Eq("uid", 99), lambda r: False)]:
        assert [r["id"] for r in db.select("e", ["id"], where=pred)] == ref(f), pred
    # 维护：update / delete / insert 之后索引与行一致
    db.update("e", {"uid": 77, "ts": lambda r: r["ts"] + 1}, Lt("ts", 100))
    db.delete("e", Eq("uid", 5))
    for _ in range(50):
        db.insert("e", {"uid": rng.randint(0, 29), "ts": rng.randint(0, 999)})
    db.update("e", {"id": lambda r: r["id"] + 1000}, Eq("uid", 77))
    db.tables["e"].check_invariants()
    assert [r["id"] for r in db.select("e", ["id"], where=Eq("uid", 77))] == ref(lambda r: r["uid"] == 77)
    _raises(DBError, lambda: db.create_index("e", "uid", "sorted"))
    _raises(NoSuchColumn, lambda: db.create_index("e", "nope", "hash"))
    # SortedIndex / HashIndex 单元
    ix = SortedIndex("x")
    for pk, v in enumerate([5, 1, 5, 3, 5, None, 9]):
        ix.add(v, pk)
    assert ix.keys == [1, 3, 5, 5, 5, 9] and sorted(ix.eq(5)) == [0, 2, 4]
    assert ix.range(3, True, 9, False) == (1, 5) and ix.range(3, False, 9, True) == (2, 6) and ix.range(10, True, None, True) == (6, 6)
    ix.remove(5, 2)
    assert sorted(ix.eq(5)) == [0, 4]
    hx = HashIndex("x")
    hx.add(1, "a"); hx.add(1, "b"); hx.add(None, "n")
    hx.remove(1, "a")
    assert hx.eq(1) == ["b"] and hx.eq(2) == [] and None not in hx.map
    hx.remove(1, "b")
    assert hx.map == {}


def test_aggregates() -> None:
    db = _make_company()
    agg = lambda cols, **kw: db.select("users", cols, **kw)   # noqa: E731
    assert agg([Agg("count")]) == [{"count(*)": 4}]
    assert agg([Agg("count", "age"), Agg("sum", "age"), Agg("min", "age"), Agg("max", "age")]) == \
        [{"count(age)": 3, "sum(age)": 90, "min(age)": 25, "max(age)": 35}]                       # NULL 被忽略
    assert agg([Agg("avg", "age", "mean")]) == [{"mean": 30.0}]
    assert agg([Agg("count"), Agg("sum", "age"), Agg("avg", "age"), Agg("min", "age")], where=Gt("id", 99)) == \
        [{"count(*)": 0, "sum(age)": None, "avg(age)": None, "min(age)": None}]                   # 空输入、无 GROUP BY：仍是一行
    assert agg(["city", Agg("count")], group_by=["city"], where=Gt("id", 99)) == []                 # 空输入、有 GROUP BY：没有行
    assert agg(["city", Agg("count"), Agg("max", "age")], group_by=["city"], order_by=["city"]) == \
        [{"city": "nyc", "count(*)": 2, "max(age)": 25}, {"city": "sf", "count(*)": 2, "max(age)": 35}]
    assert agg(["city", Agg("sum", "age")], group_by=["city"], order_by=[(Agg("sum", "age"), "DESC")]) == \
        [{"city": "sf", "sum(age)": 65}, {"city": "nyc", "sum(age)": 25}]
    assert agg(["city", Agg("count")], group_by=["city"], order_by=[("count(*)", "DESC"), "city"], limit=1) == [{"city": "nyc", "count(*)": 2}]
    # NULL 分到同一组
    db.insert("users", {"name": "nul1", "age": None, "city": None})
    db.insert("users", {"name": "nul2", "age": None, "city": None})
    assert agg(["city", Agg("count")], group_by=["city"], order_by=["city"])[0] == {"city": None, "count(*)": 2}
    # 带 JOIN 的聚合：每个用户的订单数和总额（LEFT JOIN 保留没订单的人；COUNT(o.id) 对补 NULL 的行是 0）
    rows = db.select("users", ["u.name", Agg("count", "o.id"), Agg("sum", "o.amount")], alias="u", group_by=["u.name"], order_by=["u.name"],
                     joins=[Join("orders", Eq("u.id", Col("o.user_id")), "left", "o")], where=Lt("u.id", 5))
    assert _tuples(rows) == [("ann", 2, 70), ("bob", 1, 70), ("cat", 0, None), ("dan", 1, 40)]
    _raises(DBError, lambda: agg(["name", Agg("count")], group_by=["city"]))                       # name 不在 GROUP BY 里
    _raises(DBError, lambda: agg(["name", Agg("count")]))
    _raises(DBError, lambda: agg(["*"], group_by=["city"]))
    _raises(TypeMismatch, lambda: agg([Agg("sum", "city")]))
    _raises(DBError, lambda: Agg("sum", "*"))
    _raises(DBError, lambda: Agg("median", "age"))
    _raises(NoSuchColumn, lambda: agg(["city", Agg("count")], group_by=["city"], order_by=["age"]))


def test_transactions() -> None:
    db = Database()
    db.create_table("acct", [("id", int), ("bal", int)], "id")
    db.create_index("acct", "bal", "sorted")
    for bal in (100, 50):
        db.insert("acct", {"bal": bal})
    snapshot = lambda: db.select("acct", order_by=["id"])   # noqa: E731

    before = snapshot()
    db.begin()
    db.update("acct", {"bal": lambda r: r["bal"] - 30}, {"id": 1})
    db.update("acct", {"bal": lambda r: r["bal"] + 30}, {"id": 2})
    db.insert("acct", {"bal": 7})
    db.delete("acct", {"id": 2})
    db.create_table("tmp", [("k", int)], "k")
    assert db.select("acct", order_by=["id"]) != before
    db.rollback()
    assert snapshot() == before and "tmp" not in db.tables
    assert db.insert("acct", {"bal": 1}) == 3                       # 回滚把自增计数器也恢复了（id 3 没有被消耗）
    db.delete("acct", {"id": 3})
    db.tables["acct"].check_invariants()

    with db.transaction():
        db.update("acct", {"bal": 0}, {"id": 1})
    assert db.select("acct", ["bal"], where={"id": 1}) == [{"bal": 0}]
    before = snapshot()
    try:
        with db.transaction():
            db.update("acct", {"bal": 999}, {"id": 1})
            db.insert("acct", {"bal": 5, "id": 2})                    # 重复主键 → 异常 → 整个事务回滚
    except DuplicateKey:
        pass
    assert snapshot() == before
    db.tables["acct"].check_invariants()
    # 语句原子性：不在事务里时，失败的语句不留痕迹；事务里失败的语句也只撤销它自己
    _raises(DuplicateKey, lambda: db.update("acct", {"id": 1}, Gt("id", 0)))
    assert snapshot() == before
    db.begin()
    db.insert("acct", {"bal": 11})
    _raises(DuplicateKey, lambda: db.insert("acct", {"id": 1, "bal": 0}))
    assert len(db.select("acct")) == 3                                # 第一条 insert 还在
    db.commit()
    assert len(db.select("acct")) == 3 and db._journal == []
    # 误用
    _raises(TransactionError, db.commit)
    _raises(TransactionError, db.rollback)
    db.begin()
    _raises(TransactionError, db.begin)
    db.rollback()
    # 随机操作 + 随机回滚：回滚后与快照完全一致
    rng = random.Random(3)
    for _ in range(40):
        before = snapshot()
        db.begin()
        for _ in range(rng.randint(1, 8)):
            op = rng.choice("iud")
            try:
                if op == "i":
                    db.insert("acct", {"bal": rng.randint(0, 9)})
                elif op == "u":
                    db.update("acct", {"bal": rng.randint(0, 9)}, Lt("bal", rng.randint(0, 9)))
                else:
                    db.delete("acct", Eq("bal", rng.randint(0, 9)))
            except DBError:
                pass
        if rng.random() < 0.5:
            db.rollback()
            assert snapshot() == before
        else:
            db.commit()
        db.tables["acct"].check_invariants()


def test_threads() -> None:
    db = ThreadSafeDatabase()
    db.create_table("c", [("id", int), ("n", int)], "id")
    db.insert("c", {"id": 1, "n": 0})
    db.create_table("acct", [("id", int), ("bal", int)], "id")
    for i in range(4):
        db.insert("acct", {"id": i, "bal": 100})
    errors: list[BaseException] = []

    def incrementer() -> None:
        try:
            for _ in range(300):
                with db.transaction():                              # 读-改-写必须在同一个事务里
                    n = db.select("c", ["n"], where={"id": 1})[0]["n"]
                    db.update("c", {"n": n + 1}, {"id": 1})
        except BaseException as e:   # noqa: BLE001
            errors.append(e)

    def transferer(seed: int) -> None:
        rng = random.Random(seed)
        try:
            for _ in range(200):
                a, b = rng.sample(range(4), 2)
                with db.transaction():
                    bal = db.select("acct", ["bal"], where={"id": a})[0]["bal"]
                    amount = rng.randint(1, 30)
                    if bal >= amount:
                        db.update("acct", {"bal": lambda r, d=-amount: r["bal"] + d}, {"id": a})
                        db.update("acct", {"bal": lambda r, d=amount: r["bal"] + d}, {"id": b})
        except BaseException as e:   # noqa: BLE001
            errors.append(e)

    def auditor() -> None:
        try:
            for _ in range(100):
                with db.transaction():
                    assert sum(r["bal"] for r in db.select("acct")) == 400   # 任何时刻总额守恒：看不到转账的中间状态
        except BaseException as e:   # noqa: BLE001
            errors.append(e)

    threads = [threading.Thread(target=incrementer) for _ in range(6)]
    threads += [threading.Thread(target=transferer, args=(s,)) for s in range(3)] + [threading.Thread(target=auditor)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    assert not errors, errors
    assert db.select("c", ["n"])[0]["n"] == 6 * 300
    assert sum(r["bal"] for r in db.select("acct")) == 400
    # 锁的释放：异常、误用之后别的线程仍能拿到锁
    _raises(TransactionError, db.commit)
    _raises(DuplicateKey, lambda: db.insert("c", {"id": 1, "n": 0}))
    done = []
    t = threading.Thread(target=lambda: done.append(db.select("c")))
    t.start()
    t.join(timeout=5)
    assert done, "锁泄漏：另一个线程拿不到锁"


# ───────────────────────── 与 SQLite 对拍 ─────────────────────────

_CITIES = ["nyc", "sf", "la", "sea"]
_STATUS = ["new", "paid", "void"]
# 列规格：(限定名, 类型, 取值域)
_U_COLS = [("u.id", int), ("u.age", int), ("u.city", str), ("u.score", int)]
_O_COLS = [("o.id", int), ("o.uid", int), ("o.amount", int), ("o.status", str)]
_DOMAIN = {"age": list(range(18, 26)), "score": list(range(0, 6)), "city": _CITIES, "amount": list(range(0, 8)),
           "status": _STATUS, "id": list(range(0, 12)), "uid": list(range(0, 12))}


def _lit(v: Any) -> str:
    return "NULL" if v is None else (f"'{v}'" if isinstance(v, str) else str(v))


def _rand_atom(rng: random.Random, cols: list[tuple[str, type]]) -> str:
    name, typ = rng.choice(cols)
    dom = _DOMAIN[name.split(".")[-1]]
    pick = lambda: rng.choice(dom + [None] if rng.random() < 0.15 else dom)   # noqa: E731
    kind = rng.choice(["cmp", "cmp", "cmp", "in", "notin", "null", "notnull", "between", "colcol"])
    if kind == "cmp":
        return f"{name} {rng.choice(['=', '<>', '!=', '<', '<=', '>', '>='])} {_lit(pick())}"
    if kind in ("in", "notin"):
        values = ", ".join(_lit(pick()) for _ in range(rng.randint(1, 4)))
        return f"{name} {'NOT ' if kind == 'notin' else ''}IN ({values})"
    if kind in ("null", "notnull"):
        return f"{name} IS {'NOT ' if kind == 'notnull' else ''}NULL"
    if kind == "between" and typ is int:
        lo, hi = sorted((rng.choice(dom), rng.choice(dom)))
        return f"{name} {'NOT ' if rng.random() < 0.3 else ''}BETWEEN {lo} AND {hi}"
    same = [c for c, t in cols if t is typ and c != name]
    if kind == "colcol" and same:
        return f"{name} {rng.choice(['=', '<', '>=', '<>'])} {rng.choice(same)}"
    return f"{name} = {_lit(pick())}"


def _rand_expr(rng: random.Random, cols: list[tuple[str, type]], depth: int) -> str:
    """故意生成大量不加括号的 AND / OR / NOT 链：优先级由 SQLite 裁判。"""
    if depth == 0 or rng.random() < 0.3:
        atom = _rand_atom(rng, cols)
        return f"NOT {atom}" if rng.random() < 0.15 and " BETWEEN " not in atom and " IN " not in atom and " IS " not in atom else atom
    n = rng.randint(2, 3)
    parts = [_rand_expr(rng, cols, depth - 1) for _ in range(n)]
    parts = [f"({p})" if (" OR " in p or " AND " in p) and rng.random() < 0.6 else p for p in parts]
    text = (f" {rng.choice(['AND', 'OR'])} ").join(parts)
    return f"NOT ({text})" if rng.random() < 0.1 else text


def _make_pair(rng: random.Random, with_indexes: bool) -> tuple[Database, sqlite3.Connection]:
    lite = sqlite3.connect(":memory:")
    ours = Database()
    ddl = ["CREATE TABLE u (id INTEGER PRIMARY KEY, age INTEGER, city TEXT, score INTEGER)",
           "CREATE TABLE o (id INTEGER PRIMARY KEY, uid INTEGER, amount INTEGER, status TEXT)"]
    for stmt in ddl:
        lite.execute(stmt)
        ours.execute(stmt)
    n_u, n_o = rng.randint(0, 25), rng.randint(0, 40)
    ids = list(range(1, n_u + 1))
    rng.shuffle(ids)                                                  # 插入顺序 ≠ 主键顺序
    maybe = lambda dom: rng.choice(dom + [None]) if rng.random() < 0.8 else None   # noqa: E731
    for uid in ids:
        stmt = f"INSERT INTO u VALUES ({uid}, {_lit(maybe(_DOMAIN['age']))}, {_lit(maybe(_CITIES))}, {_lit(maybe(_DOMAIN['score']))})"
        lite.execute(stmt)
        ours.execute(stmt)
    for oid in range(1, n_o + 1):
        stmt = f"INSERT INTO o VALUES ({oid}, {_lit(maybe(list(range(0, n_u + 3))))}, {_lit(maybe(_DOMAIN['amount']))}, {_lit(maybe(_STATUS))})"
        lite.execute(stmt)
        ours.execute(stmt)
    if with_indexes:
        ours.create_index("u", "age", "sorted")
        ours.create_index("u", "city", "hash")
        ours.create_index("u", "score", "sorted")
        ours.create_index("o", "uid", "hash")
        ours.create_index("o", "amount", "sorted")
    return ours, lite


def _same(ours_rows: list[tuple], lite_rows: list[tuple], sql: str) -> None:
    assert len(ours_rows) == len(lite_rows), (sql, ours_rows, lite_rows)
    for a, b in zip(ours_rows, lite_rows):
        for x, y in zip(a, b):
            if isinstance(x, float) or isinstance(y, float):
                assert (x is None) == (y is None) and (x is None or abs(x - y) < 1e-9), (sql, a, b)
            else:
                assert x == y, (sql, a, b)


def test_sqlite_crosscheck() -> None:
    rng = random.Random(20261016)
    n_queries = 0
    for round_no in range(60):
        plain, lite = _make_pair(random.Random(round_no), with_indexes=False)
        indexed, lite2 = _make_pair(random.Random(round_no), with_indexes=True)
        for _ in range(25):
            shape = rng.choice(["single", "single", "join", "left", "agg", "agg_join"])
            if shape == "single":
                cols = [(c.split(".")[1], t) for c, t in _U_COLS]
                where = _rand_expr(rng, cols, 3) if rng.random() < 0.9 else None
                sel = rng.choice(["*", ", ".join(rng.sample([c for c, _ in cols], rng.randint(1, 4)))])
                order = ", ".join(f"{c} {rng.choice(['ASC', 'DESC'])}" for c in rng.sample(["age", "city", "score"], rng.randint(0, 3)))
                order = (order + ", " if order else "") + f"id {rng.choice(['ASC', 'DESC'])}"
                sql = f"SELECT {sel} FROM u" + (f" WHERE {where}" if where else "") + f" ORDER BY {order}" + (f" LIMIT {rng.randint(0, 12)}" if rng.random() < 0.4 else "")
            elif shape in ("join", "left"):
                cols = _U_COLS + _O_COLS
                where = _rand_expr(rng, cols, 2) if rng.random() < 0.7 else None
                on = rng.choice(["u.id = o.uid", "o.uid = u.id", "u.id = o.uid AND o.amount > 2", "u.id = o.uid AND u.city = 'sf' OR o.status = 'paid'",
                                 "u.age < o.amount", "u.id = o.uid AND u.score >= o.amount", "o.uid = u.id AND o.status IS NOT NULL"])
                sel = rng.choice(["*", "u.id, o.id", "u.city, o.amount, o.status, u.age"])
                order = ", ".join(f"{c} {rng.choice(['ASC', 'DESC'])}" for c in rng.sample(["u.city", "o.amount", "u.age"], rng.randint(0, 2)))
                order = (order + ", " if order else "") + "u.id, o.id"
                join = "LEFT JOIN" if shape == "left" else rng.choice(["JOIN", "INNER JOIN"])
                sql = f"SELECT {sel} FROM u {join} o ON {on}" + (f" WHERE {where}" if where else "") + f" ORDER BY {order}" + (f" LIMIT {rng.randint(0, 15)}" if rng.random() < 0.3 else "")
            elif shape == "agg":
                cols = [(c.split(".")[1], t) for c, t in _U_COLS]
                where = _rand_expr(rng, cols, 2) if rng.random() < 0.6 else None
                group = rng.choice(["city", "age", None])
                aggs = ", ".join(rng.sample(["COUNT(*)", "COUNT(age)", "SUM(score)", "AVG(age)", "MIN(age)", "MAX(score)", "COUNT(city)"], rng.randint(1, 4)))
                sql = f"SELECT {group + ', ' if group else ''}{aggs} FROM u" + (f" WHERE {where}" if where else "") + (f" GROUP BY {group} ORDER BY {group}" if group else "")
            else:
                cols = _U_COLS + _O_COLS
                where = _rand_expr(rng, cols, 2) if rng.random() < 0.5 else None
                sql = ("SELECT u.city, COUNT(o.id), SUM(o.amount), MAX(o.amount), AVG(u.age) FROM u LEFT JOIN o ON u.id = o.uid"
                       + (f" WHERE {where}" if where else "") + " GROUP BY u.city ORDER BY u.city")
            expected = lite.execute(sql).fetchall()
            for db in (plain, indexed):
                _same(_tuples(db.execute(sql)), expected, sql)
                if shape.startswith("join") or shape == "left":
                    db.join_strategy = "nested"
                    _same(_tuples(db.execute(sql)), expected, sql + " [nested]")
                    db.join_strategy = "auto"
            n_queries += 1
        # DML 对拍：随机 INSERT / UPDATE / DELETE，出错也要两边一致；之后全表比较
        for _ in range(12):
            kind = rng.choice(["ins", "upd", "del", "pkupd"])
            if kind == "ins":
                stmt = f"INSERT INTO u VALUES ({rng.randint(1, 40)}, {_lit(rng.choice(_DOMAIN['age']))}, {_lit(rng.choice(_CITIES))}, {rng.randint(0, 5)})"
            elif kind == "upd":
                stmt = f"UPDATE u SET age = {_lit(rng.choice(_DOMAIN['age'] + [None]))}, city = {_lit(rng.choice(_CITIES + [None]))} WHERE {_rand_expr(rng, [(c.split('.')[1], t) for c, t in _U_COLS], 2)}"
            elif kind == "del":
                stmt = f"DELETE FROM u WHERE {_rand_expr(rng, [(c.split('.')[1], t) for c, t in _U_COLS], 2)}"
            else:
                stmt = f"UPDATE u SET id = {rng.randint(1, 40)} WHERE id = {rng.randint(1, 40)}"
            try:
                lite.execute(stmt)
                lite_failed = False
            except sqlite3.IntegrityError:
                lite_failed = True
            for db in (plain, indexed):
                try:
                    db.execute(stmt)
                    assert not lite_failed, stmt
                except DuplicateKey:
                    assert lite_failed, stmt
            check = "SELECT * FROM u ORDER BY id"
            for db in (plain, indexed):
                _same(_tuples(db.execute(check)), lite.execute(check).fetchall(), stmt)
                db.tables["u"].check_invariants()
    assert n_queries >= 1000


# ───────────────────────── 性能：索引 vs 全表扫描 ─────────────────────────

def test_perf() -> dict[str, float]:
    rng = random.Random(1)
    db = Database()
    db.create_table("ev", [("id", int), ("uid", int), ("ts", int)], "id")
    n = 20_000
    for _ in range(n):
        db.insert("ev", {"uid": rng.randint(0, 1999), "ts": rng.randint(0, 10 ** 6)})
    uids = [rng.randint(0, 1999) for _ in range(40)]
    starts = [rng.randint(0, 10 ** 6 - 100) for _ in range(40)]

    def run_eq() -> list:
        return [db.select("ev", ["id"], where=Eq("uid", u)) for u in uids]

    def run_range() -> list:
        return [db.select("ev", ["id"], where=And(Ge("ts", s), Lt("ts", s + 100))) for s in starts]

    def timed(fn: Callable[[], Any]) -> tuple[float, Any]:
        t0 = time.perf_counter()
        out = fn()
        return time.perf_counter() - t0, out

    scan_eq, ref_eq = timed(run_eq)
    scan_rng, ref_rng = timed(run_range)
    db.create_index("ev", "uid", "hash")
    db.create_index("ev", "ts", "sorted")
    idx_eq, got_eq = timed(run_eq)
    idx_rng, got_rng = timed(run_range)
    assert got_eq == ref_eq and got_rng == ref_rng                      # 索引不改变结果
    assert sum(len(r) for r in ref_eq) > 0 and sum(len(r) for r in ref_rng) > 0
    speed = {"eq": scan_eq / idx_eq, "range": scan_rng / idx_rng}
    assert speed["eq"] > 20 and speed["range"] > 20, speed              # 实测是几百倍；断言留足余量防止机器抖动
    # 哈希连接 vs 嵌套循环
    db.create_table("a", [("id", int), ("k", int)], "id")
    db.create_table("b", [("id", int), ("k", int)], "id")
    for _ in range(600):
        db.insert("a", {"k": rng.randint(0, 599)})
        db.insert("b", {"k": rng.randint(0, 599)})
    j = Join("b", Eq("a.k", Col("b.k")), "inner", "b")
    t_hash, fast = timed(lambda: db.select("a", ["a.id", "b.id"], alias="a", joins=[j], order_by=["a.id", "b.id"]))
    db.join_strategy = "nested"
    t_nested, slow = timed(lambda: db.select("a", ["a.id", "b.id"], alias="a", joins=[j], order_by=["a.id", "b.id"]))
    db.join_strategy = "auto"
    assert fast == slow and t_nested / t_hash > 5, (t_nested, t_hash)
    speed["join"] = t_nested / t_hash
    return speed


def test_worked_example() -> None:
    """讲义第 0 章手算的例子：逐阶段的中间结果。"""
    db = _make_company()
    sql = ("SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id "
           "WHERE o.amount >= 20 AND u.age IS NOT NULL ORDER BY o.amount DESC LIMIT 2")
    joined = db.select("users", ["u.name", "u.age", "o.id", "o.amount"], alias="u", order_by=["o.id"],
                       joins=[Join("orders", Eq("u.id", Col("o.user_id")), "inner", "o")])
    assert _tuples(joined) == [("ann", 30, 10, 50), ("ann", 30, 11, 20), ("bob", 25, 12, 70), ("dan", None, 14, 40)]   # FROM + JOIN
    after_where = [r for r in joined if r["o.amount"] >= 20 and r["u.age"] is not None]
    assert _tuples(after_where) == [("ann", 30, 10, 50), ("ann", 30, 11, 20), ("bob", 25, 12, 70)]                      # WHERE：dan 的 age 是 NULL
    ordered = sorted(after_where, key=lambda r: r["o.amount"], reverse=True)
    assert [(r["u.name"], r["o.amount"]) for r in ordered][:2] == [("bob", 70), ("ann", 50)]                           # ORDER BY + LIMIT
    assert db.execute(sql) == [{"u.name": "bob", "o.amount": 70}, {"u.name": "ann", "o.amount": 50}]


def _run_tests() -> None:
    test_lc2408()
    test_crud()
    test_predicates()
    test_order_by()
    test_join()
    test_parser()
    test_indexes_and_planner()
    test_aggregates()
    test_transactions()
    test_threads()
    test_worked_example()
    test_sqlite_crosscheck()
    speed = test_perf()
    print(f"index speedup over full scan (20k rows): hash '=' x{speed['eq']:.0f}, sorted range x{speed['range']:.0f}; "
          f"hash join over nested loop (600x600): x{speed['join']:.0f}")


if __name__ == "__main__":
    _run_tests()
    print("OK in_memory_database")
