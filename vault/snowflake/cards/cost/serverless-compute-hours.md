---
id: serverless-compute-hours
node: cost.serverless-feature-billing
type: qa
source: snowflake-docs
---
## Q
无服务器（serverless）功能的费用具体按什么计量？为什么不同功能每小时消耗的信用点不同？

## A
按 Snowflake 管理计算资源的总使用量计量，单位是计算小时（compute-hour），按秒计算并向上取整到整秒，而不是像仓库那样每次启动至少 60 秒。每个计算小时消耗多少信用点因功能而异，由服务消耗表中的“无服务器功能信用点表”规定，因为不同功能所用的底层资源类型和规模不同。
