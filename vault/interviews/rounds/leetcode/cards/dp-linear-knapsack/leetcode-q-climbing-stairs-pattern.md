---
id: leetcode-q-climbing-stairs-pattern
node: dp-linear-knapsack.memoization
type: qa
anki: 1787613694050
tags: [lc::70, leetcode, pattern, recall]
---
## Q
爬楼梯问题（LeetCode 70）：为什么状态转移是 f(n) = f(n-1) + f(n-2)？如何把空间优化到 O(1)？

## A
组合意义：到达第 n 阶的最后一步只能是跨 1 阶（来自 f(n-1)）或跨 2 阶（来自 f(n-2)），两者互斥且覆盖所有情况，故 f(n)=f(n-1)+f(n-2)，本质是斐波那契数列。朴素递归会重复计算相同子问题（递归树中 f(n-2) 等子问题被多分支重复求解），可用记忆化消除重复，将时间复杂度从指数级降到 O(n)，空间 O(n)（递归栈/缓存表）。由于状态转移只依赖前两项，可用两个滚动变量代替整个数组/缓存表，将空间进一步优化到 O(1)，时间仍为 O(n)。

**Evidence**

fragment_prompt: 不写代码，口述爬楼梯问题：为什么状态转移是 f(n)=f(n-1)+f(n-2)，这个不变量对应什么组合意义？递归树的重复子问题在哪，记忆化如何消除，最终时间/空间复杂度多少，能否把空间优化到 O(1)？；topics: Math, Dynamic Programming, Memoization

[原文 ↗](obsidian://open?vault=lc&file=questions%2F70%20-%20Climbing%20Stairs)
