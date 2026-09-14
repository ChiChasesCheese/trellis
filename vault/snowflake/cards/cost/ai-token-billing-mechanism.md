---
id: ai-token-billing-mechanism
node: cost.ai-token-metering
type: qa
tags: [grown]
---
## Q
在 SQL 里调用 Snowflake Cortex 的 LLM 函数（如 `AI_COMPLETE`）处理一张表，费用按什么计量？为什么不像普通查询那样只看仓库运行时长？

## A
Cortex LLM 函数按处理的令牌（token，模型切分文本的基本单位）数量计费，通常输入和输出令牌都计入，每百万令牌消耗的信用点因模型而异，大模型比小模型贵。推理在 Snowflake 管理的 GPU 资源上执行，与虚拟仓库的计算是分开的，所以费用取决于处理了多少文本、选了哪个模型，而不是仓库开了多久。执行这条 SQL 的仓库本身仍按自己的运行时间另外计费。
