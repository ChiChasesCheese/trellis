---
id: amz-closest-store-common-mistake-one-candidate
node: amazon.amz-closest-store
type: qa
step: 9
tags: [grown]
---
## Q
在 Amazon 增删查最近值设计里，候选人最常见的错误是什么？给出一个会暴露它的输入。

## A
只比较一个候选：拿 `bisect_left` 返回位置的元素当答案，忘了它的左邻居。输入：集合 {10, 20}，target=11，`bisect_left` 指向 20，但 10 更近（距离 1 对 9）。修法：同时取 `xs[i-1]` 与 `xs[i]`（并处理 i 为 0 或 len 的两个边界）再比距离。另一个同类错误：用 `bisect_left` 当前驱用，target 恰好在集合里时会取到它左边的值。
