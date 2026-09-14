---
id: min60-rules
node: cost.warehouse-billing-60s-minimum
type: qa
source: snowflake-docs
---
## Q
Snowflake 虚拟仓库“按秒计费、60 秒起计”的具体规则是什么？仓库运行 20 秒和运行 61 秒分别怎么计费？

## A
仓库每次启动或恢复（resume）时，先按小时费率收取 1 分钟的费用；运行满 1 分钟后，只要持续运行就按秒计费。因此运行 20 秒也按 60 秒计费；运行 61 秒则按 61 秒计费。例如 X-Large（16 credit/小时）运行 0–60 秒计 0.267 credit，61 秒计 0.271 credit。
