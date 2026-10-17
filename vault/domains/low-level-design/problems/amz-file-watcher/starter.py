"""文件监听器练习骨架：公开 API 与 solution.py 完全一致，方法体全部待补全。
把每个 raise NotImplementedError 换成你自己的实现，然后用 IMPL=starter uv run --with pytest python -m pytest <本目录> -q 验收。
内部表示随你换，测试只通过公开方法断言。"""
from __future__ import annotations
import os
import threading
from collections import deque
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

class WatchError(Exception):
    """本模块所有异常的根。"""

class RootNotFoundError(WatchError, FileNotFoundError):
    """被监听的根目录不存在。"""

@dataclass(frozen=True, slots=True)
class Stat:
    """一个文件在某一刻的指纹。只用 mtime 会漏掉同一时间粒度内的第二次修改，所以再加 size。"""
    mtime_ns: int
    size: int
Snapshot = dict[str, Stat]

class EventKind(Enum):
    CREATED = 'created'
    MODIFIED = 'modified'
    DELETED = 'deleted'

@dataclass(frozen=True, slots=True)
class Event:
    """发生了什么：订阅者只靠它就能更新自己。"""
    kind: EventKind
    path: str

class FileSystem(Protocol):
    """监听器需要从文件系统得到的唯一能力：给我这个目录下所有文件的指纹。"""

    def scan(self, root: str, recursive: bool) -> Snapshot:
        raise NotImplementedError

class DiskFileSystem:
    """真实磁盘：os.scandir 遍历，不跟随符号链接（避免目录环），遍历中途消失的文件直接跳过。"""

    def scan(self, root: str, recursive: bool) -> Snapshot:
        raise NotImplementedError

def diff(old: Snapshot, new: Snapshot) -> list[Event]:
    """两张快照的差：新增、变化、消失。按路径排序，结果是确定的。"""
    raise NotImplementedError
Callback = Callable[[Event], None]

@dataclass(frozen=True, slots=True)
class CallbackFailure:
    """一次回调失败的记录：哪个事件、什么异常。"""
    event: Event
    error: Exception

class Watcher:
    """监听一个目录。`poll()` 推进一次；`start()` 再开一条后台线程按间隔反复调用它。"""

    def __init__(self, fs: FileSystem, root: str, *, recursive: bool=True, include: Callable[[str], bool]=lambda path: True, settle: bool=False) -> None:
        raise NotImplementedError

    def subscribe(self, callback: Callback, kinds: Iterable[EventKind] | None=None) -> Callable[[], None]:
        """登记回调；返回一个取消订阅的函数。kinds 为 None 表示三种事件都要。"""
        raise NotImplementedError

    @property
    def failures(self) -> tuple[CallbackFailure, ...]:
        raise NotImplementedError

    @property
    def running(self) -> bool:
        raise NotImplementedError

    def poll(self) -> list[Event]:
        """拍一次快照，和已提交的世界比对，把事件交给订阅者，并返回这些事件。

第一次调用只建立基线（监听开始前就存在的文件不算「新建」），返回空列表。"""
        raise NotImplementedError

    def _settled_view(self, raw: Snapshot) -> Snapshot:
        """一个路径的状态只有在连续两次轮询里相同才被采纳；否则沿用订阅者已知的旧状态。"""
        raise NotImplementedError

    def _dispatch(self, events: list[Event], targets: list[tuple[Callback, frozenset[EventKind] | None]]) -> None:
        """在锁外调用回调：回调里可以订阅、取消订阅甚至 stop() 而不死锁；一个回调出错不影响别人。"""
        raise NotImplementedError

    def start(self, interval: float) -> None:
        """开一条守护线程，每隔 interval 秒 poll() 一次；已在运行则忽略。"""
        raise NotImplementedError

    def _loop(self, interval: float) -> None:
        raise NotImplementedError

    def stop(self, timeout: float | None=5.0) -> None:
        """请求停止并等待线程退出。在回调（即轮询线程自己）里调用时不 join，否则会等自己。"""
        raise NotImplementedError
