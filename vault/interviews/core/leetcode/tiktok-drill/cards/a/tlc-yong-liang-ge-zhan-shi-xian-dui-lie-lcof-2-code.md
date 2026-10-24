---
id: tlc-yong-liang-ge-zhan-shi-xian-dui-lie-lcof-2-code
node: a.yong-liang-ge-zhan-shi-xian-dui-lie-lcof
type: qa
step: 2
---
## Q
**剑指 Offer 09 用两个栈实现队列**｜写出 Python 实现

用两个栈（Python 里用两个 `list`，只调用 `append` / `pop()`）实现队列 `BookQueue`：`push(book_id)` 入队尾，`pop()` 出队首，空时返回 `-1`。`bookID` 在 `1..10000`，调用总数最多 `10000`。要求均摊 `O(1)`。

## A
**思路。** 两个 `list` 当栈用。`push` 永远压进 `inbox`。`pop` 时：如果 `outbox` 是空的，把 `inbox` 逐个弹出压进 `outbox`（次序翻转）；然后从 `outbox` 弹出栈顶返回，两个栈都空则返回 `-1`。

```python
class BookQueue:
    def __init__(self) -> None:
        self.inbox: list[int] = []     # 只负责 push：新书压在栈顶
        self.outbox: list[int] = []    # 只负责 pop：栈顶就是最早入队的元素

    def push(self, book_id: int) -> None:
        self.inbox.append(book_id)

    def pop(self) -> int:
        if not self.outbox:            # 只有 outbox 空了才倒，倒一次次序就翻转对了
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox.pop() if self.outbox else -1
```

运行：`["BookQueue","push","push","pop"], [[],[1],[2],[]]` → `[None, None, None, 1]`，`空队列直接 pop 两次` → `[None, -1, -1]`，`push 1,2 → pop → push 3 → pop,pop,pop` → `[None, None, None, 1, None, 2, 3, -1]`。

**复杂度。** `push` 严格 `O(1)`；`pop` 均摊 `O(1)`：每个元素至多从 `inbox` 倒到 `outbox` 一次、弹出一次，`n` 次操作总共搬运不超过 `n` 次，单次最坏 `O(n)`。空间 `O(n)`。

**写法要点。** `list.append` / `list.pop()` 就是栈，均为 `O(1)`；`return self.outbox.pop() if self.outbox else -1` 用条件表达式把「空则 `-1`」写成一行；`if not self.outbox:` 比 `len(...) == 0` 更惯用。搬运也可写成 `self.outbox.extend(reversed(self.inbox)); self.inbox.clear()`，一次完成且在 C 层执行，面试里先写 `while` 循环让「逐个弹出、逐个压入」的动作可见。
