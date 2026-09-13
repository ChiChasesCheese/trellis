---
id: leetcode-q-confusing-number-pattern
node: math-number-theory.math
type: qa
anki: 1787175409683
tags: [lc::1056, leetcode, pattern, recall]
---
## Q
如何判断一个数字是否为 Confusing Number（旋转180度后变成不同的合法数字）？

## A
1. 只有数字 0,1,6,8,9 旋转后仍合法，其余数字（2,3,4,5,7）出现即直接返回 False。
2. 映射表：0→0, 1→1, 8→8, 6→9, 9→6。
3. 用 divmod(n,10) 逐位取出数字，这样得到的顺序天然就是原数倒序，直接映射后拼接即为旋转结果，无需额外反转。
4. 最后比较 旋转结果 != 原数，相等则不算 confusing。

**Evidence**

num2reverse = {'0':'0','1':'1','6':'9','8':'8','9':'6'}；注释「digits 已经是反转的顺序了」；return res != n

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1056%20-%20Confusing%20Number)
