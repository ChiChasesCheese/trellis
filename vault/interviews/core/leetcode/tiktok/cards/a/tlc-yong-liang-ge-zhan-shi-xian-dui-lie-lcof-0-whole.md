---
id: tlc-yong-liang-ge-zhan-shi-xian-dui-lie-lcof-0-whole
node: a.yong-liang-ge-zhan-shi-xian-dui-lie-lcof
type: qa
---
## Q
**剑指 Offer 09 用两个栈实现队列**｜Easy · CodeTop 国内累计 25 次 · 最近 2026-10-09（CodeTop）

用两个栈实现一个队列。要实现 `push(bookID)`：把编号 `bookID` 的书归还到队尾（入队）；`pop()`：借出**最早**归还的书并返回它的值，没有书可借时返回 `-1`。栈是后进先出，队列是先进先出，只允许对栈做压入 / 弹出。

约束：`1 <= bookID <= 10000`，`push`、`pop` 总共最多调用 `10000` 次。

例：`["BookQueue","push","push","pop"]`，`[[],[1],[2],[]]` → `[null,null,null,1]`（先入队的 `1` 先被取走）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 两个栈各管一头：`inbox` 只进、`outbox` 只出；只有 `outbox` 空时才把 `inbox` 整个倒过去（倒一次顺序恰好翻转成先进先出）。每个元素最多搬一次，`pop` 均摊 `O(1)`。

**识别。** 「用 A 结构模拟 B 结构」+「只允许基本操作」是设计题里的经典：先问两种结构次序的差别（栈后进先出，队列先进先出），再想怎么用「翻转两次 = 不变」。一个栈的栈顶是最新的，倒进第二个栈后，栈顶变成最老的——这恰好是队首。复杂度的重点是**均摊**（amortized）。

**推导。** 暴力：只用一个栈 `s` 和一个辅助栈，每次 `push` 都把 `s` 全倒到辅助栈、放入新元素、再倒回来，`push` `O(n)`。浪费在于每次都做了两次整体搬运，而大多数操作之间并不需要保持「栈顶是队首」。洞察：把「倒」推迟到真正需要时——`pop` 时如果 `outbox` 还有元素，队首就在它的栈顶，什么也不用做；只有它空了，才把 `inbox` 整个倒过来。倒过来的元素在 `outbox` 里按先进先出的次序排列，后续到达的新元素留在 `inbox`，不会插队。每个元素生命周期里只被搬运一次。

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

**易错点。**
- `outbox` 非空时也去倒：次序错乱。`push 1, push 2, pop, push 3, pop` 应依次得 `1, 2`，这样写得 `1, 3`（第二次 `pop` 把 `3` 倒到 `outbox` 顶部，先返回了 `3`）。
- 每次 `pop` 都全倒过去再倒回来：次序对，但每次 `pop` 都是 `O(n)`；队里有数千个元素时，每次 `pop` 都搬运数千次，总量到千万级，没有利用均摊。
- 空队列：`pop` 要返回 `-1`，而不是对空 `list` 调 `pop()` 抛 `IndexError`。

**追问。**
- `peek()` / `empty()`：`peek` 与 `pop` 同样先补充 `outbox`，再读 `outbox[-1]`；`empty` 看 `not inbox and not outbox`。
- 要求每次操作最坏也是 `O(1)`（实时队列）：把整体搬运拆到后续的每次操作里分摊，需要三个栈或带计数器的增量翻转，面试里能说出「均摊 vs 最坏」的区别即可。
- 反过来，用两个队列实现栈（LC 225）：`push` 时把新元素入队后，把前面的元素依次出队再入队，使新元素到队首；`pop` 直接出队。`push` `O(n)`。

**同模式。** LC 232 用栈实现队列（同题）、LC 225 用队列实现栈、LC 155 最小栈、LC 622 设计循环队列、LC 716 最大栈。
