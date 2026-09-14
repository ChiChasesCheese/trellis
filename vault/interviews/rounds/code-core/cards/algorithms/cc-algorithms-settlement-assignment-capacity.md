---
id: cc-algorithms-settlement-assignment-capacity
node: algorithms.settlement
type: qa
---
## Q
Assign each task to the least-loaded worker that has the skill and the room. Why is "least loaded" not enough?

## A
**The least-loaded worker may not fit, while a busier one does.** The rule is *least loaded among those that fit*, with the boundary `load + cost <= capacity` — non-strict, so a worker filled exactly to capacity is a legal assignment.

- Per-skill priority queues keyed `(load, preference…, worker_id)`; pop, test capacity, park the non-fitting candidates, restore them after the choice ([[cc-toolbox-heap-park-and-restore]]).
- Loads change between consecutive tasks, so the structure must stay re-orderable — a list sorted once is wrong from the second task onward ([[cc-algorithms-greedy-with-heap]]).
- Tie-breaks arrive in layers and all of them belong in the heap key: load first, then a preference (fewer skills = the specialist), then the id as a **plain string** (`w10 < w2`) ([[cc-output-ordering-string-vs-numeric]]).
- A task nobody can take is not an error: emit the declared `UNASSIGNED` token and carry on ([[cc-output-sentinels-error-contract]]).
- Capacity 0 accepts only zero-cost tasks — and zero-cost tasks *are* assignable.

## Q zh
把每个任务分给「拥有该技能且还装得下」的负载最小的 worker。为什么「负载最小」不够？

## A zh
**负载最小的 worker 可能装不下，而更忙的那个装得下。** 规则是*在装得下的人中取负载最小者*，边界是 `load + cost <= capacity` —— 非严格，所以恰好被填满的 worker 是一次合法分配。

- 按技能各建一个优先队列，key 为 `(load, 偏好…, worker_id)`；pop、检查容量、把装不下的候选寄存、选完后放回（[[cc-toolbox-heap-park-and-restore]]）。
- 负载在相邻任务之间会变，所以结构必须可重排 —— 只排一次的列表从第二个任务起就错了（[[cc-algorithms-greedy-with-heap]]）。
- tie-break 是分层给出的，而且全都应该放进堆的 key 里：先负载，再偏好（技能更少 = 专才），再 id 的**普通字符串序**（`w10 < w2`）（[[cc-output-ordering-string-vs-numeric]]）。
- 没人能接的任务不是错误：输出约定的 `UNASSIGNED` 标记然后继续（[[cc-output-sentinels-error-contract]]）。
- 容量为 0 时只接受零成本任务 —— 而零成本任务*是*可以被分配的。
