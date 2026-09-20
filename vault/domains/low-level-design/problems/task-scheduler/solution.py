"""任务调度器（Task Scheduler）——进程内的延时/周期任务调度，不是分布式任务队列。

五行设计：`_SchedulerCore` 是一个纯粹的堆（按到期时间排序），一把锁保护它，时间只从**注入的
时钟**来，所以调度逻辑可以在没有任何真实线程、任何真实 sleep 的情况下用 `run_pending(now)`
驱动，被单元测试逐步推进；`Scheduler` 在它之上叠一条只管掐点的调度线程和一个并发执行到期
任务的工作线程池，二者用 `threading.Condition` 联系。固定速率与固定延迟的区别只在"下一次
到期时间什么时候被算出来"：前者在取出时立刻算（`due + period`，与实际跑多久无关，落后了会
连续追赶），后者在任务跑完之后才算（`完成时刻 + period`，永远不会追赶）。取消是一枚**墓碑**
——任务表里的条目被立刻删掉，堆里的过期指针留到被取出或被压缩时才真正消失，因此"还没轮到"
的取消不会让堆无限增长。
"""

from __future__ import annotations

import heapq
import itertools
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

Callback = Callable[[], None]
Clock = Callable[[], datetime]
ErrorHook = Callable[[int, BaseException], None]

_COMPACT_FLOOR = 64
"""堆至少攒到这么多条目才值得整理一次，避免任务很少时反复空扫。"""


# --------------------------------------------------------------------------
# 失败路径。


class SchedulerError(Exception):
    """本设计所有失败路径的公共基类。"""


class InvalidScheduleError(SchedulerError, ValueError):
    """调度参数本身不合法：负的延时、非正的周期、既没给 delay 也没给 at（或者两个都给了）。"""


class SchedulerClosedError(SchedulerError):
    """调度器已经 `shutdown`，不再接受新的调度请求。"""


class RepeatMode(Enum):
    """周期任务的两种语义，差别只在"下一次到期时间从哪算起"。"""

    FIXED_RATE = "fixed_rate"
    FIXED_DELAY = "fixed_delay"


@dataclass(frozen=True, slots=True)
class _TaskMeta:
    """一个任务的静态信息。它在任务表里"存在"这件事本身就是"这个任务还活着"的唯一判据。"""

    id: int
    callback: Callback
    priority: int
    period: timedelta | None
    mode: RepeatMode | None


@dataclass(order=True, frozen=True, slots=True)
class _HeapEntry:
    """堆里的一个位置。字段声明的顺序就是比较顺序：到期时间 → 优先级 → 到达序号 → id。

    优先级从第 1 关的签名起就存在，但语义直到"同一时刻的优先级"这个扩展点才第一次被用到——
    这正是"扩展不改堆"的证据：多出来的能力只是元组多了一栏，`heapq` 的比较自动生效。
    """

    due: datetime
    priority: int
    seq: int
    id: int


@dataclass(frozen=True, slots=True)
class _Job:
    """一次可执行的派发：任务 id 加它的回调。到期之后，堆条目就被换成了这个。"""

    id: int
    callback: Callback


class _SchedulerCore:
    """纯粹的调度逻辑：一个堆、一张任务表、一把锁。不碰线程，只认注入的时间。

    这是"可以不靠真实睡眠测试"的全部机密：`pop_due(now)` 和 `complete(id, now)` 都是普通
    方法调用，测试想推进多快就推进多快。`Scheduler` 的调度线程只是循环调用这两个方法。
    """

    def __init__(self) -> None:
        self._heap: list[_HeapEntry] = []
        self._tasks: dict[int, _TaskMeta] = {}
        self._lock = threading.Lock()
        self._ids = itertools.count(1)
        self._seq = itertools.count(1)
        self._dead_since_compact = 0

    @property
    def pending_count(self) -> int:
        """还活着的任务数——取消或一次性任务跑完之后立刻变小。"""
        with self._lock:
            return len(self._tasks)

    @property
    def heap_size(self) -> int:
        """堆的物理大小，可能比 `pending_count` 大——多出来的是还没被清理的墓碑。"""
        with self._lock:
            return len(self._heap)

    def time_until_next(self, now: datetime) -> timedelta | None:
        """离下一次可能有事情发生还有多久；堆是空的就返回 `None`（无限久）。"""
        with self._lock:
            if not self._heap:
                return None
            return self._heap[0].due - now

    def schedule(self, callback: Callback, due: datetime, priority: int,
                 period: timedelta | None, mode: RepeatMode | None) -> int:
        """登记一个任务（一次性或周期性）并把它第一次的到期时间压进堆。返回任务 id。"""
        with self._lock:
            task_id = next(self._ids)
            self._tasks[task_id] = _TaskMeta(task_id, callback, priority, period, mode)
            self._push_locked(task_id, due)
            return task_id

    def cancel(self, task_id: int) -> bool:
        """取消一个任务。返回它取消前是否还活着——已经跑完或已经取消过都返回 `False`。

        堆里那个位置留成了一枚墓碑：任务表里的条目立刻消失（`pending_count` 立刻变小），
        堆本身按"取消次数"计数，攒够 `_COMPACT_FLOOR` 次就整理一遍——这个门槛只认取消的
        **次数**，不看堆此刻有多大，所以连续取消一百万个还没轮到的任务，堆不会陪着攒到
        一百万：每 `_COMPACT_FLOOR` 次就被压回只剩活着的那些。
        """
        with self._lock:
            if task_id not in self._tasks:
                return False
            del self._tasks[task_id]
            self._dead_since_compact += 1
            if self._dead_since_compact >= _COMPACT_FLOOR:
                self._compact_locked()
            return True

    def pop_due(self, now: datetime) -> tuple[_Job, ...]:
        """取出所有到期（`due <= now`）且仍然存活的任务，返回可执行的派发。

        固定速率在这里立刻算下一次到期——与这次到底跑了多久无关，所以如果一次批量取出
        涵盖了不止一个周期，它会在同一次调用里再次被取出、再次派发：这就是"追赶"。
        固定延迟不在这里重新入堆，要等 `complete` 用实际完成时刻来算。
        """
        with self._lock:
            jobs: list[_Job] = []
            while self._heap and self._heap[0].due <= now:
                entry = heapq.heappop(self._heap)
                meta = self._tasks.get(entry.id)
                if meta is None:
                    continue  # 墓碑：被取消了，或者是一次性任务留下的空指针
                if meta.mode is RepeatMode.FIXED_RATE:
                    self._push_locked(entry.id, entry.due + meta.period)  # type: ignore[arg-type]
                elif meta.mode is None:
                    del self._tasks[entry.id]  # 一次性任务：派发即终结
                jobs.append(_Job(entry.id, meta.callback))
            return tuple(jobs)

    def complete(self, task_id: int, finished_at: datetime) -> None:
        """一次执行**真正结束**之后调用。固定延迟的下一次到期在这里、以这一刻为起点算出。

        任务在执行期间被取消，或者根本不是固定延迟，这里什么都不做——调用方总是可以无条件
        调用它（`finally` 里），不需要先判断任务是什么类型。
        """
        with self._lock:
            meta = self._tasks.get(task_id)
            if meta is not None and meta.mode is RepeatMode.FIXED_DELAY:
                self._push_locked(task_id, finished_at + meta.period)  # type: ignore[arg-type]

    def compact(self) -> None:
        """立刻把堆压缩到只剩活着的条目。测试和运维都可以随时调用；正常运行不必手动调。"""
        with self._lock:
            self._compact_locked()

    def _push_locked(self, task_id: int, due: datetime) -> None:
        meta = self._tasks[task_id]
        heapq.heappush(self._heap, _HeapEntry(due, meta.priority, next(self._seq), task_id))

    def _compact_locked(self) -> None:
        self._heap = [entry for entry in self._heap if entry.id in self._tasks]
        heapq.heapify(self._heap)
        self._dead_since_compact = 0


class Scheduler:
    """调度器门面：一条调度线程只管掐点，一个工作线程池并发执行到期任务。

    不变量：一个任务不会在它的到期时间**之前**运行（`pop_due` 只认 `due <= now`）；一个任务
    抛出的异常不会杀死调度线程或线程池，也不会取消它自己未来的调度（`_run_job` 兜底并且总是
    调用 `complete`）。busy 的进程只保证"不早于"，从不保证"恰好在"——固定速率任务如果连续
    落后，会在下一次真正被看到时**连续追赶**，而不是被悄悄跳过或无限期推迟。
    """

    def __init__(self, *, clock: Clock = datetime.now, workers: int = 4,
                 max_wait: timedelta = timedelta(seconds=1),
                 on_error: ErrorHook | None = None) -> None:
        if workers <= 0:
            raise InvalidScheduleError(f"workers must be positive, got {workers}")
        self._core = _SchedulerCore()
        self._clock = clock
        self._max_wait = max_wait
        self._on_error = on_error or (lambda task_id, exc: None)
        self._workers = workers
        self._cv = threading.Condition()
        self._closed = False
        self._thread: threading.Thread | None = None
        self._pool: ThreadPoolExecutor | None = None

    @property
    def pending_count(self) -> int:
        """还活着（会在未来某一刻被执行）的任务数。"""
        return self._core.pending_count

    @property
    def heap_size(self) -> int:
        """堆的物理大小——包含还没被清理的取消墓碑。"""
        return self._core.heap_size

    def compact(self) -> None:
        """立刻清掉堆里的取消墓碑。"""
        self._core.compact()

    def schedule_after(self, callback: Callback, delay: timedelta, *, priority: int = 0) -> int:
        """`delay` 之后运行一次。"""
        if delay < timedelta(0):
            raise InvalidScheduleError(f"delay must not be negative, got {delay}")
        return self._schedule_once(callback, self._clock() + delay, priority)

    def schedule_at(self, callback: Callback, at: datetime, *, priority: int = 0) -> int:
        """在给定的时刻运行一次；`at` 早于现在也接受——意味着"尽快运行一次"。"""
        return self._schedule_once(callback, at, priority)

    def schedule_periodic(self, callback: Callback, period: timedelta, *,
                           mode: RepeatMode = RepeatMode.FIXED_DELAY,
                           first_due: datetime | None = None, priority: int = 0) -> int:
        """按周期重复运行；`first_due` 缺省时第一次在一个周期之后运行。"""
        self._check_open()
        if period <= timedelta(0):
            raise InvalidScheduleError(f"period must be positive, got {period}")
        due = first_due if first_due is not None else self._clock() + period
        task_id = self._core.schedule(callback, due, priority, period, mode)
        self._wake()
        return task_id

    def cancel(self, task_id: int) -> bool:
        """取消一个任务，返回它取消前是否还活着。对已经跑完/取消过的 id 调用是安全的。"""
        return self._core.cancel(task_id)

    def run_pending(self, now: datetime) -> tuple[int, ...]:
        """同步地、在调用者的线程里执行所有到期任务，返回被执行的任务 id。

        不涉及调度线程也不涉及工作线程池——这是让调度逻辑不需要真实 sleep 就能被测试的
        入口，`Scheduler` 自己的调度线程只是在真实时间上反复调用这同一条路径（经工作线程池）。
        """
        ran: list[int] = []
        for job in self._core.pop_due(now):
            self._run_job(job, now)
            ran.append(job.id)
        return tuple(ran)

    def start(self) -> None:
        """启动调度线程和工作线程池。只能调用一次。"""
        if self._thread is not None:
            raise SchedulerError("scheduler already started")
        self._pool = ThreadPoolExecutor(max_workers=self._workers, thread_name_prefix="task-scheduler")
        self._thread = threading.Thread(target=self._loop, name="task-scheduler-loop", daemon=True)
        self._thread.start()

    def shutdown(self, *, drain: bool = True) -> None:
        """停止接受新的到期派发。`drain=True`（默认）等已经派给线程池的任务跑完；
        `drain=False` 不等待，还没开始跑的任务被直接丢弃，正在跑的不会被打断。
        """
        with self._cv:
            self._closed = True
            self._cv.notify_all()
        if self._thread is not None:
            self._thread.join()
        if self._pool is not None:
            self._pool.shutdown(wait=drain, cancel_futures=not drain)

    def _schedule_once(self, callback: Callback, due: datetime, priority: int) -> int:
        self._check_open()
        task_id = self._core.schedule(callback, due, priority, None, None)
        self._wake()
        return task_id

    def _check_open(self) -> None:
        if self._closed:
            raise SchedulerClosedError("scheduler is shut down")

    def _wake(self) -> None:
        """新任务可能比堆里现有的都早到期，叫醒调度线程重新算一次该睡多久。"""
        with self._cv:
            self._cv.notify_all()

    def _run_job(self, job: _Job, finished_hint: datetime | None = None) -> None:
        """执行一个到期任务；异常在这里被拦下，绝不传到调度线程或线程池之外。"""
        try:
            job.callback()
        except BaseException as exc:  # noqa: BLE001 - 一个任务的 bug 不能拖垮别的任务
            self._on_error(job.id, exc)
        finally:
            self._core.complete(job.id, finished_hint if finished_hint is not None else self._clock())

    def _loop(self) -> None:
        """调度线程：只负责"现在该看一眼堆了吗"，真正执行的活全部丢给线程池。"""
        while True:
            with self._cv:
                if self._closed:
                    return
                wait = self._core.time_until_next(self._clock())
                timeout = self._max_wait.total_seconds() if wait is None else \
                    max(0.0, min(wait.total_seconds(), self._max_wait.total_seconds()))
                if timeout > 0:
                    self._cv.wait(timeout=timeout)
                    continue
            now = self._clock()
            for job in self._core.pop_due(now):
                assert self._pool is not None
                self._pool.submit(self._run_job, job)


if __name__ == "__main__":
    from datetime import UTC

    clock_box = [datetime(2026, 1, 1, tzinfo=UTC)]
    scheduler = Scheduler(clock=lambda: clock_box[0])

    log: list[str] = []
    scheduler.schedule_after(lambda: log.append("once"), timedelta(seconds=5))
    tick_id = scheduler.schedule_periodic(
        lambda: log.append("tick"), timedelta(seconds=10), mode=RepeatMode.FIXED_RATE)

    clock_box[0] += timedelta(seconds=5)
    print("t+5s ran:", scheduler.run_pending(clock_box[0]), log)
    clock_box[0] += timedelta(seconds=25)  # 落后两个多周期
    print("t+30s ran:", scheduler.run_pending(clock_box[0]), log, "(固定速率追赶)")

    scheduler.cancel(tick_id)
    print("pending after cancel:", scheduler.pending_count, "heap:", scheduler.heap_size)
