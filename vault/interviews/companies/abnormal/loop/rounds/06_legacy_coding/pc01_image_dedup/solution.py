"""pc01 Image dedup -- reference solution.

Part 1: find_duplicates (size buckets -> streaming full hash)
Part 2: find_duplicates_verified (weak hash buckets -> byte-by-byte confirmation)
Part 3: plan_deletions (which copy to keep; dry-run by default)
Part 4: average_hash / hamming / group_similar (near-duplicate images on 8x8 grayscale matrices)
"""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import zlib
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Iterable

DEFAULT_CHUNK = 1 << 16


# ---------------------------------------------------------------- the given (deliberately weak) hash
def _calculate_hash(path: str) -> int:
    """GIVEN by the interviewer. Weak on purpose: CRC32 of the first 1 KiB, seeded with the file size.
    Two files of equal size that share their first 1 KiB always collide."""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        head = f.read(1024)
    return zlib.crc32(head, size & 0xFFFFFFFF)


@dataclass
class ScanResult:
    groups: list[list[str]] = field(default_factory=list)
    skipped: int = 0  # unreadable files (counted once per path)


def _check_chunk(chunk_size: int) -> None:
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive int")


def _strong_hash(path: str, chunk_size: int) -> bytes:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(chunk_size)
            if not block:
                break
            h.update(block)
    return h.digest()


def files_equal(a: str, b: str, chunk_size: int = DEFAULT_CHUNK) -> bool:
    """Byte-by-byte comparison, chunked, stops at the first differing chunk."""
    _check_chunk(chunk_size)
    if os.path.getsize(a) != os.path.getsize(b):
        return False
    with open(a, "rb") as fa, open(b, "rb") as fb:
        while True:
            ba = fa.read(chunk_size)
            bb = fb.read(chunk_size)
            if ba != bb:
                return False
            if not ba:
                return True


def _size_buckets(root: str) -> tuple[dict[int, list[str]], int]:
    buckets: dict[int, list[str]] = defaultdict(list)
    skipped = 0
    for dirpath, _dirs, names in os.walk(root, followlinks=False):
        for name in names:
            p = os.path.join(dirpath, name)
            if os.path.islink(p):
                continue  # never follow symlinks
            try:
                if not os.path.isfile(p):
                    continue
                buckets[os.path.getsize(p)].append(p)
            except OSError:
                skipped += 1
    return buckets, skipped


def _finish(groups: Iterable[list[str]]) -> list[list[str]]:
    out = [sorted(g) for g in groups if len(g) >= 2]
    out.sort(key=lambda g: g[0])
    return out


def scan_duplicates(
    root: str, chunk_size: int = DEFAULT_CHUNK, hash_fn: Callable[[str], object] | None = None
) -> ScanResult:
    """hash_fn=None: full-content SHA-256 streamed in chunks (no verification needed).
    hash_fn given: treated as a *weak* bucket key; every bucket is confirmed byte by byte."""
    _check_chunk(chunk_size)
    buckets, skipped = _size_buckets(root)
    groups: list[list[str]] = []
    bad: set[str] = set()
    for size, paths in buckets.items():
        if len(paths) < 2:
            continue  # unique size => cannot be a duplicate, never read
        by_hash: dict[object, list[str]] = defaultdict(list)
        for p in paths:
            try:
                key = _strong_hash(p, chunk_size) if hash_fn is None else hash_fn(p)
            except OSError:
                bad.add(p)
                continue
            by_hash[key].append(p)
        for same in by_hash.values():
            if len(same) < 2:
                continue
            if hash_fn is None:
                groups.append(same)
                continue
            classes: list[list[str]] = []  # equivalence classes by real content
            for p in same:
                for cls in classes:
                    try:
                        eq = files_equal(cls[0], p, chunk_size)
                    except OSError:
                        bad.add(p)
                        break
                    if eq:
                        cls.append(p)
                        break
                else:
                    if p not in bad:
                        classes.append([p])
            groups.extend(classes)
    return ScanResult(_finish(g for g in groups if not (set(g) & bad) or True), skipped + len(bad))


def find_duplicates(root: str, chunk_size: int = DEFAULT_CHUNK) -> list[list[str]]:
    """Part 1."""
    return scan_duplicates(root, chunk_size).groups


def find_duplicates_verified(
    root: str, hash_fn: Callable[[str], object] = _calculate_hash, chunk_size: int = DEFAULT_CHUNK
) -> list[list[str]]:
    """Part 2: survives a colliding hash_fn because equal hashes are only candidates."""
    return scan_duplicates(root, chunk_size, hash_fn).groups


# ---------------------------------------------------------------- Part 3
def plan_deletions(
    groups: list[list[str]], policy: str = "oldest", prefer_dir: str | None = None, dry_run: bool = True
) -> list[str]:
    """Pick one file to keep per group, return the sorted list of the others.
    policy: 'oldest' (earliest mtime) | 'shortest_path' | 'prefer_dir' (keep a copy under prefer_dir,
    falling back to 'oldest' when the group has none there). Ties: shorter path, then lexicographic.
    dry_run=True (default) only reports; dry_run=False deletes and returns what it deleted."""
    if policy not in ("oldest", "shortest_path", "prefer_dir"):
        raise ValueError(f"unknown policy: {policy}")
    if policy == "prefer_dir" and not prefer_dir:
        raise ValueError("prefer_dir policy needs prefer_dir")

    def under(p: str) -> bool:
        base = os.path.abspath(prefer_dir)
        return os.path.commonpath([base, os.path.abspath(p)]) == base

    victims: list[str] = []
    for group in groups:
        alive = [p for p in group if os.path.lexists(p)]
        if len(alive) < 2:
            continue
        if policy == "shortest_path":
            key = lambda p: (len(p), p)  # noqa: E731
            keep = min(alive, key=key)
        else:
            pool = alive
            if policy == "prefer_dir":
                pool = [p for p in alive if under(p)] or alive
            keep = min(pool, key=lambda p: (os.stat(p).st_mtime, len(p), p))
        victims.extend(p for p in alive if p != keep)
    victims.sort()
    if not dry_run:
        for p in victims:
            os.remove(p)
    return victims


# ---------------------------------------------------------------- Part 4
def average_hash(matrix: list[list[int]]) -> int:
    """64-bit aHash of an 8x8 grayscale matrix: bit i (row-major, MSB first) = pixel > mean."""
    if len(matrix) != 8 or any(len(r) != 8 for r in matrix):
        raise ValueError("matrix must be 8x8")
    flat = [int(v) for r in matrix for v in r]
    total = sum(flat)
    h = 0
    for v in flat:
        h = (h << 1) | (1 if v * 64 > total else 0)  # integer compare: v > total/64
    return h


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def group_similar(images: dict[str, list[list[int]]], threshold: int = 5) -> list[list[str]]:
    """Connected components of the 'hamming <= threshold' graph (transitive). Groups of >= 2 only."""
    if threshold < 0:
        raise ValueError("threshold must be >= 0")
    names = sorted(images)
    hashes = {n: average_hash(images[n]) for n in names}
    parent = {n: n for n in names}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            if hamming(hashes[a], hashes[b]) <= threshold:
                parent[find(b)] = find(a)
    comps: dict[str, list[str]] = defaultdict(list)
    for n in names:
        comps[find(n)].append(n)
    return _finish(comps.values())


# ---------------------------------------------------------------- line-driven main
def _materialise(lines: list[str], root: str) -> None:
    """FILE <relpath> <content> [mtime]  |  LINK <relpath> <target-relpath>"""
    for ln in lines:
        parts = ln.split()
        if parts[0] == "FILE":
            p = os.path.join(root, parts[1])
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as f:
                f.write(parts[2].encode() if len(parts) > 2 else b"")
            if len(parts) > 3:
                os.utime(p, (float(parts[3]), float(parts[3])))
        elif parts[0] == "LINK":
            p = os.path.join(root, parts[1])
            os.makedirs(os.path.dirname(p), exist_ok=True)
            os.symlink(os.path.join(root, parts[2]), p)
        else:
            raise ValueError(f"bad line: {ln}")


def _rel(root: str, paths: list[str]) -> list[str]:
    return [os.path.relpath(p, root) for p in paths]


def part1(lines: list[str]) -> list[str]:
    with tempfile.TemporaryDirectory() as root:
        _materialise(lines, root)
        return [" ".join(_rel(root, g)) for g in find_duplicates(root, chunk_size=4)]


def part2(lines: list[str]) -> list[str]:
    with tempfile.TemporaryDirectory() as root:
        _materialise(lines, root)
        return [" ".join(_rel(root, g)) for g in find_duplicates_verified(root, chunk_size=4)]


def part3(lines: list[str]) -> list[str]:
    """First line: POLICY <oldest|shortest_path|prefer:<dir>>; rest as part1."""
    if not lines or not lines[0].startswith("POLICY "):
        raise ValueError("part3 input must start with 'POLICY <p>'")
    pol = lines[0].split()[1]
    with tempfile.TemporaryDirectory() as root:
        _materialise(lines[1:], root)
        groups = find_duplicates(root)
        if pol.startswith("prefer:"):
            out = plan_deletions(groups, "prefer_dir", prefer_dir=os.path.join(root, pol[7:]))
        else:
            out = plan_deletions(groups, pol)
        return _rel(root, out)


def part4(lines: list[str]) -> list[str]:
    """First line: THRESHOLD <t>; then IMG <name> <64 comma-separated ints>."""
    if not lines or not lines[0].startswith("THRESHOLD "):
        raise ValueError("part4 input must start with 'THRESHOLD <t>'")
    t = int(lines[0].split()[1])
    images = {}
    for ln in lines[1:]:
        _, name, vals = ln.split()
        nums = [int(x) for x in vals.split(",")]
        images[name] = [nums[i : i + 8] for i in range(0, 64, 8)]
    return [" ".join(g) for g in group_similar(images, t)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3, 4: part4}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
