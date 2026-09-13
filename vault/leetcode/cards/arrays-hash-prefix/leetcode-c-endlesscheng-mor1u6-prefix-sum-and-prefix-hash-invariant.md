---
id: leetcode-c-endlesscheng-mor1u6-prefix-sum-and-prefix-hash-invariant
node: arrays-hash-prefix.prefix-sum-and-prefix-hash
type: cloze
anki: 1789002112794
tags: [concept-cloze, invariant, leetcode, recall]
---
统计和为 target 的子数组时，初始计数必须有 {{c1::0: 1}}。

pre[0]=0；处理右端前，计数表包含所有此前前缀状态；区间 [l,r) 的和为 pre[r]-pre[l]

**Evidence**

§1.2 前缀和与哈希表

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.03%20-%20%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%89%8D%E7%BC%80%E7%8A%B6%E6%80%81%E5%93%88%E5%B8%8C)
