---
id: leetcode-q-hamming-distance-pattern
node: bitwise-tricks.bit-manipulation
type: qa
anki: 1787268625561
tags: [lc::461, leetcode, pattern, recall]
---
## Q
如何求两个整数的 Hamming Distance（汉明距离）？

## A
先对两数做异或 x ^ y，得到的结果中每一位为1的地方就是两数不同的二进制位；再统计这个异或结果中1的个数（popcount）即为汉明距离。Python 可直接用 (x ^ y).bit_count()；若手写，则可用逐位右移比较 (x & 1) != (y & 1) 的方式累加计数。

**Evidence**

def hammingDistance(self, x: int, y: int) -> int:
 return (x ^ y).bit_count()

[原文 ↗](obsidian://open?vault=lc&file=questions%2F461%20-%20Hamming%20Distance)
