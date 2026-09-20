---
id: problems-auction-10x-fanout-sharding-not-actor-throughput
node: problems.commerce.auction
type: qa
step: 8
tags: [grown]
---
## Q
At 10x scale, the number of simultaneously active auctions grows from 5 million to 50 million, and the count of the hottest 0.1% of auctions grows proportionally from 5,000 to 50,000. Given that each auction already gets its own dedicated serialized actor (which scales horizontally since actors for different auctions are independent), why does the watcher fan-out layer — not the per-auction actors — become the part of the design that needs to change at 10x?

## A
Adding more auctions just means instantiating more independent, stateless-to-scale actors, one per auction, which is not a bottleneck since they don't coordinate with each other. But the pub/sub fan-out layer that broadcasts price updates to watchers has active watch relationships that scale with both the number of hot auctions and watchers per auction — going from roughly 5,000 x 50,000 = 250 million active watch relationships to about 2.5 billion at 10x. That growth concentrates load on whichever fan-out nodes serve the busiest auctions, so the fan-out layer needs finer-grained sharding by auction id to keep any single node from carrying a disproportionate share of the busiest auctions' broadcast traffic.

## Q zh
在 10 倍演进场景下，同时活跃的拍卖数从 500 万增长到 5,000 万，最热门的 0.1% 拍卖数量同比例从 5,000 场增长到 5 万场。既然每场拍卖已经有自己专属的序列化 actor（这天然可以水平扩展，因为不同拍卖的 actor 互相独立），为什么真正需要在 10 倍规模下调整的是围观者扇出层，而不是每场拍卖的 actor？

## A zh
增加拍卖数量只是意味着实例化更多互相独立的 actor，每场拍卖一个，这不是瓶颈，因为它们之间不需要协调。但负责把价格更新广播给围观者的发布订阅扇出层，其活跃围观关系数量同时随热门拍卖数量和每场拍卖的围观者数量增长——从大约 5,000 × 50,000 = 2.5 亿活跃围观关系，在 10 倍后增长到约 25 亿。这种增长会把负载集中在服务最繁忙拍卖的那些扇出节点上，所以扇出层需要按拍卖 id 做更细粒度的分片，避免单个节点承担不成比例的最繁忙拍卖广播流量。
