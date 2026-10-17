"""【练习骨架】Linux find 命令 API：公开 API 与参考解答完全一致，把每个 raise NotImplementedError 换成你的实现。

设计五行：
1. 树节点只有三种：`File`、`Directory`、`Symlink`；节点不存自己的路径，路径是遍历时算出的 `Entry`。
2. 过滤器 `Filter` 只有一个方法 `matches(entry) -> bool`（Specification 模式）；`& | ~` 组合出 AND / OR / NOT。
3. 新增一种条件 = 新增一个 `Filter` 子类，`FileSearcher` 和已有过滤器一行都不用改。
4. 遍历是惰性生成器 + 显式栈：取第一个结果不必走完整棵树，深目录不会撞递归上限。
5. 符号链接默认不跟随；跟随时只用“当前祖先链”检测环，不用全局 visited（否则会漏掉合法的第二条路径）。
"""

from __future__ import annotations

import fnmatch
import os
import re
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from enum import Enum


class FindError(Exception):
    """本模块的失败基类。"""


class InvalidSizeError(FindError):
    """无法解析的大小字符串，例如 "5XB"。"""


class DuplicateNameError(FindError):
    """同一目录下已有同名节点。"""


# ───────────────────────────── 节点 ─────────────────────────────

class Kind(Enum):
    FILE = "file"
    DIR = "dir"
    SYMLINK = "symlink"


@dataclass
class File:
    name: str
    size: int                                     # 字节
    mtime: int = 0                                # Unix 秒；时间由调用方给，逻辑里不读系统时钟
    kind = Kind.FILE


@dataclass
class Symlink:
    name: str
    target: str                                   # 绝对路径；解析发生在遍历时，所以允许悬空
    mtime: int = 0
    size: int = 0
    kind = Kind.SYMLINK


@dataclass
class Directory:
    name: str
    mtime: int = 0
    size: int = 0
    children: dict[str, "Node"] = field(default_factory=dict)
    kind = Kind.DIR

    def add(self, node: "Node") -> "Node":
        raise NotImplementedError


Node = File | Directory | Symlink


@dataclass(frozen=True, slots=True)
class Entry:
    """遍历到的一个位置：路径 + 节点 + 深度。过滤器看 Entry，不看裸节点。"""
    path: str
    node: Node
    depth: int

    @property
    def name(self) -> str:
        raise NotImplementedError


# ───────────────────────────── 过滤器（Specification）─────────────────────────────

class Filter(ABC):
    """一个谓词。组合运算符返回新对象，不改原对象：不可变，所以可复用、可跨线程共享。"""

    @abstractmethod
    def matches(self, entry: Entry) -> bool: ...

    def __and__(self, other: "Filter") -> "Filter":
        raise NotImplementedError

    def __or__(self, other: "Filter") -> "Filter":
        raise NotImplementedError

    def __invert__(self) -> "Filter":
        raise NotImplementedError


class AllFilter(Filter):
    def matches(self, entry: Entry) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class AndFilter(Filter):
    left: Filter
    right: Filter

    def matches(self, entry: Entry) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class OrFilter(Filter):
    left: Filter
    right: Filter

    def matches(self, entry: Entry) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class NotFilter(Filter):
    inner: Filter

    def matches(self, entry: Entry) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class NameGlob(Filter):
    """`-name`：只匹配最后一段名字，区分大小写；`*` 不会跨目录，因为名字里没有 `/`。"""
    pattern: str

    def matches(self, entry: Entry) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class Extension(Filter):
    """扩展名（不含点，不区分大小写）：`a.tar.gz` 取最后一段 `gz`；`.bashrc` 这类隐藏文件没有扩展名。"""
    ext: str

    def matches(self, entry: Entry) -> bool:
        raise NotImplementedError


_UNITS = {"": 1, "B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}


def parse_size(text: str) -> int:
    """"5MB" → 5242880；单位按 1024 进制，和 `find -size` 的 k / M / G 一致。"""
    raise NotImplementedError


@dataclass(frozen=True)
class Size(Filter):
    """闭区间 [min_bytes, max_bytes]，None 表示不限。只有普通文件有“大小”，目录和链接恒不匹配。"""
    min_bytes: int | None = None
    max_bytes: int | None = None

    @classmethod
    def over(cls, text: str) -> "Size":
        raise NotImplementedError

    def matches(self, entry: Entry) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class Modified(Filter):
    after: int | None = None
    before: int | None = None

    def matches(self, entry: Entry) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class OfType(Filter):
    kind: Kind

    def matches(self, entry: Entry) -> bool:
        raise NotImplementedError


# ───────────────────────────── 遍历 ─────────────────────────────

@dataclass
class FindStats:
    """测试用它证明“惰性”和“剪枝”真的发生了，而不是只看结果对不对。"""
    visited: int = 0                              # 取出并检查过的 Entry 数
    dirs_entered: int = 0                         # 真正展开了 children 的目录数


class FileSearcher:
    def __init__(self, *, follow_symlinks: bool = False, max_depth: int | None = None) -> None:
        raise NotImplementedError

    def find(self, root: Directory, flt: Filter | None = None, *,
             prune: Callable[[Entry], bool] | None = None,
             stats: FindStats | None = None) -> Iterator[Entry]:
        """前序深度优先、同目录按名字排序。根目录自己不输出。

        `prune(entry)` 为真时该目录本身仍会被 `flt` 检查，但不展开子节点（对应 `find -prune`）。
        栈里放 (entry, 祖先目录 id 链)：祖先链只用来检测符号链接环。
        """
        raise NotImplementedError

    def _resolve_link(self, root: Directory, node: Node) -> Node | None:
        raise NotImplementedError

    def paths(self, root: Directory, flt: Filter | None = None, **kw) -> list[str]:
        raise NotImplementedError


def scan_disk(path: str, _top: str | None = None) -> Directory:
    """把真实磁盘目录读成同样的树，于是同一套过滤器可以搜真实文件。
    链接记成 Symlink，目标改写成“相对扫描根的绝对路径”（指到根外的记成悬空）。"""
    raise NotImplementedError
