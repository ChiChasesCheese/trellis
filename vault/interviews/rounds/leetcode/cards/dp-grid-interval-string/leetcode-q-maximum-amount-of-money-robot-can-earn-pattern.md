---
id: leetcode-q-maximum-amount-of-money-robot-can-earn-pattern
node: dp-grid-interval-string.matrix
type: qa
anki: 1787102262408
tags: [lc::3418, leetcode, pattern, recall]
---
## Q
网格图 DP + 有限次「中和」操作（如最多消除k次负数格子）该如何建模状态？

## A
在标准的 dp(i,j) 基础上加一维 k 表示剩余中和次数：dp(i,j,k) = max(不中和: dp(i+1,j,k)/dp(i,j+1,k) + coins[i][j], 中和(仅当 coins[i][j]<0 且 k>0): dp(i+1,j,k-1)/dp(i,j+1,k-1))。终点特判：若 k>0 则可将终点负数也归零。用手动构造的三维数组做 memo（而非 functools.cache），避免闭包缓存的额外开销。

**Evidence**

def dfs(i,j,k): ... res = max(dfs(i+1,j,k), dfs(i,j+1,k)) + x; if k>0 and x<0: res = max(res, dfs(i+1,j,k-1), dfs(i,j+1,k-1))；终点处理 return max(0,x) if k>0 else x

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3418%20-%20Maximum%20Amount%20of%20Money%20Robot%20Can%20Earn)
