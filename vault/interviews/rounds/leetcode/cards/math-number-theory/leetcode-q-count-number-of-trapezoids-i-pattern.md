---
id: leetcode-q-count-number-of-trapezoids-i-pattern
node: math-number-theory.geometry
type: qa
anki: 1787354597157
tags: [lc::3623, leetcode, pattern, recall]
---
## Q
如何统计“跨分组配对数量”这类问题(例如:按 y 分组统计点对，再统计不同组线段两两组合的梯形数)？

## A
先按分组(如 y 值)统计每组可配对数 k = C(c,2)(c 为组内元素数)。然后按分组顺序遍历，维护前缀和 s(已遍历组的 k 之和)，对当前组做 res += s * k，再 s += k。这等价于 C(S,2) - Σ C(m_i,2)(S 为所有 k 之和)，但只需一次遍历、O(n) 完成，不需要两两组合分组或额外做减法容斥。

**Evidence**

代码中给出两个版本：countTrapezoids0 先算出每行线段数列表 m_list，再用 S*(S-1)//2 - Σ m*(m-1)//2 的容斥方式；countTrapezoids 用 Counter 统计后单次遍历，靠 res += s*k; s += k 的前缀和累积方式得到同样结果，更简洁直接。

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F3623%20-%20Count%20Number%20of%20Trapezoids%20I)
