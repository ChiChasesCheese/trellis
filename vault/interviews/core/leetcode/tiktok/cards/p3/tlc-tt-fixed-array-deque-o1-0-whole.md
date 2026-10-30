---
id: tlc-tt-fixed-array-deque-o1-0-whole
node: p3.tt-fixed-array-deque-o1
type: qa
---
## Q
**定长数组实现的双端队列（所有操作 O(1)）**｜Medium · 近一年被问：美国 4 次、国内 0 次 · 最近 2026-07-06（美国面试记录）

用一个定长数组实现双端结构 `FixedDeque(capacity)`，所有操作都要 `O(1)`：`push_head(x)`、`push_tail(x)`（成功返回 `True`，已满返回 `False`）；`pop_head()`、`pop_tail()`（返回弹出的值，空时返回 `None`）；`index(i)` 返回从队首数起第 `i` 个元素（`0` 起），越界返回 `None`。类似 Redis 的 list：`lpush`、`rpush`、`lpop`、`rpop`、`index`。`1 <= capacity <= 10^5`，值为整数。例：容量 `3`，`push_tail(1)`、`push_head(2)`、`push_tail(3)` 都是 `True`，`push_head(4)` → `False`（已满）；此时 `index(0), index(1), index(2), index(3)` → `2, 1, 3, None`；`pop_head()` → `2`，`pop_tail()` → `3`，`pop_tail()` → `1`，`pop_head()` → `None`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 环形缓冲区（ring buffer）：定长数组加两个整数——队首下标 `head` 和元素个数 `size`；队首入队是 `head` 往回退一格（对容量取模）再写入，队尾入队写在 `(head + size) % cap`，两端弹出分别移动 `head` 或减小 `size`，第 `i` 个元素在 `(head + i) % cap`，每个操作 `O(1)`。

**识别。** 「定长数组、两端都能进出、按位置随机访问都要 `O(1)`」只有环形缓冲区能同时满足：链表不能 `O(1)` 随机访问，普通数组头部插入要整体移动。「search」更合理的读法是按位置访问（`index`）；按值查找 `O(1)` 需要额外的哈希表，是单独的追问。

**推导。** 暴力：用 `list`，`insert(0, x)` 和 `pop(0)` 是 `O(n)`。第二步：用定长数组只在尾部操作，头部操作仍要搬动。浪费：为了让头部也 `O(1)`，只要不固定“队首在下标 `0`”这件事。洞察：记录队首下标 `head`，让数组首尾相接（下标对 `cap` 取模）：队首入队就是 `head - 1`，队尾入队写在队首之后 `size` 格；第 `i` 个元素在 `head` 之后 `i` 格。用 `size` 区分空和满，不浪费格子。

```python
class FixedDeque:
    """定长数组实现的双端队列：五个操作全部 O(1)。"""

    def __init__(self, capacity: int) -> None:
        self.buf: list[int | None] = [None] * capacity
        self.cap = capacity
        self.head = 0                               # 队首元素的下标
        self.size = 0                               # 元素个数：用 size 区分空和满，不浪费一格

    def push_head(self, x: int) -> bool:
        if self.size == self.cap:
            return False
        self.head = (self.head - 1) % self.cap      # 头指针往回退一格；Python 的 % 对负数也给非负结果
        self.buf[self.head] = x
        self.size += 1
        return True

    def push_tail(self, x: int) -> bool:
        if self.size == self.cap:
            return False
        self.buf[(self.head + self.size) % self.cap] = x
        self.size += 1
        return True

    def pop_head(self) -> int | None:
        if self.size == 0:
            return None
        x = self.buf[self.head]
        self.buf[self.head] = None                  # 清掉引用，方便垃圾回收
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return x

    def pop_tail(self) -> int | None:
        if self.size == 0:
            return None
        tail = (self.head + self.size - 1) % self.cap
        x = self.buf[tail]
        self.buf[tail] = None
        self.size -= 1
        return x

    def index(self, i: int) -> int | None:
        """第 i 个元素（从队首数，0 起）；越界返回 None。"""
        if not 0 <= i < self.size:
            return None
        return self.buf[(self.head + i) % self.cap]
```

运行：容量 `3`：`push_tail(1)`、`push_head(2)`、`push_tail(3)`、`push_head(4)` → `True, True, True, False`；`index(0)` 到 `index(3)` → `2, 1, 3, None`；`pop_head()`、`pop_tail()`、`pop_tail()`、`pop_head()` → `2, 3, 1, None`，之后 `index(0)` → `None`。

**复杂度。** 五个操作都是 `O(1)`，空间 `O(capacity)`。

**易错点。**
- 队尾元素下标写成 `(head + size) % cap`（那是下一个空位）：`push_tail(1)` 后 `pop_tail()` 读到空槽，得到 `None`，正确是 `1`；队尾元素在 `(head + size - 1) % cap`。
- `index(i)` 忘记加 `head`：`push_tail(1)`、`push_head(2)` 之后数组是 `[1, None, 2]`，`head = 2`；`index(0)` 直接读 `buf[0]` 得到 `1`，正确是 `2`。
- 头部入队先改 `size` 再算位置，或忘记先检查是否已满：满了还写入会覆盖队尾元素。
- 空队列弹出要先判断 `size == 0`，否则会弹出数组里残留的值。

**追问。**
- 「按值查找 `O(1)`」：额外维护 `Counter[int]`（值 → 个数），入队加一、出队减一，`contains(x)` 是 `count[x] > 0`；返回位置则要处理下标随两端入队而整体偏移，通常只做存在性判断。
- 容量可增长：满时分配两倍的新数组，按逻辑顺序（从 `head` 起绕一圈）拷贝过去，`head` 归零，均摊 `O(1)`。
- 线程安全：每个方法持同一把锁；生产者消费者场景用条件变量等待满、空。

**同模式。** LC 641 设计循环双端队列、LC 622 设计循环队列、LC 1670 设计前中后队列、LC 346 数据流中的移动平均值。
