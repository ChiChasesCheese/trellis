---
id: problems-auction-watcher-fanout-decoupled-eventual-consistency
node: problems.commerce.auction
type: qa
step: 4
tags: [grown]
---
## Q
In an online auction design, why is the pub/sub fan-out that pushes the current price to watchers built as a completely separate, asynchronous path from the write that actually decides the new current price, rather than having the bid-writing operation itself push to every watcher before returning success to the bidder?

## A
The write path (deciding who is currently leading) has to be strongly consistent — every read of the current price must reflect every accepted bid so far, with no split-brain view. Watchers, in contrast, only need eventual consistency — seeing the new price a few hundred milliseconds late is an acceptable product trade-off, not a correctness violation. Coupling the fan-out into the same transaction as the bid write would make the bid's confirmation latency depend on how many thousands of watchers must be notified, which directly threatens the bid path's own tight latency budget for no correctness benefit, since the fan-out layer doesn't need the same consistency guarantee.

## Q zh
在一个在线拍卖设计中，为什么把当前价格推送给围观者的发布订阅扇出，要构建成一条和“真正决定新的当前价格”的写入完全分离的异步路径，而不是让出价写入操作本身在返回成功之前就推送给每一个围观者？

## A zh
写路径（决定谁当前领先）必须强一致——任何时刻查询当前价格都必须反映到目前为止所有被接受的出价，不能出现两个视图分裂的情况。而围观者只需要最终一致——晚几百毫秒看到新价格是可以接受的产品取舍，不是正确性问题。如果把扇出耦合进和出价写入相同的事务，出价的确认延迟就会取决于需要通知多少成千上万个围观者，这会直接威胁出价路径本就紧张的延迟预算，却换不来任何正确性上的好处，因为扇出层根本不需要相同的一致性保证。
