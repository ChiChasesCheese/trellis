---
id: ai-bigger-warehouse-no-help
node: cost.ai-token-metering
type: qa
tags: [grown]
---
## Q
一条对百万行文本调用 Cortex LLM 函数的查询很慢，工程师把仓库从 Medium 调到 2X-Large。为什么这通常既不会明显提速，又会增加费用？

## A
LLM 推理的耗时主要在 Snowflake 管理的模型服务上，而不是仓库节点的算力上；仓库只负责扫描数据和分发调用，调大仓库不会让模型推理本身变快。仓库费用却随尺寸翻倍增长，令牌费用则不变。Cortex LLM 函数一般建议用不大于 Medium 的仓库；真正影响成本的是令牌量，应通过选更小的模型、截断或精简输入文本、先过滤掉不需要处理的行来控制。
