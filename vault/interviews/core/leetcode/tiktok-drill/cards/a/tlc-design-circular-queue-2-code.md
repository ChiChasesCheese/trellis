---
id: tlc-design-circular-queue-2-code
node: a.design-circular-queue
type: qa
step: 2
---
## Q
**LC 622 设计循环队列**｜写出 Python 实现

写类 `MyCircularQueue(k)`，容量 `k`：`enQueue(value)` 成功返回 `True`、队满返回 `False`；`deQueue()` 成功返回 `True`、队空返回 `False`；`Front()`、`Rear()` 空时返回 `-1`；`isEmpty()`、`isFull()`。值在 `0` 到 `1000`，操作数在 `1` 到 `1000`，不要使用内置的队列库，每个操作 `O(1)`。

## A
**思路。** 长度 `k` 的数组 `buf`、队首下标 `head`、元素个数 `size`。入队写在 `(head + size) % k`，出队让 `head` 前进一格，队尾元素在 `(head + size - 1) % k`。

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

运行：容量 `3`：`enQueue(1)`、`enQueue(2)`、`enQueue(3)`、`enQueue(4)`、`Rear()`、`isFull()`、`deQueue()`、`enQueue(4)`、`Rear()`、`Front()` → `[True, True, True, False, 3, True, True, True, 4, 2]`；空队列的 `Front()`、`Rear()` → `-1`；容量 `1`：`enQueue(7)` 为 `True`，`enQueue(8)` 为 `False`，`deQueue()` 之后 `enQueue(8)` 为 `True`。

**复杂度。** 每个操作 `O(1)`，空间 `O(k)`。

**写法要点。**
- 用 `size` 代替 `tail`：状态只有两个整数，空满判断一目了然，也不需要为区分空满多开一格。
- `%` 在 Python 里对非负数的结果恒在 `[0, cap)`，`(head + size) % cap` 直接可用；其他语言里负数取模要额外处理。
- `-1 if self.isEmpty() else ...` 条件表达式让空队列的返回值和取值写在一行；`isEmpty`、`isFull` 复用在入队、出队里，判断逻辑只写一处。
- 不用 `collections.deque`：题目禁止内置队列库，面试里也是考你对下标的掌握。
