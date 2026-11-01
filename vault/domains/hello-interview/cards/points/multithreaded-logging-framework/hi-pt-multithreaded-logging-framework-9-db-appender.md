---
id: hi-pt-multithreaded-logging-framework-9-db-appender
node: qb.lld.multithreaded-logging-framework.points
type: qa
step: 9
---
## Q
**多线程日志框架 · 文件滚动与日志落库优化**｜出自：多线程日志框架 › 深入 4

日志要写进数据库时应该怎么优化？文件滚动在哪个线程做？Appender 抽象长什么样？

## A
**落库。** 批量插入（一批一个事务或多行 INSERT）而不是逐条；按时间分区的表，旧分区整体删除；索引只建时间、级别、来源，因为索引拖慢写入；高吞吐先落文件或消息队列再异步导入，数据库挂了不丢日志。
**Appender。** `write_batch(records)` 的不同实现（文件、数据库、远程），写入线程只依赖该接口。
**滚动。** 只在写入线程里做，无并发问题。
