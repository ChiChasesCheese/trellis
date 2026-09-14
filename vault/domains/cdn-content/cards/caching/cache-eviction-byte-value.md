---
id: cache-eviction-byte-value
node: caching.eviction
type: qa
---
## Q
Why can optimizing object hit ratio choose the wrong eviction policy for a CDN?

## A
Objects have different sizes and miss costs. Keeping ten rarely requested 1 GiB objects may displace thousands of popular small assets, while one large expensive-to-regenerate object may be worth retaining. Evaluate byte hit ratio, saved origin latency/egress/compute per cache byte, churn, and tail latency—not only the count of hits.

## Q zh
为什么只优化 object hit ratio 可能让 CDN 选错 eviction policy？

## A zh
object 的 size 与 miss cost 不同。保留十个很少请求的 1 GiB object 可能驱逐几千个热门小 asset；但一个昂贵重算的大 object 又可能值得保留。应评估 byte hit ratio、每 cache byte 节省的 origin latency/egress/compute、churn 与 tail latency，而不只是 hit 数量。
