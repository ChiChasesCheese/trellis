---
slug: yong-liang-ge-zhan-shi-xian-dui-lie-lcof
---
## Q
**剑指 Offer 09 用两个栈实现队列**｜Easy

用两个栈实现队列：`push(bookID)` 入队，`pop()` 取出最早入队的值，没有则返回 `-1`。

## A
**一句话。** `inbox` 只进、`outbox` 只出，仅当 `outbox` 空时才把 `inbox` 整个倒过去，倒一次顺序恰好翻转成先进先出。

```python
class BookQueue:
    def __init__(self):
        self.inbox = []     # 只负责 push
        self.outbox = []    # 只负责 pop，栈顶是最早入队的

    def push(self, book_id):
        self.inbox.append(book_id)

    def pop(self):
        if not self.outbox:     # 空了才倒
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox.pop() if self.outbox else -1
```

**复杂度。** 时间 `push` 为 `O(1)`、`pop` 均摊 `O(1)`，空间 `O(n)`。

**易错点。**
- `outbox` 非空也去倒：次序错乱，`push 1, push 2, pop, push 3, pop` 应得 `1, 2`，却得 `1, 3`。
- 每次 `pop` 都全倒过去再倒回来：次序对，但每次 `O(n)`，没利用均摊。
- 空队列直接 `pop()`：对空 `list` 抛 `IndexError`，要返回 `-1`。

**追问。**
- 加 `peek()` 和 `empty()`？：`peek` 同样先补充 `outbox` 再读 `outbox[-1]`，`empty` 看两个栈是否都空。
- 反过来用两个队列实现栈（LC 225）？：`push` 时新元素入队后，把前面的元素依次出队再入队，使新元素到队首，`push` 为 `O(n)`。

**同模式。** LC 232 用栈实现队列、LC 225 用队列实现栈、LC 155 最小栈、LC 622 设计循环队列
