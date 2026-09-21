---
id: condition-wait-spurious-wakeup-needs-recheck
node: asyncio.sync-primitives
type: qa
source: python-docs
---
## Q
用 `asyncio.Condition` 时，`await cond.wait()` 被 `notify()` 唤醒后，条件（condition）就一定已经满足了吗？

## A
不一定。文档明确指出协程可能被虚假唤醒（spuriously return），所以调用方必须在唤醒后重新检查一次目标状态，不满足就再次 `wait()`——因此惯用写法是 `while` 循环而不是一次性的 `if`；官方文档也提到可以改用 `Condition.wait_for()` 作为替代写法。
