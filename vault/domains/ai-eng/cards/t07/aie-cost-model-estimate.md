---
id: aie-cost-model-estimate
node: t07.cost-model-input-output-cache-read-write
type: qa
step: 2
tags: [实践]
---
## Q
**Cost model · 上线前怎么估月成本**｜实践 · 必会

一个客服机器人，预计每天 10 万次对话。你怎么在上线前估计月成本，并找到最该优化的地方？

## A
**步骤：**
1. **采样真实请求**，统计每次调用的：输入 token 数（system prompt、历史、检索资料、用户输入）、输出 token 数、调用次数（一次对话可能调多次）；
2. **按分位数而不是平均数**估：长尾请求（长对话、长文档）会拉高成本；
3. 套公式：`日成本 = 调用次数 × (输入 × 输入单价 + 输出 × 输出单价)`，再扣掉缓存命中节省的部分；
4. **分项占比**：哪一部分占输入的大头？

| 常见发现 | 优化 |
|---|---|
| 固定的 system prompt 占输入大头 | prompt caching；精简 prompt |
| 检索资料太多 | 减少 k、reranking 截断 |
| 历史越来越长 | 摘要、只保留相关部分 |
| 输出很长 | 要求简洁、设最大输出、结构化输出 |
| 简单问题也用最贵的模型 | 模型路由 |
| 重复的问题 | exact cache |

5. **指标进监控：** 每个请求的输入 / 输出 token 数、缓存命中率、按功能和用户统计的成本。

**书里的提醒：** 输入和输出 token 越多越贵，很多应用因此去减少输入和输出的 token 数；要区分"必须满足"和"最好有"的成本与延迟要求。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch4 §Cost and Latency；ch10 §Metrics（跟踪 token 数、缓存成本与命中率）

</details>
