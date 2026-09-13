---
id: leetcode-c-endlesscheng-sqopeo-binary-search-maximize-minimum-invariant
node: binary-search.binary-search-maximize-minimum
type: cloze
anki: 1787272402104
tags: [concept-cloze, invariant, leetcode, recall]
---
最大化最小值中，mid 代表一个{{c1::下界}}，check(mid) 判断是否存在方案使所有子问题的最小值都{{c2::不低于 mid}}。

check(mid) 表示下界为 mid 时能否满足要求，mid 越小越容易满足

**Evidence**

§2.5 最大化最小值

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.07%20-%20%E6%9C%80%E5%A4%A7%E5%8C%96%E6%9C%80%E5%B0%8F%E5%80%BC%EF%BC%88%E4%BA%8C%E5%88%86%E4%B8%8B%E7%95%8C%EF%BC%89)
