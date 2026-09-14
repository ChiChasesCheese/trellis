---
id: copy-into-load-metadata-dedupe
node: ingestion.bulk-copy-into
type: qa
source: snowflake-docs
---
## Q
同一批文件被两次 `COPY INTO` 到同一张表，为什么第二次默认不会重复加载？这份去重记录能保存多久？

## A
批量加载会把每个已加载文件的加载历史记录在目标表的元数据中，保存 64 天；再次执行 COPY 时，已经记录为加载过的文件会被跳过，从而避免数据重复。Snowpipe 的加载历史则存放在管道（pipe）的元数据里，只保存 14 天。由于两份记录互不相通，同一组文件应只用批量加载或只用 Snowpipe 其中一种方式加载，否则可能重复加载。
