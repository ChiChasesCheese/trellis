---
id: rap-performance-guidelines
node: security.row-access-policies
type: qa
source: snowflake-docs
---
## Q
设计行级访问策略（row access policy）时，哪些做法能减少它对查询性能的影响？

## A
(1) 少绑定参数列：策略绑定的列即使查询没引用也要被扫描；(2) 表达式尽量简单：基于 `CURRENT_ROLE` 或 `CASE` 的策略开销几乎可以忽略，而查映射表的策略更慢，映射表引用可改用可记忆函数（memoizable function）缓存查找结果；(3) 超大表按策略过滤所用的属性做聚簇（clustering），提升剪枝；(4) 搜索优化服务（Search Optimization Service）也能加速挂有策略的表；(5) 用真实工作负载测试，而非 `COUNT(*)` 之类的极端例子。
