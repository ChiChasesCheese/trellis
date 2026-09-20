---
id: problems-stock-exchange-headroom-vs-lmax-benchmark
node: problems.commerce.stock-exchange
type: qa
step: 1
tags: [grown]
---
## Q
In a stock exchange design with 8,000 listed symbols and a peak market-wide order rate of 300,000 orders/sec skewed so the hottest 1% of symbols (80 symbols) carry 40% of that volume, the busiest single symbol sees about 1,500 orders/sec. LMAX, a real trading platform, has publicly benchmarked its single-threaded business logic processor at 6,000,000 orders/sec on one thread. What does comparing these two numbers (6,000,000 / 1,500 = 4,000x headroom) tell you about whether the matching engine needs multi-threading per symbol?

## A
It shows that even the single busiest symbol's real order load uses only 1/4,000th of what a single CPU thread has been shown capable of processing, so raw compute is not the constraint on a per-symbol matching engine — one dedicated single thread per symbol has enormous headroom. This flips the common assumption that matching must be parallelized for throughput: the actual engineering problem is guaranteeing that all orders for one symbol are processed by exactly one place in one deterministic order, not finding enough compute.

## Q zh
在一个有 8,000 支上市股票的交易所设计中，全市场峰值订单速率为 300,000 单/秒，按幂律倾斜假设最热门 1%（80 支）股票占 40% 的量，最繁忙的单支股票每秒约有 1,500 笔订单。真实交易平台 LMAX 公开披露其单线程业务逻辑处理器（business logic processor）在一个线程上实测可达每秒 600 万笔订单。把这两个数字对比（6,000,000 / 1,500 = 4,000 倍冗余）说明了什么，关于撮合引擎是否需要为每支股票做多线程？

## A zh
这说明即使是负载最重的单支股票，其真实订单量也只用到了单个 CPU 线程已证明能力的 1/4,000，所以算力从来不是单支股票撮合引擎的约束——每支股票绑定一个专用单线程有巨大的冗余空间。这推翻了“撮合必须并行化才能扛住吞吐”的常见直觉：真正的工程难题是保证同一支股票的所有订单只被一个地方、按一个确定的顺序处理，而不是找到足够的算力。
