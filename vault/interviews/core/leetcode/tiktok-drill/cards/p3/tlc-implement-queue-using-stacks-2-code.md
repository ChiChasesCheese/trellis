---
id: tlc-implement-queue-using-stacks-2-code
node: p3.implement-queue-using-stacks
type: qa
step: 2
---
## Q
**LC 232 用栈实现队列**｜写出 Python 实现

实现类 `MyQueue`：只用两个栈（Python 里用 `list` 的 `append` / `pop` / `[-1]` 当栈）模拟先入先出队列，支持 `push(x)`、`pop()`、`peek()`、`empty()`（`1 <= x <= 9`，至多 100 次调用，调用都合法）。要求每个操作均摊 `O(1)`。

## A
**思路。** `inbox` 接收新元素；`outbox` 的栈顶永远是队首。取队首前，如果 `outbox` 为空，就把 `inbox` 一次性全部倒进去。

```python
class MyQueue:
    def __init__(self) -> None:
        self.inbox: list[int] = []        # 只负责 push：新元素压在栈顶
        self.outbox: list[int] = []       # 只负责 pop / peek：栈顶就是队首

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def _move(self) -> None:
        if not self.outbox:               # 只有 outbox 空了才倒，倒的时候整个 inbox 一次倒完
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self) -> int:
        self._move()
        return self.outbox.pop()

    def peek(self) -> int:
        self._move()
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox
```

运行：`push(1)`、`push(2)` 后 `peek()` → `1`，`pop()` → `1`，`empty()` → `False`；再 `pop()` → `2`，`empty()` → `True`；`push(1)`、`push(2)`、`pop()`（得 `1`）、`push(3)`、`pop()` → `2`。

**复杂度。** `push`、`empty` 为 `O(1)`；`pop`、`peek` 最坏 `O(n)`，均摊 `O(1)`（每个元素最多进出 `inbox` 和 `outbox` 各一次）；空间 `O(n)`。

**写法要点。**
- 把「必要时倒栈」抽成 `_move()`，`pop` 和 `peek` 共用，避免两处逻辑不一致。
- `list.append` / `list.pop()` 都是均摊 `O(1)`，`self.outbox[-1]` 就是看栈顶，完全符合「只用标准栈操作」。
- `empty()` 用 `not a and not b`，两个栈都要查。
- 类型标注 `list[int]` 写在 `__init__` 里的属性上，让 `self.outbox[-1]` 的类型明确。
