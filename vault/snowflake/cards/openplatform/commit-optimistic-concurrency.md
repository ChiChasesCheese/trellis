---
id: commit-optimistic-concurrency
node: openplatform.external-engine-commit-protocol
type: qa
source: snowflake-docs
---
## Q
Snowflake 和一个 Spark 作业几乎同时向同一张 Iceberg 表提交写入。catalog 的原子指针更新怎样保证不会互相覆盖对方的提交？

## A
提交采用乐观并发控制（optimistic concurrency）：每个写者基于自己读到的元数据版本 N 生成新元数据，再请求 catalog “仅当当前指针仍是 N 时才替换为我的新版本”（类似比较并交换 CAS）。先提交者成功把指针推进到 N+1；后提交者的前提不再成立，提交被拒绝，必须基于 N+1 重新检查冲突并重试提交。所以不会有写入被静默覆盖，冲突的代价是失败方重试。
