---
id: cc-model-ev-same-timestamp-ties
node: model.event-stream
type: qa
---
## Q
`5,start,A` and `5,check,A` share a timestamp. What does the check print, and what is the general rule?

## A
**`active` — same-timestamp events take effect in input order, so the start has already happened when the check runs.**

The general rule: a timestamp is a *field*, not the processing order. Two events at the same instant are still sequential, and the sequence is the file. The mirror case is the trap: `5,end,A` followed by `5,check,A` prints `inactive` for exactly the same reason.

Where this bites is any code that batches events by timestamp before applying them — that batching destroys the intra-instant order the statement relies on.

## Q zh
`5,start,A` 和 `5,check,A` 共享同一个时间戳。check 打印什么？通则是什么？

## A zh
**打印 `active` —— 同时间戳的事件按输入顺序生效，所以 check 运行时 start 已经发生了。**

通则：时间戳是一个**字段**，不是处理顺序。同一瞬间的两个事件仍然是有先后的，而先后由文件决定。镜像情形正是陷阱：`5,end,A` 后跟 `5,check,A` 打印 `inactive`，理由完全相同。

会被咬到的地方是任何"先按时间戳把事件分批、再统一应用"的代码 —— 这种分批会毁掉题面所依赖的瞬间内顺序。
