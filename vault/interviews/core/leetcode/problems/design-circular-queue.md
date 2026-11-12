---
slug: design-circular-queue
---
## Q
**LC 622 设计循环队列**｜Medium

实现容量为 `k` 的循环队列：`enQueue`、`deQueue`、`Front`、`Rear`、`isEmpty`、`isFull`，不得使用内置队列。

## A
**一句话。** 定长数组加队首下标 `head` 和元素个数 `size`，下标一律对 `k` 取模。

```python
class MyCircularQueue:
    def __init__(self, k):
        self.buf = [0] * k
        self.k = k
        self.head = self.size = 0

    def enQueue(self, v):
        if self.isFull():
            return False
        self.buf[(self.head + self.size) % self.k] = v
        self.size += 1
        return True

    def deQueue(self):
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.k
        self.size -= 1
        return True

    def Front(self):
        return -1 if self.isEmpty() else self.buf[self.head]

    def Rear(self):
        if self.isEmpty():
            return -1
        i = (self.head + self.size - 1) % self.k
        return self.buf[i]

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.k
```

**复杂度。** 时间 每个操作 `O(1)`，空间 `O(k)`。

**易错点。**
- 队尾下标不取模：容量 `3`，入队 `1,2,3`，出队一次后再入队，下标 `3` 越界。
- 只用 `head`、`tail` 两个下标：空和满都是 `head == tail`，为区分而牺牲一格，容量变成 `k - 1`。

**追问。**
- 满了就覆盖最旧元素？：入队时若已满先让 `head` 前进一格再写（`deque(maxlen=k)` 即此语义）。
- 动态扩容？：满时开两倍数组，从 `head` 起按逻辑顺序拷贝，`head` 归零，均摊 `O(1)`。

**同模式。** LC 641 设计循环双端队列、LC 346 数据流中的移动平均值、LC 232 用栈实现队列
