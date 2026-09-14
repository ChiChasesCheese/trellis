---
nodes:
- cost.warehouse-billing-60s-minimum
- cost.serverless-feature-billing
- cost.cloud-services-free-tier
- cost.credit-model-per-second-billing
title: 计算成本细则:60 秒起收、serverless 计费与云服务 10% 免费额度
corpus: snowflake-docs
section: 33-cost-understanding-compute
url: https://docs.snowflake.com/en/user-guide/cost-understanding-compute
tags:
- canonical
---

# 计算成本细则:60 秒起收、serverless 计费与云服务 10% 免费额度

信用点(credit)是为消耗计算资源付费的计量单位,虚拟仓库每次启动或恢复都按 1 分钟起收,之后转为按秒计费;把仓库从 5X-Large/6X-Large 降到 4X-Large 及以下时,新旧资源会有短暂重叠计费的窗口。Serverless 特性(Search Optimization、Snowpipe 等)不依赖用户仓库,而是按“计算小时”(compute-hour,精确到秒后向上取整)单独计费,费率因特性而异。云服务层(cloud services)每天的消耗只有超过当日仓库计算总量 10% 的部分才会被计入账单,这个 10% 调整按 UTC 每天单独计算,因此月度账单里的实际调整幅度往往显著小于名义上的 10%。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/cost-understanding-compute)

## Archived copy
![[snowflak-compute-cost-detail-clip]]
%% trellis:end %%
