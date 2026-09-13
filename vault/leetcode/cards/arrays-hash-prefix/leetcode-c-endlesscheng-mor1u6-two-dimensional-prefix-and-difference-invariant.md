---
id: leetcode-c-endlesscheng-mor1u6-two-dimensional-prefix-and-difference-invariant
node: arrays-hash-prefix.two-dimensional-prefix-and-difference
type: cloze
anki: 1789002113170
tags: [concept-cloze, invariant, leetcode, recall]
---
一维区间加 [l,r] 的差分终止操作是 {{c1::diff[r+1]-=v}}。

二维前缀 s[i][j] 表示原矩阵左上 [0,i)×[0,j)；矩形和使用四项容斥；差分的前缀还原后才是实际值

**Evidence**

§2.1 一维差分

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.04%20-%20%E4%BA%8C%E7%BB%B4%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E4%BA%8C%E7%BB%B4%E5%B7%AE%E5%88%86)
