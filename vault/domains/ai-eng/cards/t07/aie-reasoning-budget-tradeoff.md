---
id: aie-reasoning-budget-tradeoff
node: t07.reasoning-budget-thinking-mode
type: qa
step: 1
tags: [摘要]
---
## Q
**Reasoning budget · thinking mode 开不开、给多少**｜摘要 · 必会

分类接口和一个复杂的数学证明接口都接到了带 thinking mode 的模型。两个接口都开最大的思考预算吗？

## A
**thinking tokens 是模型在给出最终回答前的内部推理，按输出 token 计费**（接口会报告其中多少是 thinking tokens）。所以多思考 = 多花钱 + 多等待。

**对应的原理是 test time compute：** 给每次推理多分配算力（多采样几个、或让模型想更久）通常能提升效果，但**成本近似线性增长**（采样 2 个输出约花 2 倍）。DeepMind 的研究认为，增加推理算力有时比增大模型更划算。

| 任务 | 思考预算 |
|---|---|
| 分类、抽取、改写、简单问答 | 不开，或最低档 |
| 多步推理、数学、复杂代码 | 开，并随难度增加 |
| 不确定 | 用评测集在几档预算下各跑一遍，画「质量 vs 成本 vs 延迟」 |

**以 Anthropic 的 API 为例（2026-11）：**
- 手动模式 `budget_tokens`：最小 1,024，必须小于 `max_tokens`；预算是**目标而非硬上限**，`max_tokens` 才是硬上限；
- 新的模型（4.7 及以后）不再支持手动预算，改用 **adaptive thinking**：模型自己决定想不想、想多久，用 `effort` 控制深度，简单输入可能完全不思考；
- 手动模式下中途更改预算会让 prompt cache 失效；
- 预算超过 32k 的任务建议走批处理，避免长连接超时。

**监控：** 记录每次请求的 thinking token 数，按接口看分布。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch2 §Test Time Compute；Anthropic 文档 Extended thinking（platform.claude.com/docs/en/build-with-claude/extended-thinking，2026-11-21 读，版本会变）

</details>
