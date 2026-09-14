---
id: leetcode-q-construct-uniform-parity-array-i-pattern
node: math-number-theory.math
type: qa
anki: 1788391211898
tags: [lc::3875, leetcode, pattern, recall]
---
## Q
脑筋急转弯类构造题：题目问「能否构造出某种数组」时，先想清楚极端情况——是否无论输入什么都恒成立？

## A
本题（Construct Uniform Parity Array I）看似要判断奇偶性分布是否满足构造条件，实际上对任意输入都恒为 True，直接 return True 即可通过。做这类题先花几秒判断答案是否是常数，避免把简单题写复杂。

**Evidence**

注释里写了完整的奇偶性分析（odd-odd=even, even-even=even, even-odd=odd 等），但最终提交代码只是 `return True`，且该题被打上 `脑筋急转弯` 列表标签，Runtime 0ms 通过。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3875%20-%20Construct%20Uniform%20Parity%20Array%20I)
