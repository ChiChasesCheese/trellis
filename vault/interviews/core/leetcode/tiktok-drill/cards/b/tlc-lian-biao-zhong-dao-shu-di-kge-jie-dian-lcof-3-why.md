---
id: tlc-lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof-3-why
node: b.lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof
type: qa
step: 3
---
## Q
**剑指 Offer 22 链表中倒数第k个节点**｜正确性

为什么 `fast` 先走 `cnt` 步、再同步走到 `fast` 为 `None`，`slow` 就落在倒数第 `cnt` 个？循环条件该写 `while fast` 还是 `while fast.next`？

## A
**不变量。** 设链表有 `n` 个节点，下标 `0..n-1`，末尾之后是 `None`（下标 `n`）。倒数第 `cnt` 个节点的下标是 `n - cnt`。`fast` 先走 `cnt` 步后在下标 `cnt`，`slow` 在 `0`，间距始终是 `cnt`。同步前进直到 `fast` 在下标 `n`（即 `None`），此时 `slow` 在 `n - cnt`，正是目标。

**循环条件。** `fast` 先走 `cnt` 步对应 `while fast`（走到 `None` 为止）。若改成 `while fast.next`（走到最后一个节点为止），`fast` 少走一步，`slow` 也少走一步，落在下标 `n - cnt - 1`，即倒数第 `cnt + 1` 个；此时应把预走步数减一，成对修改。

**反例。** 先走 `cnt` 步，却配 `while fast.next`：`[2,4,7,8], cnt = 1` 返回值为 `7` 的节点，正确答案是值为 `8` 的节点。另一个反例：`cnt` 超过长度（题目不会给，但防御性代码要处理）时 `fast` 在循环里变成 `None` 后再取 `.next` 会抛 `AttributeError`，所以预走阶段要检查 `fast is None`。
