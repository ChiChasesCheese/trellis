%% trellis:begin %%
# 自动重新聚簇（automatic reclustering）
*存储引擎与微分区（micro-partition）*

在 DML 操作使聚簇状态漂移后，负责重写微分区以恢复聚簇的后台服务，以及它消耗的信用点（credit）成本。

**Requires:** [[domains/snowflake/map/storage.clustering-keys|聚簇键（clustering key）]]

## Readings
- [[snowflak-automatic-clustering|自动重新聚簇服务(Automatic Clustering)]]

## Cards (6)
- [[auto-recluster-classic-vs-optima]]
- [[auto-recluster-key-change-cost-traps]]
- [[auto-recluster-not-under-resource-monitor]]
- [[auto-recluster-optima-ingest-billing]]
- [[auto-recluster-optima-suspend-catch-up]]
- [[auto-recluster-serverless-nonblocking]]
%% trellis:end %%

## Notes
