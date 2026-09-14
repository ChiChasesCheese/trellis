---
id: txn-granularity-tradeoff
node: txn.acid-guarantees
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 标准表上，把 10 条互不相关的单行 INSERT 合并进一个事务，和各自单独提交相比，有什么收益和风险？

## A
收益：管理事务本身消耗资源，一个事务插入 10 行通常比 10 个事务各插一行更快、更便宜。风险：事务应只包含必须一起成功或失败的相关语句（如从一个账户扣款并存入另一个账户）；把无关语句打包后，一次回滚会连带撤销本不需要撤销的工作，而且事务持有的锁（lock）时间更长，会拖慢其他查询甚至引发死锁（deadlock）。
