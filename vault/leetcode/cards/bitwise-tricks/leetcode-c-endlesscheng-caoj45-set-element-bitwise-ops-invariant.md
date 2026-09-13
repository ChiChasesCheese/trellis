---
id: leetcode-c-endlesscheng-caoj45-set-element-bitwise-ops-invariant
node: bitwise-tricks.set-element-bitwise-ops
type: cloze
anki: 1787272453180
tags: [concept-cloze, invariant, leetcode, recall]
---
设全集大小为 n，集合 s 的补集用位运算表示为 {{c1::((1 << n) - 1) ^ s}}，因为需要先构造出恰好 n 位全 1 的全集掩码再与 s 做异或。

(1<<n)-1 是构造 n 位全 1 掩码的标准写法。

**Evidence**

二、集合与元素

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.02%20-%20%E9%9B%86%E5%90%88%E4%B8%8E%E5%8D%95%E4%B8%AA%E5%85%83%E7%B4%A0%E7%9A%84%E4%BD%8D%E8%BF%90%E7%AE%97)
