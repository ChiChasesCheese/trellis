---
id: isolation-chargeback-and-access
node: warehouse.isolation-workload-separation
type: qa
tags: [grown]
---
## Q
按团队或负载划分虚拟仓库（virtual warehouse），除了性能隔离，在成本归属和权限控制上还带来什么好处？

## A
成本归属：credit（信用点）按仓库计量，可在 `WAREHOUSE_METERING_HISTORY` 等视图中按仓库直接统计，每个团队或负载的花费一目了然，便于内部分摊（chargeback）。权限控制：只有被授予某仓库 USAGE 权限的角色才能用它运行查询，于是可以限制谁能动用昂贵的大仓库，并给每个仓库单独挂 resource monitor（资源监控器）设置额度。
