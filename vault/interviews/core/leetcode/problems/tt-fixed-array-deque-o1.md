---
slug: tt-fixed-array-deque-o1
---
## Q
**定长数组实现的双端队列（所有操作 O(1)）**｜Medium

用定长数组实现 `FixedDeque(capacity)`：`push_head`、`push_tail`（成功 `True`，已满 `False`）、`pop_head`、`pop_tail`（空时返回 `None`）、`index(i)`（从队首数第 `i` 个，越界 `None`），全部 `O(1)`。

## A
**一句话。** 环形缓冲区：数组加队首下标 `head` 和元素个数 `size`，两端靠对容量取模移动，第 `i` 个元素在 `(head + i) % cap`。

```python
class FixedDeque:
    def __init__(self, capacity):
        self.buf = [None] * capacity
        self.cap = capacity
        self.head = 0       # 队首下标
        self.size = 0       # 用 size 区分空和满

    def push_head(self, x):
        if self.size == self.cap:
            return False
        self.head = (self.head - 1) % self.cap   # 回退一格
        self.buf[self.head] = x
        self.size += 1
        return True

    def push_tail(self, x):
        if self.size == self.cap:
            return False
        self.buf[(self.head + self.size) % self.cap] = x
        self.size += 1
        return True

    def pop_head(self):
        if self.size == 0:
            return None
        x = self.buf[self.head]
        self.buf[self.head] = None
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return x

    def pop_tail(self):
        if self.size == 0:
            return None
        tail = (self.head + self.size - 1) % self.cap
        x = self.buf[tail]
        self.buf[tail] = None
        self.size -= 1
        return x

    def index(self, i):
        if not 0 <= i < self.size:
            return None
        return self.buf[(self.head + i) % self.cap]
```

**复杂度。** 每个操作时间 `O(1)`，空间 `O(capacity)`。

**易错点。**
- 队尾元素下标写成 `(head + size) % cap`：那是下一个空位，`push_tail(1)` 后 `pop_tail()` 得 `None`，应为 `1`。
- `index(i)` 忘了加 `head`：先 `push_tail(1)`、`push_head(2)`，`index(0)` 读 `buf[0]` 得 `1`，应为 `2`。
- 满了还写入：覆盖队尾元素，必须先判满。

**追问。**
- 要按值查找 `O(1)`？：额外维护 `Counter`，入队加一出队减一，只判存在性。
- 容量可增长？：满时开两倍新数组，从 `head` 起按逻辑顺序拷贝，`head` 归零，均摊 `O(1)`。

**同模式。** LC 641 设计循环双端队列、LC 622 设计循环队列、LC 1670 设计前中后队列、LC 346 数据流中的移动平均值
