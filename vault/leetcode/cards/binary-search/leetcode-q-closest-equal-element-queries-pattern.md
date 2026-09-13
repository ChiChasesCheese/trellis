---
id: leetcode-q-closest-equal-element-queries-pattern
node: binary-search.binary-search
type: qa
anki: 1787102262557
tags: [lc::3488, leetcode, pattern, recall]
---
## Q
如何用二分查找快速求循环数组中「同值最近位置」的距离（如 LC 3488 Closest Equal Element Queries）？

## A
先用哈希表记录每个值出现的下标列表 pos[v]（按序）。为处理循环特性，对每个列表首尾各补一个哨兵：在开头插入 p[-1]-n（上一圈的最后一个位置），在末尾插入 p[0]+n（下一圈的第一个位置）。查询下标 q 时，用 bisect_left 在该值的位置列表中定位 q，答案就是 min(arr[idx+1]-arr[idx], arr[idx]-arr[idx-1])。若某值只出现 1 次（补哨兵后长度为 3），直接返回 -1。核心不变量：补哨兵后数组严格递增，且首尾哨兵天然处理了循环边界，无需单独判断绕圈。时间复杂度 O(n + q log n)，空间 O(n)。

**Evidence**

pos[p].insert(0, p[-1]-n); p.append(x+n) 处理循环边界；用 bisect_left 定位后取 min(arr[idx+1]-arr[idx], arr[idx]-arr[idx-1])；len(arr)==3 时返回 -1（原始只出现一次）。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3488%20-%20Closest%20Equal%20Element%20Queries)
