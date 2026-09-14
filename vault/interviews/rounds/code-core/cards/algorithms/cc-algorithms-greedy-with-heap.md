---
id: cc-algorithms-greedy-with-heap
node: algorithms.greedy
type: qa
---
## Q
The greedy choice is "the currently least loaded server", and every assignment changes the loads. What structure, and what must go into it?

## A
**Greedy plus a heap** — the sort key is re-evaluated as you go, so a priority queue replaces the sorted list.

- Pop the best, apply the choice, push the updated entry. A list sorted once is already wrong from the second assignment onward ([[cc-toolbox-sorted-maintain-vs-resort]]).
- **The tie-break must live in the heap key**, not in code after the pop: a heap gives you the minimum, never a second-best to compare against ([[cc-toolbox-heap-tuple-key]]).
- If the greedy choice must also satisfy a constraint, park the non-fitting candidates and restore them ([[cc-toolbox-heap-park-and-restore]]).
- Same shape elsewhere: meeting rooms (heap of end times), scheduling by deadline (heap of durations), merging k sorted streams, Dijkstra ([[cc-algorithms-shortest-path-dijkstra-heap]]) — Dijkstra *is* a greedy with a heap and a proof.

## Q zh
贪心选择是「当前负载最小的服务器」，而每次分配都会改变负载。用什么结构，里面必须放什么？

## A zh
**贪心加堆** —— 排序 key 会随着推进被重新求值，所以用优先队列取代有序列表。

- pop 出最优者、应用选择、push 更新后的条目。只排一次序的列表从第二次分配起就已经错了（[[cc-toolbox-sorted-maintain-vs-resort]]）。
- **tie-break 必须放进堆的 key 里**，而不是 pop 之后再写代码处理：堆只给你最小值，从不给你可比较的次优（[[cc-toolbox-heap-tuple-key]]）。
- 如果贪心选择还必须满足某个约束，就把装不下的候选寄存起来再放回去（[[cc-toolbox-heap-park-and-restore]]）。
- 其他同形态场景：会议室（结束时间的堆）、按截止时间调度（时长的堆）、归并 k 个有序流、Dijkstra（[[cc-algorithms-shortest-path-dijkstra-heap]]）—— Dijkstra *就是*一个带堆且带证明的贪心。
