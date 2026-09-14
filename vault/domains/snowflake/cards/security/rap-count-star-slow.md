---
id: rap-count-star-slow
node: security.row-access-policies
type: qa
source: snowflake-docs
---
## Q
没挂策略时 `SELECT COUNT(*) FROM t1` 毫秒级返回，挂上行级访问策略（row access policy）后同一查询变慢了很多，而且 `MAX(c)` 的结果也变了。原因是什么？

## A
没有策略时，Snowflake 直接用维护好的表/列统计元数据回答 COUNT、MAX 这类简单查询，不必扫描数据。挂策略后必须先找出当前上下文有权看到的行子集，这些统计优化不再适用，只能扫描表来计数，因此变慢；返回的统计值也只基于可访问的行，而非全表的“真实”值。这类查询虽然差异巨大，但并不代表大多数真实工作负载的开销。
