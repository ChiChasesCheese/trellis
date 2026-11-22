---
id: aie-long-context-vs-rag
node: t03.long-context-vs-rag
type: qa
step: 1
tags: [考点]
---
## Q
**Long context vs RAG · 什么时候直接塞整库**｜考点 · 必会

知识库约 15 万 token，模型的 context window 是 20 万。直接全塞进 prompt，还要不要做 RAG？

## A
**能塞，但要算三笔账：**

| 账 | 直接塞整库 | RAG |
|---|---|---|
| 成本 | 每次请求都为所有输入 token 付费 | 只放最相关的几块 |
| 延迟 | 输入越长越慢 | 检索多一步，但 prompt 短 |
| 质量 | 模型能装不等于能用好；中间位置的信息最容易被忽略 | 噪声更少 |

- 质量证据：Liu 等（2023）发现模型对 prompt 开头和结尾的信息理解得比中间好，用 **needle in a haystack** 测试可以测出来；
- Anthropic 对 Claude 的建议：知识库小于 200,000 token（约 500 页）时，可以整库放进 prompt，不用 RAG；其他模型没有同类建议。

**结论：**
- 库小、问题少、要求实现简单 → 整库放入，配合 **prompt caching**（让不变的前缀便宜很多，见 Cost 那组卡）；
- 数据会一直增长（人们很少删数据）、有按用户的权限、成本敏感 → RAG；
- 没有定论的时候，用自己的评测集对比两种方案的质量和单次成本。

**别忘了：** 上下文再长也会有应用的数据需求超过它。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch6 §RAG（Note）；ch5 §Context Length and Context Efficiency

</details>
