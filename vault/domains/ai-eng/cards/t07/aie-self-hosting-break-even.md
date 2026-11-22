---
id: aie-self-hosting-break-even
node: t07.self-hosting-vs-api-break-even-point
type: qa
step: 1
tags: [考点]
---
## Q
**Self-hosting vs API · 盈亏平衡点**｜考点 · 必会

API 每月花 3 万美元，团队想自己买 GPU 部署开源模型。怎么算账，关键变量是什么？

## A
**成本结构的差别：**

| | model API | self-hosting |
|---|---|---|
| 单价 | 按 token 计费，单价基本不随规模变 | 集群成本固定，**用量越大单价越低** |
| 额外成本 | 依赖供应商 SLA、限流 | 工程时间、人才、优化、运维、guardrails |

一个例子：集群最多服务 10 亿 token/天，则服务 100 万还是 10 亿 token，算力成本相同。

**盈亏平衡的算式（示意）：**

`API 日成本 = 日 token 数 × API 单价`
`自建日成本 = GPU 日成本（含闲置）+ 工程与运维摊销`

当 `日 token 数 × API 单价 > 自建日成本`，自建才开始划算。**关键变量是利用率：** GPU 不管有没有请求都要付钱，利用率越低，实际每 token 成本越高。训练时利用率 50% 算尚可、超过 70% 算很好（这是训练时的经验说法；推理要自己测）。

**算账时别漏：**
1. 显存：模型要放得下，7B 参数按 2 字节算至少 14 GB；加上 KV cache 和并发；
2. 峰谷差：按峰值买卡，平时空转；
3. 工程成本：「API 贵，但工程可能更贵」；
4. API 价格会降：自建几个月后供应商降价一半，自建反而更贵；
5. 非成本因素：数据不能出境、要冻结模型版本、要访问 logprobs、要微调，这些可能直接决定要自建。

**判断流程：** 先量出日均与峰值 token 数 → 用评测确认开源模型质量够用 → 算含利用率的自建成本 → 对比，并留 30–50% 的安全边际（经验取值，不是实测）。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch4 §Cost and Latency；§API cost versus engineering cost；ch2 §Model Size（训练利用率）；ch9 §Selecting Accelerators

</details>
