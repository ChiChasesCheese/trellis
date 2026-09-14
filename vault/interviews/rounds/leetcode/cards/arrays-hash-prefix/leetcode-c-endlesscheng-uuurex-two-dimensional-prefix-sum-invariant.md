---
id: leetcode-c-endlesscheng-uuurex-two-dimensional-prefix-sum-invariant
node: arrays-hash-prefix.two-dimensional-prefix-sum
type: cloze
anki: 1787272452579
tags: [concept-cloze, invariant, leetcode, recall]
---
查询子矩阵和时，用整体矩形减去上方和左方多余部分后，还需加回被重复减去一次的{{c1::左上角}}部分，这是二维版本的{{c2::容斥原理}}。

对应公式 s[r2][c2] - s[r2][c1] - s[r1][c2] + s[r1][c1]。

**Evidence**

模板代码

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F15.01%20-%20%E4%BA%8C%E7%BB%B4%E5%89%8D%E7%BC%80%E5%92%8C)
