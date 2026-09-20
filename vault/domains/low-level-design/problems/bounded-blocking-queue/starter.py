"""有界阻塞队列（Bounded Blocking Queue）——起始模板。

公开的类名、方法签名和异常都和 `solution.py` 一致；把标了 `raise NotImplementedError`
的地方一个个填上，就是一份完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/bounded-blocking-queue -q
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

    要补全的不变式：`0 <= size <= capacity`；元素不丢不重；等待永远写成
    `while 谓词: cond.wait()`；`close()` 之后 `put` 立刻失败，`take`／`drain` 把剩下的
    取完才失败；任何时刻最多持有这把锁一次。
    """

    def __init__(self, capacity: int) -> None:
        raise NotImplementedError

    @property
    def capacity(self) -> int:
        raise NotImplementedError

    @property
    def size(self) -> int:
        """当前元素数量。永远在 `[0, capacity]` 之内。"""
        raise NotImplementedError

    @property
    def full(self) -> bool:
        raise NotImplementedError

    @property
    def empty(self) -> bool:
        raise NotImplementedError

    @property
    def closed(self) -> bool:
        raise NotImplementedError

    @property
    def waiting_putters(self) -> int:
        """当前卡在"非满"条件上的线程数——测试用它确认一个线程真的已经阻塞。"""
        raise NotImplementedError

    @property
    def waiting_takers(self) -> int:
        """当前卡在"非空"条件上的线程数，用途和 `waiting_putters` 对称。"""
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def put(self, item: T, timeout: float | None = None) -> None:
        """放入一个元素；满则阻塞，直到有空位、超时，或队列被关闭。

        队列已经关闭时立即失败——哪怕此刻明明有空位。
        """
        raise NotImplementedError

    def put_nowait(self, item: T) -> None:
        """`put(item, timeout=0)` 的简写：立刻成功或立刻失败，从不阻塞。"""
        raise NotImplementedError

    def take(self, timeout: float | None = None) -> T:
        """取出队首元素；空则阻塞，直到有元素、超时，或队列关闭且确认排空。"""
        raise NotImplementedError

    def take_nowait(self) -> T:
        """`take(timeout=0)` 的简写。"""
        raise NotImplementedError

    def drain(self, max_items: int | None = None) -> list[T]:
        """等到至少有一个元素，再一次性取出最多 `max_items` 个（默认取走当前全部）。

        复用 `take` 已经写好的等待谓词，不为凑够 `max_items` 而再等第二轮。
        """
        raise NotImplementedError

    def close(self) -> None:
        """关闭队列：唤醒每一个等待者。之后 `put` 立即失败；`take`／`drain` 继续放行到排空。"""
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


if __name__ == "__main__":
    q: BoundedBlockingQueue[int] = BoundedBlockingQueue(capacity=2)
    q.put(1)
    print(q.take())
