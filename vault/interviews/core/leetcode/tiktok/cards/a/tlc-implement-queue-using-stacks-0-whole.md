---
id: tlc-implement-queue-using-stacks-0-whole
node: a.implement-queue-using-stacks
type: qa
---
## Q
**LC 232 用栈实现队列**｜Easy · 字节 高频

只用两个栈实现先入先出（FIFO）队列，支持 `push(x)` 把 `x` 放到队尾、`pop()` 移除并返回队首、`peek()` 返回队首、`empty()` 判断队列是否为空。只能使用标准的栈操作（压栈、弹栈、看栈顶、取大小、判空），Python 里可以用 `list` 或 `deque` 模拟栈。`1 <= x <= 9`，最多调用 `100` 次，调用都合法（空队列不会 `pop` / `peek`）。进阶：每个操作**均摊** `O(1)`。例：依次 `push(1)`、`push(2)`、`peek()` 得 `1`、`pop()` 得 `1`、`empty()` 得 `False`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 一个栈 `inbox` 只管压入，另一个栈 `outbox` 只管弹出；`outbox` 空了才把 `inbox` 全部倒进去（顺序恰好反转，栈顶变成最老的元素）。每个元素至多被倒一次，所以每个操作均摊 `O(1)`。

**识别。** 「用一种数据结构模拟另一种」且两者出入顺序相反（栈后进先出、队列先进先出），一次倒序就能把后进先出变成先进先出：两个栈串联，顺序反转两次回到原顺序。「均摊」说明允许个别操作慢，只要总成本摊平后是常数。

**推导。** 暴力：每次 `push` 都把现有元素倒到辅助栈、压入新元素再倒回来，`push` 是 `O(n)`；或者每次 `pop` 都整个倒两遍。浪费在于倒来倒去：倒过去之后，`outbox` 里的顺序已经就是出队顺序，只要它非空就可以一直直接弹，没有理由倒回去。新来的元素进 `inbox` 等着；只有 `outbox` 空了才需要再倒一批。每个元素的一生是「进 `inbox`、倒入 `outbox`、弹出」，每步各一次，所以 `n` 个操作总共 `O(n)`。

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

运行：`push(1)`、`push(2)` 后 `peek()` → `1`，`pop()` → `1`，`empty()` → `False`；再 `pop()` → `2`，`empty()` → `True`。`push(1)`、`push(2)`、`pop()` 得 `1`、`push(3)`、`pop()` 得 `2`。

**复杂度。** `push`、`empty` 是 `O(1)`；`pop`、`peek` 单次最坏 `O(n)`（触发一次整体倒入），均摊 `O(1)`：每个元素至多被倒入 `outbox` 一次；空间 `O(n)`。

**易错点。**
- 每次 `pop` / `peek` 都倒，不管 `outbox` 是否为空：`push(1)`、`push(2)`、`pop()`、`push(3)`、`pop()` 得到 `[1, 3]`（正确 `[1, 2]`），因为新元素 `3` 压在了老元素 `2` 的上面，顺序乱了。
- `empty()` 只检查 `inbox` 或只检查 `outbox`：元素可能全在另一个栈里。
- 倒的时候只倒一部分：必须整个 `inbox` 一次倒完，否则新老元素交错。

**追问。**
- 反过来，用队列实现栈（LC 225）：一个队列，每次 `push` 后把前面的元素依次出队再入队，使新元素到队首，`push` 是 `O(n)`，其余 `O(1)`。
- 要让 `peek` 也严格 `O(1)`：额外记一个 `front` 变量，`inbox` 为空时第一个 `push` 的元素记为队首。
- Python 里别用 `list.pop(0)` 当队列，它是 `O(n)`；真正的队列用 `collections.deque` 的 `popleft()`。

**同模式。** LC 225 用队列实现栈、LC 155 最小栈、LC 622 设计循环队列、LC 641 设计循环双端队列。
