---
id: auto-suspend-multi-cluster-whole-warehouse
node: warehouse.auto-suspend-resume
type: qa
source: snowflake-docs
---
## Q
多集群仓库（multi-cluster warehouse）上，auto-suspend（自动挂起）和 auto-resume（自动恢复）是对单个集群生效还是对整个仓库生效？具体何时触发？

## A
只对整个仓库生效，不作用于单个集群。自动挂起只在仓库已缩到最小集群数（通常为 1，也可能更多）且在设定时间内没有任何活动时才发生；多出来的集群由伸缩机制按负载关闭，与 auto-suspend 无关。自动恢复只在整个仓库都已挂起（没有任何集群在运行）时适用。
