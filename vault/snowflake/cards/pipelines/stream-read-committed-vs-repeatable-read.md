---
id: stream-read-committed-vs-repeatable-read
node: pipelines.stream-consumption-and-offset-advance
type: qa
source: snowflake-docs
---
## Q
在同一个事务里：先查询流 `s1`，接着 UPDATE 源表 `t1`，再次查询 `s1`。第二次查询能看到刚才的 UPDATE 吗？这和查询普通表有什么不同？

## A
看不到，第二次查询返回的与第一次完全相同。流在事务内采用可重复读（repeatable read），返回的是从流位置到事务开始时间的变更，事务内对源表的 DML 只有在事务提交后才会记录到流中。普通表采用读已提交（READ COMMITTED），同一事务内后面的语句能看到前面语句尚未提交的改动。
