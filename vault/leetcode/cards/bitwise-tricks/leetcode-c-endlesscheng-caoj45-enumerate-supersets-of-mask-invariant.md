---
id: leetcode-c-endlesscheng-caoj45-enumerate-supersets-of-mask-invariant
node: bitwise-tricks.enumerate-supersets-of-mask
type: cloze
anki: 1787272454980
tags: [concept-cloze, invariant, leetcode, recall]
---
枚举超集时通过按位或 | 强制保留 t 的所有元素，保证生成的每个 s 都满足 {{c1::t 是 s 的子集}}。

这一点与枚举子集的思路正好相反，用 | 代替 &。

**Evidence**

§4.4 枚举超集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.08%20-%20%E6%9E%9A%E4%B8%BE%E7%BB%99%E5%AE%9A%E9%9B%86%E5%90%88%E7%9A%84%E8%B6%85%E9%9B%86)
