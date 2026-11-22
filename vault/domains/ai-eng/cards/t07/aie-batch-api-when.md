---
id: aie-batch-api-when
node: t07.batch-api-async-processing
type: qa
step: 1
tags: [摘要]
---
## Q
**Batch API 与 async processing**｜摘要 · 必会

下面五件事，哪些适合走 batch API，哪些必须走在线 API？为什么？

1. 聊天机器人回复用户；
2. 每天夜里总结当天的客服工单；
3. 新模型上线，要把 200 万条历史数据重新处理一遍；
4. 为评测集的每条样本跑 LLM judge；
5. 代码编辑器里的补全。

## A
**两类 API：**

| | Online API | Batch API |
|---|---|---|
| 优化目标 | **延迟**，请求一到就处理 | **成本**（和吞吐） |
| 周转时间 | 秒到分钟 | 小时级 |
| 价格 | 标准 | 书里：Google Gemini 和 OpenAI 的 batch API 成本**降低 50%**（写书时，2024 年） |

延迟要求放宽，供应商就能把请求攒在一起处理，用更便宜的硬件。

| 需求 | 走哪个 | 理由 |
|---|---|---|
| 1 聊天 | 在线 | 用户在等 |
| 2 夜间总结 | **batch** | 没人等，周期性报表 |
| 3 重新处理 200 万条 | **batch** | 数据迁移，量大不急 |
| 4 评测的 judge | **batch** | 离线，不追求即时 |
| 5 补全 | 在线 | 要求极低延迟 |

**书里列的 batch 适用场景：** 合成数据、周期性报表（总结消息、分析工单）、新客户上线时处理全部上传文档、换模型后全量重处理、给大量客户生成个性化推荐或简报、重建知识库索引。

**注意（与传统 ML 的区别）：** 传统 ML 里的 batch inference 是**提前算好**再取；基础模型的输入是开放的，没法预先算，所以这里的 batch 只是"晚点、成批地处理"。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch9 §Online and batch inference APIs

</details>
