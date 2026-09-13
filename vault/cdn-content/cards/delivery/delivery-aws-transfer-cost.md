---
id: delivery-aws-transfer-cost
node: delivery.aws
type: qa
---
## Q
Moving an origin to another region lowers compute price but increases CDN-to-origin transfer and latency. How should the decision be evaluated?

## A
Model cost per delivered request or byte using regional miss volume, transfer direction, request charges, shield behavior, and compute—not instance price alone. Then test user latency, failure isolation, and capacity. A cheaper origin can be more expensive overall if every miss crosses regions; improving hit ratio or selecting the shield/origin region may dominate compute savings.

## Q zh
把 origin 移到另一个 region 会降低 compute price，但增加 CDN-to-origin transfer 和 latency。应如何评估这个决策？

## A zh
用 regional miss volume、transfer direction、request charge、shield behavior 和 compute 建模每个 delivered request 或 byte 的成本，而不是只看 instance price。然后测试 user latency、failure isolation 和 capacity。如果每次 miss 都跨 region，更便宜的 origin 可能让总成本更高；提高 hit ratio 或选择合适的 shield/origin region 可能比 compute saving 更重要。
