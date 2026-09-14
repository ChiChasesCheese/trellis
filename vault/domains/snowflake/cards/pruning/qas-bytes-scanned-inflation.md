---
id: qas-bytes-scanned-inflation
node: pruning.query-acceleration-service
type: qa
source: snowflake-docs
---
## Q
开启查询加速服务（QAS）后，发现 QUERY_HISTORY 里某查询的 `QUERY_ACCELERATION_BYTES_SCANNED + BYTES_SCANNED` 比未开启时更大，而且 `bytes_spilled_to_remote_storage`（溢出到远程存储的字节数）非零。这说明有问题吗？

## A
通常不是问题。QAS 为实现加速会生成中间结果，这些中间结果被计入扫描量，因此字节数和分区数之和会比不用 QAS 时更大。另外，开启 QAS 后 Snowflake 会为每条符合条件的查询向远程存储写入少量数据，即使该查询最终没有使用 QAS，所以非零的溢出值也不代表内存不足。
