---
id: cc-model-ev-incremental-vs-replay
node: model.event-stream
type: qa
---
## Q
When do you maintain derived state incrementally, and when do you replay the whole stream?

## A
**Incremental when each event touches one entity and the derived value is a running aggregate; replay when an event changes the meaning of *earlier* events.**

- Incremental: counters, balances, a flagged set — O(1) per event, and reversal is just the inverse operation.
- Replay: a rule registered mid-stream that applies retroactively, or a correction that changes how earlier records are grouped.

Most timed problems are incremental by construction, and the statement protects you: rules "apply to every later line", not to earlier ones. When you *do* need a replay, keep the raw events — a summary cannot be replayed.

## Q zh
什么时候增量维护派生状态，什么时候重放整条流？

## A zh
**当每个事件只触及一个实体、派生值是滚动聚合时，用增量；当某个事件改变了更早事件的含义时，用重放。**

- 增量：计数器、余额、被标记集合 —— 每事件 O(1)，而撤销就是逆运算。
- 重放：流中途注册、却要追溯生效的规则；或者改变早期记录分组方式的更正。

大多数限时题在构造上就是增量的，而且题面会保护你：规则「只对其后的行生效」，不对更早的行。当你**确实**需要重放时，记得保留原始事件 —— 摘要是重放不了的。
