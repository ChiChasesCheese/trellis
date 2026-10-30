---
id: tlc-yong-liang-ge-zhan-shi-xian-dui-lie-lcof-4-followup
node: p5.yong-liang-ge-zhan-shi-xian-dui-lie-lcof
type: qa
step: 4
---
## Q
**剑指 Offer 09 用两个栈实现队列**｜追问

面试官接着问：（1）加 `peek()` 和 `empty()`？（2）最坏单次 `O(n)` 不能接受，能做到每次最坏 `O(1)` 吗？（3）反过来用队列实现栈？

## A
1. **`peek` / `empty`**：`peek` 与 `pop` 共用「`outbox` 空则倒」这一步，抽成私有方法 `_refill()`，之后读 `outbox[-1]`；`empty` 是 `not (inbox or outbox)`。
2. **最坏 `O(1)`**：这是「实时队列」。把一次大搬运分摊到后续每次 `push` / `pop` 里，每次多搬常数个元素，同时在搬运期间维护额外的栈和计数。面试里说清「均摊 `O(1)` 与最坏 `O(1)` 不同，后者要增量式搬运」就够了。
3. **两个队列实现栈**：`push` 时先入队，再把此前的全部元素依次出队重新入队，让新元素到队首，`pop` 直接出队。`push` `O(n)`、`pop` `O(1)`；一个队列也能做，旋转 `len - 1` 次即可。

**Python 提醒**：Python 的 `list.pop(0)` 是 `O(n)`；生产里要队列用 `collections.deque`（两端 `O(1)`）。此处的限制是只许用栈，答题时说一句「实际会用 `deque`」显示你知道标准库。
