---
id: dt-target-lag-not-guarantee
node: pipelines.dynamictable-target-lag
type: qa
source: snowflake-docs
---
## Q
动态表设置了 `TARGET_LAG = '10 minutes'`，监控却显示某段时间数据落后了 25 分钟。这是违反了承诺吗？什么样的需求不适合用动态表？

## A
不算违约。目标延迟表示 Snowflake 尽量让数据落后基表不超过 10 分钟，但当刷新耗时超出预期时，实际延迟可能超过目标，它是目标而非保证。因此动态表不适合要求数据新鲜度高于 60 秒（最小目标延迟）或需要严格保证刷新时间的工作负载，也不支持在定义中使用存储过程或外部函数。
