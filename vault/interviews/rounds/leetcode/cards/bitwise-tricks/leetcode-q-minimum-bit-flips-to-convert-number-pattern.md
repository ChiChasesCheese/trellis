---
id: leetcode-q-minimum-bit-flips-to-convert-number-pattern
node: bitwise-tricks.bit-manipulation
type: qa
anki: 1787175410433
tags: [lc::2220, leetcode, pattern, recall]
---
## Q
如何求把 start 变成 goal 所需的最少 bit flip 次数？

## A
先对 start ^ goal 做异或，得到所有不同位的掩码，答案就是这个掩码中 1 的个数（popcount）。可以用 bin() 统计、内置 bit_count()，或用 Brian Kernighan 算法（每次 x &= x - 1 消去最低位的 1，循环计数）逐位剥离统计。

**Evidence**

minBitFlips1: return (start ^ goal).bit_count()；minBitFlips (Brian Kernighan): x = start ^ goal; while x: x &= x - 1; res += 1

[原文 ↗](obsidian://open?vault=lc&file=questions%2F2220%20-%20Minimum%20Bit%20Flips%20to%20Convert%20Number)
