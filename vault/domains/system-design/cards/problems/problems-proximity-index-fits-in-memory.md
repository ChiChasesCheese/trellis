---
id: problems-proximity-index-fits-in-memory
node: problems.geo.proximity
type: qa
step: 1
tags: [grown]
---
## Q
In a Yelp-like proximity search design with 20 million indexed businesses, each business record (id, geohash, name, category, lat/lon, address, phone, rating stats, and overhead) taking about 188 bytes, why does the resulting ~3.76GB total size push the design toward keeping the entire spatial index in memory on every search server instance rather than treating it as a sharding problem?

## A
20 million businesses x 188 bytes/record is about 3.76GB, small enough to fit comfortably in the RAM of a single modern server, and a compact geohash-to-business-id index adds under 0.4GB more. Since the dataset easily fits in memory, distributing it across shards would only add cross-shard merge overhead without solving a capacity problem that doesn't exist at this scale — sharding only becomes necessary once the indexed set grows 2-3 orders of magnitude (e.g. covering all global points of interest), not at ordinary business-directory scale.

## Q zh
在一个类 Yelp 邻近搜索设计中，索引 2,000 万个商户，每条商户记录（id、geohash、名称、类别、经纬度、地址、电话、评分统计和其他开销）约 188 字节，为什么由此得到的约 3.76GB 总大小会把设计推向'把整个空间索引放进每个搜索服务实例的内存里'，而不是把它当作一个分片问题处理？

## A zh
2,000 万商户 × 188 字节/记录约等于 3.76GB，完全能舒服地放进一台现代服务器的内存，一份紧凑的 geohash 到 business_id 的索引再加不到 0.4GB。既然整个数据集轻松放进内存，把它分布到多个分片上只会带来跨分片合并的额外开销，却解决不了一个在这个规模下根本不存在的容量问题——只有当索引规模再涨 2 到 3 个数量级（比如覆盖全球所有兴趣点）时，分片才是必需品，普通商户目录量级用不上。
