---
id: uth-compose-ring-buffer-5-interview
node: compose.ring-buffer
type: qa
step: 5
---
## Q
**借到面试题上：下标怎样绕回来**｜环形数组 · 面试写法

面试要你用定长数组实现循环队列或双端队列。生产环境的序号写法，和面试里常见的「队首下标 + 个数」写法有什么区别？

## A
**结构。** 两种写法都靠多记一个量来区分空和满。面试写法是 `buf`、`head`（队首下标）、`size`（个数），队尾的下一个空位是 `(head + size) % cap`。生产写法是 `read`、`write` 两个序号。

| | `head` + `size` | `read` / `write` 序号 |
|---|---|---|
| 空 | `size == 0` | `read == write` |
| 满 | `size == cap` | `write - read == cap` |
| 第 i 个元素 | `(head + i) % cap` | `序号 & mask` |
| 队首也能进 | 能：`head` 退一格 | 不能：只在队尾进、队首出 |
| 多线程 | `size` 被两端同时改 | 两个序号各一个写者 |

**坑。** 只存队首、队尾两个下标，空和满都是 `head == tail`；常见的补救是留一个空格，容量就少了一格。

**例题：** 定长数组实现的双端队列（所有操作 O(1)）

用一个定长数组实现双端结构 `FixedDeque(capacity)`，所有操作都要 `O(1)`：`push_head`、`push_tail`（成功返回 `True`，已满返回 `False`），`pop_head`、`pop_tail`（空时返回 `None`），`index(i)` 返回从队首数起第 `i` 个元素，越界返回 `None`。例：容量 3，`push_tail(1)`、`push_head(2)`、`push_tail(3)` 都是 `True`，`push_head(4)` → `False`，此时 `index(0)`、`index(1)`、`index(2)` → `2, 1, 3`。

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
