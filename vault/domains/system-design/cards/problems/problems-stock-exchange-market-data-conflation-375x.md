---
id: problems-stock-exchange-market-data-conflation-375x
node: problems.commerce.stock-exchange
type: qa
step: 5
tags: [grown]
---
## Q
A hot stock has a tick rate of 1,500 order/trade events per second and 1,500,000 subscribers watching it. Pushing every tick to every subscriber directly would be 1,500 x 1,500,000 = 2,250,000,000 messages/sec for that one symbol. If a market-data fan-out layer instead conflates updates into one snapshot per subscriber every 250ms (4 updates/sec/subscriber), the push rate becomes 4 x 1,500,000 = 6,000,000 messages/sec — a 375x reduction. What is given up to get that reduction, and why is it an acceptable trade for a retail brokerage's quote feed?

## A
Conflation discards the intermediate ticks between snapshots: a subscriber only ever sees the latest price at each 250ms interval, not every individual trade that happened in between. This is acceptable specifically because a retail quote feed is allowed to be eventually consistent and briefly stale (unlike the exchange's own matching, which must be exact and deterministic) — the fan-out layer is not the system of record, so dropping intermediate state is safe as long as the next snapshot always carries the current truth.

## Q zh
一支热门股票的 tick（成交/挂单变化）速率是每秒 1,500 次，有 1,500,000 个订阅者在关注它。如果把每次 tick 都直接推给每个订阅者，速率会是 1,500 × 1,500,000 = 22.5 亿条消息/秒。如果行情分发层改为把更新合并（conflate）成每个订阅者每 250ms 一份快照（相当于每秒 4 次更新），推送速率就变成 4 × 1,500,000 = 6,000,000 条/秒——降低了 375 倍。换来这个降低倍数，牺牲了什么？为什么这对零售经纪商的报价推送来说是可以接受的？

## A zh
合并（conflation）丢弃了两次快照之间的所有中间 tick：订阅者在每 250ms 的间隔里只会看到那一刻的最新价格，看不到期间发生的每一笔具体成交。这之所以可以接受，是因为零售报价推送本身被允许最终一致、短暂陈旧（不像交易所自己的撮合必须精确且确定性）——分发层不是权威数据源，只要下一份快照始终携带当前的真实状态，丢弃中间状态就是安全的。
