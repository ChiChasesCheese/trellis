---
id: leetcode-c-endlesscheng-sqopeo-binary-search-minimize-maximum-invariant
node: binary-search.binary-search-minimize-maximum
type: cloze
anki: 1787272401807
tags: [concept-cloze, invariant, leetcode, recall]
---
最小化最大值中，mid 代表一个{{c1::上界（盖子）}}，check(mid) 判断该上界是否能{{c2::压住}}所有子问题的最大值。

check(mid) 表示上界为 mid 时能否满足分配要求，mid 越大越容易满足

**Evidence**

§2.4 最小化最大值

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.06%20-%20%E6%9C%80%E5%B0%8F%E5%8C%96%E6%9C%80%E5%A4%A7%E5%80%BC%EF%BC%88%E4%BA%8C%E5%88%86%E4%B8%8A%E7%95%8C%EF%BC%89)
