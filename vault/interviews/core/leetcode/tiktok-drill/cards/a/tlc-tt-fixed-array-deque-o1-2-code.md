---
id: tlc-tt-fixed-array-deque-o1-2-code
node: a.tt-fixed-array-deque-o1
type: qa
step: 2
---
## Q
**定长数组实现的双端队列（所有操作 O(1)）**｜写出 Python 实现

写类 `FixedDeque(capacity)`（`1 <= capacity <= 10^5`，值为整数）：`push_head(x)`、`push_tail(x)` 成功返回 `True`、已满返回 `False`；`pop_head()`、`pop_tail()` 返回弹出的值，空时返回 `None`；`index(i)` 返回从队首数起第 `i` 个元素，越界返回 `None`。底层只用一个定长列表，所有操作 `O(1)`。

## A
**思路。** 定长数组 `buf`、队首下标 `head`、元素个数 `size`。队首入队：`head` 往回退一格取模再写；队尾入队：写在 `(head + size) % cap`；队尾元素在 `(head + size - 1) % cap`；第 `i` 个元素在 `(head + i) % cap`。

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

**写法要点。**
- `(self.head - 1) % self.cap`：Python 的 `%` 对负数返回非负结果，`head = 0` 时回退到 `cap - 1`；C++、Java 要写 `(head - 1 + cap) % cap`。
- `0 <= i < self.size` 用链式比较写成一行，`not` 取反处理越界。
- 弹出时把槽位置回 `None`：不影响逻辑，但释放对对象的引用；存对象而不是整数时尤其重要。
- 类型标注 `list[int | None]`：槽位可能为空；返回 `int | None` 把「空」交给调用方显式处理。
