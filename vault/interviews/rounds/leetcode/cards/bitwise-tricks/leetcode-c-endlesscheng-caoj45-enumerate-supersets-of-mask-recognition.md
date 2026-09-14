---
id: leetcode-c-endlesscheng-caoj45-enumerate-supersets-of-mask-recognition
node: bitwise-tricks.enumerate-supersets-of-mask
type: cloze
anki: 1787272454881
tags: [concept-cloze, leetcode, recall, recognition]
---
当需要枚举某个集合 t 的所有超集（在大小为 n 的全集范围内）时，应使用 {{c1::s = (s + 1) | t}} 递推公式，而不是对全集所有子集逐一过滤。

直接过滤全集所有子集的复杂度是 O(2^n)，效率远低于该递推法。

**Evidence**

§4.4 枚举超集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.08%20-%20%E6%9E%9A%E4%B8%BE%E7%BB%99%E5%AE%9A%E9%9B%86%E5%90%88%E7%9A%84%E8%B6%85%E9%9B%86)
