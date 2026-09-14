---
id: snowpipe-pipe-object-and-triggers
node: ingestion.snowpipe-auto-ingest
type: qa
source: snowflake-docs
---
## Q
Snowpipe 是怎么知道暂存区（stage）来了新文件的？管道（pipe）对象里又定义了什么？

## A
管道是一个具名的一等 Snowflake 对象，内含一条 COPY 语句，指明源暂存区和目标表。发现新文件有两种机制：1) 自动摄取：云存储的事件通知发送到队列，Snowpipe 轮询队列，根据其中的元数据以无服务器方式持续加载新文件；2) REST 端点：客户端应用调用公开的 REST 端点，传入管道名和文件名列表，匹配的文件进入加载队列，调用时需要使用基于 JWT 的密钥对认证。
