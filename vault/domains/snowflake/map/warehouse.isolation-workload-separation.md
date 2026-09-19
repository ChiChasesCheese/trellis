%% trellis:begin %%
# 工作负载隔离
*虚拟仓库（virtual warehouse）*

将 ETL、BI 与临时查询（ad hoc）工作负载分别运行在独立的仓库上，使某个负载的突增不会抢占另一个负载的计算资源。

**Requires:** [[domains/snowflake/map/warehouse.sizing-t-shirt|仓库规格（T 恤尺码式）]]

## Cards (5)
1. [[isolation-chargeback-and-access]]
2. [[isolation-over-fragmentation-cost]]
3. [[isolation-per-workload-tuning]]
4. [[isolation-separate-warehouses-same-data]]
5. [[isolation-what-is-not-isolated]]
%% trellis:end %%

## Notes
