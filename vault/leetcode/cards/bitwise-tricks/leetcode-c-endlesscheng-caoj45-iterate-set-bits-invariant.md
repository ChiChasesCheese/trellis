---
id: leetcode-c-endlesscheng-caoj45-iterate-set-bits-invariant
node: bitwise-tricks.iterate-set-bits
type: cloze
anki: 1787272453779
tags: [concept-cloze, invariant, leetcode, recall]
---
逐位扫描遍历集合的时间复杂度固定为 {{c1::O(n)}}，与集合实际大小无关；lowbit 剥离法的时间复杂度为 {{c2::O(popcount(s))}}，只与集合大小有关。

选择哪种方法取决于 n 与集合实际大小谁更小。

**Evidence**

三、遍历集合

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.04%20-%20%E9%81%8D%E5%8E%86%E4%BD%8D%E5%8E%8B%E7%BC%A9%E9%9B%86%E5%90%88%E4%B8%AD%E7%9A%84%E5%85%83%E7%B4%A0)
