---
id: leetcode-q-stone-game-v-pattern
node: dp-game-probability.game-theory
type: qa
anki: 1787102261482
tags: [lc::1563, leetcode, pattern, recall]
---
## Q
区间 DP 中，若某一维的转移候选值只依赖“留下的那半区间”而与另一端点无关，如何把 O(n³) 优化到 O(n²)？（以 Stone Game V 为例）

## A
把候选值按“左端点固定、右端点变化”和“右端点固定、左端点变化”拆成两族，分别预处理成前缀 max 表 L[l][r]=max_{j∈[l..r]}(sum(l..j)+f[l][j]) 和后缀 max 表 R[l][r]=max_{j∈[l..r]}(sum(j..r)+f[j][r])。由于石头值恒正，sum(l..k) 随 k 单调递增，使得“左半更小”对应的切点集合必是前缀区间、“右半更小”对应后缀区间，分界点 m 随 r 增大单调右移，可用双指针 O(1) 摊销维护，无需二分。循环顺序由依赖关系决定：L 依赖同行左边（r 需递增），R 依赖下一行（l 需递减），两者不冲突，一次“l 倒序、r 正序”的双层循环即可算完，总复杂度 O(n²)。

**Evidence**

代码注释：“左半被留下 → 项 = sum(l..k)+f[l][k] 只含(l,k)，与r无关”“右半被留下 → 项只含(k+1,r)，与l无关”；以及双指针推进 `while 2*(s[m+1]-s[l]) < total: m += 1` 与 L/R 表的定义和更新逻辑。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1563%20-%20Stone%20Game%20V)
