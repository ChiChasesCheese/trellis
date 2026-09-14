---
id: leetcode-q-max-sum-of-a-pair-with-equal-sum-of-digits-pattern
node: advanced-ds-heap.heap-priority-queue
type: qa
anki: 1787354596430
tags: [lc::2342, leetcode, pattern, recall]
---
## Q
数组中找『数位和相等的两数之和』的最大值，如何用一次遍历（不排序、不存全部数字）解决？

## A
按数位和分组，用哈希表 sum2largest 只保存每个数位和当前见过的最大值。遍历每个数：先算出它的数位和 total；如果 total 已在哈希表中，说明找到一对，用 sum2largest[total] + num 更新答案；然后无论是否命中，都用 max(旧值, num) 更新 sum2largest[total]。这样只需一次遍历、O(n) 时间、O(n) 额外空间，比对每组用堆取 top2（sum2num + heapq.nlargest）更省内存和代码量。

**Evidence**

maximumSum 方法：for num in nums: total = sum(int(d) for d in str(num)); if total in sum2largest: res = max(res, sum2largest[total] + num); sum2largest[total] = max(sum2largest[total], num) else: sum2largest[total] = num

[原文 ↗](obsidian://open?vault=lc&file=questions%2F2342%20-%20Max%20Sum%20of%20a%20Pair%20With%20Equal%20Sum%20of%20Digits)
