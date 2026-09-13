---
id: security-abuse-layered-limits
node: security-cost.abuse
type: qa
---
## Q
Why is one global requests-per-second limit insufficient for an image optimization endpoint?

## A
Requests have radically different cost by tenant, input pixels, output variants, cache outcome, and transform complexity. Combine coarse edge rate limits with authenticated tenant quotas, concurrency and queue bounds, input-size/pixel limits, and per-operation cost budgets. Reject before decode when possible, and preserve capacity for cheap cached delivery so expensive misses cannot starve the whole service.

## Q zh
为什么一个 global requests-per-second limit 不足以保护 image optimization endpoint？

## A zh
不同 request 的成本会因 tenant、input pixel、output variant、cache outcome 和 transform complexity 而巨大不同。应组合 coarse edge rate limit、authenticated tenant quota、concurrency/queue bound、input-size/pixel limit 和 per-operation cost budget。尽可能在 decode 前 reject，并为 cheap cached delivery 保留 capacity，防止 expensive miss 饿死整个 service。
