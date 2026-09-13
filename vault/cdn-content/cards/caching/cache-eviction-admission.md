---
id: cache-eviction-admission
node: caching.eviction
type: qa
---
## Q
Why can "cache every miss" reduce hit ratio during a one-time scan of millions of objects?

## A
Those one-hit objects are admitted and evict the established hot working set, causing **cache pollution**. Admission policy asks whether a newcomer is likely more valuable than the victim—using frequency sketches, repeated access, object-size limits, or a probation segment. Eviction chooses what leaves; admission decides whether the new object enters at all.

## Q zh
为什么在一次性扫描几百万个 object 时，“每个 miss 都缓存”反而会降低 hit ratio？

## A zh
这些 one-hit object 被 admission 后，会驱逐已有 hot working set，形成 **cache pollution**。admission policy 会判断 newcomer 是否比 victim 更有价值，可使用 frequency sketch、重复访问、object-size limit 或 probation segment。eviction 决定谁离开；admission 决定新 object 是否进入。
