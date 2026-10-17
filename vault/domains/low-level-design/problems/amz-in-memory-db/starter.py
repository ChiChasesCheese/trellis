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
Tri = bool | None

class DBError(Exception):
    """本模块所有可预期失败的基类。"""

class SchemaError(DBError):
    """表、列不存在或已存在，列名有歧义，类型比较不合法。"""

class ConstraintError(DBError):
    """值违反约束：类型不符、主键重复或为 NULL。"""

class SQLSyntaxError(DBError):
    """SQL 文本不合文法。"""

@dataclass(frozen=True)
class Col:
    """比较里的列引用（区别于字面量）。"""
    name: str

def _val(operand: Any, row: Row) -> Any:
    raise NotImplementedError

class Pred(ABC):
    """谓词：`pred(row)` 返回 True / False / None。`refs` 列出它引用的列名，供执行前统一校验。"""

    @property
    @abstractmethod
    def refs(self) -> frozenset[str]:
        ...

    @abstractmethod
    def __call__(self, row: Row) -> Tri:
        ...
_OPS: dict[str, Callable[[Any, Any], bool]] = {'=': operator.eq, '<>': operator.ne, '<': operator.lt, '<=': operator.le, '>': operator.gt, '>=': operator.ge}

@dataclass(frozen=True)
class Cmp(Pred):
    left: Any
    op: str
    right: Any

    @property
    def refs(self) -> frozenset[str]:
        raise NotImplementedError

    def __call__(self, row: Row) -> Tri:
        raise NotImplementedError

@dataclass(frozen=True)
class In(Pred):
    col: str
    values: tuple[Any, ...]

    @property
    def refs(self) -> frozenset[str]:
        raise NotImplementedError

    def __call__(self, row: Row) -> Tri:
        raise NotImplementedError

@dataclass(frozen=True)
class IsNull(Pred):
    col: str

    @property
    def refs(self) -> frozenset[str]:
        raise NotImplementedError

    def __call__(self, row: Row) -> Tri:
        raise NotImplementedError

@dataclass(frozen=True)
class And(Pred):
    parts: tuple[Pred, ...]

    @property
    def refs(self) -> frozenset[str]:
        raise NotImplementedError

    def __call__(self, row: Row) -> Tri:
        raise NotImplementedError

@dataclass(frozen=True)
class Or(Pred):
    parts: tuple[Pred, ...]

    @property
    def refs(self) -> frozenset[str]:
        raise NotImplementedError

    def __call__(self, row: Row) -> Tri:
        raise NotImplementedError

@dataclass(frozen=True)
class Not(Pred):
    part: Pred

    @property
    def refs(self) -> frozenset[str]:
        raise NotImplementedError

    def __call__(self, row: Row) -> Tri:
        raise NotImplementedError

class Table:
    """一张表：列名 → 类型、主键列、`{主键: 行}`。整数主键自增，删除不回退。"""

    def __init__(self, name: str, columns: dict[str, type], pk: str) -> None:
        raise NotImplementedError

    def check(self, col: str, value: Any) -> Any:
        raise NotImplementedError

    @property
    def row_count(self) -> int:
        raise NotImplementedError

@dataclass(frozen=True)
class Join:
    table: str
    left: str
    right: str
    kind: str = 'inner'
    alias: str | None = None

class Database:

    def __init__(self) -> None:
        raise NotImplementedError

    def _table(self, name: str) -> Table:
        raise NotImplementedError

    def create_table(self, name: str, columns: dict[str, type], primary_key: str) -> None:
        raise NotImplementedError

    def count(self, table: str) -> int:
        raise NotImplementedError

    def columns(self, table: str) -> list[str]:
        raise NotImplementedError

    def insert(self, table: str, values: Row) -> Any:
        raise NotImplementedError

    def _matching(self, t: Table, where: Pred | None) -> list[Row]:
        raise NotImplementedError

    def update(self, table: str, assignments: Row, where: Pred | None=None) -> int:
        raise NotImplementedError

    def delete(self, table: str, where: Pred | None=None) -> int:
        raise NotImplementedError

    @staticmethod
    def _check_refs(refs: frozenset[str], scope: dict[str, Any]) -> None:
        raise NotImplementedError

    def select(self, table: str, columns: Sequence[str] | None=None, where: Pred | None=None, order_by: Sequence[str | tuple[str, str]] | None=None, limit: int | None=None, joins: Sequence[Join]=(), alias: str | None=None) -> list[Row]:
        """逻辑顺序：FROM → JOIN → WHERE → ORDER BY → LIMIT → 投影。`columns=None` 即 `*`。"""
        raise NotImplementedError

    @staticmethod
    def _scope(members: list[tuple[str, Table]]) -> dict[str, str]:
        """可用的列名 → 行里的限定键。不重名的列同时可以不带限定符，重名的必须限定。"""
        raise NotImplementedError

    @staticmethod
    def _hash_join(left: list[Row], left_key: str, right: Table, alias: str, right_key: str, kind: str) -> list[Row]:
        """build 右表（O(|R|)），probe 左表（O(|L| + 输出)）。NULL 键不匹配任何东西。"""
        raise NotImplementedError

    def execute(self, sql: str) -> list[Row] | int | None:
        """执行一条 SQL：SELECT 返回行，INSERT / UPDATE / DELETE 返回主键或影响的行数，CREATE 返回 None。"""
        raise NotImplementedError
KEYWORDS = {'SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'ON', 'AND', 'OR', 'NOT', 'IN', 'IS', 'NULL', 'ORDER', 'BY', 'ASC', 'DESC', 'LIMIT', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE', 'PRIMARY', 'KEY', 'TRUE', 'FALSE'}
SQL_TYPES = {'INT': int, 'TEXT': str, 'REAL': float, 'BOOL': bool}
_TOKEN = re.compile("\\s*(?:(?P<num>\\d+\\.\\d+|\\d+)|(?P<str>'(?:[^']|'')*')|(?P<id>[A-Za-z_]\\w*(?:\\.[A-Za-z_]\\w*)?)|(?P<op><=|>=|<>|!=|[=<>(),*;-]))")

def tokenize(sql: str) -> list[tuple[str, Any]]:
    """文本 → [(kind, value)]，kind ∈ lit / kw / id / op / eof。"""
    raise NotImplementedError

class Parser:
    """递归下降：每条文法规则一个方法；优先级 OR < AND < NOT < 比较，靠方法的调用层次表达。"""

    def __init__(self, db: Database, sql: str) -> None:
        raise NotImplementedError

    def error(self, message: str) -> SQLSyntaxError:
        raise NotImplementedError

    def accept(self, *words: str) -> str | None:
        raise NotImplementedError

    def expect(self, word: str) -> None:
        raise NotImplementedError

    def ident(self) -> str:
        raise NotImplementedError

    def literal(self) -> Any:
        raise NotImplementedError

    def run(self) -> list[Row] | int | None:
        raise NotImplementedError

    def select(self) -> list[Row]:
        raise NotImplementedError

    def insert(self) -> Any:
        raise NotImplementedError

    def update(self) -> int:
        raise NotImplementedError

    def delete(self) -> int:
        raise NotImplementedError

    def create(self) -> None:
        raise NotImplementedError

    def expr(self) -> Pred:
        raise NotImplementedError

    def and_expr(self) -> Pred:
        raise NotImplementedError

    def not_expr(self) -> Pred:
        raise NotImplementedError

    def operand(self) -> Any:
        raise NotImplementedError

    def atom(self) -> Pred:
        raise NotImplementedError

class SQL:
    """只有“表 + 按行号增删查”的最小接口，是上面 `Database` 的一个特例：所有列都是 str，行号就是自增主键。"""

    def __init__(self, names: list[str], columns: list[int]) -> None:
        raise NotImplementedError

    def insert_row(self, name: str, row: list[str]) -> None:
        raise NotImplementedError

    def delete_row(self, name: str, row_id: int) -> None:
        raise NotImplementedError

    def select_cell(self, name: str, row_id: int, column_id: int) -> str:
        raise NotImplementedError
