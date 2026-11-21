---
id: aie-online-evals-signals
node: t05.online-evals-production-monitoring-sampled-scori
type: qa
step: 1
tags: [摘要]
---
## Q
**Online evals 与 production monitoring · 该监控什么**｜摘要 · 必会

应用上线后，没有标准答案可对照。你能持续跟踪哪些信号来发现质量问题？全量评还是抽样评？

## A
**思路：** 先想清楚**要抓哪些失败**，再据此设计指标。指标本身不是目的，目的是知道"哪里出问题"和"哪里能改进"。

| 类别 | 例子 |
|---|---|
| **格式失败**（最容易） | 非法 JSON 的比例；其中容易修复的比例 |
| **质量**（开放式输出） | 事实一致性、简洁等，多数可用 judge 计算 |
| **安全** | 毒性、输入输出里的敏感信息、guardrail 触发率、拒答率、异常查询 |
| **用户信号** | 中途停止生成的频率、平均对话轮数、每次输入和输出的平均 token 数 |
| **延迟、成本** | TTFT、TPOT、总延迟、token 数、每秒请求数（有限流时） |
| **各组件的指标** | RAG 的 context precision；向量库的存储和查询时间 |

**抽样还是全量：**
- **spot check（抽样）：** 抽一部分快速发现问题，便宜；
- **exhaustive check（全量）：** 看每个请求，全面，贵；
- 通常两者结合：便宜的指标全量，贵的 judge 抽样。

**要能按维度切开：** 用户、版本、prompt 版本、请求类型、时间。

**与评测的关系：** 线上指标应该和离线评测对应：离线好的模型线上也该好；监控里发现的问题**要回流到评测集**。

**出处：** Huyen《AI Engineering》ch10 §Monitoring and Observability → Metrics
