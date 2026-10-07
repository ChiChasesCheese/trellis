"""pc01 Image dedup -- YOUR implementation. Run tests against this file with IMPL=starter.

Part 1 find_duplicates -> Part 2 find_duplicates_verified (the given hash collides) ->
Part 3 plan_deletions -> Part 4 average_hash / hamming / group_similar.
"""

from __future__ import annotations

import os
import sys
import zlib
from typing import Callable

DEFAULT_CHUNK = 1 << 16


def _calculate_hash(path: str) -> int:
    """GIVEN by the interviewer. Weak on purpose: CRC32 of the first 1 KiB, seeded with the file size.
    Two files of equal size that share their first 1 KiB always collide."""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        head = f.read(1024)
    return zlib.crc32(head, size & 0xFFFFFFFF)


class ScanResult:
    """groups: list[list[str]] of duplicate paths; skipped: number of unreadable files."""

    def __init__(self, groups=None, skipped=0):
        self.groups = groups if groups is not None else []
        self.skipped = skipped


def files_equal(a: str, b: str, chunk_size: int = DEFAULT_CHUNK) -> bool:
    """Part2: chunked byte-by-byte comparison; stop at the first difference."""
    # TODO
    return False


def scan_duplicates(
    root: str, chunk_size: int = DEFAULT_CHUNK, hash_fn: Callable[[str], object] | None = None
) -> ScanResult:
    """Part1/2: os.walk (do not follow symlinks), bucket by size, then by hash, then (only when
    hash_fn is given, i.e. it is weak) confirm with files_equal. Unreadable files are skipped and
    counted in ScanResult.skipped. chunk_size <= 0 -> ValueError."""
    # TODO
    return ScanResult()


def find_duplicates(root: str, chunk_size: int = DEFAULT_CHUNK) -> list[list[str]]:
    """Part1: groups of >= 2 identical files; paths sorted inside a group, groups sorted by first path."""
    # TODO
    return []


def find_duplicates_verified(
    root: str, hash_fn: Callable[[str], object] = _calculate_hash, chunk_size: int = DEFAULT_CHUNK
) -> list[list[str]]:
    """Part2: like find_duplicates but bucketed by a WEAK hash_fn; equal hash is only a candidate."""
    # TODO
    return []


def plan_deletions(
    groups: list[list[str]], policy: str = "oldest", prefer_dir: str | None = None, dry_run: bool = True
) -> list[str]:
    """Part3: per group keep one file, return the sorted list of the rest.
    policy: 'oldest' | 'shortest_path' | 'prefer_dir'; ties: shorter path, then lexicographic.
    Unknown policy / prefer_dir without prefer_dir -> ValueError. dry_run=False really deletes."""
    # TODO
    return []


def average_hash(matrix: list[list[int]]) -> int:
    """Part4: 64-bit average hash of an 8x8 grayscale matrix (bit = pixel > mean, row-major, MSB first).
    Wrong shape -> ValueError."""
    # TODO
    return 0


def hamming(a: int, b: int) -> int:
    """Part4: number of differing bits."""
    # TODO
    return 0


def group_similar(images: dict[str, list[list[int]]], threshold: int = 5) -> list[list[str]]:
    """Part4: group names whose hashes are within `threshold` bits (transitively); groups of >= 2 only,
    sorted inside and by first name. threshold < 0 -> ValueError."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """Build the described tree in a temp dir, run find_duplicates(chunk_size=4); one line per group."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3, 4: part4}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
