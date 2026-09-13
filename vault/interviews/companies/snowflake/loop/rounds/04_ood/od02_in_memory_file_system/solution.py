"""od02 In-Memory File System -- reference solution.

A tree of _Dir/_File nodes. A single "structural" lock guards every mutation of the tree shape
(mkdir/rm/rmdir, and the moment a new _File node is inserted) and every traversal that walks the
tree to find a node -- but it is held only for that O(depth) traversal, never across a file's
content operation. Each _File additionally has its own lock guarding its chunk list, so
concurrent add_content_to_file calls on *different* files never contend on the structural lock's
critical section for their actual write.
"""

from __future__ import annotations

import sys
import threading


class _Dir:
    __slots__ = ("children",)

    def __init__(self) -> None:
        self.children: dict[str, "_Dir | _File"] = {}


class _File:
    __slots__ = ("chunks", "total_len", "lock")

    def __init__(self) -> None:
        self.chunks: list[str] = []
        self.total_len = 0
        self.lock = threading.Lock()


def _split(path: str) -> list[str]:
    return [c for c in path.split("/") if c]


class FileSystem:
    def __init__(self) -> None:
        self._root = _Dir()
        self._tree_lock = threading.Lock()

    # ---------------------------------------------------------------- internals (tree_lock held)
    def _get_node(self, components: list[str]):
        node = self._root
        for name in components:
            if not isinstance(node, _Dir):
                raise NotADirectoryError("/" + "/".join(components))
            if name not in node.children:
                raise FileNotFoundError("/" + "/".join(components))
            node = node.children[name]
        return node

    # ---------------------------------------------------------------- public API
    def ls(self, path: str) -> list[str]:
        components = _split(path)
        with self._tree_lock:
            node = self._get_node(components)
            if isinstance(node, _File):
                return [components[-1]]
            return sorted(node.children.keys())

    def mkdir(self, path: str) -> None:
        components = _split(path)
        with self._tree_lock:
            node = self._root
            for name in components:
                if not isinstance(node, _Dir):
                    raise NotADirectoryError(path)
                if name in node.children:
                    node = node.children[name]
                else:
                    new_dir = _Dir()
                    node.children[name] = new_dir
                    node = new_dir
            if isinstance(node, _File):
                raise FileExistsError(path)
            # else: already a directory (freshly made or pre-existing) -> idempotent no-op

    def add_content_to_file(self, file_path: str, content: str) -> None:
        components = _split(file_path)
        if not components:
            raise IsADirectoryError(file_path)  # root
        *parent_components, name = components
        with self._tree_lock:
            parent = self._get_node(parent_components)
            if not isinstance(parent, _Dir):
                raise NotADirectoryError(file_path)
            existing = parent.children.get(name)
            if existing is None:
                file_node = _File()
                parent.children[name] = file_node
            elif isinstance(existing, _Dir):
                raise IsADirectoryError(file_path)
            else:
                file_node = existing
        with file_node.lock:
            file_node.chunks.append(content)
            file_node.total_len += len(content)

    def read_content_from_file(self, file_path: str) -> str:
        components = _split(file_path)
        if not components:
            raise IsADirectoryError(file_path)
        with self._tree_lock:
            node = self._get_node(components)
        if isinstance(node, _Dir):
            raise IsADirectoryError(file_path)
        with node.lock:
            return "".join(node.chunks)

    def size(self, file_path: str) -> int:
        components = _split(file_path)
        if not components:
            raise IsADirectoryError(file_path)
        with self._tree_lock:
            node = self._get_node(components)
        if isinstance(node, _Dir):
            raise IsADirectoryError(file_path)
        with node.lock:
            return node.total_len

    def rm(self, path: str) -> None:
        components = _split(path)
        if not components:
            raise PermissionError(path)
        *parent_components, name = components
        with self._tree_lock:
            parent = self._get_node(parent_components)
            if not isinstance(parent, _Dir) or name not in parent.children:
                raise FileNotFoundError(path)
            target = parent.children[name]
            if isinstance(target, _Dir):
                raise IsADirectoryError(path)
            del parent.children[name]

    def rmdir(self, path: str) -> None:
        components = _split(path)
        if not components:
            raise PermissionError(path)
        *parent_components, name = components
        with self._tree_lock:
            parent = self._get_node(parent_components)
            if not isinstance(parent, _Dir) or name not in parent.children:
                raise FileNotFoundError(path)
            target = parent.children[name]
            if isinstance(target, _File):
                raise NotADirectoryError(path)
            if target.children:
                raise OSError(path)
            del parent.children[name]


# ---------------------------------------------------------------------- line-driven wrappers
_ERROR_TYPES = {
    "FileNotFoundError": FileNotFoundError,
    "FileExistsError": FileExistsError,
    "IsADirectoryError": IsADirectoryError,
    "NotADirectoryError": NotADirectoryError,
    "PermissionError": PermissionError,
    "OSError": OSError,
}
_CATCH = tuple(_ERROR_TYPES.values())


def _run(fs: FileSystem, lines: list[str], verbs: set[str]) -> list[str]:
    out: list[str] = []
    for raw in lines:
        fields = raw.split(" ", 2)
        verb = fields[0]
        if verb not in verbs:
            raise ValueError(f"bad line for this part: {raw!r}")
        try:
            if verb == "MKDIR":
                fs.mkdir(fields[1])
            elif verb == "ADD":
                content = fields[2] if len(fields) > 2 else ""
                fs.add_content_to_file(fields[1], content)
            elif verb == "LS":
                out.append(repr(fs.ls(fields[1])))
            elif verb == "READ":
                out.append(fs.read_content_from_file(fields[1]))
            elif verb == "RM":
                fs.rm(fields[1])
            elif verb == "RMDIR":
                fs.rmdir(fields[1])
            elif verb == "SIZE":
                out.append(str(fs.size(fields[1])))
        except _CATCH as exc:
            out.append(f"ERROR:{type(exc).__name__}")
    return out


def part1(lines: list[str]) -> list[str]:
    return _run(FileSystem(), lines, {"MKDIR", "ADD", "LS", "READ"})


def part2(lines: list[str]) -> list[str]:
    return _run(FileSystem(), lines, {"MKDIR", "ADD", "LS", "READ", "RM", "RMDIR"})


def part3(lines: list[str]) -> list[str]:
    return _run(FileSystem(), lines, {"MKDIR", "ADD", "LS", "READ", "RM", "RMDIR", "SIZE"})


def part4(lines: list[str]) -> list[str]:
    return part3(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = lines[1:]
    out = {1: part1, 2: part2, 3: part3, 4: part4}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
