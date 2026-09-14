---
id: cc-verification-edge-duplicate-and-out-of-order
node: verification.edge-catalog
type: qa
---
## Q
The statement never mentions duplicates or ordering. Why do you still test them, and what are you actually testing for?

## A
**Because the grader's input generator does not read your assumptions.** Real event streams repeat and arrive out of order, so hidden tests contain both.

- **Duplicate**: the same id appearing twice. Is the second a no-op, a replacement, or an error? Any of the three can be right — choose deliberately and record the choice in a comment beside the handler.
- **Out-of-order**: an event referring to an entity declared later in the file, a reversal before its original, a timestamp that moves backwards. Either sort first or state explicitly that arrival order *is* the order.
- Both are where a maintained aggregate silently drifts from the truth ([[cc-performance-amortized-incremental-aggregate]]), because the rare path forgot to apply the same delta.

## Q zh
题面完全没提重复和顺序。你为什么还要测它们？你实际上在测什么？

## A zh
**因为评测机的输入生成器不会去读你的假设。** 真实事件流会重复、会乱序，所以隐藏测试里两者都有。

- **重复**：同一个 id 出现两次。第二次是空操作、是覆盖、还是报错？三种都可能是对的 —— 有意识地选，并把选择写在处理函数旁的注释里。
- **乱序**：事件引用了文件里更靠后才声明的实体、冲正出现在原始事件之前、时间戳倒退。要么先排序，要么明确声明到达顺序*就是*顺序。
- 这两者正是增量维护的聚合值悄悄偏离真相的地方（[[cc-performance-amortized-incremental-aggregate]]），因为那条罕见路径忘了施加同样的差量。
