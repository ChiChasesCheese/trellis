---
id: tlc-design-circular-queue-0-whole
node: p3.design-circular-queue
type: qa
---
## Q
**LC 622 设计循环队列**｜Medium · 近一年被问：美国 4 次、国内 0 次 · CodeTop 国内累计 2 次 · 最近 2026-07-06（面试记录）

设计循环队列（环形缓冲器）：先进先出，队尾连接到队首形成环，可以重复利用出队腾出的空间。实现类 `MyCircularQueue(k)`，容量为 `k`，支持：`enQueue(value)` 入队，成功返回 `True`，队满返回 `False`；`deQueue()` 出队，成功返回 `True`，队空返回 `False`；`Front()` 取队首，空则返回 `-1`；`Rear()` 取队尾，空则返回 `-1`；`isEmpty()`、`isFull()`。值在 `0` 到 `1000`，操作数在 `1` 到 `1000`，不要使用内置的队列库。例：容量 `3`，`enQueue(1)`、`enQueue(2)`、`enQueue(3)` 都是 `True`，`enQueue(4)` → `False`，`Rear()` → `3`，`isFull()` → `True`，`deQueue()` → `True`，`enQueue(4)` → `True`，`Rear()` → `4`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用长度为 `k` 的数组加两个整数：队首下标 `head` 和元素个数 `size`；队尾的下一个空位是 `(head + size) % k`，出队时 `head` 前进一格并对 `k` 取模；用 `size` 区分空和满，每个操作 `O(1)`。

**识别。** 「固定容量的 FIFO、空间循环利用、不许用内置队列」就是环形缓冲区（ring buffer）：下标对容量取模，让数组首尾相接。真正的难点是**空和满怎么区分**。

**推导。** 朴素做法：用 `list` 的 `pop(0)` 出队，每次 `O(k)`，而且这不是定长数组。把队列做成定长数组、出队只移动队首下标，数组前面空出的位置就浪费了，这正是循环队列要解决的问题。循环利用需要下标取模；再记 `head` 与 `tail` 两个下标的话，空和满时都有 `head == tail`，无法区分，要么牺牲一个格子（容量实际是 `k - 1`），要么多存一个状态。直接存元素个数 `size`：空是 `size == 0`，满是 `size == k`，队尾位置由 `head` 和 `size` 算出，不需要 `tail`。

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

运行：容量 `3` 的例子依次返回 `[True, True, True, False, 3, True, True, True, 4, 2]`（最后一个是出队后再入队 `4` 的 `Front()`）；空队列 `Front()`、`Rear()` 都是 `-1`；容量 `1` 时 `enQueue(7)` 为 `True`，再 `enQueue(8)` 为 `False`，`deQueue()` 后 `enQueue(8)` 为 `True`。

**复杂度。** 每个操作 `O(1)`，空间 `O(k)`。

**易错点。**
- 队尾下标不取模：`Rear()` 写成 `buf[head + size - 1]`。容量 `3`，入队 `1,2,3`，出队一次，再入队 `4`，此时 `head = 1`、`size = 3`，下标是 `3`，`IndexError`；正确是 `(1 + 3 - 1) % 3 = 0`。
- 只用 `head`、`tail` 两个下标：空和满都是 `head == tail`；为了区分让满的条件变成 `(tail + 1) % k == head`，容量实际只有 `k - 1`，容量 `3` 的例子第三次 `enQueue` 就返回 `False`。
- 入队位置写成 `buf[self.head + self.size]` 不取模，同样会在绕回时越界；空队列的 `Front()`、`Rear()` 要先判断再取值，返回 `-1`。

**追问。**
- 线程安全的生产者消费者：加一把锁和两个条件变量（队满时生产者等待，队空时消费者等待）；Python 里直接用 `queue.Queue(maxsize=k)`。
- 满了就覆盖最旧元素（日志缓冲区）：入队满时先 `head` 前进一格再写；`collections.deque(maxlen=k)` 就是这个语义。
- 动态扩容：满时开一个两倍容量的新数组，按逻辑顺序（从 `head` 开始）拷贝过去，`head` 归零，均摊 `O(1)`。

**同模式。** LC 641 设计循环双端队列、LC 346 数据流中的移动平均值、LC 232 用栈实现队列、LC 225 用队列实现栈。
