%% trellis:begin %%
# 仓库规格（T 恤尺码式）
*虚拟仓库（virtual warehouse）*

从 XS 到 6XL 实际改变的是什么（节点数量，而非单节点算力），以及规格选择如何在延迟与成本之间权衡。

**Requires:** [[architecture.storage-compute-separation|存储与计算分离（storage/compute separation）]]

**Unlocks:** [[warehouse.multi-cluster-scaling-policy|多集群伸缩策略]], [[warehouse.auto-suspend-resume|自动挂起与自动恢复]], [[warehouse.isolation-workload-separation|工作负载隔离]], [[warehouse.resource-monitors|资源监控器（resource monitor）]], [[query.spilling-to-remote-disk|溢出（spilling）到本地与远程磁盘]], [[cache.warehouse-local-disk-cache|仓库本地 SSD 缓存]], [[pipelines.task-serverless-vs-warehouse|无服务器任务与仓库支持型任务]], [[cost.warehouse-billing-60s-minimum|仓库最低计费时长]]

## Readings
- [[snowflak-warehouse-best-practices|仓库调优:扩容(up)还是扩出(out)、本地磁盘缓存]]
- [[snowflak-warehouses-overview|虚拟仓库总览:尺寸、自动挂起与排队]]

## Cards (6)
- [[wh-size-bigger-can-cost-same]]
- [[wh-size-credits-doubling]]
- [[wh-size-data-loading-files-matter]]
- [[wh-size-larger-not-faster-small-queries]]
- [[wh-size-resize-running-effects]]
- [[wh-size-table-bytes-over-rows]]
%% trellis:end %%

## Notes
