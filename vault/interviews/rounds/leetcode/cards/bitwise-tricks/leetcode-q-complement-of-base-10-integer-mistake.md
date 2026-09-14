---
id: leetcode-q-complement-of-base-10-integer-mistake
node: bitwise-tricks.bit-manipulation
type: qa
anki: 1787175625257
tags: [lc::1009, leetcode, mistake, recall]
---
## Q
用 n.bit_length() 求按位补数时，为什么必须单独特判 n == 0？

## A
因为 0 的二进制表示长度 n.bit_length() 返回 0（不是 1），若不特判，掩码会算成 (1<<0)-1 = 0，导致补数计算错误。必须在函数开头判断 if n == 0: return 1。

**Evidence**

代码注释：'if n == 0: # 0 的二进制长度是0，不是1，会导致下面默认return出错 return 1'

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1009%20-%20Complement%20of%20Base%2010%20Integer)
