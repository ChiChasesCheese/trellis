---
id: leetcode-c-endlesscheng-luu0kb-prefix-suffix-and-difference-array-invariant
node: arrays-hash-prefix.prefix-suffix-and-difference-array
type: cloze
anki: 1787272456779
tags: [concept-cloze, invariant, leetcode, recall]
---
对闭区间 [l, r] 加 delta 的差分更新是 diff[l]+=delta，并在 {{c1::diff[r+1]-=delta}} 撤销。

prefix[i] 只由 i 左侧或含 i 的定义区域得到；suffix[i] 只由 i 右侧或含 i 的定义区域得到；差分前缀和恢复后等于所有覆盖该点的更新之和

**Evidence**

一、技巧类题目：差分数组

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.04%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E5%88%86%E8%A7%A3%E4%B8%8E%E5%B7%AE%E5%88%86%E6%95%B0%E7%BB%84)
