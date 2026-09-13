---
id: leetcode-q-minimum-jumps-to-reach-end-via-prime-teleportation-pattern
node: math-number-theory.number-theory
type: qa
anki: 1787102262657
tags: [lc::3629, leetcode, pattern, recall]
---
## Q
如何用 BFS 求解“通过质数传送到达终点的最少跳数”问题（如 LC 3629）？

## A
1) 用线性筛预处理最小质因子表 spf（sieve of smallest prime factor），复杂度 O(MX log log MX)。2) 对每个下标 i 分解 nums[i] 的质因子，建立 质数 -> 拥有该质因子的下标列表 的映射 p2j。3) BFS 时，每一步除了走相邻下标 i-1/i+1，还可以通过当前下标的每个质因子 p，一次性跳到 p2j[p] 里所有未访问的下标（相当于所有含相同质因子的下标互相连通）。4) 关键优化：某个质数对应的下标列表一旦被用过一次就 clear()，因为这些边已经在同一 BFS 层被使用过，避免重复扫描导致复杂度退化。

**Evidence**

spf 预处理 + p2j = defaultdict(list) 收集质因子对应下标 + BFS 中 `p2j[v].clear()` 优化，来自提交代码。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3629%20-%20Minimum%20Jumps%20to%20Reach%20End%20via%20Prime%20Teleportation)
