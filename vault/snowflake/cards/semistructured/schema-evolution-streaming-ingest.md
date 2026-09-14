---
id: schema-evolution-streaming-ingest
node: semistructured.schema-evolution-tables
type: qa
tags: [grown]
---
## Q
除了文件批量加载，行级实时摄取的 Snowpipe Streaming 能否也让目标表跟随数据自动加列？

## A
可以。Snowpipe Streaming（不经暂存文件、按行直接写表的摄取服务）同样支持模式演进：当流入数据中出现新列时，Snowflake 可以自动为目标表添加这些列，无需手动执行 DDL。因此无论数据以文件还是以行的形式到达，都能保持表结构与上游同步。
