"""od02 In-Memory File System -- YOUR implementation. Run pytest against this file with
IMPL=starter.

See problem.md for the full contract: the asymmetric mkdir-vs-add_content_to_file
parent-creation rule, the rm/rmdir error taxonomy, chunked storage, and per-path locking.
"""

from __future__ import annotations

import sys


class FileSystem:
    def __init__(self) -> None:
        pass  # TODO: a root directory node + a structural lock (see problem.md Part4)

    def ls(self, path: str) -> list[str]:
        """File -> [basename]. Dir -> sorted list of direct child names. Missing path ->
        FileNotFoundError."""
        raise NotImplementedError  # TODO

    def mkdir(self, path: str) -> None:
        """Create missing directories recursively (like mkdir -p). Already a dir -> no-op.
        Already a file -> FileExistsError."""
        raise NotImplementedError  # TODO

    def add_content_to_file(self, file_path: str, content: str) -> None:
        """Create-or-append. Parent directory must already exist (FileNotFoundError if not --
        unlike mkdir, this method never creates missing parents). Path is a directory ->
        IsADirectoryError. Stores content as an appended chunk, not a string concatenation."""
        raise NotImplementedError  # TODO

    def read_content_from_file(self, file_path: str) -> str:
        """Full concatenated content. Missing -> FileNotFoundError. Directory ->
        IsADirectoryError."""
        raise NotImplementedError  # TODO

    def rm(self, path: str) -> None:
        """Delete a file. Missing -> FileNotFoundError. Directory -> IsADirectoryError. Root ->
        PermissionError."""
        raise NotImplementedError  # TODO

    def rmdir(self, path: str) -> None:
        """Delete an empty directory. Missing -> FileNotFoundError. File -> NotADirectoryError.
        Non-empty -> OSError. Root -> PermissionError."""
        raise NotImplementedError  # TODO

    def size(self, file_path: str) -> int:
        """O(1) total byte length of the file's content (maintained incrementally, not by
        joining chunks)."""
        raise NotImplementedError  # TODO


def part1(lines: list[str]) -> list[str]:
    """Drive a fresh FileSystem from MKDIR/ADD/LS/READ lines (LC 588 subset)."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Like part1, plus RM/RMDIR lines."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Like part2, plus SIZE lines; content is stored/queried through the chunked
    representation described in problem.md Part3."""
    return part2(lines)


def part4(lines: list[str]) -> list[str]:
    """Same driver as part3 -- the per-path locking guarantee is exercised directly against
    FileSystem with real threads in test_od02.py, not through this single-threaded line
    driver."""
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
