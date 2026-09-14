---
nodes:
- cost.credit-model-per-second-billing
title: 整体成本构成:计算、存储与数据传输
corpus: snowflake-docs
section: 32-cost-understanding-overall
url: https://docs.snowflake.com/en/user-guide/cost-understanding-overall
tags:
- canonical
---

# 整体成本构成:计算、存储与数据传输

Snowflake 的总成本拆分成三类,彼此独立计量:计算资源消耗信用点(credit),按信用点单价折算成账单金额;存储按月度平均字节数、按 TB 计费;数据传输只在跨区域/跨云传出(egress)时收费,导入不收费。计算资源本身又分三种:用户管理的虚拟仓库(按秒计费、每次启动 60 秒最低消费)、Snowflake 托管的 serverless 特性(如 Search Optimization、Snowpipe)自动伸缩、以及云服务层(cloud services)——后者只有当日消耗超过当日仓库计算量的 10% 时才单独计费。读完这份总账,能理解为什么后续每个具体计费细则(仓库、serverless、云服务)都要单独展开讲。
