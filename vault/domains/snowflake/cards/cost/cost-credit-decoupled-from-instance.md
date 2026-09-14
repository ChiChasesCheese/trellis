---
id: cost-credit-decoupled-from-instance
node: cost.credit-model-per-second-billing
type: qa
source: snowflake-docs
---
## Q
为什么 Snowflake 用“信用点（credit）”而不是“按某种云主机实例每小时多少美元”来计价计算资源？

## A
信用点是抽象的资源计量单位，只在实际使用资源时消耗：仓库运行、云服务层工作、无服务器功能运行时才计。它把计费与底层是哪家云、哪种实例解耦：仓库尺寸按 T 恤码定义，每大一级算力约翻倍、每小时信用点也翻倍（X-Small 1、Small 2、Medium 4、Large 8……）；信用点单价则由版本、区域和合同决定。因此同一工作负载在不同云上的信用点消耗可比，价格谈判只涉及单价。
