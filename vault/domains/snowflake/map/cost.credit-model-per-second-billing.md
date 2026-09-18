%% trellis:begin %%
# 信用点模型与按秒计费
*成本、计量与可观测性*

仓库按秒以信用点（credit）计费（最低 60 秒起计），与任何固定的实例价格脱钩。

**Requires:** [[domains/snowflake/map/architecture.storage-compute-separation|存储与计算分离（storage/compute separation）]]

**Unlocks:** [[domains/snowflake/map/cost.warehouse-billing-60s-minimum|仓库最低计费时长]], [[domains/snowflake/map/cost.serverless-feature-billing|无服务器功能计费]], [[domains/snowflake/map/cost.cloud-services-free-tier|云服务免费额度]], [[domains/snowflake/map/cost.ai-token-metering|AI/Cortex 令牌计量]]

## Readings
- [[snowflak-compute-cost-detail|计算成本细则:60 秒起收、serverless 计费与云服务 10% 免费额度]]
- [[snowflak-cost-overview|整体成本构成:计算、存储与数据传输]]

## Cards (5)
- [[cost-credit-decoupled-from-instance]]
- [[cost-monthly-credit-calc]]
- [[cost-storage-average-daily-bytes]]
- [[cost-three-usage-types]]
- [[cost-warehouse-idle-vs-suspended]]
%% trellis:end %%

## Notes
