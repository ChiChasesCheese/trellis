---
id: stream-create-or-replace-table-stale
node: pipelines.stream-staleness-and-retention-extension
type: qa
source: snowflake-docs
---
## Q
有人对源表执行了 `CREATE OR REPLACE TABLE` 来改表结构，此后表上的流全部失效。为什么？重命名表会有同样的问题吗？

## A
`CREATE OR REPLACE` 重建对象会丢弃其历史，流依赖的版本历史不复存在，于是表上的流立即陈旧；对于视图上的流，重建或删除任何一张底层表也会使流陈旧。重命名源对象不会破坏流，也不会使其陈旧。另外，若删除源对象后再创建一个同名新对象，原来的流不会关联到新对象上。
