"""条件解析与内存表查询——起始模板。公开的类名、方法签名和异常与 solution.py 一致，把标了 NotImplementedError 的方法体补全。"""
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

class Table:

    def __init__(self, columns: Sequence[str] | None=None) -> None:
        """建表。给列名就是固定结构（插入和查询都校验列）；不给就是文档表（第 4 关）。"""
        raise NotImplementedError

    def insert(self, row: Mapping[str, Any]) -> None:
        """插入一行（存的是副本）。固定结构的表要求列与表完全一致，否则 QueryError。"""
        raise NotImplementedError

    def create_index(self, column: str) -> None:
        """给一列建等值索引；已有的行立即纳入，之后的插入自动维护。重复建无副作用。"""
        raise NotImplementedError

    def select(self, where: str='', columns: Sequence[str] | None=None) -> list[Row]:
        """返回满足条件（结果为真）的行，按插入顺序；返回的是副本。

空条件返回全部行。`columns` 为空时返回整行。条件错误、未知列都抛 QueryError，
且错误只取决于条件和表结构，不取决于表里有没有数据。"""
        raise NotImplementedError
