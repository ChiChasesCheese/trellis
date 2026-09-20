---
id: problems-online-auction-shrinking-containers
node: problems.marketplaces.online-auction
type: qa
step: 8
tags: [grown]
---
## Q
在线拍卖系统跑得越久，哪些容器会无限增长？各自靠什么机制保证会缩小？

## A
两个：**关注者表**和**拍卖行的拍品目录**。

- **关注者表**（每场拍卖内部）：`watch()` 返回一个 `unwatch` 闭包，把退订手段和订阅一起交出去；更重要的是，拍卖一进入终态（`_tick` 发出 CLOSED 事件时），整张关注者表**当场清空**，因为结束之后不会再有任何事件，留着这些引用只是内存泄漏。
- **拍品目录**（`AuctionHouse._auctions`）：靠 `purge_closed_before(cutoff)` 把结束早于 `cutoff` 的拍卖清出字典，`auction_count` 随之真的变小。没有它，目录会随着上架量无限增长，而其中绝大多数早就尘埃落定，能被清理是因为它们的关注者表在结束那一刻已经清空——`Auction` 对象因此没有任何外部引用拖着，真的能被回收。

出价历史（`Auction._bids`）是唯一被故意设计成**只增不减**的容器：它是审计所需的流水账，真实系统会随拍卖归档一起搬走，而不是原地清理。
