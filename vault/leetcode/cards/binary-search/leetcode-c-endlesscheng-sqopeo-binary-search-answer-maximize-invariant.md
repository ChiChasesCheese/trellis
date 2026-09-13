---
id: leetcode-c-endlesscheng-sqopeo-binary-search-answer-maximize-invariant
node: binary-search.binary-search-answer-maximize
type: cloze
anki: 1787272401205
tags: [concept-cloze, invariant, leetcode, recall]
---
求最大值的开区间二分中，check(left) 恒为 {{c1::True}}，check(right) 恒为 {{c2::False}}。

循环全程 check(left) 恒为 True，check(right) 恒为 False；循环结束时 left+1==right，答案为 left

**Evidence**

§2.2 求最大

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.04%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88%E6%B1%82%E6%9C%80%E5%A4%A7%E5%80%BC%EF%BC%88%E5%BC%80%E5%8C%BA%E9%97%B4%E6%A8%A1%E6%9D%BF%EF%BC%89)
