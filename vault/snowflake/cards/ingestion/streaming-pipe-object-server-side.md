---
id: streaming-pipe-object-server-side
node: ingestion.snowpipe-streaming-offset-tokens
type: qa
source: snowflake-docs
---
## Q
在 Snowpipe Streaming 中，PIPE 对象承担什么职责？如果没有手动创建管道，会怎样？

## A
PIPE 对象是所有流式摄取在服务端的处理层：负责模式校验、传输过程中的转换（使用 COPY 语法重排列、类型转换、应用表达式），以及在摄取时按聚簇键预先排序（pre-clustering）。Snowflake 会为每张表自动创建一个默认管道，所以不创建也能直接写入；需要高级处理时再创建自定义管道。这与 Snowpipe 中管道负责排队和加载暂存文件的角色不同。
