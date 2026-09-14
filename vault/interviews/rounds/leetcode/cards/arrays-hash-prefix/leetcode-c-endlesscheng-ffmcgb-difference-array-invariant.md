---
id: leetcode-c-endlesscheng-ffmcgb-difference-array-invariant
node: arrays-hash-prefix.difference-array
type: cloze
anki: 1787272452279
tags: [concept-cloze, invariant, leetcode, recall]
---
差分数组定义为 d[0]=a[0]，d[i]=a[i]-a[i-1]；对 a 的区间 [i,j] 整体加 x 等价于 {{c1::d[i] += x, d[j+1] -= x}}，最终通过对 d 做 {{c2::前缀和}} 还原出 a。

核心性质：区间操作 → 差分数组上的两个单点操作。

**Evidence**

定义和性质

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F14.01%20-%20%E5%B7%AE%E5%88%86%E6%95%B0%E7%BB%84)
