---
id: async-command-vs-event
node: async.streaming.cdc
type: qa
---
## Q
In an event-sourced system, why must "ReserveSeat" (a command) and "SeatReserved" (an event) be different things, and at which exact moment does one become the other?

## A
- A **command** is a *request* that may be rejected: it must be validated against current state (seat still free? balance sufficient?) and represents intent, not truth.
- An **event** is an *accepted, immutable fact*: once appended to the log it has happened, is never edited or deleted, and every consumer — projections, downstream services, replays years later — must be able to treat it as unconditionally true.

The conversion point is **synchronous validation at append time**: check the invariant, and only if it holds, atomically append the event (the check and append must serialize — e.g. via the log's ordering — or two commands can both pass validation). The user can be told "no" at this point, and only this point.

Why the discipline matters: if you let consumers validate events instead, a consumer that says "no" cannot un-happen a fact others already processed — you'd need compensating events and cross-consumer disagreement handling. Blur the line (write raw commands to the log) and every reader must re-implement validation, inconsistently.

## Q zh
在一个事件溯源（event sourcing）系统里，为什么 "ReserveSeat"（command）和 "SeatReserved"（event）必须是两种不同的东西？前者在哪个确切时刻变成后者？

## A zh
- **Command（命令）**是一个*可以被拒绝的请求*：它必须对照当前状态校验（座位还空着吗？余额够吗？），代表的是意图，不是事实。
- **Event（事件）**是一个*已被接受的、不可变的事实*：一旦追加进日志就已然发生，永不修改或删除；每个消费者——投影、下游服务、多年后的回放——都必须能把它当作无条件为真。

转换点是**追加时的同步校验**：检查不变量，只有通过才原子地追加事件（检查与追加必须串行化——比如借助日志的定序——否则两条命令可能都通过校验）。用户只能在这个点、也只有这个点被告知"不行"。

这条纪律为何重要：如果让消费者去校验事件，一个说"不"的消费者无法让别人已经处理过的事实"没发生"——你将需要补偿事件和跨消费者的分歧处理。而若模糊边界（把原始命令直接写进日志），每个读者都得各自重新实现一遍校验，且注定不一致。
