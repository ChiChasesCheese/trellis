---
id: leetcode-c-endlesscheng-0vinmk-exactly-k-via-two-at-least-invariant
node: two-pointers-window.exactly-k-via-two-at-least
type: cloze
anki: 1787268627735
tags: [concept-cloze, invariant, leetcode, recall]
---
恰好型分解的核心等式是:恰好(=k) = 至少(>=k) - 至少({{c1::>=k+1}})。

恰好(=k) = 至少(>=k) - 至少(>=k+1)；等价地也可写成 至多(<=k) - 至多(<=k-1)；两次调用必须共用同一个solve函数,且solve内部逻辑必须具有单调性

**Evidence**

§2.3.3 恰好型滑动窗口

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.06%20-%20%E6%81%B0%E5%A5%BD%E5%9E%8B%E6%BB%91%E7%AA%97%E7%9A%84%E5%AE%B9%E6%96%A5%E5%88%86%E8%A7%A3)
