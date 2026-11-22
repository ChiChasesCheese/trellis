---
id: aie-unbounded-consumption-controls
node: t06.unbounded-consumption-abuse-control-rate-limit-q
type: qa
step: 1
tags: [实践]
---
## Q
**Unbounded consumption · 钱包攻击与限额**｜实践 · 必会

一个公开的聊天功能，某用户发来大量超长请求，一夜之间账单翻了十倍。怎么防？

## A
**OWASP LLM10（2025）Unbounded Consumption：** 允许用户进行过多且不受控的推理，导致拒绝服务、经济损失、模型被窃取。

| 攻击 | 含义 |
|---|---|
| **Denial of Wallet** | 利用按用量计费，制造天价账单 |
| 资源密集型查询 | 构造复杂输入拖慢系统 |
| model extraction | 用大量精心设计的查询复刻你的模型 |

**控制措施（OWASP 列出的，挑关键）：**
1. **input validation：** 限定输入大小；
2. **rate limiting 与 user quotas：** 限制某一来源的单位时间请求数；
3. **timeouts 与 throttling：** 限制耗资源的操作；
4. 动态资源分配，不让单个用户或请求独占；
5. **限制 logits 和 logprobs 的暴露**（防模型窃取）；
6. 日志、监控和异常检测；
7. **graceful degradation：** 高负载时保留部分功能，而不是全挂；
8. 限制排队的动作数，并稳健扩容。

**落地的三层限额：**

| 层 | 限什么 |
|---|---|
| 每请求 | 最大输入 token、最大输出 token、超时、agent 最大步数 |
| 每用户 | 每分钟请求数、每日 token 数 |
| 每租户或全局 | 预算上限 **cost cap**，超出就熔断或降级，并报警 |

**看什么指标：** 每用户 token 用量的分布；单请求 token 用量的异常值；成本曲线的突增。

<details class="pt" markdown="1"><summary>出处</summary>

OWASP《LLM10:2025 Unbounded Consumption》genai.owasp.org/llmrisk/llm102025-unbounded-consumption/（2026-11-21 读）；Huyen ch10 §Gateway

</details>
