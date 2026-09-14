---
id: leetcode-c-endlesscheng-k0n2go-subset-partition-combination-backtracking-template
node: backtracking-search.subset-partition-combination-backtracking
type: cloze
anki: 1787272446306
tags: [concept-cloze, leetcode, recall, template]
---
选择 nums[i] 后，下层搜索起点应为 {{c1::i + 1}}。

从而不重用元素且避免排列重复。

**Evidence**

§4.4 组合型回溯

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F11.21%20-%20%E5%AD%90%E9%9B%86%E3%80%81%E5%88%92%E5%88%86%E4%B8%8E%E7%BB%84%E5%90%88%E5%9B%9E%E6%BA%AF)
