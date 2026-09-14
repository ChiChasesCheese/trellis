---
id: micro-partition-size-50-500mb-uncompressed
node: storage.micro-partition-format
type: cloze
source: snowflake-docs
---
Snowflake 表的每个微分区（micro-partition，连续的存储单元）容纳 {{c1::50 MB 到 500 MB}} 的 {{c2::未压缩}} 数据；实际落盘更小，因为数据始终以压缩形式存储。
