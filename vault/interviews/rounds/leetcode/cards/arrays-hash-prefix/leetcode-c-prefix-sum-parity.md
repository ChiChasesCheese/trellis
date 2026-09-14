---
id: leetcode-c-prefix-sum-parity
node: arrays-hash-prefix.prefix-sum-parity
type: cloze
anki: 1787102263561
tags: [concept-cloze, leetcode, recall]
---
在计数满足条件子数组的前缀和技巧中，将原数组转化为 {{c1::±1}} 序列（符合条件记为+1，不符合记为-1）后，子数组[i,j]满足条件当且仅当 {{c2::pre[j] - pre[i] > 0}}（即区间和为正）。

累积和数组初始为0（长度为n+1），因此计数满足条件的子数组等价于统计满足 pre[j] > pre[i] 且 i < j 的下标对数，可用哈希表/BIT/归并排序在O(n log n)或O(n)内完成，避免O(n²)枚举子数组。

**Evidence**

转化为01序列（1表示符合，0表示不符）；pre_freq[j] - pre_freq[i] > 0 ⟹ [i, j]满足条件

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E5%89%8D%E7%BC%80%E5%92%8C%E5%A5%87%E5%81%B6%E8%AE%A1%E6%95%B0)
