---
id: hi-c-sd-data-structures-for-big-data-n11-hll-use
node: sd.deep-dives.data-structures-for-big-data.notes
type: qa
step: 11
---
## Q
**大数据结构 · HyperLogLog 适用场景与坑**｜摘要 · 必会

HyperLogLog 在分析、安全、缓存规划里分别怎么用？什么时候不该用？

## A
- **适合：** 要数海量数据的不同元素个数，内存有限，能接受小误差。Redis 内置（`PFADD`/`PFCOUNT`），PostgreSQL 有 hll 扩展。
- **不该用：** 要精确数（它给不出）；不同元素本来就很少（它反而增加开销，用哈希集合）。
- **分析与指标：** 日活、月活、每页独立访客、不同搜索词、不同 IP 数。可以流式维护，也可以扫描数据时用 HLL 估算。
- **反爬虫：** 只看请求数最多的 IP 会误伤大企业代理；用 HLL 估算每个 IP 访问了多少个不同 URL，爬虫总在访问新网页，而真人会反复回访热门页，可据此区分，也不用存下该 IP 看过的所有 URL。
- **缓存规模分析：** 估算被访问的不同键数（工作集大小）与更新速度，用来决定缓存要多大、是否需要分区。
