---
id: problems-meeting-scheduler-merge-intervals-cost
node: problems.booking.meeting-scheduler
type: qa
step: 3
tags: [grown]
---
## Q
在会议室预订设计里，给一组与会人找公共空档时，为什么先用区间合并（merge intervals）算法把所有人的忙碌区间合并、再线性扫描找空档，而不是两两比较任意一对区间是否冲突？

## A
设这组人一共有 n 段忙碌区间，两两比较判断冲突是 O(n²)；先按起点排序（O(n log n)）、再一次线性扫描合并首尾相接或重叠的区间（O(n)），总复杂度是 O(n log n)，由排序主导。参会人数越多，两种复杂度的差距越明显——这是“先合并再扫描”在这道题里被选中的直接理由，而不是因为它听起来更优雅。
