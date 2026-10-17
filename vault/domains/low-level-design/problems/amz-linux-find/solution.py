"""Linux find 命令 API（File Search API）：一棵目录树 + 可组合的过滤器 + 惰性遍历。

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
        if node.name in self.children:
            raise DuplicateNameError(node.name)
        self.children[node.name] = node
        return node


Node = File | Directory | Symlink


@dataclass(frozen=True, slots=True)
class Entry:
    """遍历到的一个位置：路径 + 节点 + 深度。过滤器看 Entry，不看裸节点。"""
    path: str
    node: Node
    depth: int

    @property
    def name(self) -> str:
        return self.node.name


# ───────────────────────────── 过滤器（Specification）─────────────────────────────

class Filter(ABC):
    """一个谓词。组合运算符返回新对象，不改原对象：不可变，所以可复用、可跨线程共享。"""

    @abstractmethod
    def matches(self, entry: Entry) -> bool: ...

    def __and__(self, other: "Filter") -> "Filter":
        return AndFilter(self, other)

    def __or__(self, other: "Filter") -> "Filter":
        return OrFilter(self, other)

    def __invert__(self) -> "Filter":
        return NotFilter(self)


class AllFilter(Filter):
    def matches(self, entry: Entry) -> bool:
        return True


@dataclass(frozen=True)
class AndFilter(Filter):
    left: Filter
    right: Filter

    def matches(self, entry: Entry) -> bool:
        return self.left.matches(entry) and self.right.matches(entry)   # 短路：便宜的条件放左边


@dataclass(frozen=True)
class OrFilter(Filter):
    left: Filter
    right: Filter

    def matches(self, entry: Entry) -> bool:
        return self.left.matches(entry) or self.right.matches(entry)


@dataclass(frozen=True)
class NotFilter(Filter):
    inner: Filter

    def matches(self, entry: Entry) -> bool:
        return not self.inner.matches(entry)


@dataclass(frozen=True)
class NameGlob(Filter):
    """`-name`：只匹配最后一段名字，区分大小写；`*` 不会跨目录，因为名字里没有 `/`。"""
    pattern: str

    def matches(self, entry: Entry) -> bool:
        return fnmatch.fnmatchcase(entry.name, self.pattern)


@dataclass(frozen=True)
class Extension(Filter):
    """扩展名（不含点，不区分大小写）：`a.tar.gz` 取最后一段 `gz`；`.bashrc` 这类隐藏文件没有扩展名。"""
    ext: str

    def matches(self, entry: Entry) -> bool:
        stem = entry.name.lstrip(".")
        return "." in stem and stem.rsplit(".", 1)[1].lower() == self.ext.lower()


_UNITS = {"": 1, "B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}


def parse_size(text: str) -> int:
    """"5MB" → 5242880；单位按 1024 进制，和 `find -size` 的 k / M / G 一致。"""
    m = re.fullmatch(r"\s*(\d+)\s*([A-Za-z]*)\s*", text)
    unit = m.group(2).upper() if m else None
    if m is None or unit not in _UNITS:
        raise InvalidSizeError(text)
    return int(m.group(1)) * _UNITS[unit]


@dataclass(frozen=True)
class Size(Filter):
    """闭区间 [min_bytes, max_bytes]，None 表示不限。只有普通文件有“大小”，目录和链接恒不匹配。"""
    min_bytes: int | None = None
    max_bytes: int | None = None

    @classmethod
    def over(cls, text: str) -> "Size":
        return cls(min_bytes=parse_size(text) + 1)           # “> 5MB”是严格大于

    def matches(self, entry: Entry) -> bool:
        if entry.node.kind is not Kind.FILE:
            return False
        size = entry.node.size
        return ((self.min_bytes is None or size >= self.min_bytes)
                and (self.max_bytes is None or size <= self.max_bytes))


@dataclass(frozen=True)
class Modified(Filter):
    after: int | None = None
    before: int | None = None

    def matches(self, entry: Entry) -> bool:
        t = entry.node.mtime
        return (self.after is None or t >= self.after) and (self.before is None or t <= self.before)


@dataclass(frozen=True)
class OfType(Filter):
    kind: Kind

    def matches(self, entry: Entry) -> bool:
        return entry.node.kind is self.kind


# ───────────────────────────── 遍历 ─────────────────────────────

@dataclass
class FindStats:
    """测试用它证明“惰性”和“剪枝”真的发生了，而不是只看结果对不对。"""
    visited: int = 0                              # 取出并检查过的 Entry 数
    dirs_entered: int = 0                         # 真正展开了 children 的目录数


class FileSearcher:
    def __init__(self, *, follow_symlinks: bool = False, max_depth: int | None = None) -> None:
        self._follow = follow_symlinks
        self._max_depth = max_depth

    def find(self, root: Directory, flt: Filter | None = None, *,
             prune: Callable[[Entry], bool] | None = None,
             stats: FindStats | None = None) -> Iterator[Entry]:
        """前序深度优先、同目录按名字排序。根目录自己不输出。

        `prune(entry)` 为真时该目录本身仍会被 `flt` 检查，但不展开子节点（对应 `find -prune`）。
        栈里放 (entry, 祖先目录 id 链)：祖先链只用来检测符号链接环。
        """
        flt = flt or AllFilter()
        stats = stats if stats is not None else FindStats()
        stack: list[tuple[Entry, frozenset[int]]] = [(Entry("/", root, 0), frozenset())]
        while stack:
            entry, ancestors = stack.pop()
            stats.visited += 1
            if entry.depth > 0 and flt.matches(entry):
                yield entry
            node = self._resolve_link(root, entry.node)
            if node is None or node.kind is not Kind.DIR or id(node) in ancestors:
                continue                          # 文件、悬空链接，或祖先链上已有的目录（环）
            if (prune is not None and prune(entry)) or (
                    self._max_depth is not None and entry.depth >= self._max_depth):
                continue
            stats.dirs_entered += 1
            chain = ancestors | {id(node)}
            base = "" if entry.path == "/" else entry.path
            for name in sorted(node.children, reverse=True):     # 逆序压栈，弹出时就是升序
                stack.append((Entry(f"{base}/{name}", node.children[name], entry.depth + 1), chain))

    def _resolve_link(self, root: Directory, node: Node) -> Node | None:
        if node.kind is not Kind.SYMLINK:
            return node
        if not self._follow:
            return None                           # 默认把链接当叶子：既不展开，也不会有环
        current: Node = root
        for part in (p for p in node.target.split("/") if p):
            if current.kind is not Kind.DIR or part not in current.children:
                return None
            current = current.children[part]
        return current

    def paths(self, root: Directory, flt: Filter | None = None, **kw) -> list[str]:
        return [e.path for e in self.find(root, flt, **kw)]


def scan_disk(path: str, _top: str | None = None) -> Directory:
    """把真实磁盘目录读成同样的树，于是同一套过滤器可以搜真实文件。
    链接记成 Symlink，目标改写成“相对扫描根的绝对路径”（指到根外的记成悬空）。"""
    top = _top or os.path.realpath(path)
    root = Directory(os.path.basename(path.rstrip("/")) or "/")
    with os.scandir(path) as it:
        for e in it:
            st = e.stat(follow_symlinks=False)
            if e.is_symlink():
                rel = os.path.relpath(os.path.realpath(e.path), top)
                root.add(Symlink(e.name, "/" + rel if not rel.startswith("..") else "/<outside>", int(st.st_mtime)))
            elif e.is_dir(follow_symlinks=False):
                child = scan_disk(e.path, top)
                child.mtime = int(st.st_mtime)
                root.add(child)
            else:
                root.add(File(e.name, st.st_size, int(st.st_mtime)))
    return root


if __name__ == "__main__":
    root = Directory("")
    docs = root.add(Directory("docs"))
    docs.add(File("a.xml", 6 * 1024 ** 2))
    docs.add(File("b.txt", 10))
    root.add(File("c.xml", 100))
    big_xml = Size.over("5MB") | Extension("xml")
    print(FileSearcher().paths(root, big_xml & OfType(Kind.FILE)))
