---
id: leetcode-q-stone-game-ii-pattern
node: dp-game-probability.zero-sum-game
type: qa
anki: 1787175410011
tags: [lc::1140, leetcode, pattern, recall]
---
## Q
博弈 DP（如 Stone Game II）中，状态 (idx, M) 下如何用递归同时算出双方最优差值，而不是分别写两个玩家的 DP？

## A
利用零和博弈性质：dfs(idx, m) 定义为「当前玩家能获得的石子数 - 对手在剩余局面下能获得的最大石子数」。转移时枚举 x∈[1,2m]：diff = presum(idx,idx+x) - dfs(idx+x, max(m,x))，取所有 x 中的最大 diff。终止条件是 idx+2m>=n 时可直接拿走剩余全部石子。最终答案 = (总石子数 + dfs(0,1)) // 2，因为 dfs(0,1) = Alice石子 - Bob石子，两者之和是总数，联立可解出 Alice 的石子数。核心技巧：用前缀和 O(1) 查询区间和，避免博弈 DP 写成难以维护的双人对称结构。

**Evidence**

@cache
def dfs(idx, m):
 if idx + 2*m >= n: return pre_piles[n]-pre_piles[idx]
 for x in range(1, 2*m+1):
 diff = pre_piles[idx+x]-pre_piles[idx] - dfs(idx+x, max(m,x))
 res = max(res, diff)
 return res
return (pre_piles[n] + dfs(0,1)) // 2

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1140%20-%20Stone%20Game%20II)
