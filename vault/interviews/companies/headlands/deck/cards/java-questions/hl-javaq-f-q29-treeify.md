---
id: hl-javaq-f-q29-treeify
node: java-questions.f-concurrency
type: qa
step: 16
---
## Q
`HashMap` 的桶里累计到 8 个冲突节点就一定转红黑树吗？实验里在第几次冲突 put 才变成 `TreeNode`？树内查找为什么依赖 `Comparable`？

## A
- 不一定：桶里 ≥ 8 个节点但**表容量 < 64** 时，先**扩容**，不转树。
- 实验：第 8 次冲突 put 表长 16，第 9 次扩到 32，第 10 次扩到 64，都还是 `Node`；**第 11 次**表长已达 64，才真正变成 `TreeNode`。
- 树内查找：键实现 `Comparable` 时按 `compareTo` 二分，8000 次查找约 **3.4 ms**；不可比较时只能比 hash 再 tieBreak，要遍历子树，约 **20 ms**。
- 构造碰撞很容易：`"Aa".hashCode() == "BB".hashCode()`（都是 2112）。
