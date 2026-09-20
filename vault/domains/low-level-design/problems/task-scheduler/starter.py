"""任务调度器（Task Scheduler）——起始模板。

公开的类名、方法签名、`Enum` 和异常都和 `solution.py` 一致；把标了 `raise NotImplementedError`
的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/task-scheduler -q
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

Callback = Callable[[], None]
Clock = Callable[[], datetime]
ErrorHook = Callable[[int, BaseException], None]


class SchedulerError(Exception):
    """本设计所有失败路径的公共基类。"""


class InvalidScheduleError(SchedulerError, ValueError):
    """调度参数本身不合法。"""


class SchedulerClosedError(SchedulerError):
    """调度器已经 `shutdown`。"""


class RepeatMode(Enum):
    FIXED_RATE = "fixed_rate"
    FIXED_DELAY = "fixed_delay"


@dataclass(frozen=True, slots=True)
class _TaskMeta:
    id: int
    callback: Callback
    priority: int
    period: timedelta | None
    mode: RepeatMode | None


@dataclass(order=True, frozen=True, slots=True)
class _HeapEntry:
    due: datetime
    priority: int
    seq: int
    id: int


@dataclass(frozen=True, slots=True)
class _Job:
    id: int
    callback: Callback


class _SchedulerCore:
    """纯粹的调度逻辑：一个堆、一张任务表、一把锁。"""

    def __init__(self) -> None:
        raise NotImplementedError

    @property
    def pending_count(self) -> int:
        """还活着的任务数。"""
        raise NotImplementedError

    @property
    def heap_size(self) -> int:
        """堆的物理大小。"""
        raise NotImplementedError

    def time_until_next(self, now: datetime) -> timedelta | None:
        """离下一次可能有事情发生还有多久。"""
        raise NotImplementedError

    def schedule(self, callback: Callback, due: datetime, priority: int,
                 period: timedelta | None, mode: RepeatMode | None) -> int:
        """登记一个任务并把它第一次的到期时间压进堆。返回任务 id。"""
        raise NotImplementedError

    def cancel(self, task_id: int) -> bool:
        """取消一个任务。"""
        raise NotImplementedError

    def pop_due(self, now: datetime) -> tuple[_Job, ...]:
        """取出所有到期且仍然存活的任务。"""
        raise NotImplementedError

    def complete(self, task_id: int, finished_at: datetime) -> None:
        """一次执行真正结束之后调用；固定延迟的下一次到期在这里算。"""
        raise NotImplementedError

    def compact(self) -> None:
        """立刻把堆压缩到只剩活着的条目。"""
        raise NotImplementedError


class Scheduler:
    """调度器门面：一条调度线程只管掐点，一个工作线程池并发执行到期任务。"""

    def __init__(self, *, clock: Clock = datetime.now, workers: int = 4,
                 max_wait: timedelta = timedelta(seconds=1),
                 on_error: ErrorHook | None = None) -> None:
        raise NotImplementedError

    @property
    def pending_count(self) -> int:
        raise NotImplementedError

    @property
    def heap_size(self) -> int:
        raise NotImplementedError

    def compact(self) -> None:
        raise NotImplementedError

    def schedule_after(self, callback: Callback, delay: timedelta, *, priority: int = 0) -> int:
        """`delay` 之后运行一次。"""
        raise NotImplementedError

    def schedule_at(self, callback: Callback, at: datetime, *, priority: int = 0) -> int:
        """在给定的时刻运行一次。"""
        raise NotImplementedError

    def schedule_periodic(self, callback: Callback, period: timedelta, *,
                           mode: RepeatMode = RepeatMode.FIXED_DELAY,
                           first_due: datetime | None = None, priority: int = 0) -> int:
        """按周期重复运行。"""
        raise NotImplementedError

    def cancel(self, task_id: int) -> bool:
        """取消一个任务，返回它取消前是否还活着。"""
        raise NotImplementedError

    def run_pending(self, now: datetime) -> tuple[int, ...]:
        """同步地执行所有到期任务，返回被执行的任务 id。"""
        raise NotImplementedError

    def start(self) -> None:
        """启动调度线程和工作线程池。"""
        raise NotImplementedError

    def shutdown(self, *, drain: bool = True) -> None:
        """停止接受新的到期派发，按 drain 处理线程池里的任务。"""
        raise NotImplementedError
