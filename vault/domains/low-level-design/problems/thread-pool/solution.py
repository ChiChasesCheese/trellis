"""线程池（Thread Pool）——固定数量的工作线程、按优先级出队的任务队列、Future 结果。

核心思路：任务队列内部永远不设容量上限（`queue.PriorityQueue()` 默认无界），背压不是
让队列本身在满时挡住调用方，而是在 `submit()` 前面包一个信号量——这样关闭线程池时往
队列里投递"停止"哨兵永远不会被队列已满卡住，背压和关闭这两件事天然不会互相干扰。每个
任务带一个优先级和一个只增的序号，数值小的优先级先出队，同优先级之间按提交顺序——这
正是第 4 关"加优先级不碰 worker 循环"的答案：优先级从第一天就是队列条目的一部分，第 4
关只是把它从内部默认值开放成 `submit()` 的一个可选参数。工作线程捕获任务体抛出的一切
异常并封进对应的 `Future`，绝不因为一个任务出错就退出。
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

    不变式：只经历"未完成 → 完成"一次性的状态迁移，之后永远保持完成；每个回调只被
    调用一次；"判断是否已完成"和"取出回调列表并清空它"必须是同一次加锁下的原子操作，
    否则一次 `add_done_callback` 可能插在两步中间，被静静地漏掉。
    """

    def __init__(self) -> None:
        self._done = threading.Event()
        self._lock = threading.Lock()
        self._result: R | None = None
        self._exception: BaseException | None = None
        self._callbacks: list[Callable[[Future[R]], None]] = []

    def done(self) -> bool:
        return self._done.is_set()

    def result(self, timeout: float | None = None) -> R:
        """阻塞到任务完成并返回结果；任务里抛出的异常会在这里原样重新抛出。"""
        if not self._done.wait(timeout):
            raise FutureTimeout("result not available within timeout")
        if self._exception is not None:
            raise self._exception
        return self._result  # type: ignore[return-value]

    def exception(self, timeout: float | None = None) -> BaseException | None:
        """阻塞到任务完成，返回任务抛出的异常，没有异常则返回 `None`。"""
        if not self._done.wait(timeout):
            raise FutureTimeout("result not available within timeout")
        return self._exception

    def add_done_callback(self, callback: Callable[[Future[R]], None]) -> None:
        """注册完成后要执行的回调；如果调用这个方法时已经完成，立刻在调用者的线程里执行。"""
        with self._lock:
            if not self._done.is_set():
                self._callbacks.append(callback)
                return
        callback(self)

    def _set_result(self, value: R) -> None:
        self._result = value
        self._finish()

    def _set_exception(self, exc: BaseException) -> None:
        self._exception = exc
        self._finish()

    def _finish(self) -> None:
        with self._lock:
            self._done.set()
            callbacks, self._callbacks = self._callbacks, []
        for callback in callbacks:
            callback(self)


@dataclass(order=True)
class _QueuedTask:
    """队列里的一条记录：排序只看优先级和提交序号，任务本体和 `Future` 不参与比较——
    两个任务的 `fn` 之间没有大小关系，让它们参与比较只会在同优先级时抛 `TypeError`。"""

    priority: float
    sequence: int
    fn: Callable[..., Any] = field(compare=False)
    args: tuple[Any, ...] = field(compare=False)
    kwargs: dict[str, Any] = field(compare=False)
    future: Future[Any] = field(compare=False)
    is_sentinel: bool = field(default=False, compare=False)


class ThreadPool:
    """固定数量的工作线程从一个共享队列里取任务执行。

    不变式：
    1. 同时运行的任务数不超过工作线程数——线程数量在构造时固定。
    2. 一个任务抛出的异常只终结这一个任务（封进它的 `Future`），绝不终结工作线程。
    3. `shutdown(wait=True)` 返回时，此前提交的每一个任务都已经跑完；
       `shutdown(wait=False)` 立即返回，之后一切还没被工作线程取走的任务被放弃执行，
       它们的 `Future` 收到 `PoolShutdown`；正在执行的任务不受影响，会跑完。
    4. `shutdown()` 之后的 `submit()` 一律拒绝。
    """

    def __init__(self, num_workers: int, queue_capacity: int | None = None) -> None:
        if num_workers <= 0:
            raise ValueError(f"num_workers must be positive, got {num_workers}")
        if queue_capacity is not None and queue_capacity <= 0:
            raise ValueError(f"queue_capacity must be positive, got {queue_capacity}")
        self._queue: queue.PriorityQueue[_QueuedTask] = queue.PriorityQueue()
        self._admission = threading.Semaphore(queue_capacity) if queue_capacity else None
        self._sequence = itertools.count()
        self._lock = threading.Lock()
        self._shutdown_requested = False
        self._waiting_submitters = 0
        self._workers = [threading.Thread(target=self._worker_loop, daemon=True)
                          for _ in range(num_workers)]
        for worker in self._workers:
            worker.start()

    @property
    def size(self) -> int:
        return len(self._workers)

    @property
    def is_shutdown(self) -> bool:
        with self._lock:
            return self._shutdown_requested

    @property
    def pending(self) -> int:
        """队列里还没被取走的任务数，近似值——标准库 `qsize()` 本身就不承诺精确。"""
        return self._queue.qsize()

    @property
    def waiting_submitters(self) -> int:
        """当前卡在背压信号量上的调用者数——测试用它确认一次 `submit()` 真的被队满挡住
        了，而不是靠猜一个 `sleep` 的时长。"""
        with self._lock:
            return self._waiting_submitters

    def submit(self, fn: Callable[..., R], *args: Any,
               priority: float = 0.0, **kwargs: Any) -> Future[R]:
        """提交一个任务，返回它的 `Future`。`priority` 越小越先执行，同优先级先进先出。

        队列本身永远不设容量上限；`queue_capacity` 的背压由 `submit()` 前面的一个
        信号量实现——满了就挡住调用方，绝不是悄悄丢弃或者让队列本身涨到失控。
        """
        if self._admission is not None:
            with self._lock:
                self._waiting_submitters += 1
            try:
                self._admission.acquire()
            finally:
                with self._lock:
                    self._waiting_submitters -= 1
        with self._lock:
            if self._shutdown_requested:
                if self._admission is not None:
                    self._admission.release()
                raise PoolShutdown("cannot submit after shutdown")
            future: Future[R] = Future()
            task = _QueuedTask(priority, next(self._sequence), fn, args, kwargs, future)
            self._queue.put(task)
        return future

    def shutdown(self, wait: bool = True) -> None:
        """关闭线程池。`wait=True` 等所有已提交任务跑完；`wait=False` 立即返回，放弃
        队列里还没被取走的任务。两种情况下之后的 `submit()` 都会被拒绝。"""
        with self._lock:
            if self._shutdown_requested:
                return
            self._shutdown_requested = True
            abandoned = [] if wait else self._drain_pending()
        for task in abandoned:
            task.future._set_exception(PoolShutdown("task abandoned: pool is shutting down"))
        for _ in self._workers:
            sentinel = _QueuedTask(math.inf, next(self._sequence), _noop, (), {}, Future(), True)
            self._queue.put(sentinel)
        if wait:
            for worker in self._workers:
                worker.join()

    def __enter__(self) -> ThreadPool:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.shutdown(wait=True)

    def _drain_pending(self) -> list[_QueuedTask]:
        """必须在持有 `_lock` 时调用：清空当前队列，返回被放弃的任务。"""
        drained: list[_QueuedTask] = []
        while True:
            try:
                task = self._queue.get_nowait()
            except queue.Empty:
                break
            if self._admission is not None:
                self._admission.release()
            drained.append(task)
        return drained

    def _worker_loop(self) -> None:
        while True:
            task = self._queue.get()
            if task.is_sentinel:
                return
            if self._admission is not None:
                self._admission.release()
            self._run(task)

    def _run(self, task: _QueuedTask) -> None:
        try:
            result = task.fn(*task.args, **task.kwargs)
        except BaseException as exc:          # 任务体抛什么都不许杀死工作线程
            task.future._set_exception(exc)
        else:
            task.future._set_result(result)


def _noop() -> None:
    """哨兵任务占位用的空函数；`_worker_loop` 在调用它之前就已经按 `is_sentinel` 返回。"""
    return None


if __name__ == "__main__":
    with ThreadPool(num_workers=4) as pool:
        futures = [pool.submit(lambda x: x * x, i) for i in range(8)]
        print([f.result() for f in futures])

        def boom() -> None:
            raise RuntimeError("任务自己的问题，不该拖累整个池子")

        failing = pool.submit(boom)
        try:
            failing.result()
        except RuntimeError as exc:
            print("任务失败，工作线程活得好好的:", exc)
