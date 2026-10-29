---
id: uth-compose-ring-buffer-1-spec
node: compose.ring-buffer
type: qa
step: 1
---
## Q
**有界队列要同时做到什么**｜Disruptor · 4.0.0

线程之间传消息：生产者往里放，消费者往外取，缓冲区大小固定。要支持哪些操作？为什么 `list.pop(0)` 和链表都不够好？

## A
**背景。** 缓冲区要支持：

| 操作 | 要求 |
|---|---|
| `offer` 入队 | O(1)，满了立刻返回失败 |
| `poll` 出队 | O(1)，空了立刻返回失败 |
| 判空、判满 | O(1)，不能把空和满混淆 |
| 内存 | 启动时一次分配，运行中不再分配 |

三种直接的做法各差一点：

- 数组，出队后后面的元素整体前移：出队 O(n)
- 链表：出队 O(1)，但每个元素一个节点（`LinkedBlockingQueue` 每次入队都 `new Node`），要分配、要垃圾回收
- 数组，队首、队尾下标只往后走：前面空出来的格子再也用不上

把数组首尾相接成一个环，下标走到末尾就绕回 0，格子就能循环使用。剩下的难点是：队首下标等于队尾下标时，是空还是满？

**例题：** LC 622 设计循环队列

设计循环队列 `MyCircularQueue(k)`：`enQueue(value)` 入队（满则返回 `False`），`deQueue()` 出队（空则返回 `False`），`Front()`、`Rear()` 取队首、队尾（空返回 `-1`），`isEmpty()`、`isFull()`；不能用内置的队列。例：容量 3，入队 1、2、3 都成功，再入队 4 返回 `False`，`Rear()` → `3`，`isFull()` → `True`。

```python
class MyCircularQueue:
    def __init__(self, k: int) -> None:
        self.buf = [0] * k
        self.cap = k
        self.head = 0                           # 队首下标
        self.size = 0                           # 元素个数：用 size 区分空和满，不浪费一格

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.buf[(self.head + self.size) % self.cap] = value
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.buf[self.head]

    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.buf[(self.head + self.size - 1) % self.cap]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.cap
```
