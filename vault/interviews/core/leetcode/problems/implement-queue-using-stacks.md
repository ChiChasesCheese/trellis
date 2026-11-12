---
slug: implement-queue-using-stacks
---
## Q
**LC 232 用栈实现队列**｜Easy

只用栈实现 FIFO 队列：`push`、`pop`、`peek`、`empty`。

## A
**一句话。** 双栈：`inbox` 只压入，`outbox` 只弹出，`outbox` 空了才把 `inbox` 整个倒进去，均摊 `O(1)`。

```python
class MyQueue:
    def __init__(self):
        self.inbox = []     # 只 push
        self.outbox = []    # 栈顶是队首

    def push(self, x):
        self.inbox.append(x)

    def _move(self):
        if not self.outbox:    # 空了才倒，且一次倒完
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self):
        self._move()
        return self.outbox.pop()

    def peek(self):
        self._move()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox
```

**复杂度。** 时间 `pop`、`peek` 均摊 `O(1)`，空间 `O(n)`。

**易错点。**
- 每次 `pop` 都倒，不管 `outbox` 是否为空：新元素压到老元素上，顺序乱，`push(1),push(2),pop,push(3),pop` 得 `[1,3]`。
- `empty` 只查一个栈：元素可能全在另一个栈里。
- 只倒一部分：必须一次倒完，否则新老元素交错。

**追问。**
- 用队列实现栈（LC 225）？：一个队列，每次 `push` 后把前面的元素依次出队再入队，使新元素到队首。
- Python 里能用 `list.pop(0)` 当队列吗？：不能，它是 `O(n)`；用 `deque.popleft()`。

**同模式。** LC 225 用队列实现栈、LC 155 最小栈、LC 622 设计循环队列、LC 641 设计循环双端队列
