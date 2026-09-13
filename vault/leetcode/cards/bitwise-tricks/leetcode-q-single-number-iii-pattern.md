---
id: leetcode-q-single-number-iii-pattern
node: bitwise-tricks.bit-manipulation
type: qa
anki: 1787102262007
tags: [lc::260, leetcode, pattern, recall]
---
## Q
数组中恰好两个元素各出现一次、其余都出现两次，如何用 O(n) 时间 O(1) 空间找出这两个数？（Single Number III）

## A
1) 对全体元素异或得到 bitmask = a ^ b（两个目标数的异或）；2) 取 diff = bitmask & (-bitmask)，得到 a、b 二进制中某一个不同的最低位（利用补码性质分离出最低设置位）；3) 按该位是否为 1 把所有数分两组，各组内异或即可分别还原 a 和 b。核心不变量：diff 这一位上 a 和 b 必然一个是 0 一个是 1，而其余相同元素成对出现会在各自分组内相互抵消，不影响结果。

**Evidence**

singleNumber 方法：bitmask = reduce(xor, nums, 0); diff = bitmask & (-bitmask); 按 num & diff 分组后异或得 x 和 bitmask ^ x

[原文 ↗](obsidian://open?vault=lc&file=questions%2F260%20-%20Single%20Number%20III)
