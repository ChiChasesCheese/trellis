%% trellis:begin %%
# 存储与计算分离（storage/compute separation）
*核心架构*

为何将持久化存储与瞬时计算解耦，能让二者独立伸缩、独立失败，以及这种解耦在网络往返上的代价。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/snowflake/map/storage.micro-partition-format|微分区（micro-partition）格式]], [[domains/snowflake/map/storage.object-storage-backend|对象存储后端]], [[domains/snowflake/map/warehouse.sizing-t-shirt|仓库规格（T 恤尺码式）]], [[domains/snowflake/map/cost.credit-model-per-second-billing|信用点模型与按秒计费]]

## Readings
- [[snowflak-key-concepts-architecture|Snowflake 关键概念与整体架构]]

## Cards (5)
1. [[storage-compute-sep-independent-scaling]]
2. [[storage-compute-sep-multiple-warehouses-one-copy]]
3. [[storage-compute-sep-no-shared-compute]]
4. [[storage-compute-sep-self-managed]]
5. [[storage-compute-sep-vs-coupled-traditional]]
%% trellis:end %%

## Notes
