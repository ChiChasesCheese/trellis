---
id: leetcode-c-endlesscheng-caoj45-iterate-set-bits-recognition
node: bitwise-tricks.iterate-set-bits
type: cloze
anki: 1787272453680
tags: [concept-cloze, leetcode, recall, recognition]
---
当集合是稀疏的（全集范围很大但集合内元素很少）时，遍历集合元素应优先选择 {{c1::lowbit 剥离法（t & -t）}}，而不是对 0..n-1 逐位扫描。

稀疏集合下逐位扫描会浪费大量时间在不存在的元素上。

**Evidence**

三、遍历集合

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.04%20-%20%E9%81%8D%E5%8E%86%E4%BD%8D%E5%8E%8B%E7%BC%A9%E9%9B%86%E5%90%88%E4%B8%AD%E7%9A%84%E5%85%83%E7%B4%A0)
