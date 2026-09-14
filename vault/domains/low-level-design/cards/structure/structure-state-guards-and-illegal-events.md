---
id: structure-state-guards-and-illegal-events
node: structure.state-machines
type: qa
---
## Q
"An order may ship from PAID only if every line item is in stock." Why can't a state→state table express this, and how should the illegal case be reported?

## A
Legality is a triple **(current state, event, guard)** — not a pair of states. Model transitions keyed by *event* and attach a predicate:

```java
record Transition(State from, Event on, Predicate<Order> guard, State to) {}
```
`state × event` picks the row; the guard decides. Otherwise the stock check leaks back into the caller, which is what the table was supposed to prevent.

Reporting the rejection — choose by what the caller can do:
- **Throw** when it's a programming error (`SHIPPED → PAID`): unreachable if callers are correct.
- **Return a typed failure** when it's expected business flow ("out of stock") — the caller retries or messages the user; exceptions for control flow here are noise.
- **No-op** for idempotent repeats (`cancel()` on a CANCELLED order) — but only if repeat is genuinely harmless.


## Q zh
"一个订单可能从 PAID 只有当每一个行项是库存中的运送。"为什么一个状态→状态表不能表达这个，非法情况应该怎样被报告?

## A zh
合法性是一个三元组 **(当前状态、事件、保护)** — 不是一对状态。模型转变由**事件**作为关键并附加一个谓词:

```java
record Transition(State from, Event on, Predicate<Order> guard, State to) {}
```
`state × event` 挑选行；保护决定。否则库存检查泄漏回调用者，那是表所本想阻止的。

报告拒绝 — 选择通过调用者能做什么:
- **抛出**当它是一个编程错误（`SHIPPED → PAID`）: 无法接近如果调用者是正确的。
- **返回一个类型化的失败**当它是预期的商业流（"缺货"）— 调用者重试或给用户消息；这里异常为控制流是噪音。
- **不操作**对等幂重复（`cancel()` 在一个 CANCELLED 订单）— 但只有如果重复真正是无害的。
