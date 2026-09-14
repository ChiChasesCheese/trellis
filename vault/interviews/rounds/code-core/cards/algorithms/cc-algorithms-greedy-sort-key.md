---
id: cc-algorithms-greedy-sort-key
node: algorithms.greedy
type: qa
---
## Q
"Take as many non-overlapping meetings as possible." Which sort key, and why not the other two?

## A
**Sort by end time ascending.** Taking the earliest-finishing compatible meeting leaves the most room for everything after it, and the exchange argument is one line: any optimal schedule's first meeting can be replaced by the earliest-finishing one without losing anything ([[cc-algorithms-greedy-exchange-argument]]).

- By **start** time: one early meeting that runs all day blocks the rest.
- By **duration**: two short meetings can straddle a slot where one medium meeting would have let more in.
- The pattern generalizes — the whole algorithm usually *is* the sort key: deadline first for scheduling, value/weight ratio for fractional knapsack, largest-first for bin packing (a heuristic, not an optimum).
- Name the key and its justification in a comment. That sentence is what an interviewer probes, and what you will re-read when a later part changes the objective.

## Q zh
「尽可能多地选出互不重叠的会议。」用哪个排序 key，另外两个为什么不行？

## A zh
**按结束时间升序排。** 选择最早结束且相容的会议，给后面留下的空间最多，而交换论证只需一句：任何最优安排的第一个会议都可以替换成最早结束的那个而不损失什么（[[cc-algorithms-greedy-exchange-argument]]）。

- 按**开始**时间：一个开得早却占满整天的会议会挡住其余全部。
- 按**时长**：两个短会可能横跨一个本可以放进更多会议的时段。
- 这个模式可以推广 —— 整个算法通常*就是*那个排序 key：调度按截止时间、分数背包按价值重量比、装箱按从大到小（那是启发式，不是最优）。
- 把 key 及其理由写进注释。那句话正是面试官会追问的，也是后面某个 part 改变目标时你要回头读的。
