"""内存文件系统练习骨架：公开 API 与 `solution.py` 完全一致，方法体全部待补全。
把每个 `raise NotImplementedError` 换成你自己的实现，然后用
`IMPL=starter uv run --with pytest python -m pytest <本目录> -q` 验收。
内部表示随你换，但测试只会通过公开方法断言，所以公开面不要改。
"""

from __future__ import annotations

from dataclasses import dataclass, field


class FSError(Exception):
    """本设计所有失败路径的公共基类。"""


class InvalidPathError(FSError):
    """路径本身不成立：不是绝对路径，或者这个操作不允许作用在根目录上。"""


class PathEscapesRootError(FSError):
    """路径里的 `..` 试图越过根目录。"""


class PathNotFoundError(FSError):
    """路径途中某一段目录、或者路径本身指向的条目不存在。"""


class PathAlreadyExistsError(FSError):
    """`move`/`copy`/`add_file` 的目标位置已经被占用。"""


class ExpectedDirectoryError(FSError):
    """路径途中某一段本该是目录，实际却是文件。"""


class ExpectedFileError(FSError):
    """这个位置本该是文件，实际却是目录（或者是根目录本身）。"""


class DirectoryNotEmptyError(FSError):
    """目录非空，删除它需要显式传 `recursive=True`。"""


@dataclass
class File:
    """一个文件：只有内容，没有名字。"""

    content: bytes = b""


@dataclass
class Directory:
    """一个目录：只有子条目表，同样没有名字。"""

    entries: dict[str, "File | Directory"] = field(default_factory=dict)


class FileSystem:
    """整棵目录树的唯一入口。见 `solution.py` 的类文档字符串了解每一关对应哪些方法。"""

    def __init__(self) -> None:
        self._root = Directory({})

    # ---------- 第 1 关：目录树与基本读写 ----------

    def mkdir(self, path: str) -> None:
        raise NotImplementedError

    def ls(self, path: str) -> list[str]:
        raise NotImplementedError

    def add_file(self, path: str, content: bytes) -> None:
        raise NotImplementedError

    def read_file(self, path: str) -> bytes:
        raise NotImplementedError

    # ---------- 第 2 关：删除、移动、复制、体积 ----------

    def remove(self, path: str, *, recursive: bool = False) -> None:
        raise NotImplementedError

    def move(self, src: str, dst: str) -> None:
        raise NotImplementedError

    def copy(self, src: str, dst: str) -> None:
        raise NotImplementedError

    def size(self, path: str) -> int:
        raise NotImplementedError

    # ---------- 第 3 关：按通配符搜索 ----------

    def find(self, pattern: str) -> list[str]:
        raise NotImplementedError

    # ---------- 第 4 关：快照与恢复 ----------

    def snapshot(self) -> Directory:
        raise NotImplementedError

    def restore(self, snapshot: Directory) -> None:
        raise NotImplementedError
