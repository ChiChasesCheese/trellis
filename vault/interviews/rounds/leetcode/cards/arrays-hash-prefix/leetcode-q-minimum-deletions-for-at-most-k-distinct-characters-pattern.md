---
id: leetcode-q-minimum-deletions-for-at-most-k-distinct-characters-pattern
node: arrays-hash-prefix.counting
type: qa
anki: 1787102262609
tags: [lc::3545, leetcode, pattern, recall]
---
## Q
给定字符串 s 和整数 k，要求删除最少字符使得剩余字符串中不同字符种类数 ≤ k，如何贪心求解？

## A
统计每个字符的出现频次，把频次数组从小到大排序；若不同字符种类数 count 超过 k，就删掉频次最小的 (count - k) 个字符对应的全部出现次数（即累加最小的那几个频次），因为要保留 k 种字符时，删除总数最少的策略必然是舍弃出现频次最低的那些字符类别。复杂度 O(n + m log m)，m 为不同字符数。

**Evidence**

freqs = sorted(Counter(s).values()); return sum(freqs[:len(freqs) - k]) if len(freqs) > k else 0

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3545%20-%20Minimum%20Deletions%20for%20At%20Most%20K%20Distinct%20Characters)
