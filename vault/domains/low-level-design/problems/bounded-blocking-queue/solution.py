"""有界阻塞队列（Bounded Blocking Queue）——一把锁、两个条件变量的经典生产者-消费者结构。

核心思路：容量是这个队列唯一的不变式，`0 <= size <= capacity` 任何时刻都成立。满则 `put`
等，空则 `take` 等，两类等待各配一个 `Condition`（共用同一把锁），才能在腾出一个位置或
放进一个元素时精确 `notify()` 该醒来的那一类线程，而不必每次都 `notify_all()` 惊动所有人。
`close()` 是一次广播式关闭：唤醒每一个正在等待的线程；此后的 `put` 一律立即失败，`take`
则继续把关闭前留下的元素放行，直到取空才失败。超时统一以异常收场，交给调用方决定重试、
丢弃还是升级，而不是悄悄吞掉一次失败的操作。`drain` 只是把 `take` 已经写好的等待谓词多
榨一次，不引入第二套等待逻辑。
"""

from __future__ import annotations

import threading
import time
from collections import deque
from typing import Generic, TypeVar

T = TypeVar("T")


class BoundedQueueError(Exception):
    """本设计全部失败路径的公共基类。"""


class QueueClosed(BoundedQueueError):
    """队列已经关闭：`put` 一律拒绝；`take`／`drain` 只在关闭且确认排空之后才抛出这个。"""


class QueueTimeout(BoundedQueueError):
    """`put`／`take`／`drain` 在调用方给定的截止时间内没能完成。"""


class BoundedBlockingQueue(Generic[T]):
    """容量固定、线程安全的队列：满则 `put` 阻塞，空则 `take` 阻塞。

    不变式：
    1. `0 <= size <= capacity`，任何时刻都成立——扩容和缩容都在同一把锁内完成。
    2. 元素不丢不重：一次成功的 `put` 恰好对应未来某一次 `take`／`drain` 取出的同一个对象。
    3. 等待永远写成 `while 谓词: cond.wait()`，绝不是 `if`——见 `_wait_for`。
    4. `close()` 之后：`put` 立刻失败；`take`／`drain` 把队列里剩下的取完，取空后也失败。
    5. 任何时刻最多持有这把锁一次；两个 `Condition` 共享同一把锁，所以判定谓词、
       修改队列、`notify` 目标类型的等待者，这三步天然发生在同一次加锁里。
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity}")
        self._capacity = capacity
        self._items: deque[T] = deque()
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)
        self._closed = False
        self._waiting_putters = 0
        self._waiting_takers = 0

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def size(self) -> int:
        """当前元素数量。永远在 `[0, capacity]` 之内。"""
        with self._lock:
            return len(self._items)

    @property
    def full(self) -> bool:
        with self._lock:
            return len(self._items) >= self._capacity

    @property
    def empty(self) -> bool:
        with self._lock:
            return not self._items

    @property
    def closed(self) -> bool:
        with self._lock:
            return self._closed

    @property
    def waiting_putters(self) -> int:
        """当前卡在 `not_full` 上的线程数——测试用它确认一个线程真的已经阻塞，而不是
        靠猜一个 `sleep` 的时长。生产环境里它也是判断要不要扩容的信号。"""
        with self._lock:
            return self._waiting_putters

    @property
    def waiting_takers(self) -> int:
        """当前卡在 `not_empty` 上的线程数，用途和 `waiting_putters` 对称。"""
        with self._lock:
            return self._waiting_takers

    def __len__(self) -> int:
        return self.size

    def put(self, item: T, timeout: float | None = None) -> None:
        """放入一个元素；满则阻塞，直到有空位、超时，或队列被关闭。

        队列已经关闭时立即失败——哪怕此刻明明有空位。关闭意味着"不再接受新工作"，
        不是"容量恢复之前继续收"，这条规则不该因为队里恰好还有空位而破例。
        """
        deadline = None if timeout is None else time.monotonic() + timeout
        with self._not_full:
            while len(self._items) >= self._capacity and not self._closed:
                self._waiting_putters += 1
                try:
                    self._wait_for(self._not_full, deadline, "put")
                finally:
                    self._waiting_putters -= 1
            if self._closed:
                raise QueueClosed("cannot put into a closed queue")
            self._items.append(item)
            self._not_empty.notify()

    def put_nowait(self, item: T) -> None:
        """`put(item, timeout=0)` 的简写：立刻成功或立刻失败，从不阻塞。"""
        self.put(item, timeout=0)

    def take(self, timeout: float | None = None) -> T:
        """取出队首元素；空则阻塞，直到有元素、超时，或队列关闭且确认排空。"""
        deadline = None if timeout is None else time.monotonic() + timeout
        with self._not_empty:
            while not self._items and not self._closed:
                self._waiting_takers += 1
                try:
                    self._wait_for(self._not_empty, deadline, "take")
                finally:
                    self._waiting_takers -= 1
            if not self._items:
                raise QueueClosed("queue is closed and drained")
            item = self._items.popleft()
            self._not_full.notify()
            return item

    def take_nowait(self) -> T:
        """`take(timeout=0)` 的简写。"""
        return self.take(timeout=0)

    def drain(self, max_items: int | None = None) -> list[T]:
        """等到至少有一个元素，再一次性取出最多 `max_items` 个（默认取走当前全部）。

        复用 `take` 已经写好的等待谓词——"空且未关闭就等"——不为了凑够 `max_items`
        而再等第二轮：叫醒之后能拿多少算多少，这正是"不碰等待逻辑"这条约束的意思。
        """
        with self._not_empty:
            while not self._items and not self._closed:
                self._waiting_takers += 1
                try:
                    self._wait_for(self._not_empty, None, "drain")
                finally:
                    self._waiting_takers -= 1
            if not self._items:
                raise QueueClosed("queue is closed and drained")
            n = len(self._items) if max_items is None else min(max_items, len(self._items))
            batch = [self._items.popleft() for _ in range(n)]
            self._not_full.notify(n)
            return batch

    def close(self) -> None:
        """关闭队列：唤醒每一个等待者。之后 `put` 立即失败；`take`／`drain` 继续放行到排空。"""
        with self._lock:
            self._closed = True
            self._not_full.notify_all()
            self._not_empty.notify_all()

    def _wait_for(self, cond: threading.Condition, deadline: float | None, op: str) -> None:
        """在给定的条件变量上等一轮；超过截止时间仍没等到就抛 `QueueTimeout`。

        `deadline` 是绝对时刻（`time.monotonic()` 的坐标系），而不是"再等多久"——
        因为一次 `wait()` 返回不代表谓词已经成立（虚假唤醒，或者被叫醒的那一刻已经被
        别的线程抢先改了状态），外层的 `while` 还会再检查一次、可能再等一轮，用剩余
        时间而不是完整的 `timeout` 重新调用，总等待时长才不会因为多次唤醒被悄悄拉长。
        """
        if deadline is None:
            cond.wait()
            return
        remaining = deadline - time.monotonic()
        if remaining <= 0 or not cond.wait(timeout=remaining):
            raise QueueTimeout(f"{op} timed out")

    def __repr__(self) -> str:
        return f"BoundedBlockingQueue(size={self.size}, capacity={self._capacity}, closed={self.closed})"


if __name__ == "__main__":
    q: BoundedBlockingQueue[int] = BoundedBlockingQueue(capacity=2)

    def producer() -> None:
        for i in range(5):
            q.put(i)
            print("put", i)
        q.close()

    def consumer() -> None:
        while True:
            try:
                print("take", q.take(timeout=1))
            except QueueClosed:
                print("consumer sees the queue closed and drained")
                return

    t1, t2 = threading.Thread(target=producer), threading.Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
