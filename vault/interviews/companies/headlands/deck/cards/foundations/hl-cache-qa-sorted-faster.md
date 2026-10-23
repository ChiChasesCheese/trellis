---
id: hl-cache-qa-sorted-faster
node: foundations.cpu-cache-locality
type: qa
step: 37
---
## Q
追问：为什么排序后的数组处理更快？

## A
推荐答法：「分支预测。数据相关的 `if` 在随机数据下无法预测，每次预测错误约 10–20 个周期；排序后分支有规律，预测几乎总对。我测过 **9 倍**差距，但 JIT 可能把简单分支编译成条件移动，那就看不出差异。」
