%% trellis:begin %%
# 自动挂起与自动恢复
*虚拟仓库（virtual warehouse）*

在最后一条查询结束后的数秒内停止计费的空闲超时机制，以及恢复时的冷启动代价。

**Requires:** [[domains/snowflake/map/warehouse.sizing-t-shirt|仓库规格（T 恤尺码式）]]

## Readings
- [[snowflak-warehouse-best-practices|仓库调优:扩容(up)还是扩出(out)、本地磁盘缓存]]
- [[snowflak-warehouses-overview|虚拟仓库总览:尺寸、自动挂起与排队]]

## Cards (5)
1. [[auto-resume-trigger-and-cost-control]]
2. [[auto-suspend-60s-restart-billing]]
3. [[auto-suspend-match-query-gaps]]
4. [[auto-suspend-multi-cluster-whole-warehouse]]
5. [[auto-suspend-when-to-disable]]
%% trellis:end %%

## Notes
