---
id: cache-hierarchy-shield
node: caching.hierarchy
type: qa
---
## Q
Why add a regional shield between hundreds of edge POPs and one origin?

## A
Without a shield, the same cold object can miss independently in every POP and generate hundreds of origin fetches. A shield aggregates those misses, increases reuse, reduces origin connections/egress, and centralizes coalescing. The trade-offs are an extra hop on shield misses/hits, shield capacity and failure risk, and routing to a shield near the origin.

## Q zh
为什么要在几百个 edge POP 与一个 origin 之间增加 regional shield？

## A zh
没有 shield 时，同一个 cold object 可能在每个 POP 独立 miss，产生几百次 origin fetch。shield 聚合这些 miss，提高 reuse，减少 origin connection/egress，并集中 request coalescing。代价是多一个 hop、shield capacity/failure risk，以及必须把请求路由到靠近 origin 的合适 shield。
