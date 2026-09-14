---
id: snowpipe-file-cadence-and-event-filtering
node: ingestion.snowpipe-auto-ingest
type: qa
source: snowflake-docs
---
## Q
为了在成本和延迟之间取得平衡，上游应该以什么节奏向 Snowpipe 暂存文件？还有什么降低成本的配置建议？

## A
建议遵循文件大小的最佳实践，并大约每分钟暂存一次文件：文件过碎会增加 Snowpipe 队列管理的开销，文件过大、间隔过长则增加加载延迟。同时建议在云存储侧开启事件过滤（event filtering），只把相关路径的事件发给 Snowpipe，以减少成本、事件噪声和延迟。实际延迟受文件格式、大小和 COPY 转换复杂度影响，应通过典型负载实测估算。
