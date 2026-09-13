---
id: leetcode-q-identify-the-largest-outlier-in-an-array-pattern
node: arrays-hash-prefix.enumeration
type: qa
anki: 1787354596907
tags: [lc::3371, leetcode, pattern, recall]
---
## Q
数组中，一部分数字之和等于另一部分的固定倍数关系（如“special 数字之和 = outlier 之外所有数的和”），如何枚举求解？

## A
先算总和 total 和每个数字出现次数的 Counter。枚举每个数 num 作为“离群值”候选：diff = total - num（即所有 special 数之和 + outlier 之和，这里 outlier = num 本身重复出现的另一份），若 diff 为奇数则跳过；否则 target = diff // 2 就是 special 数之和应满足的目标值，用哈希表判断 target 是否存在。注意去重陷阱：若 target == num，需要 cnt[target] >= 2 才合法（因为 num 本身已被排除在 special 集合外，需要另一个相同值来当 target）。时间复杂度 O(n)。

**Evidence**

for num in nums: diff = total - num; if diff % 2: continue; target = diff // 2; if target in cnt and (target != num or cnt[target] >= 2): res = max(res, num)

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3371%20-%20Identify%20the%20Largest%20Outlier%20in%20an%20Array)
