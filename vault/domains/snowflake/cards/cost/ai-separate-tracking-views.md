---
id: ai-separate-tracking-views
node: cost.ai-token-metering
type: qa
tags: [grown]
---
## Q
财务发现 AI 相关支出上升，但查看各仓库的信用点消耗却看不出变化。Cortex AI 的消耗应该去哪里看？为什么仓库视图里看不到？

## A
Cortex AI 函数的令牌消耗与仓库计算分开计量，在 `METERING_HISTORY` / `METERING_DAILY_HISTORY` 中以 AI 服务（AI_SERVICES）这一服务类型出现，并可在 `CORTEX_FUNCTIONS_USAGE_HISTORY`、`CORTEX_FUNCTIONS_QUERY_USAGE_HISTORY` 等 ACCOUNT_USAGE 视图中按函数、模型乃至查询查看令牌数和信用点。仓库计量视图只记录仓库自身的运行时长，所以看不到令牌费用。
