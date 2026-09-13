---
id: security-optimization-hit-value
node: security-cost.optimization
type: qa
---
## Q
Which objects should receive scarce shield-cache capacity: tiny popular icons or large moderately popular downloads?

## A
Rank by avoided cost and protected bottleneck, not raw request frequency alone. Estimate reuse probability times avoided origin bytes, requests, compute, and latency, divided by residency cost and eviction pressure. Tiny icons may dominate request savings; large downloads may dominate bytes. Measure request and byte hit ratios and validate that admission does not evict more valuable hot objects.

## Q zh
稀缺 shield-cache capacity 应优先给 tiny popular icon，还是 large moderately popular download？

## A zh
应按 avoided cost 和 protected bottleneck 排序，而不是只看 raw request frequency。估算 reuse probability 乘以可避免的 origin byte、request、compute 与 latency，再除以 residency cost 和 eviction pressure。tiny icon 可能主导 request saving，large download 可能主导 byte saving。测量 request/byte hit ratio，并验证 admission 不会 evict 更有价值的 hot object。
