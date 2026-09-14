---
id: leetcode-q-number-complement-pattern
node: bitwise-tricks.bit-manipulation
type: qa
anki: 1787268625663
tags: [lc::476, leetcode, pattern, recall]
---
## Q
如何求一个整数 num 的按位补数（Number Complement）？核心技巧是什么？

## A
先用 num.bit_length() 得到 num 二进制表示的位数，构造一个同样位数、全为1的掩码 mask = (1 << num.bit_length()) - 1；补数就是 mask - num（等价于 mask ^ num，也等价于 (-num - 1) & mask）。关键在于补数只在 num 的有效位数内取反，不能直接对 num 做全局按位取反（~num 会翻转所有位，包括更高位的隐含符号位）。

**Evidence**

findComplement1: `return ((1 << num.bit_length())) - 1 - num`；以及等价写法 findComplement0: `return (-num - 1) & ((1 << num.bit_length()) - 1)`

[原文 ↗](obsidian://open?vault=lc&file=questions%2F476%20-%20Number%20Complement)
