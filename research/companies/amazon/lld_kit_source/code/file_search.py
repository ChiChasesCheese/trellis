"""Unix `find` / 文件搜索：目录树 + 可组合的过滤器（Specification 模式）+ 惰性遍历。

运行：`python3 -I file_search.py`（全部 assert 通过则打印 OK）。

设计要点（讲解见同目录上一级的 `file_search.md`）：
1. 树节点只有三种：`File`、`Directory`、`Symlink`。节点**不存自己的路径**——路径是遍历时算出来的
   `Entry(path, node, depth)`，和 inode 把名字存在父目录里是同一个道理。
2. 过滤器是一个只有 `matches(entry) -> bool` 的小对象（Specification 模式）。新增一种条件 = 新增一个子类，
   `FileSearcher` 和已有过滤器一行都不用改（开闭原则 OCP）。`& | ~` 运算符组合出 AND / OR / NOT。
3. 遍历是**惰性生成器**（迭代器模式），用显式栈而不是递归：深目录不会撞递归深度上限，调用方
   `next(...)` 取第一个结果时不需要走完整棵树；"对结果做什么"（打印、求总大小、删除）是调用方消费迭代器的事，
   不需要 Visitor 或 Command 类。
4. 符号链接默认不跟随；跟随时用"当前祖先链上的目录集合"检测环（不是全局 visited，否则同一目录经由两条
   合法路径可达时会漏报）。
5. `prune` 回调让调用方在**进入目录之前**就跳过整棵子树（对应 `find -prune`），用 `FindStats` 可以证明剪枝生效。
"""

from __future__ import annotations

import fnmatch
import re
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from enum import Enum


# ───────────────────────────── 节点 ─────────────────────────────

class NodeType(Enum):
    FILE = "file"
    DIR = "dir"
    SYMLINK = "symlink"


@dataclass
class File:
    name: str
    size: int                 # 字节
    mtime: int                # 修改时间，Unix 秒（时间一律由调用方给，代码里不读系统时钟）
    owner: str = "root"
    type = NodeType.FILE


@dataclass
class Symlink:
    name: str
    target: str               # 绝对路径；解析发生在遍历时，不在创建时
    mtime: int = 0
    owner: str = "root"
    size: int = 0
    type = NodeType.SYMLINK


@dataclass
class Directory:
    name: str
    mtime: int = 0
    owner: str = "root"
    size: int = 0
    children: dict[str, "Node"] = field(default_factory=dict)
    type = NodeType.DIR

    def add(self, node: "Node") -> "Node":
        if node.name in self.children:
            raise ValueError(f"重名: {node.name}")
        self.children[node.name] = node
        return node


Node = File | Directory | Symlink


@dataclass(frozen=True)
class Entry:
    """遍历到的一个位置：路径 + 节点 + 深度。过滤器看的是 Entry，不是裸节点。"""
    path: str
    node: Node
    depth: int

    @property
    def name(self) -> str:
        return self.node.name


# ───────────────────────────── 过滤器（Specification）─────────────────────────────

class Filter(ABC):
    """一个谓词。组合运算符返回新的过滤器，不修改原对象（不可变，可复用、可跨线程共享）。"""

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
        # 短路：左边为假就不算右边——把便宜的条件（名字、类型）放左边能省掉昂贵条件
        return self.left.matches(entry) and self.right.matches(entry)


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
    """`-name`：只匹配最后一段名字，不匹配整条路径；`*` 不跨目录，因为名字里没有 `/`。"""
    pattern: str

    def matches(self, entry: Entry) -> bool:
        return fnmatch.fnmatchcase(entry.name, self.pattern)


@dataclass(frozen=True)
class NameRegex(Filter):
    pattern: str

    def matches(self, entry: Entry) -> bool:
        return re.fullmatch(self.pattern, entry.name) is not None


@dataclass(frozen=True)
class Extension(Filter):
    """扩展名（不含点，不区分大小写）。`archive.tar.gz` 的扩展名取最后一段 `gz`；没有点或以点开头的隐藏文件算无扩展名。"""
    ext: str

    def matches(self, entry: Entry) -> bool:
        name = entry.name
        if "." not in name.lstrip("."):
            return False
        return name.rsplit(".", 1)[1].lower() == self.ext.lower()


@dataclass(frozen=True)
class Size(Filter):
    """闭区间 [min_bytes, max_bytes]；任一端为 None 表示不限。目录与符号链接的 size 不参与，恒不匹配。"""
    min_bytes: int | None = None
    max_bytes: int | None = None

    def matches(self, entry: Entry) -> bool:
        if entry.node.type is not NodeType.FILE:
            return False
        s = entry.node.size
        return (self.min_bytes is None or s >= self.min_bytes) and (
            self.max_bytes is None or s <= self.max_bytes)


@dataclass(frozen=True)
class Modified(Filter):
    """修改时间落在 [after, before] 闭区间内（Unix 秒）；时间由调用方传入，所以可确定性测试。"""
    after: int | None = None
    before: int | None = None

    def matches(self, entry: Entry) -> bool:
        t = entry.node.mtime
        return (self.after is None or t >= self.after) and (self.before is None or t <= self.before)


@dataclass(frozen=True)
class OfType(Filter):
    kind: NodeType

    def matches(self, entry: Entry) -> bool:
        return entry.node.type is self.kind


@dataclass(frozen=True)
class OwnedBy(Filter):
    owner: str

    def matches(self, entry: Entry) -> bool:
        return entry.node.owner == self.owner


@dataclass(frozen=True)
class MaxDepth(Filter):
    """`-maxdepth` 作为过滤器只能"不输出"，仍会遍历更深的层；要真正少走路用 FileSearcher(max_depth=…)。"""
    depth: int

    def matches(self, entry: Entry) -> bool:
        return entry.depth <= self.depth


# ───────────────────────────── 遍历 ─────────────────────────────

@dataclass
class FindStats:
    """遍历统计：测试用它证明"惰性"和"剪枝"真的发生了，而不是只看结果对不对。"""
    visited: int = 0          # 取出并检查过的 Entry 数
    dirs_entered: int = 0     # 实际展开 children 的目录数


class FileSearcher:
    def __init__(self, *, follow_symlinks: bool = False, max_depth: int | None = None) -> None:
        self._follow = follow_symlinks
        self._max_depth = max_depth

    def find(
        self,
        root: Directory,
        flt: Filter | None = None,
        *,
        prune: Callable[[Entry], bool] | None = None,
        stats: FindStats | None = None,
    ) -> Iterator[Entry]:
        """前序深度优先、同一目录内按名字排序（输出稳定，便于测试和 diff）。

        `prune(entry)` 为真时：该目录**本身仍会被 `flt` 检查**，但不会展开它的子节点。
        显式栈里放 (entry, 祖先目录 id 链)；祖先链只用于符号链接环检测。
        """
        flt = flt or AllFilter()
        stats = stats if stats is not None else FindStats()
        resolve = _Resolver(root)
        start = Entry("/", root, 0)
        stack: list[tuple[Entry, frozenset[int]]] = [(start, frozenset())]
        while stack:
            entry, ancestors = stack.pop()
            stats.visited += 1
            if entry.path != "/" and flt.matches(entry):   # 根目录自己不输出，和 `find /` 之外的常见用法一致
                yield entry
            node = entry.node
            if node.type is NodeType.SYMLINK and self._follow:
                target = resolve.lookup(node.target)
                if target is None or target.type is not NodeType.DIR:
                    continue                                 # 悬空链接：当作叶子
                node = target
            if node.type is not NodeType.DIR:
                continue
            if id(node) in ancestors:
                continue                                     # 环：祖先链上已经有这个目录
            if prune is not None and prune(entry):
                continue
            if self._max_depth is not None and entry.depth >= self._max_depth:
                continue
            stats.dirs_entered += 1
            chain = ancestors | {id(node)}
            base = "" if entry.path == "/" else entry.path
            # 逆序压栈 → 弹出时是升序，保证输出顺序是字典序前序遍历
            for name in sorted(node.children, reverse=True):
                child = node.children[name]
                stack.append((Entry(f"{base}/{name}", child, entry.depth + 1), chain))

    def paths(self, root: Directory, flt: Filter | None = None, **kw) -> list[str]:
        return [e.path for e in self.find(root, flt, **kw)]


class _Resolver:
    """把绝对路径解析成节点。解析在遍历时按需做，所以符号链接可以悬空、可以指向后来才创建的东西。"""

    def __init__(self, root: Directory) -> None:
        self._root = root

    def lookup(self, path: str) -> Node | None:
        node: Node = self._root
        for part in [p for p in path.split("/") if p]:
            if node.type is not NodeType.DIR or part not in node.children:
                return None
            node = node.children[part]
        return node


# ───────────────────────────── 查询小语言（追问：把命令行写成过滤器）─────────────────────────────

_TOKEN = re.compile(r"\s*(\(|\)|and\b|or\b|not\b|[a-z_]+(?:>=|<=|=|>|<)[^\s()]+)", re.IGNORECASE)
_UNITS = {"k": 1024, "m": 1024 ** 2, "g": 1024 ** 3}


def _size_value(text: str) -> int:
    text = text.lower()
    return int(text[:-1]) * _UNITS[text[-1]] if text[-1] in _UNITS else int(text)


def parse_query(query: str) -> Filter:
    """文法（优先级 not > and > or，括号可改）：
        expr   := term ('or' term)*
        term   := factor ('and' factor)*
        factor := 'not' factor | '(' expr ')' | atom
        atom   := name=GLOB | ext=EXT | size>N | size<N | type=file|dir | owner=NAME | mtime>T | mtime<T
    递归下降，每个产生式一个函数。语法错误抛 ValueError，位置在消息里。
    """
    tokens: list[str] = []
    pos = 0
    while pos < len(query):
        m = _TOKEN.match(query, pos)
        if not m:
            if query[pos:].strip():
                raise ValueError(f"无法解析的输入，位置 {pos}: {query[pos:]!r}")
            break
        tokens.append(m.group(1))
        pos = m.end()
    i = 0

    def peek() -> str | None:
        return tokens[i] if i < len(tokens) else None

    def take() -> str:
        nonlocal i
        tok = tokens[i]
        i += 1
        return tok

    def expr() -> Filter:
        node = term()
        while (peek() or "").lower() == "or":
            take()
            node = node | term()
        return node

    def term() -> Filter:
        node = factor()
        while (peek() or "").lower() == "and":
            take()
            node = node & factor()
        return node

    def factor() -> Filter:
        tok = peek()
        if tok is None:
            raise ValueError("表达式意外结束")
        if tok.lower() == "not":
            take()
            return ~factor()
        if tok == "(":
            take()
            node = expr()
            if peek() != ")":
                raise ValueError("缺少右括号")
            take()
            return node
        return atom(take())

    def atom(tok: str) -> Filter:
        m = re.fullmatch(r"([a-z_]+)(>=|<=|=|>|<)(.+)", tok, re.IGNORECASE)
        if not m:
            raise ValueError(f"不是条件: {tok}")
        key, op, val = m.group(1).lower(), m.group(2), m.group(3)
        if key == "name" and op == "=":
            return NameGlob(val)
        if key == "ext" and op == "=":
            return Extension(val)
        if key == "type" and op == "=":
            return OfType(NodeType(val))
        if key == "owner" and op == "=":
            return OwnedBy(val)
        if key == "size" and op in (">", ">=", "<", "<="):
            n = _size_value(val)
            if op == ">":
                return Size(min_bytes=n + 1)
            if op == ">=":
                return Size(min_bytes=n)
            if op == "<":
                return Size(max_bytes=n - 1)
            return Size(max_bytes=n)
        if key == "mtime" and op in (">", "<"):
            n = int(val)
            return Modified(after=n + 1) if op == ">" else Modified(before=n - 1)
        raise ValueError(f"不支持的条件: {tok}")

    result = expr()
    if i != len(tokens):
        raise ValueError(f"多余的输入: {tokens[i:]}")
    return result


# ───────────────────────────── 测试（assert）─────────────────────────────

def _sample_tree() -> Directory:
    root = Directory("")
    root.add(File("a.txt", 100, 1000))
    root.add(File("b.py", 2048, 2000, owner="chi"))
    docs = root.add(Directory("docs"))
    docs.add(File("readme.md", 5000, 3000))
    docs.add(File("old.md", 10, 100))
    img = docs.add(Directory("img"))
    img.add(File("logo.png", 1_000_000, 4000))
    src = root.add(Directory("src"))
    src.add(File("main.py", 3000, 5000, owner="chi"))
    src.add(File("util.py", 500, 6000))
    src.add(File("test_main.py", 700, 7000))
    root.add(File(".bashrc", 50, 10))
    root.add(File("archive.tar.gz", 9000, 8000))
    root.add(Symlink("link_to_docs", "/docs"))
    root.add(Symlink("loop", "/"))
    root.add(Symlink("dangling", "/nowhere"))
    return root


def _run_tests() -> None:
    tree = _sample_tree()
    finder = FileSearcher()

    # 1. 无过滤器：全部条目，前序、同目录字典序；根自己不输出，符号链接只作为叶子出现
    all_paths = finder.paths(tree)
    assert all_paths[0] == "/.bashrc" and all_paths[1] == "/a.txt"
    assert "/docs/img/logo.png" in all_paths and "/link_to_docs" in all_paths
    assert "/link_to_docs/readme.md" not in all_paths          # 默认不跟随
    assert len(all_paths) == 16

    # 2. 名字 / 扩展名；扩展名取最后一段、隐藏文件无扩展名
    assert finder.paths(tree, Extension("py")) == ["/b.py", "/src/main.py", "/src/test_main.py", "/src/util.py"]
    assert finder.paths(tree, Extension("gz")) == ["/archive.tar.gz"]
    assert finder.paths(tree, Extension("bashrc")) == []        # `.bashrc` 没有扩展名
    assert finder.paths(tree, NameGlob("test_*")) == ["/src/test_main.py"]
    assert finder.paths(tree, NameRegex(r"[a-z]+\.md")) == ["/docs/old.md", "/docs/readme.md"]

    # 3. 大小：闭区间；目录与链接不匹配 Size
    assert finder.paths(tree, Size(min_bytes=3000)) == ["/archive.tar.gz", "/docs/img/logo.png", "/docs/readme.md", "/src/main.py"]
    assert finder.paths(tree, Size(max_bytes=100, min_bytes=50)) == ["/.bashrc", "/a.txt"]

    # 4. 组合：& | ~ 与优先级（Python 里 ~ > & > |，和 not > and > or 一致）
    py_big = Extension("py") & Size(min_bytes=1024)
    assert finder.paths(tree, py_big) == ["/b.py", "/src/main.py"]
    code_not_test = (Extension("py") | Extension("md")) & ~NameGlob("test_*")
    assert finder.paths(tree, code_not_test) == ["/b.py", "/docs/old.md", "/docs/readme.md", "/src/main.py", "/src/util.py"]
    assert finder.paths(tree, ~Extension("py") & OfType(NodeType.FILE) & Size(min_bytes=5000)) == [
        "/archive.tar.gz", "/docs/img/logo.png", "/docs/readme.md"]

    # 5. 修改时间、属主、类型
    assert finder.paths(tree, Modified(after=6000)) == ["/archive.tar.gz", "/src/test_main.py", "/src/util.py"]
    # 目录与符号链接的 mtime 默认 0，所以也落在 before=100 内；想只要文件就再 & OfType(FILE)
    assert finder.paths(tree, Modified(before=100)) == [
        "/.bashrc", "/dangling", "/docs", "/docs/img", "/docs/old.md", "/link_to_docs", "/loop", "/src"]
    assert finder.paths(tree, Modified(before=100) & OfType(NodeType.FILE)) == ["/.bashrc", "/docs/old.md"]
    assert finder.paths(tree, OwnedBy("chi")) == ["/b.py", "/src/main.py"]
    assert finder.paths(tree, OfType(NodeType.DIR)) == ["/docs", "/docs/img", "/src"]
    assert finder.paths(tree, OfType(NodeType.SYMLINK)) == ["/dangling", "/link_to_docs", "/loop"]

    # 6. 符号链接：跟随时不陷入死循环（loop -> /），悬空链接当叶子，且经由链接可达的路径都能搜到
    follow = FileSearcher(follow_symlinks=True)
    followed = follow.paths(tree, Extension("md"))
    assert "/link_to_docs/readme.md" in followed and "/docs/readme.md" in followed   # 同一目录两条合法路径都报
    assert all(len(p) < 80 for p in followed)                                         # 没有 /loop/loop/loop/... 的无穷展开
    assert follow.paths(tree, NameGlob("dangling")) == ["/dangling"]
    # 更深的环：docs/img/up -> /docs，祖先链上已有 docs，所以只列出链接本身、不再展开
    tree.children["docs"].children["img"].add(Symlink("up", "/docs"))
    deep = follow.paths(tree, NameGlob("logo.png"))
    assert deep == ["/docs/img/logo.png", "/link_to_docs/img/logo.png"]
    tree.children["docs"].children["img"].children.pop("up")

    # 7. 最大深度：真正少走路，而不是遍历后过滤
    s_all, s_d1 = FindStats(), FindStats()
    list(FileSearcher().find(tree, stats=s_all))
    list(FileSearcher(max_depth=1).find(tree, stats=s_d1))
    assert s_d1.visited < s_all.visited and s_d1.dirs_entered == 1       # 只展开根
    depth1 = FileSearcher(max_depth=1).paths(tree, OfType(NodeType.DIR))
    assert depth1 == ["/docs", "/src"]

    # 8. 剪枝：整棵 docs 子树根本不展开
    s_prune = FindStats()
    pruned = FileSearcher().paths(tree, Extension("md"), prune=lambda e: e.name == "docs", stats=s_prune)
    assert pruned == []
    assert s_prune.visited < s_all.visited

    # 9. 惰性：只要第一个结果，不走完整棵树
    lazy_stats = FindStats()
    first = next(FileSearcher().find(tree, Extension("py"), stats=lazy_stats))
    assert first.path == "/b.py" and lazy_stats.visited < s_all.visited

    # 10. 开闭原则：新增一种条件只写一个子类，Searcher 与其他过滤器不动
    @dataclass(frozen=True)
    class NameLongerThan(Filter):
        n: int

        def matches(self, entry: Entry) -> bool:
            return len(entry.name) > self.n

    assert finder.paths(tree, NameLongerThan(11) & OfType(NodeType.FILE)) == ["/archive.tar.gz", "/src/test_main.py"]

    # 11. 过滤器不可变且可复用：组合不改变原对象
    base = Extension("py")
    _ = base & Size(min_bytes=10 ** 9)
    assert finder.paths(tree, base) == ["/b.py", "/src/main.py", "/src/test_main.py", "/src/util.py"]

    # 12. 查询小语言：和手写组合等价
    q = parse_query("ext=py and size>1k and not name=test_*")
    assert finder.paths(tree, q) == ["/b.py", "/src/main.py"]
    q2 = parse_query("(ext=md or ext=py) and not (owner=chi) and size<=600")
    assert finder.paths(tree, q2) == ["/docs/old.md", "/src/util.py"]
    assert finder.paths(tree, parse_query("type=dir or name=a.*")) == ["/a.txt", "/docs", "/docs/img", "/src"]
    for bad in ["ext=", "(ext=py", "ext=py and", "size>abc", "foo=bar", "ext=py ext=md"]:
        try:
            parse_query(bad)
        except (ValueError, KeyError):
            pass
        else:
            raise AssertionError(f"应该报语法错误: {bad!r}")

    # 13. 重名保护
    d = Directory("x")
    d.add(File("f", 1, 1))
    try:
        d.add(File("f", 2, 2))
    except ValueError:
        pass
    else:
        raise AssertionError("同目录重名应报错")

    # 14. 空目录 / 只有根
    assert finder.paths(Directory("")) == []


if __name__ == "__main__":
    _run_tests()
    print("OK file_search")
