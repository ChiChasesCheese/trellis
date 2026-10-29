---
id: uth-compose-indexed-heap-1-needs
node: compose.indexed-heap
type: qa
step: 1
---
## Q
**堆为什么删不了中间的元素**｜Java ScheduledThreadPoolExecutor · JDK 21

定时任务调度器要「取最早到期的任务」，还要能取消、改期。普通堆为什么做不到，缺的是什么？

## A
**背景。** 堆（heap）是用数组存的二叉树，每个父节点都不比孩子大，所以最小的永远在堆顶（数组第 0 格）。加入元素：放到末尾，沿父节点往上换（上浮）；取走堆顶：把末尾元素放到堆顶，往下换（下沉）。两者都只走一条路径，O(log n)。调度器的需求：

| 操作 | 要求 |
|---|---|
| 加入任务（到期时刻 t） | O(log n) |
| 取最早到期的任务 | O(log n) |
| 取消某个任务 | O(log n) |
| 改期 | O(log n) |

**为什么。** 堆只保证「父 ≤ 子」，兄弟之间无序，没人告诉你任务 X 在数组第几格，找它得扫一遍，O(n)。有序数组好找，但插入要搬一半元素，也是 O(n)。哈希表能秒找到 X，却取不出最小。要同时做到「按名字找位置」和「按到期时刻取最小」。

**例题：** 手写最小堆（上浮、下沉）

不用 `heapq`，用列表实现最小堆 `MinHeap`：`push`、`pop`（返回并删除最小值）、`peek`、`__len__`，以及线性建堆 `heapify`；`push` / `pop` 要 O(log n)，建堆要 O(n)。例：`[5, 3, 8, 1, 9, 2]` 建堆后内部数组是 `[1, 3, 2, 5, 9, 8]`，连续 `pop` 得到 1, 2, 3, 5, 8, 9。

```python
from collections.abc import Iterable


class MinHeap[T]:
    """数组存完全二叉树：下标 i 的父节点是 (i - 1) // 2，子节点是 2i + 1、2i + 2。元素需支持 <。"""

    def __init__(self, items: Iterable[T] = ()) -> None:
        self.a: list[T] = []
        self.heapify(items)

    def __len__(self) -> int:
        return len(self.a)

    def peek(self) -> T:
        if not self.a:
            raise IndexError("peek from empty heap")
        return self.a[0]

    def push(self, x: T) -> None:
        self.a.append(x)
        self._sift_up(len(self.a) - 1)

    def pop(self) -> T:
        if not self.a:
            raise IndexError("pop from empty heap")
        last = self.a.pop()                  # 先取走最后一个元素，数组保持连续
        if not self.a:
            return last
        top, self.a[0] = self.a[0], last     # 把它放到根，再下沉
        self._sift_down(0)
        return top

    def heapify(self, items: Iterable[T]) -> None:
        self.a = list(items)
        for i in range(len(self.a) // 2 - 1, -1, -1):   # 从最后一个非叶子节点倒着下沉：O(n)
            self._sift_down(i)

    def _sift_up(self, i: int) -> None:
        a, x = self.a, self.a[i]
        while i > 0:
            parent = (i - 1) // 2
            if not x < a[parent]:            # 只用 <，和 heapq 一致
                break
            a[i] = a[parent]                 # 父节点下移，留一个“空位”，不做交换
            i = parent
        a[i] = x

    def _sift_down(self, i: int) -> None:
        a, n, x = self.a, len(self.a), self.a[i]
        while (child := 2 * i + 1) < n:
            if child + 1 < n and a[child + 1] < a[child]:
                child += 1                   # 取较小的孩子
            if not a[child] < x:
                break
            a[i] = a[child]                  # 较小的孩子上移
            i = child
        a[i] = x
```
