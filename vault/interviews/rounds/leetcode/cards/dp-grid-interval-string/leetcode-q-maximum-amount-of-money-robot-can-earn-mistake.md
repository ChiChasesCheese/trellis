---
id: leetcode-q-maximum-amount-of-money-robot-can-earn-mistake
node: dp-grid-interval-string.matrix
type: qa
anki: 1787103483562
tags: [lc::3418, leetcode, mistake, recall]
---
## Q
用 functools.cache 写多维网格 DP 记忆化搜索时，可能踩到什么坑？

## A
functools.cache 装饰的递归在状态数较大（如 m*n*3）时可能导致 MLE（内存超限），因为它要缓存整个调用带来的额外开销（如闭包、hash key 存储）。应改为手动预分配的多维数组（如 [[[-inf]*3 for _ in range(n)] for _ in range(m)]）做 memo，直接用下标访问，更省内存。

**Evidence**

注释「想不mle得自己构造 memo...」，且保留了一版失败方案 maximumAmount_mle 使用 @functools.cache，对应提交 Memory: 176708000（远高于手动 memo 版本）

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3418%20-%20Maximum%20Amount%20of%20Money%20Robot%20Can%20Earn)
