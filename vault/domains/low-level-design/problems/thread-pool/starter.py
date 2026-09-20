"""线程池（Thread Pool）——起始模板。

公开的类名、方法签名、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的地方一个个填上，就是一份完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/thread-pool -q
"""

from __future__ import annotations

import itertools
import math
import queue
import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, TypeVar

R = TypeVar("R")


class ThreadPoolError(Exception):
    """本设计全部失败路径的公共基类。"""


class PoolShutdown(ThreadPoolError):
    """线程池已经（或正在）关闭：拒绝新提交，或者一个还没被取走的任务被放弃执行。"""


class FutureTimeout(ThreadPoolError):
    """`Future.result()`／`Future.exception()` 在给定的超时内仍未完成。"""


class Future(Generic[R]):
    """一次异步调用的句柄：携带最终的结果或者异常，可以查询、等待、注册完成回调。

    要补全的不变式：只经历"未完成 → 完成"一次性的状态迁移；每个回调只被调用一次；
    "判断是否已完成"和"取出回调列表并清空它"必须是同一次加锁下的原子操作。
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def done(self) -> bool:
        raise NotImplementedError

    def result(self, timeout: float | None = None) -> R:
        """阻塞到任务完成并返回结果；任务里抛出的异常会在这里原样重新抛出。"""
        raise NotImplementedError

    def exception(self, timeout: float | None = None) -> BaseException | None:
        """阻塞到任务完成，返回任务抛出的异常，没有异常则返回 `None`。"""
        raise NotImplementedError

    def add_done_callback(self, callback: Callable[[Future[R]], None]) -> None:
        """注册完成后要执行的回调；如果调用这个方法时已经完成，立刻在调用者的线程里执行。"""
        raise NotImplementedError

    def _set_result(self, value: R) -> None:
        raise NotImplementedError

    def _set_exception(self, exc: BaseException) -> None:
        raise NotImplementedError


@dataclass(order=True)
class _QueuedTask:
    """队列里的一条记录：排序只看优先级和提交序号，任务本体和 `Future` 不参与比较。"""

    priority: float
    sequence: int
    fn: Callable[..., Any] = field(compare=False)
    args: tuple[Any, ...] = field(compare=False)
    kwargs: dict[str, Any] = field(compare=False)
    future: Future[Any] = field(compare=False)
    is_sentinel: bool = field(default=False, compare=False)


class ThreadPool:
    """固定数量的工作线程从一个共享队列里取任务执行。

    要补全的不变式：同时运行的任务数不超过工作线程数；一个任务抛出的异常只终结这一个
    任务，绝不终结工作线程；`shutdown(wait=True)` 等全部任务跑完，`shutdown(wait=False)`
    放弃还没被取走的任务；`shutdown()` 之后的 `submit()` 一律拒绝。
    """

    def __init__(self, num_workers: int, queue_capacity: int | None = None) -> None:
        raise NotImplementedError

    @property
    def size(self) -> int:
        raise NotImplementedError

    @property
    def is_shutdown(self) -> bool:
        raise NotImplementedError

    @property
    def pending(self) -> int:
        """队列里还没被取走的任务数，近似值。"""
        raise NotImplementedError

    @property
    def waiting_submitters(self) -> int:
        """当前卡在背压信号量上的调用者数，测试用它确认一次 `submit()` 真的被队满挡住了。"""
        raise NotImplementedError

    def submit(self, fn: Callable[..., R], *args: Any,
               priority: float = 0.0, **kwargs: Any) -> Future[R]:
        """提交一个任务，返回它的 `Future`。`priority` 越小越先执行，同优先级先进先出。"""
        raise NotImplementedError

    def shutdown(self, wait: bool = True) -> None:
        """关闭线程池。`wait=True` 等所有已提交任务跑完；`wait=False` 立即返回，放弃
        队列里还没被取走的任务。"""
        raise NotImplementedError

    def __enter__(self) -> ThreadPool:
        raise NotImplementedError

    def __exit__(self, *exc_info: object) -> None:
        raise NotImplementedError


if __name__ == "__main__":
    with ThreadPool(num_workers=4) as pool:
        print(pool.submit(lambda x: x * x, 5).result())
