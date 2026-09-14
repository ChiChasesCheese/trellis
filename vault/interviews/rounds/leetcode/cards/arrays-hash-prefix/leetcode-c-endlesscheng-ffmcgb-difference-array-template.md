---
id: leetcode-c-endlesscheng-ffmcgb-difference-array-template
node: arrays-hash-prefix.difference-array
type: cloze
anki: 1787272452380
tags: [concept-cloze, leetcode, recall, template]
---
差分数组模板中，处理完所有区间查询后，若 right+1 < n 需要执行 {{c1::diff[right + 1] -= x}}，最后用一层 for 循环执行 {{c2::diff[i] += diff[i - 1]}} 完成还原。

对应 solve(n, queries) 模板中的关键两行。

**Evidence**

代码模板

[原文 ↗](obsidian://open?vault=lc&amp;file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F14.01%20-%20%E5%B7%AE%E5%88%86%E6%95%B0%E7%BB%84)
