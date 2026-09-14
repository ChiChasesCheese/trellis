---
id: leetcode-c-endlesscheng-caoj45-enumerate-all-subsets-bitmask-template
node: dp-grid-interval-string.enumerate-all-subsets-bitmask
type: cloze
anki: 1787272454180
tags: [concept-cloze, leetcode, recall, template]
---
枚举全集所有子集的标准 Python 写法是 for s in {{c1::range(1 << n)}}: ，循环次数固定为 {{c2::2**n}}。

该写法是所有状压枚举模板的起点。

**Evidence**

§4.1 枚举所有集合

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.05%20-%20%E6%9E%9A%E4%B8%BE%E5%85%A8%E9%9B%86%E7%9A%84%E6%89%80%E6%9C%89%E5%AD%90%E9%9B%86%EF%BC%88%E7%8A%B6%E5%8E%8B%E6%9E%9A%E4%B8%BE%E5%9F%BA%E7%A1%80%EF%BC%89)
