---
id: leetcode-c-endlesscheng-caoj45-set-element-bitwise-ops-template
node: bitwise-tricks.set-element-bitwise-ops
type: cloze
anki: 1787272453280
tags: [concept-cloze, leetcode, recall, template]
---
从集合 s 中删除一个已知存在的元素 i，最简洁的写法是 s {{c1::^= (1 << i)}}；若不确定 i 是否在 s 中，则必须写成 s {{c2::&= ~(1 << i)}} 以保证结果始终正确。

两种删除写法在 i 确实属于 s 时结果相同，但语义安全性不同。

**Evidence**

二、集合与元素

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.02%20-%20%E9%9B%86%E5%90%88%E4%B8%8E%E5%8D%95%E4%B8%AA%E5%85%83%E7%B4%A0%E7%9A%84%E4%BD%8D%E8%BF%90%E7%AE%97)
