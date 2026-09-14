---
id: cost-warehouse-idle-vs-suspended
node: cost.credit-model-per-second-billing
type: qa
source: snowflake-docs
---
## Q
一个 Large 仓库（每小时 8 credit）白天开着但大部分时间没有查询，晚上被挂起。它在两种状态下各自计费吗？

## A
仓库只要处于运行状态就按秒计费，不论是否在执行查询，所以空转也在消耗每小时 8 credit 的费率；挂起（suspended）后不消耗任何信用点。按秒计费意味着账单只反映仓库实际运行的时长，因此控制成本的关键是缩短运行但空闲的时间（例如合理设置自动挂起），而不是担心按整小时取整。
