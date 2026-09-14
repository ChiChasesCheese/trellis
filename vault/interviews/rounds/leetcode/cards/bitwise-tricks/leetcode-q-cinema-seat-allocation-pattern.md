---
id: leetcode-q-cinema-seat-allocation-pattern
node: bitwise-tricks.bit-manipulation
type: qa
anki: 1787268624915
tags: [lc::1386, leetcode, pattern, recall]
---
## Q
如何用位运算(bitmask)判断某一行座位能容纳几个 4 人组(seats 2-5, 4-7, 6-9)?

## A
把每行已预订的座位压缩成一个 10 位 bitmask(bit i 表示座位 i+1)。预定义三个区间的 mask:left=座位2-5, mid=座位4-7, right=座位6-9。用 (mask & interval_mask) == 0 判断该区间是否全空。注意 mid 与 left/right 有重叠(座位4,5,6,7),所以只有在 left 和 right 都不可用时才能用 mid,避免重复占用同一批座位。没有任何预订记录的行必然能坐 2 组(left+right)。只需对有预订记录的行(用 hash map 存储,而非开长度为 n 的数组)单独计算,其余行数直接乘 2,这样处理 n 达到 1e9 也不会超内存。

**Evidence**

left_mask/mid_mask/right_mask 的定义与 valid_mid = ... and not (valid_left or valid_right) 的写法,以及用 defaultdict(int) 存储 row->mask 而非长度为 n 的数组,并用 (n - len(row_map)) * 2 处理未出现的行。

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F1386%20-%20Cinema%20Seat%20Allocation)
