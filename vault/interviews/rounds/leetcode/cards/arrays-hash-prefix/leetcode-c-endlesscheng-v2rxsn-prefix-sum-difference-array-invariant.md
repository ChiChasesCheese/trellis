---
id: leetcode-c-endlesscheng-v2rxsn-prefix-sum-difference-array-invariant
node: arrays-hash-prefix.prefix-sum-difference-array
type: cloze
anki: 1787272463380
tags: [concept-cloze, invariant, leetcode, recall]
---
闭区间 [l,r] 加 v 的差分更新是 diff[l]+=v 与 {{c1::diff[r+1]-=v}}。

prefix[i] 表示前 i 个元素的聚合值；对闭区间 [l,r] 加 v 后，diff[l]+=v 且 diff[r+1]-=v

**Evidence**

一、技巧类题目：差分

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.03%20-%20%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%B7%AE%E5%88%86)
