"""文件去重流水线（ArchiveSweep）的参考解。

设计五句话：
1. 发现：一个显式栈走遍所有根路径，用 lstat 判类型，不跟随软链接；路径身份是 str(Path(p))，每个身份只处理一次。
2. 逐级缩小候选：先按大小分组，再比首尾抽样，最后算流式全量摘要；每一级只处理上一级留下的同组文件。
3. 抽样与全量哈希共用一个 max_workers 大小的线程池，一组抽样全部回来就立刻提交这一组的全量哈希，两级流水线重叠。
4. 摘要相等不等于内容相等：每个摘要桶再用有界内存的逐字节比较拆成内容完全相同的等价类。
5. 每个文件的失败只记一条问题（以路径为键，后写覆盖先写），不影响别的文件；最后统一排序，结果与调度顺序无关。
"""

from __future__ import annotations

import hashlib
import os
import queue
import stat
from collections import defaultdict
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import ExitStack
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path
from typing import BinaryIO, Iterable

CHUNK = 1 << 20  # 每次最多读 1 MiB：内存上界与文件大小无关


@dataclass(frozen=True)
class DuplicateGroup:
    canonical: str
    duplicates: tuple[str, ...]
    size: int


@dataclass(frozen=True)
class FileIssue:
    path: str
    error: str


@dataclass(frozen=True)
class ScanReport:
    groups: tuple[DuplicateGroup, ...]
    issues: tuple[FileIssue, ...]
    files_considered: int
    bytes_hashed: int


def describe(exc: BaseException) -> str:
    """问题文本：异常类型加底层消息，消息必须保留。"""
    return f"{type(exc).__name__}: {exc}"


class _ReadFailure(Exception):
    """逐字节比较时某个文件打不开或读不动；path 指出是哪一个，问题记在它头上。"""

    def __init__(self, path: Path, cause: Exception) -> None:
        super().__init__(describe(cause))
        self.path = path


@dataclass
class _Batch:
    """同一大小（或同一抽样摘要）的一批文件：全部回来之后才知道哪些桶值得进下一级。"""

    stage: str  # "sample" 或 "full"
    size: int
    left: int
    buckets: dict[str, list[Path]] = field(default_factory=lambda: defaultdict(list))


def _feed(stream: BinaryIO, digest: "hashlib._Hash", limit: int | None = None) -> int:
    """把流按块喂给摘要，最多 limit 字节（None 表示读到尾）；返回实际读到的字节数。"""
    total = 0
    while limit is None or total < limit:
        want = CHUNK if limit is None else min(CHUNK, limit - total)
        chunk = stream.read(want)
        if not chunk:
            break
        digest.update(chunk)
        total += len(chunk)
    return total


def _open(path: Path) -> BinaryIO:
    try:
        return open(path, "rb")
    except Exception as exc:
        raise _ReadFailure(path, exc) from exc


def _read(stream: BinaryIO, path: Path) -> bytes:
    try:
        return stream.read(CHUNK)
    except Exception as exc:
        raise _ReadFailure(path, exc) from exc


def _same_content(a: Path, b: Path) -> bool:
    """逐块比较两个文件，遇到第一处不同就停；任何时刻内存里只有两块。"""
    with ExitStack() as stack:
        left = stack.enter_context(_open(a))
        right = stack.enter_context(_open(b))
        while True:
            chunk_a, chunk_b = _read(left, a), _read(right, b)
            if chunk_a != chunk_b:
                return False
            if not chunk_a:
                return True


def _place(path: Path, classes: list[list[Path]], issues: dict[str, str]) -> None:
    """把 path 放进第一个与它字节相同的等价类；每个类只和它的代表（第一个成员）比较。"""
    for members in classes:
        while members:
            try:
                same = _same_content(members[0], path)
            except _ReadFailure as failure:
                issues[str(failure.path)] = str(failure)
                if failure.path == path:
                    return  # 新来的文件读不了：丢掉它，别的类不必再比
                members.pop(0)  # 代表读不了：从类里去掉，下一个成员接任代表
                continue
            if same:
                members.append(path)
                return
            break  # 内容不同：试下一个类
    classes.append([path])


class FileDeduplicator:
    def __init__(self, max_workers: int = 4, sample_size: int = 4096):
        if max_workers < 1 or sample_size < 1:
            raise ValueError("limits must be positive")
        self.max_workers = max_workers
        self.sample_size = sample_size

    # ---- 两个测试钩子：各自只读文件、只返回（摘要，读到的字节数） ----

    def _full_digest(self, path: Path) -> tuple[str, int]:
        """流式全量 SHA-256：每次读一块，内存与文件大小无关。"""
        digest = hashlib.sha256()
        with open(path, "rb") as stream:
            nread = _feed(stream, digest)
        return digest.hexdigest(), nread

    def _sample_fingerprint(self, path: Path, size: int) -> tuple[str, int]:
        """开头最多 sample_size 字节，加结尾最多 sample_size 字节；两段不重叠。"""
        head = min(self.sample_size, size)
        tail_start = max(head, size - self.sample_size)
        digest = hashlib.sha256()
        with open(path, "rb") as stream:
            nread = _feed(stream, digest, head)
            if tail_start < size:
                stream.seek(tail_start)
                nread += _feed(stream, digest, size - tail_start)
        return digest.hexdigest(), nread

    # ---- 流水线 ----

    def scan(self, paths: Iterable[str | Path]) -> ScanReport:
        issues: dict[str, str] = {}
        files = self._discover(paths, issues)
        by_size: dict[int, list[Path]] = defaultdict(list)
        for name, size in files.items():
            by_size[size].append(Path(name))
        repeated = {size: group for size, group in by_size.items() if len(group) > 1}
        candidates, hashed = self._narrow(repeated, issues)
        groups = [g for size, bucket in candidates for g in self._verify(size, bucket, issues)]
        groups.sort(key=lambda g: g.canonical)
        ordered = sorted((FileIssue(p, e) for p, e in issues.items()), key=lambda i: (i.path, i.error))
        return ScanReport(tuple(groups), tuple(ordered), len(files), hashed)

    def _discover(self, roots: Iterable[str | Path], issues: dict[str, str]) -> dict[str, int]:
        """返回 {路径身份: 大小}，只含普通文件；根和子项用同一套处理，所以软链接、缺失、特殊文件的规则只写一遍。"""
        files: dict[str, int] = {}
        seen: set[str] = set()
        stack = [Path(root) for root in roots]  # 输入只迭代这一次
        while stack:
            path = stack.pop()
            key = str(path)
            if key in seen:
                continue
            seen.add(key)
            try:
                info = os.lstat(path)  # lstat：不跟随软链接，大小也在这里一并取到
            except Exception as exc:
                issues[key] = describe(exc)
                continue
            if stat.S_ISREG(info.st_mode):
                files[key] = info.st_size
            elif stat.S_ISDIR(info.st_mode):
                try:
                    stack.extend(path / name for name in os.listdir(path))
                except Exception as exc:
                    issues[key] = describe(exc)
            elif stat.S_ISLNK(info.st_mode):
                issues[key] = "symbolic link is not followed"
            else:
                issues[key] = "not a regular file (special file)"
        return files

    def _narrow(
        self, repeated: dict[int, list[Path]], issues: dict[str, str]
    ) -> tuple[list[tuple[int, list[Path]]], int]:
        """抽样、全量哈希两级共用一个线程池；返回（大小, 摘要都相同的路径）候选桶和 bytes_hashed。"""
        survivors: list[tuple[int, list[Path]]] = []
        hashed = 0
        in_flight = 0
        done: queue.SimpleQueue[tuple[Future[tuple[str, int]], _Batch, Path]] = queue.SimpleQueue()
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:

            def launch(stage: str, size: int, paths: list[Path]) -> None:
                nonlocal in_flight
                batch = _Batch(stage, size, left=len(paths))
                for path in paths:
                    if stage == "sample":
                        job = partial(self._sample_fingerprint, path, size)
                    else:
                        job = partial(self._full_digest, path)
                    future = pool.submit(job)
                    in_flight += 1
                    future.add_done_callback(lambda f, b=batch, p=path: done.put((f, b, p)))

            for size, paths in repeated.items():
                launch("sample", size, paths)
            while in_flight:  # 只有这个线程改 hashed、issues、桶，所以不需要锁
                future, batch, path = done.get()
                in_flight -= 1
                try:
                    digest, nread = future.result()
                except Exception as exc:
                    issues[str(path)] = describe(exc)  # 抛异常的钩子不计字节
                else:
                    hashed += nread
                    batch.buckets[digest].append(path)
                batch.left -= 1
                if batch.left:
                    continue
                for bucket in batch.buckets.values():
                    if len(bucket) < 2:
                        continue  # 唯一的摘要：不可能重复，不再读它
                    if batch.stage == "sample":
                        launch("full", batch.size, bucket)
                    else:
                        survivors.append((batch.size, bucket))
        return survivors, hashed

    def _verify(self, size: int, bucket: list[Path], issues: dict[str, str]) -> list[DuplicateGroup]:
        """把一个摘要桶按字节拆成等价类；代表是最小路径，所以结果与完成顺序无关。"""
        classes: list[list[Path]] = []
        for path in sorted(bucket, key=str):
            _place(path, classes, issues)
        groups = []
        for members in classes:
            if len(members) > 1:
                names = sorted(str(p) for p in members)
                groups.append(DuplicateGroup(names[0], tuple(names[1:]), size))
        return groups


if __name__ == "__main__":
    import sys
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, data in {"a.txt": b"same", "c.txt": b"same", "b.txt": b"other!", "d.txt": b"other!"}.items():
            (root / name).write_bytes(data)
        report = FileDeduplicator().scan([root, root / "missing.txt", *map(Path, sys.argv[1:])])
        for group in report.groups:
            print(group.canonical, "->", group.duplicates)
        print(report.issues, report.files_considered, report.bytes_hashed)
