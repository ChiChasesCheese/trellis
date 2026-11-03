"""条件解析与内存表查询：词法 -> 语法树 -> 在每一行上求值，外加等值索引和无固定列的文档表。

整体分三层，各管一件事：
1. 词法 `_tokenize`：字符串变 token 列表，引号里的内容整体算一个 token（所以不能用 split）；
2. 语法 `_Parser`：递归下降，每个优先级一个函数，优先级低的先调用、后结合，
   这就是 AND 比 OR 紧、NOT 比 AND 紧的全部实现；
3. 求值：每种节点只管自己怎么算，`matches(row)` 返回 True / False / None（未知）。
   `Table` 只负责存行和调用，解析和存储互不知道对方，所以换存储不用改解析、加运算符不用改表。

三值逻辑（第 2 关）：任何涉及 NULL 的比较都是"未知"，AND / OR / NOT 按 SQL 的规则传播，
`select` 只保留结果为 True 的行——这样 `NOT age >= 18` 不会把 age 为 NULL 的行带进来。
"""

from __future__ import annotations

import copy
import operator
import re
from dataclasses import dataclass
from functools import lru_cache
from types import MappingProxyType
from typing import Any, Mapping, Protocol, Sequence

Row = dict[str, Any]


class QueryError(ValueError):
    """条件语法错误、未知列、类型不匹配、插入的行与表结构不符，统一抛这一种。"""


# ---- 第 1 关：词法、语法、求值 ------------------------------------------------

_OPS = MappingProxyType({"=": operator.eq, "!=": operator.ne, "<": operator.lt,
                         "<=": operator.le, ">": operator.gt, ">=": operator.ge})   # 运算符表只读
# 长运算符写前面，否则 <= 会被切成 < 和 =；引号内的整段算一个 token，所以字符串里的 AND 不会被误认
_TOKEN = re.compile(r"\s*(<=|>=|!=|=|<|>|\(|\)|,|'[^']*'|-?\d+|[A-Za-z_][\w.]*)")
_IDENT = re.compile(r"[A-Za-z_][\w.]*")
_KEYWORDS = {"AND", "OR", "NOT", "IN", "IS", "NULL"}


def _tokenize(text: str) -> list[str]:
    tokens, pos, text = [], 0, text.rstrip()
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if not m:
            raise QueryError(f"无法识别: {text[pos:]!r}")
        tokens.append(m.group(1))
        pos = m.end()
    return tokens


def _literal(token: str) -> Any:
    if token.startswith("'"):
        return token[1:-1]
    if re.fullmatch(r"-?\d+", token):
        return int(token)
    raise QueryError(f"需要整数或字符串字面量，得到 {token!r}")


def _get(row: Row, path: str) -> Any:
    """按 a.b.c 取值；任何一层缺失都当作 NULL（对平铺的列，这就是 row[name]）。"""
    value: Any = row
    for part in path.split("."):
        value = value.get(part) if isinstance(value, dict) else None
    return value


class _Node(Protocol):
    """语法树节点只需要会一件事：在一行上算出 True / False / None。结构化类型，节点之间不用继承。"""

    def matches(self, row: Row) -> bool | None: ...


@dataclass(frozen=True, slots=True)
class _Cmp:
    field: str
    op: str
    value: Any

    def matches(self, row: Row) -> bool | None:
        left = _get(row, self.field)
        if left is None:
            return None                      # 第 2 关：与 NULL 比较的结果是"未知"
        try:
            return _OPS[self.op](left, self.value)
        except TypeError:                    # 整数和字符串做大小比较
            raise QueryError(f"{self.field} 与 {self.value!r} 类型不同，不能比较大小") from None


@dataclass(frozen=True, slots=True)
class _And:
    left: _Node
    right: _Node

    def matches(self, row: Row) -> bool | None:
        a, b = self.left.matches(row), self.right.matches(row)
        if a is False or b is False:         # 有一个确定为假，整体就是假，哪怕另一边未知
            return False
        return None if a is None or b is None else True


@dataclass(frozen=True, slots=True)
class _Or:
    left: _Node
    right: _Node

    def matches(self, row: Row) -> bool | None:
        a, b = self.left.matches(row), self.right.matches(row)
        if a is True or b is True:           # 有一个确定为真，整体就是真
            return True
        return None if a is None or b is None else False


# ---- 第 2 关：NOT、IN、IS NULL -----------------------------------------------


@dataclass(frozen=True, slots=True)
class _Not:
    inner: _Node

    def matches(self, row: Row) -> bool | None:
        v = self.inner.matches(row)
        return None if v is None else not v  # 未知取反还是未知


@dataclass(frozen=True, slots=True)
class _In:
    field: str
    values: tuple[Any, ...]

    def matches(self, row: Row) -> bool | None:
        left = _get(row, self.field)
        return None if left is None else left in self.values


@dataclass(frozen=True, slots=True)
class _IsNull:
    field: str

    def matches(self, row: Row) -> bool:
        return _get(row, self.field) is None  # 唯一一个永远不返回"未知"的谓词


class _Parser:
    """递归下降。文法（优先级低的在上）：

        or_expr  := and_expr (OR and_expr)*
        and_expr := not_expr (AND not_expr)*
        not_expr := NOT not_expr | primary
        primary  := '(' or_expr ')' | predicate
        predicate:= field op literal | field [NOT] IN '(' literal (',' literal)* ')'
                  | field IS [NOT] NULL
    """

    def __init__(self, text: str, columns: Sequence[str] | None) -> None:
        self.tokens, self.i, self.columns = _tokenize(text), 0, columns

    def _peek(self) -> str:
        return self.tokens[self.i] if self.i < len(self.tokens) else ""

    def _next(self) -> str:
        if self.i >= len(self.tokens):
            raise QueryError("条件意外结束")
        self.i += 1
        return self.tokens[self.i - 1]

    def _accept(self, word: str) -> bool:
        if self._peek().upper() == word:
            self.i += 1
            return True
        return False

    def parse(self) -> _Node:
        node = self._or()
        if self._peek():
            raise QueryError(f"多余的内容: {self._peek()!r}")
        return node

    def _or(self) -> _Node:
        node = self._and()
        while self._accept("OR"):
            node = _Or(node, self._and())
        return node

    def _and(self) -> _Node:
        node = self._not()
        while self._accept("AND"):
            node = _And(node, self._not())
        return node

    def _not(self) -> _Node:
        if self._accept("NOT"):
            return _Not(self._not())
        return self._primary()

    def _primary(self) -> _Node:
        if self._accept("("):
            node = self._or()                # 括号让优先级从最低重新开始
            if self._next() != ")":
                raise QueryError("缺少右括号")
            return node
        return self._predicate()

    def _predicate(self) -> _Node:
        field = self._next()
        if not _IDENT.fullmatch(field) or field.upper() in _KEYWORDS:
            raise QueryError(f"需要列名，得到 {field!r}")
        if self.columns is not None and field not in self.columns:
            raise QueryError(f"未知列: {field}")
        if self._accept("IS"):
            negate = self._accept("NOT")
            if not self._accept("NULL"):
                raise QueryError("IS 后面只能跟 NULL 或 NOT NULL")
            node = _IsNull(field)
            return _Not(node) if negate else node
        negate = self._accept("NOT")         # field NOT IN (...)
        if self._accept("IN"):
            node = _In(field, self._literal_list())
            return _Not(node) if negate else node
        if negate:
            raise QueryError("NOT 后面只能跟 IN")
        op = self._next()
        if op not in _OPS:
            raise QueryError(f"不支持的运算符: {op!r}")
        if self._peek().upper() == "NULL":
            raise QueryError("与 NULL 比较要用 IS NULL / IS NOT NULL")
        return _Cmp(field, op, _literal(self._next()))

    def _literal_list(self) -> tuple[Any, ...]:
        if self._next() != "(":
            raise QueryError("IN 后面需要括号")
        values = [_literal(self._next())]
        while self._accept(","):
            values.append(_literal(self._next()))
        if self._next() != ")":
            raise QueryError("缺少右括号")
        return tuple(values)


# ---- 第 3 关：等值索引；第 4 关：无固定列 -------------------------------------


@lru_cache(maxsize=256)
def _compile(where: str, columns: tuple[str, ...] | None) -> _Node:
    """条件字符串 -> 语法树。节点全是不可变的，所以同一棵树可以被所有表、所有线程共享。"""
    return _Parser(where, columns).parse()


class Table:
    def __init__(self, columns: Sequence[str] | None = None) -> None:
        """建表。给列名就是固定结构（插入和查询都校验列）；不给就是文档表（第 4 关）。"""
        self.columns = tuple(columns) if columns is not None else None
        self.last_scan_count = 0             # 最近一次 select 把条件真正算了多少行
        self._rows: list[Row] = []
        self._index: dict[str, dict[Any, list[int]]] = {}   # 列 -> 值 -> 行号（升序）

    def insert(self, row: Mapping[str, Any]) -> None:
        """插入一行（存的是副本）。固定结构的表要求列与表完全一致，否则 QueryError。"""
        if self.columns is not None and set(row) != set(self.columns):
            raise QueryError(f"列不匹配: {sorted(row)}")
        self._rows.append(copy.deepcopy(dict(row)))
        for col, idx in self._index.items():  # 索引与行在同一个方法里更新，不会对不上
            idx.setdefault(_get(self._rows[-1], col), []).append(len(self._rows) - 1)

    def create_index(self, column: str) -> None:
        """给一列建等值索引；已有的行立即纳入，之后的插入自动维护。重复建无副作用。"""
        if self.columns is not None and column not in self.columns:
            raise QueryError(f"未知列: {column}")
        if column in self._index:
            return
        idx: dict[Any, list[int]] = {}
        for n, row in enumerate(self._rows):
            idx.setdefault(_get(row, column), []).append(n)
        self._index[column] = idx

    def select(self, where: str = "", columns: Sequence[str] | None = None) -> list[Row]:
        """返回满足条件（结果为真）的行，按插入顺序；返回的是副本。

        空条件返回全部行。`columns` 为空时返回整行。条件错误、未知列都抛 QueryError，
        且错误只取决于条件和表结构，不取决于表里有没有数据。
        """
        cols = list(columns) if columns is not None else None
        if cols is not None and self.columns is not None:
            if unknown := [c for c in cols if c not in self.columns]:
                raise QueryError(f"未知列: {unknown}")
        cond = _compile(where, self.columns) if where.strip() else None
        pool = self._candidates(cond) if cond is not None else None
        positions = range(len(self._rows)) if pool is None else sorted(pool)
        self.last_scan_count = len(positions)
        out: list[Row] = []
        for n in positions:
            row = self._rows[n]
            if cond is None or cond.matches(row) is True:    # 候选只是超集，最后一定复查
                out.append(copy.deepcopy(row) if cols is None else {c: _get(row, c) for c in cols})
        return out

    def _candidates(self, node: _Node) -> set[int] | None:
        """用索引算出"可能满足"的行号集合，必须是真正结果的超集；None 表示只能全表扫描。"""
        match node:
            case _Cmp(field=f, op="=", value=v) if f in self._index:
                return set(self._index[f].get(v, ()))
            case _In(field=f, values=vs) if f in self._index:
                return {n for v in vs for n in self._index[f].get(v, ())}
            case _And(left=l, right=r):          # 一边能缩小就够，另一边靠复查
                a, b = self._candidates(l), self._candidates(r)
                if a is not None and b is not None:
                    return a & b
                return a if a is not None else b
            case _Or(left=l, right=r):           # 两边都能缩小才行，只用一边会漏行
                a, b = self._candidates(l), self._candidates(r)
                return a | b if a is not None and b is not None else None
            case _:
                return None                      # NOT、范围比较、IS NULL：等值索引帮不上
