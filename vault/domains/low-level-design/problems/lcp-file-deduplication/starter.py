"""文件去重流水线（ArchiveSweep）：把方法体补全。

公开接口与工作区里的 deduplicator.py 相同：三个冻结数据类、构造函数、`scan`，以及两个测试钩子
`_sample_fingerprint` 与 `_full_digest`。只用标准库，Python 3.11。

产品规则（逐条都有测试）：

输入与发现
 1. `scan(paths)` 的 paths 可以是只能迭代一次的可迭代对象，只迭代一次；每项是文件或目录的根路径。
 2. 目录递归遍历，不跟随软链接；路径身份是 `str(Path(path))`，同一身份只处理一次（根路径重叠也一样）。
 3. 缺失的路径、软链接（含断链与指向目录的链接）、特殊文件（管道、套接字等）、发现阶段的错误，
    各产生一条 `FileIssue`，不影响其他文件；`FileIssue.error` 必须含底层异常的消息。
 4. `files_considered` = 发现的、互不相同的普通文件数；某个文件后面的阶段失败了，也照样计入。
 5. 空输入合法，返回空报告；构造函数的 `max_workers`、`sample_size` 必须为正，否则 `ValueError`。

逐级缩小
 6. 按发现时记录的大小分组；大小唯一的文件不进入抽样与全量哈希，也不为它做任何"能否读取"的检查。
 7. 抽样：先从开头读最多 sample_size 字节，再从结尾读最多 sample_size 字节，两段不重叠、同一区域不读两次；
    返回 SHA-256 十六进制摘要和实际读到的字节数。只有大小相同且抽样摘要相同的文件才进入全量哈希。
 8. 全量哈希：流式增量计算 SHA-256，内存有界，不把整个文件读进内存；返回（摘要，读到的字节数）。
 9. 摘要相同不代表内容相同：用有界内存的逐字节比较确认；人为制造的碰撞可以让一个摘要桶里有多组内容相同的文件，
    每组各自成为一个重复组。

输出与失败
10. 每个确认的重复组：最小路径（按字符串比较）是 canonical，其余重复项升序；组按 canonical 排序，问题按 (path, error) 排序。
11. 元数据、抽样、哈希、比较的失败都被隔离；逐字节比较失败记在打不开或读不动的那个路径头上；别的重复组照常返回。
12. 同一路径的重复问题只留一条，保留最近一个必要阶段的问题。
13. `bytes_hashed` 只累加成功完成的抽样钩子与全量哈希钩子返回的字节数；抛异常的钩子记 0；逐字节比较读的不算。

并发
14. 抽样与全量哈希并发执行，同时处于活动状态的钩子不超过 `max_workers`；
    只要有至少 `max_workers` 个符合条件的钩子被阻塞，就必须能让 `max_workers` 个同时运行。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


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


class FileDeduplicator:
    def __init__(self, max_workers: int = 4, sample_size: int = 4096):
        if max_workers < 1 or sample_size < 1:
            raise ValueError("limits must be positive")
        self.max_workers = max_workers
        self.sample_size = sample_size

    def _full_digest(self, path: Path) -> tuple[str, int]:
        """返回整个文件的 SHA-256 十六进制摘要和读到的字节数。"""
        raise NotImplementedError

    def _sample_fingerprint(self, path: Path, size: int) -> tuple[str, int]:
        """返回开头加结尾（不重叠）的抽样摘要和读到的字节数。"""
        raise NotImplementedError

    def scan(self, paths: Iterable[str | Path]) -> ScanReport:
        """扫描所有根路径，返回全部重复组和问题。"""
        raise NotImplementedError
