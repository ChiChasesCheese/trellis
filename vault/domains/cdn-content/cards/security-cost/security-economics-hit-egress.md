---
id: security-economics-hit-egress
node: security-cost.economics
type: qa
---
## Q
Why can a higher cache hit ratio reduce origin cost but leave CDN transfer cost almost unchanged?

## A
A HIT avoids origin compute, origin requests, and origin transfer, but the CDN still sends the response bytes to the user and processes an edge request. Byte size, user region, and request count still drive delivery cost. Model each billable leg separately; then choose whether caching, compression, image sizing, or request consolidation targets the dominant unit.

## Q zh
为什么更高的 cache hit ratio 能降低 origin cost，却可能几乎不改变 CDN transfer cost？

## A zh
HIT 会避免 origin compute、origin request 和 origin transfer，但 CDN 仍需把 response byte 发送给用户，并处理 edge request。byte size、user region 和 request count 仍驱动 delivery cost。应分别建模每个 billable leg，再判断 caching、compression、image sizing 或 request consolidation 中哪个能优化主要 unit。
