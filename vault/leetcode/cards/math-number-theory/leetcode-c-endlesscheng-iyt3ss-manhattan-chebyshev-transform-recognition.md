---
id: leetcode-c-endlesscheng-iyt3ss-manhattan-chebyshev-transform-recognition
node: math-number-theory.manhattan-chebyshev-transform
type: cloze
anki: 1787272429906
tags: [concept-cloze, leetcode, recall, recognition]
---
二维点集的最大曼哈顿距离，可转化为维护 {{c1::x+y 与 x-y 的极差}}。

二维曼哈顿距离可通过 u=x+y、v=x-y 旋转变换为切比雪夫距离，从而用坐标极值求最远距离。

**Evidence**

§7.3 曼哈顿距离与切比雪夫距离

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.18%20-%20%E6%9B%BC%E5%93%88%E9%A1%BF%E8%B7%9D%E7%A6%BB%E4%B8%8E%E5%88%87%E6%AF%94%E9%9B%AA%E5%A4%AB%E8%B7%9D%E7%A6%BB%E5%8F%98%E6%8D%A2)
