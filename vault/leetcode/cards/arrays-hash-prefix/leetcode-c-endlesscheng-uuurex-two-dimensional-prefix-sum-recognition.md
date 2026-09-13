---
id: leetcode-c-endlesscheng-uuurex-two-dimensional-prefix-sum-recognition
node: arrays-hash-prefix.two-dimensional-prefix-sum
type: cloze
anki: 1787272452480
tags: [concept-cloze, leetcode, recall, recognition]
---
当需要对{{c1::不再被修改}}的矩阵进行{{c2::多次}}子矩阵元素和查询时，应预处理二维前缀和以将每次查询降到O(1)。

若矩阵会被频繁修改，需要改用二维树状数组/线段树而不是静态前缀和。

**Evidence**

模板代码

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F15.01%20-%20%E4%BA%8C%E7%BB%B4%E5%89%8D%E7%BC%80%E5%92%8C)
