---
id: problems-auction-actor-crash-rebuild-from-store-not-replay
node: problems.commerce.auction
type: qa
step: 7
tags: [grown]
---
## Q
When the single serialized actor handling bids for one auction crashes, how does its replacement instance recover the correct current-price state before accepting new bids, and how is this different from how a stock exchange's matching engine recovers after a crash?

## A
The replacement actor reads the current price and current leader from the authoritative store (a single row read) to rebuild its in-memory state, because an auction's entire state is just that one row — there's no larger order book to reconstruct. This differs from a stock exchange's matching engine, whose recovery replays an entire durable journal of every input event to deterministically rebuild a much larger in-memory order book; an auction's state is small enough that reading the latest row directly is sufficient, and bids arriving during the recovery window simply queue until the new actor is ready rather than needing replay.

## Q zh
当处理某场拍卖出价的单一序列化 actor 崩溃时，它的替代实例在接受新出价之前，如何恢复正确的当前价格状态？这和股票交易所的撮合引擎崩溃后的恢复方式有什么不同？

## A zh
替代 actor 从权威存储读取当前价格和当前领先者（只读一行）来重建内存状态，因为一场拍卖的全部状态就是这一行数据——不存在需要重建的更大的订单簿。这和股票交易所撮合引擎的恢复方式不同：后者要重放整份持久化日志里的每一条输入事件，才能确定性地重建一个大得多的内存订单簿；拍卖的状态小到直接读最新的一行就够了，恢复窗口内到达的出价只需要排队等待新 actor 就绪，不需要重放。
