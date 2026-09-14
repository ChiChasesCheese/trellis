---
id: cc-model-ev-input-order-not-timestamp-order
node: model.event-stream
type: qa
---
## Q
Every event line carries a timestamp, and the timestamps in the sample happen to be increasing. Do you sort by them?

## A
**No — process in input order unless the statement says to sort.** Sorting is a change of semantics you were not asked for, and it is unrecoverable: a stable sort of equal timestamps preserves input order, so the only thing sorting can do is silently reorder events the author intended to arrive as given.

Timestamps in such problems usually mean something narrower: a window check (`t_refund - t_create <= limit`), a bucket, or a report range. Read what the timestamp is *used for*. If events may genuinely arrive out of order, the statement says so — and then it also says what "current" means.

## Q zh
每一行事件都带时间戳，样例里的时间戳恰好是递增的。你要按它排序吗？

## A zh
**不要 —— 除非题面明说要排序，否则按输入顺序处理。** 排序是一次你没被要求做的语义改变，而且不可挽回：稳定排序对相等时间戳保留输入顺序，所以排序唯一能做的，就是悄悄重排作者本意按原样到达的事件。

这类题里的时间戳通常含义更窄：窗口判断（`t_refund - t_create <= limit`）、分桶，或报表区间。读清时间戳到底**被用来做什么**。如果事件真的可能乱序到达，题面会说 —— 并且同时会说清"当前"是什么意思。
