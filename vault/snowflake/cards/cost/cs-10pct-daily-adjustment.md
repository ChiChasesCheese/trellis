---
id: cs-10pct-daily-adjustment
node: cost.cloud-services-free-tier
type: qa
source: snowflake-docs
---
## Q
Snowflake 的云服务层（Cloud Services，负责认证、元数据管理、查询编译优化、访问控制等）也消耗信用点，为什么大多数账户的账单上几乎看不到这一项？

## A
云服务用量只有在当天的云服务消耗超过当天虚拟仓库用量的 10% 时才收费。每天（按 UTC 时区）用“当日仓库用量 × 10%”算出一个调整额度，从云服务消耗中抵扣；只有超出的部分计费。典型工作负载的云服务开销远低于仓库用量的 10%，所以通常全额被抵扣。
