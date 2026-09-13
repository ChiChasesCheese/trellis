---
id: leetcode-c-kadane-variant
node: arrays-hash-prefix.kadane-variant
type: cloze
anki: 1787102263408
tags: [concept-cloze, leetcode, recall]
---
在股票买卖一次求最大利润问题中，将 prices 转化为相邻差分数组后，用 Kadane 思想求最大子数组和；核心递推是 cur = {{c1::max(0, cur + diff)}}，一旦 cur 被重置为 0 就代表{{c2::开始新的购买周期}}（放弃之前的负利差）。

diff[i] = prices[i] - prices[i-1]；例如 prices=[7,1,5,3,6,4] → diff=[-6,4,-2,3,-2]，Kadane 在差分数组上跑得到最大利润。若直接 cur = cur + diff 不做 max(0, ...) 截断，就退化成普通前缀和，无法丢弃亏损区间。

**Evidence**

cur = max(0, cur + prices[i] - prices[i-1])；Invariants: cur被重置为0表示开始新的购买周期；负利差会被舍弃（cur=max(0, ...)）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2FKadane%20%E7%AE%97%E6%B3%95%E5%8F%98%E5%BC%8F)
