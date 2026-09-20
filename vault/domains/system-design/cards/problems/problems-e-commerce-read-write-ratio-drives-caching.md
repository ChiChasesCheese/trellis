---
id: problems-e-commerce-read-write-ratio-drives-caching
node: problems.commerce.e-commerce
type: qa
step: 2
tags: [grown]
---
## Q
In an e-commerce design with 50M DAU browsing product pages and roughly 850,000 orders/day, what read:write ratio does this imply, and what design decision does it drive?

## A
With about 1.2 billion product-page views/day against roughly 850,000 orders/day, the ratio is about 1,400:1. This is the number that rules out querying the authoritative inventory/price row on every product-page request: at tens of thousands of QPS, that read load would crowd out the write path a relational primary is sized for. It forces product pages onto a cache/CDN layer with layered freshness (long TTL for static fields, short TTL with write-through for price/stock) rather than reading the source of truth on every view.

## Q zh
在一个 50M 日活、每日约 85 万订单的电商设计中，这意味着什么样的读写比，它驱动了什么设计决策？

## A zh
约 12 亿次商品页浏览/天对约 85 万笔订单/天，比例约为 1,400:1。这个数字排除了每次商品页请求都查权威库存/价格行的做法：在几万 QPS 的规模下，这种读负载会挤占为写路径设计的关系型主库。它迫使商品页走缓存/CDN 分层新鲜度（静态字段长 TTL，价格/库存字段短 TTL + 写穿透），而不是每次浏览都读权威数据源。
