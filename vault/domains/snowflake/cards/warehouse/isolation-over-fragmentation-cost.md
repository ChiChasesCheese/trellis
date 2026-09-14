---
id: isolation-over-fragmentation-cost
node: warehouse.isolation-workload-separation
type: qa
tags: [grown]
---
## Q
工作负载隔离是不是仓库拆得越细越好？过度拆分虚拟仓库（virtual warehouse）的代价是什么？

## A
不是。每个仓库各自启动都有最少 60 秒计费、各自维护冷热不一的本地缓存，拆得太细会让许多仓库利用率很低、频繁冷启动，总花费和延迟反而上升，也增加管理负担。合理的划分依据是负载特征是否真的冲突（资源争抢、规格需求、SLA、成本归属）：特征相近、查询复杂度同质的负载应合并到同一个仓库（必要时用多集群应对并发），特征冲突的才拆开。
