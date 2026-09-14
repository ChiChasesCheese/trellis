---
id: leetcode-c-endlesscheng-iyt3ss-floor-division-grouping-invariant
node: math-number-theory.floor-division-grouping
type: cloze
anki: 1787272426407
tags: [concept-cloze, invariant, leetcode, recall]
---
left 处的商 q=n//left 保持不变的最大右端是 {{c1::n//q}}。

若 q=n//left，则所有 i∈[left,n//q] 的商都等于 q；每次跳到 right+1，不会遗漏或重复索引

**Evidence**

§1.10 数论分块

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.06%20-%20%E6%95%B0%E8%AE%BA%E5%88%86%E5%9D%97)
