---
id: tlc-yong-liang-ge-zhan-shi-xian-dui-lie-lcof-3-why
node: b.yong-liang-ge-zhan-shi-xian-dui-lie-lcof
type: qa
step: 3
---
## Q
**剑指 Offer 09 用两个栈实现队列**｜正确性

为什么「只在 `outbox` 空时才倒」是对的？如果 `outbox` 还有元素就把 `inbox` 也倒进去，会错在哪里？

## A
**不变量。** 队列的次序 = `outbox` 从栈顶到栈底，再接 `inbox` 从栈底到栈顶。`outbox` 里的所有元素都比 `inbox` 里的所有元素更早归还。

**为什么这个不变量保持。** `push` 只往 `inbox` 栈顶加，加的是最晚的书，次序仍对。`pop` 只在 `outbox` 空时搬运：此时整个队列就在 `inbox` 里，整体翻转后最早的书到了 `outbox` 栈顶；之后新书继续进 `inbox`，仍排在 `outbox` 所有元素之后。

**反例。** 操作序列 `push 1, push 2, pop, push 3, pop`，正确返回 `1, 2`。
- 第一次 `pop`：倒后 `outbox = [2, 1]`，弹出 `1`，`outbox = [2]`。
- `push 3` 进入 `inbox = [3]`。第二次 `pop` 若不检查 `outbox` 是否为空，就把 `3` 倒到 `outbox = [2, 3]`，栈顶是 `3`，返回 `3`，错；检查后直接弹 `2`。
