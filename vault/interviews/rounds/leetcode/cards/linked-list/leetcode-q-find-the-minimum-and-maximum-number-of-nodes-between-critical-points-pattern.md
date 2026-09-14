---
id: leetcode-q-find-the-minimum-and-maximum-number-of-nodes-between-critical-points-pattern
node: linked-list.linked-list
type: qa
anki: 1788391211698
tags: [lc::2058, leetcode, pattern, recall]
---
## Q
如何一次遍历找到链表的所有临界点（局部极大/极小值），并求出相邻临界点间的最小距离与首尾临界点间的最大距离？

## A
同时维护 prev、cur、cur.next 三个位置做比较：若 cur 同时大于（或小于）prev 和 cur.next，则 cur 是临界点。遍历中记录 first（第一个临界点下标）和 last（上一个临界点下标）：发现新临界点时先用 idx - last 更新 minD，再把 last 更新为 idx。遍历结束后 maxD = last - first。若临界点少于 2 个（first == last），返回 [-1, -1]。时间 O(n)，空间 O(1)。

**Evidence**

```
if (head.val < head.next.val and head.val < prev.val) or (head.val > head.next.val and head.val > prev.val):
    if first == -1:
        first = idx
    else:
        minD = min(minD, idx - last)
    last = idx
...
return [-1, -1] if first == last else [minD, last - first]
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F2058%20-%20Find%20the%20Minimum%20and%20Maximum%20Number%20of%20Nodes%20Between%20Critical%20Points)
