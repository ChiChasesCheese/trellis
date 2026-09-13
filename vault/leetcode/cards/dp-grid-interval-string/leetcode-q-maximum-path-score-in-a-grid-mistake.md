---
id: leetcode-q-maximum-path-score-in-a-grid-mistake
node: dp-grid-interval-string.matrix
type: qa
anki: 1787181734383
tags: [lc::3742, leetcode, mistake, recall]
---
## Q
用 @cache 缓存 dfs(i, j, cost) 三元组作为网格 DP 状态，为什么会导致 MLE（内存超限）？

## A
把 cost 作为独立参数传入并交给 @cache，会为同一个 (i,j) 在不同调用路径下产生大量重复的 (i,j,cost) 键值对被逐个缓存，状态数和函数调用开销随 k 线性甚至更差地膨胀；而将 cost 维度收进返回数组（每个 (i,j) 只缓存一次，返回该点对所有 c 的答案）能把同一 (i,j) 的所有 cost 结果合并成一次缓存，大幅减少缓存条目和调用次数。

**Evidence**

笔记中标注了失败版本 maxPathScore_mle（dfs(i,j,cost) 直接 @cache），随后改写为 maxPathScore（dfs(i,j) 返回 arr 数组）才通过；提交记录显示改写后版本内存仍达 437728000（约 437MB），侧面印证原始三参数缓存方式内存开销更大。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3742%20-%20Maximum%20Path%20Score%20in%20a%20Grid)
