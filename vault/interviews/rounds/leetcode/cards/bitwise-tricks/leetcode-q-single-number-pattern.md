---
id: leetcode-q-single-number-pattern
node: bitwise-tricks.bit-manipulation
type: qa
anki: 1787102261408
tags: [lc::136, leetcode, pattern, recall]
---
## Q
给定一个整数数组，除某一个元素只出现一次外，其余每个元素均出现两次，如何用 O(n) 时间、O(1) 空间找出这个只出现一次的元素？

## A
对数组所有元素做异或（XOR）归约：相同的数异或为 0，0 异或任何数等于该数本身，因此成对出现的元素两两抵消，最终剩下的就是只出现一次的元素。核心性质：x^x=0，x^0=x，异或满足交换律和结合律。

**Evidence**

def singleNumber0(self, nums: List[int]) -> int:
 return reduce(lambda acc, x: acc ^ x, nums, 0)

[原文 ↗](obsidian://open?vault=lc&file=questions%2F136%20-%20Single%20Number)
