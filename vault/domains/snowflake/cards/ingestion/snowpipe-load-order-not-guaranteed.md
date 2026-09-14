---
id: snowpipe-load-order-not-guaranteed
node: ingestion.snowpipe-auto-ingest
type: qa
source: snowflake-docs
---
## Q
业务依赖 CDC 文件按生成顺序加载（后一个文件的更新必须晚于前一个）。用 Snowpipe 自动摄取会有什么风险？

## A
Snowflake 为每个管道维护一个队列，新发现的文件追加到队列中，但有多个进程同时从队列取文件加载。因此 Snowpipe 虽然通常先加载较早的文件，却不保证加载顺序与文件暂存的顺序一致。依赖顺序的逻辑应在下游根据记录内的时间戳或序号处理，而不能依赖加载顺序。
