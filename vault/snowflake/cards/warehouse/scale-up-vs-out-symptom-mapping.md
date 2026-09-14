---
id: scale-up-vs-out-symptom-mapping
node: warehouse.scaling-up-vs-out
type: qa
source: snowflake-docs
---
## Q
Snowflake 仓库出现两种症状：A）某条大而复杂的报表查询本身很慢；B）早上 9 点大量用户同时登录，查询纷纷排队。分别该纵向扩展（scale up）还是横向扩展（scale out）？为什么？

## A
A 用纵向扩展：调大仓库规格，给每个集群更多计算资源，较大、较复杂的查询通常随规格提升而变快。B 用横向扩展：给多集群仓库（multi-cluster warehouse）增加集群（需要 Enterprise 版及以上），它专为大量并发用户/查询带来的排队而设计。调大规格虽能略微缓解排队，但并不是为并发设计的；而多集群对单条慢查询和数据加载帮助不大。
