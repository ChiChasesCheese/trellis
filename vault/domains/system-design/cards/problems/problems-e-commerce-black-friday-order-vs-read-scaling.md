---
id: problems-e-commerce-black-friday-order-vs-read-scaling
node: problems.commerce.e-commerce
type: qa
step: 9
tags: [grown]
---
## Q
In an e-commerce design, why does Black Friday scaling mainly require pre-warming the read cache rather than emergency-scaling the order-write path, given a computed peak of about 354 orders/sec in the promotional window against a 200,000 QPS read peak?

## A
Even a 5x order-volume Black Friday with 60% of orders concentrated in a 4-hour window and a further 2x burst factor works out to roughly 354 orders/sec — still one to two orders of magnitude below the few-thousand-per-second ceiling assumed for a single relational primary doing conditional updates, so the ordinary checkout write path needs no special scaling. The read side, by contrast, can spike to roughly 200,000 QPS on product pages, which does threaten to overwhelm a cold cache with a stampede of origin fetches. The scaling work that matters is pre-warming CDN/application caches before the event starts and routing any deliberately promoted 'doorbuster' SKU into a flash-sale-style admission-control path, since that one SKU's contention is structurally different from the rest of the catalogue.

## Q zh
在电商设计中，给定推广窗口内峰值约 354 订单/秒、读峰值约 20 万 QPS 的计算结果，为什么黑五扩容主要需要预热读缓存而不是给订单写路径做应急扩容？

## A zh
即使黑五订单量是平常的 5 倍、60% 集中在 4 小时窗口内、再叠加 2 倍突发系数，算出来也只是约 354 订单/秒——仍比假设的单个关系型主库做条件更新的每秒几千次上限低一到两个数量级，所以普通结账写路径不需要特殊扩容。相比之下，读侧商品页峰值可能冲到约 20 万 QPS，这确实可能让冷缓存被回源请求的踩踏效应压垮。真正需要做的扩容工作是活动开始前预热 CDN/应用缓存，以及把刻意推广的'秒杀单品'路由进类似秒杀设计的准入控制路径，因为这一个 SKU 的争用在结构上和目录里其余商品完全不同。
