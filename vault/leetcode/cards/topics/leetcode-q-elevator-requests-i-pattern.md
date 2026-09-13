---
id: leetcode-q-elevator-requests-i-pattern
node: topics.uncategorised
type: qa
anki: 1787102262782
tags: [lc::4020, leetcode, pattern, recall]
---
## Q
电梯按顺序处理请求队列，求总耗时——用什么模式？

## A
贪心模拟：维护当前楼层 cur（初始 0），遍历 requests，每次耗时为 abs(cur - request)，累加后更新 cur = request。同层请求耗时为 0，无需特判提前判断。

**Evidence**

res = 0; cur = 0; for request in requests: if request != cur: res += abs(cur - request); cur = request

[原文 ↗](obsidian://open?vault=lc&file=questions%2F4020%20-%20Elevator%20Requests%20I)
