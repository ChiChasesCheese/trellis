---
id: problems-e-commerce-marketplace-buy-box-refresh
node: problems.commerce.e-commerce
type: qa
step: 8
tags: [grown]
---
## Q
In a multi-seller e-commerce marketplace, why is the 'buy box' (the recommended offer for a product with several sellers) precomputed and stored in the product-detail cache, but refreshed by an event rather than only on a batch schedule?

## A
Recomputing the buy box on every product-page request means fetching every seller's live price/stock/rating for that product on each read, reintroducing the fan-out read load the product-page cache exists to avoid. A pure scheduled batch recompute (e.g. hourly) avoids that fan-out but leaves price drops or a sold-out seller stale until the next batch run — unacceptable when a competing seller cuts price or sells out. The middle path precomputes the buy box into the cached product document, but when a specific seller's offer changes price or stock, that write path emits an event that triggers recompute for just that one product — turning staleness from 'one batch interval' into roughly the latency of one event, without reintroducing read-time fan-out.

## Q zh
在多商家电商市场中，为什么'buy box'（一件商品在多个商家中被推荐的报价）要预计算并存进商品详情缓存里，但要靠事件而不是纯批处理周期刷新？

## A zh
每次商品页请求都重算 buy box，意味着每次读都要拉取该商品全部商家的实时价格/库存/评分，重新引入了商品页缓存本该避免的扇出读负载。纯定期批处理重算（比如每小时）避免了扇出，但会让降价或某商家售罄的信息陈旧到下一次批处理才更新——当竞争商家降价或卖光时这是不可接受的。折中方案是把 buy box 预计算进缓存的商品文档里，但当某个商家的 offer 价格或库存变化时，该写路径发一个事件只触发这一个商品的重算——把陈旧度从'一个批处理周期'降级成大约一次事件处理的延迟，同时不重新引入读时扇出。
