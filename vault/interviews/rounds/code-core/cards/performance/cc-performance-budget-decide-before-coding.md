---
id: cc-performance-budget-decide-before-coding
node: performance.budget
type: qa
---
## Q
You are 40 minutes into a 60-minute round. The final part adds a performance test, and your working solution re-scans a list on every event. What did skipping the minute-5 decision cost, and what is the discipline?

## A
**Complexity is a design decision, not an optimisation.** Retrofitting a heap, an index or a running aggregate changes the shape of your state, which invalidates the parts you already locked — typically 10–15 minutes plus the risk of breaking tests that were passing.

- At minute 5, once you have read every part, name the hot operation and the structure that makes it fast, and build that state from the start ([[cc-performance-budget-from-n]]).
- If the clock beats you, ship the slow version *working*: a correct O(n²) that passes 15 of 20 tests scores; a half-migrated heap scores nothing.

## Q zh
60 分钟的一轮已经过去 40 分钟。最后一部分加了性能测试，而你能跑的方案每个事件都要重扫一遍列表。跳过第 5 分钟那个决定的代价是什么？纪律是什么？

## A zh
**复杂度是设计决策，不是优化。** 事后塞进一个堆、一个索引或一个增量聚合，会改变状态的形状，从而作废你已经锁定的部分 —— 通常是 10–15 分钟，外加把原本通过的测试改挂的风险。

- 在第 5 分钟、读完所有 part 之后，点名热点操作和让它变快的结构，然后一开始就照那个形状建状态（[[cc-performance-budget-from-n]]）。
- 如果时钟赢了，就把慢的版本**能跑地**交上去：一个正确的 O(n²) 过 20 个测试里的 15 个是有分的；一个改到一半的堆一分没有。
