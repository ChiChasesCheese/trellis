---
id: tlc-implement-queue-using-stacks-4-followup
node: p3.implement-queue-using-stacks
type: qa
step: 4
---
## Q
**LC 232 用栈实现队列**｜追问

面试官接着问：（1）单次 `pop` 最坏 `O(n)`，怎么解释“均摊 `O(1)`”？（2）反过来，用队列实现栈（LC 225）？（3）多线程使用时要注意什么？

## A
1. **均摊解释。** 用记账法：每个元素 `push` 时多付 2 个单位，一个预付它将来被倒进 `outbox` 的成本，一个预付它被弹出的成本。`pop` 里那些大批量搬运，花的都是之前存下来的预付款，所以任意 `n` 次操作总成本 `O(n)`。注意这是**均摊**，不是平均：最坏的单次操作依然是 `O(n)`，对延迟敏感的场景要另说。
2. **用队列实现栈（LC 225）。** 一个队列即可：`push` 时先入队，再把它前面的元素依次出队并重新入队，让新元素转到队首。
```python
from collections import deque

class MyStack:
    def __init__(self) -> None:
        self.q: deque[int] = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        for _ in range(len(self.q) - 1):        # 把 x 之前的所有元素转到 x 后面
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return not self.q
```
`push` 是 `O(n)`，其余 `O(1)`；队列实现栈做不到“倒一次摊平”，因为单个队列的顺序倒不了。
3. **多线程。** `pop` 里的“检查 `outbox` 空 → 倒栈 → 弹出”不是原子的，两个线程同时进入会重复搬运或丢元素；给整个类加一把 `threading.Lock`，或用线程安全的 `queue.Queue`。

**Python 提醒**：`list.pop(0)` 是 `O(n)`，不能当队列用；需要队列时用 `collections.deque` 的 `append` 加 `popleft`，二者都是 `O(1)`。
