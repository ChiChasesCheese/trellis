%% trellis:begin %%
# 溢出（spilling）到本地与远程磁盘
*查询编译与执行*

当一个算子的工作集超出仓库内存、进而超出本地 SSD、最终溢出到远程存储时会发生什么，以及每一步所对应的延迟悬崖。

**Requires:** [[domains/snowflake/map/query.dag-execution-model|DAG 执行模型]], [[domains/snowflake/map/warehouse.sizing-t-shirt|仓库规格（T 恤尺码式）]]

## Readings
- [[snowflak-query-profile-history|查询画像(Query Profile)与查询历史的定位方法]]

## Cards (4)
1. [[spill-memory-local-remote-order]]
2. [[spill-remedies]]
3. [[spill-union-vs-union-all]]
4. [[spill-where-to-see-metrics]]
%% trellis:end %%

## Notes
