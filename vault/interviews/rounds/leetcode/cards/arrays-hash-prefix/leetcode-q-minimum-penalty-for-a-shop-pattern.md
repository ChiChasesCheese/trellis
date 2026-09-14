---
id: leetcode-q-minimum-penalty-for-a-shop-pattern
node: arrays-hash-prefix.prefix-sum
type: qa
anki: 1787776730876
tags: [lc::2483, leetcode, pattern, recall]
---
## Q
前后缀分解模板：如何用两个数组同时统计「前半部分满足条件A的数量」和「后半部分满足条件B的数量」？

## A
定义 left_no[i] = customers[0..i) 中 'N' 的个数（前缀和），right_yes[i] = customers[i..n) 中 'Y' 的个数（后缀和）。分别正向和反向遍历一次预处理出来，然后枚举分割点 i（0 到 n），答案 = min(left_no[i] + right_yes[i])，因为关店时间 i 之前的 'N'（本可以不营业却开着）和之后的 'Y'（该营业却关了）都是惩罚。

**Evidence**

left_no, right_yes = [0]*(n+1), [0]*(n+1); for i in range(n): left_no[i+1] = left_no[i] + int(customers[i]=='N'); for i in range(n-1,-1,-1): right_yes[i] = right_yes[i+1] + int(customers[i]=='Y'); return min(range(n+1), key=lambda i: left_no[i]+right_yes[i])

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F2483%20-%20Minimum%20Penalty%20for%20a%20Shop)
