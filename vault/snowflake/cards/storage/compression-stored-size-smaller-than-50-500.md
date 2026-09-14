---
id: compression-stored-size-smaller-than-50-500
node: storage.columnar-compression-encoding
type: qa
source: snowflake-docs
---
## Q
Snowflake 说每个微分区（micro-partition）装 50–500 MB 数据，但你在账户里看到的表存储量明显比“分区数 × 这个区间”小，为什么？

## A
50–500 MB 指的是未压缩数据量。Snowflake 中的数据始终以压缩形式存储（每个微分区中的每列单独压缩），所以实际占用的存储空间小于未压缩大小。计算存储量时要按压缩后的实际大小估算，而不是按这个区间。
