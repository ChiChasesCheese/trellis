"""内存文件系统（In-Memory File System）——目录树的组合模式与路径解析参考实现。

五行设计：`File` 和 `Directory` 没有共同的基类——两者共享的部分比看起来还要少，连"名字"
都不存在节点自己身上，名字只活在父目录 `entries` 字典的键里；节点也不持有指向父目录的
反向引用，一切路径解析都由 `FileSystem` 从根节点重新往下走一遍完成，`move` 因此天然拒绝
"把一个目录移进它自己的子孙目录"这种会产生环的操作，不需要专门检查；递归删除不需要手写
递归——把子树从父目录的字典里摘掉之后，Python 的垃圾回收会顺着这棵子树自己清理干净；
复制一个大文件是 `O(1)` 的——`bytes` 不可变，新文件直接共享同一份内容，真正递归、按条目
数计费的只有复制目录这一步；第 4 关的快照/恢复复用复制目录用的同一个 `_duplicate`，
`File`/`Directory` 两个类因此一行都不用改。
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass, field


class FSError(Exception):
    """本设计所有失败路径的公共基类。"""


class InvalidPathError(FSError):
    """路径本身不成立：不是绝对路径，或者这个操作不允许作用在根目录上。"""


class PathEscapesRootError(FSError):
    """路径里的 `..` 试图越过根目录——这套文件系统选择直接拒绝，而不是像大多数 shell
    的 `cd ..` 那样悄悄停在根目录，理由见题解"关键设计决策"。
    """


class PathNotFoundError(FSError):
    """路径途中某一段目录、或者路径本身指向的条目不存在。"""


class PathAlreadyExistsError(FSError):
    """`move`/`copy`/`add_file` 的目标位置已经被占用。"""


class ExpectedDirectoryError(FSError):
    """路径途中某一段本该是目录，实际却是文件——没法继续往下走。"""


class ExpectedFileError(FSError):
    """这个位置本该是文件，实际却是目录（或者是根目录本身）。"""


class DirectoryNotEmptyError(FSError):
    """目录非空，删除它需要显式传 `recursive=True`。"""


@dataclass
class File:
    """一个文件：只有内容，没有名字——它的名字是父目录 `entries` 字典里那个键，不是它
    自己的属性，见 `FileSystem` 的说明。
    """

    content: bytes = b""


@dataclass
class Directory:
    """一个目录：只有子条目表，同样没有名字。`entries` 的值可以是 `File`，也可以是另一个
    `Directory`——这就是组合模式的全部结构，但这里到此为止，不再往上抽一个共同基类。
    """

    entries: dict[str, "File | Directory"] = field(default_factory=dict)


class FileSystem:
    """整棵目录树的唯一入口，也是路径解析逻辑唯一的家：`File`/`Directory` 不知道自己在
    树里的哪个位置，每一次操作都由这个类从根节点重新往下走一遍。`mkdir`/`ls`/`add_file`/
    `read_file` 是第 1 关，`remove`/`move`/`copy`/`size` 是第 2 关，`find` 是第 3 关，
    `snapshot`/`restore` 是第 4 关。
    """

    def __init__(self) -> None:
        self._root = Directory({})

    # ---------- 路径解析 ----------

    def _normalize(self, path: str) -> list[str]:
        """把一个路径字符串变成一串规范化的目录段：必须以 `/` 开头；空段（连续的 `/`
        或结尾的 `/`）和 `.` 直接跳过；`..` 弹出上一段，如果已经在根目录上还遇到 `..`，
        判定为越过根目录，直接拒绝而不是悄悄停在原地——见"关键设计决策"。
        """
        if not path.startswith("/"):
            raise InvalidPathError(f"路径必须是绝对路径，以 / 开头：{path!r}")
        segments: list[str] = []
        for part in path.split("/"):
            if part in ("", "."):
                continue
            if part == "..":
                if not segments:
                    raise PathEscapesRootError(f"路径试图越过根目录：{path!r}")
                segments.pop()
            else:
                segments.append(part)
        return segments

    def _resolve_dir(self, segments: list[str], *, create_missing: bool) -> Directory:
        """沿着 `segments` 从根目录往下走，返回终点目录；`create_missing` 为真时，缺失的
        中间目录会被顺手创建——这是 `mkdir` 的"创建中间目录"和 `mkdir -p` 语义的全部实现。
        """
        node = self._root
        for name in segments:
            entry = node.entries.get(name)
            if entry is None:
                if not create_missing:
                    raise PathNotFoundError(f"目录不存在：{name}")
                entry = Directory({})
                node.entries[name] = entry
            elif not isinstance(entry, Directory):
                raise ExpectedDirectoryError(f"{name} 不是一个目录")
            node = entry
        return node

    def _get(self, path: str) -> File | Directory:
        """解析并返回 `path` 指向的节点（文件或目录），不关心它是哪一种。"""
        segments = self._normalize(path)
        if not segments:
            return self._root
        parent = self._resolve_dir(segments[:-1], create_missing=False)
        node = parent.entries.get(segments[-1])
        if node is None:
            raise PathNotFoundError(f"路径不存在：{path}")
        return node

    # ---------- 第 1 关：目录树与基本读写 ----------

    def mkdir(self, path: str) -> None:
        """创建目录，自动创建缺失的中间目录；路径已经是一个目录时安静地成功（`mkdir -p`
        语义），路径已经是一个文件时抛 `ExpectedDirectoryError`。
        """
        self._resolve_dir(self._normalize(path), create_missing=True)

    def ls(self, path: str) -> list[str]:
        """`path` 是目录时，返回它直接子条目的名字，按字典序排序；`path` 是文件时，
        返回只包含这一个文件名的列表——和真实的 `ls` 行为一致。
        """
        node = self._get(path)
        if isinstance(node, File):
            return [self._normalize(path)[-1]]
        return sorted(node.entries)

    def add_file(self, path: str, content: bytes) -> None:
        """在一个已经存在的目录下写入文件，路径已经有同名文件则整体覆盖。和 `mkdir` 不
        同，这里不会自动创建缺失的父目录——先 `mkdir` 再写文件，两个操作各自的失败原因
        因此不会被混在一起。
        """
        segments = self._normalize(path)
        if not segments:
            raise ExpectedFileError("根目录不能被当作文件写入")
        parent = self._resolve_dir(segments[:-1], create_missing=False)
        name = segments[-1]
        if isinstance(parent.entries.get(name), Directory):
            raise ExpectedFileError(f"{path} 已经是一个目录")
        parent.entries[name] = File(content)

    def read_file(self, path: str) -> bytes:
        """读取一个文件的全部内容；`path` 指向目录（包括根目录）时抛 `ExpectedFileError`。"""
        node = self._get(path)
        if not isinstance(node, File):
            raise ExpectedFileError(f"{path} 是一个目录，不是文件")
        return node.content

    # ---------- 第 2 关：删除、移动、复制、体积 ----------

    def remove(self, path: str, *, recursive: bool = False) -> None:
        """删除一个文件或目录。目录非空时必须传 `recursive=True` 才会连同子树一起删除——
        子树的清理不需要手写递归：从父目录的字典里摘掉之后，不再被任何引用持有的整棵
        子树会被 Python 自己的垃圾回收顺手清理。
        """
        segments = self._normalize(path)
        if not segments:
            raise InvalidPathError("不能删除根目录")
        parent = self._resolve_dir(segments[:-1], create_missing=False)
        name = segments[-1]
        node = parent.entries.get(name)
        if node is None:
            raise PathNotFoundError(f"路径不存在：{path}")
        if isinstance(node, Directory) and node.entries and not recursive:
            raise DirectoryNotEmptyError(f"{path} 不是空目录，删除需要 recursive=True")
        del parent.entries[name]

    def move(self, src: str, dst: str) -> None:
        """把 `src` 移动到 `dst`（`dst` 是完整的目标路径，不是"移进某个目录"）。目标
        位置必须在**摘下节点之前**就验证合法——先摘后验的顺序一旦目标非法就会把节点
        直接丢掉（数据丢失），如果目标恰好是它自己的子孙路径，先摘后验甚至会把这个
        目录接到它自己的子树下面，造出一个真实的环，`size`/`find`/`copy` 这些递归操作
        会因此永远走不到头。所以这里先算好目标父目录、确认目标名字没被占用、并且显式
        排除"目标是自己或者自己的子孙路径"，全部通过之后才真正做摘下和放入这两步。
        """
        src_segments = self._normalize(src)
        if not src_segments:
            raise InvalidPathError("不能移动根目录")
        dst_segments = self._normalize(dst)
        if dst_segments[:len(src_segments)] == src_segments:
            raise InvalidPathError(f"不能把 {src} 移动到它自己（或自己的子路径）{dst} 下")
        if not dst_segments:
            raise PathAlreadyExistsError("根目录已经存在")
        src_parent = self._resolve_dir(src_segments[:-1], create_missing=False)
        src_name = src_segments[-1]
        node = src_parent.entries.get(src_name)
        if node is None:
            raise PathNotFoundError(f"路径不存在：{src}")
        dst_parent = self._resolve_dir(dst_segments[:-1], create_missing=False)
        dst_name = dst_segments[-1]
        if dst_name in dst_parent.entries:
            raise PathAlreadyExistsError(f"{dst} 已经存在")
        del src_parent.entries[src_name]
        dst_parent.entries[dst_name] = node

    def _place(self, dst: str, node: File | Directory) -> None:
        segments = self._normalize(dst)
        if not segments:
            raise PathAlreadyExistsError("根目录已经存在")
        parent = self._resolve_dir(segments[:-1], create_missing=False)
        name = segments[-1]
        if name in parent.entries:
            raise PathAlreadyExistsError(f"{dst} 已经存在")
        parent.entries[name] = node

    def copy(self, src: str, dst: str) -> None:
        """复制 `src` 到 `dst`。文件的复制是 `O(1)`——`content` 是不可变的 `bytes`，新
        `File` 直接引用同一个对象，不管文件多大都不产生新的字节拷贝；目录的复制必须
        递归重建每一层 `entries` 字典（否则两份目录会共享同一个可变字典，改一份另一份
        也会跟着变），代价是 `O(子树里的条目数)`，但落到每个文件节点时依然是零拷贝。
        """
        self._place(dst, self._duplicate(self._get(src)))

    def _duplicate(self, node: File | Directory) -> File | Directory:
        if isinstance(node, File):
            return File(node.content)
        return Directory({name: self._duplicate(child) for name, child in node.entries.items()})

    def size(self, path: str) -> int:
        """`path` 指向的子树一共占多少字节：文件是自己内容的长度，目录是所有子条目的和。"""
        return self._size_of(self._get(path))

    def _size_of(self, node: File | Directory) -> int:
        if isinstance(node, File):
            return len(node.content)
        return sum(self._size_of(child) for child in node.entries.values())

    # ---------- 第 3 关：按通配符搜索 ----------

    def find(self, pattern: str) -> list[str]:
        """从根目录开始，找出所有**文件名**（不含路径）匹配通配符 `pattern` 的文件或
        目录，返回它们的绝对路径，按字典序排序。整棵树现场走一遍，`O(树的节点数)`——
        维护一份按名字分桶的索引能把它降到 `O(匹配数)`，值得不值得换成索引见"扩展与
        追问"。
        """
        matches: list[str] = []
        self._walk(self._root, "", pattern, matches)
        return sorted(matches)

    def _walk(self, node: Directory, path: str, pattern: str, matches: list[str]) -> None:
        for name, child in node.entries.items():
            child_path = f"{path}/{name}"
            if fnmatch.fnmatchcase(name, pattern):
                matches.append(child_path)
            if isinstance(child, Directory):
                self._walk(child, child_path, pattern, matches)

    # ---------- 第 4 关：快照与恢复 ----------

    def snapshot(self) -> Directory:
        """把当前整棵树复制一份，作为一个不透明的句柄交给调用方保存；复用 `copy` 用的
        同一个 `_duplicate`，`File`/`Directory` 的定义因此完全不需要为这个功能改动。
        """
        return self._duplicate(self._root)

    def restore(self, snapshot: Directory) -> None:
        """把树恢复成某个快照当时的样子。恢复时再复制一次快照，而不是直接把它当成新的
        根——否则调用方以后如果不小心改了保留着的快照对象，会反过来污染当前的树。
        """
        self._root = self._duplicate(snapshot)


def _demo() -> None:
    fs = FileSystem()
    fs.mkdir("/docs/reports")
    fs.add_file("/docs/reports/q1.txt", b"Q1 numbers")
    fs.add_file("/docs/readme.md", b"# hello")
    print("根目录:", fs.ls("/"))
    print("docs 目录:", fs.ls("/docs"))

    snap = fs.snapshot()
    fs.remove("/docs/reports", recursive=True)
    print("删除后 docs 目录:", fs.ls("/docs"))
    fs.restore(snap)
    print("恢复后 docs 目录:", fs.ls("/docs"))

    fs.copy("/docs/readme.md", "/docs/readme.bak.md")
    print("docs 目录体积:", fs.size("/docs"), "字节")
    print("匹配 *.md 的路径:", fs.find("*.md"))


if __name__ == "__main__":
    _demo()
