---
id: leetcode-c-transformer-attention-kv-cache-application
node: topics.uncategorised
type: qa
anki: 1787365291381
tags: [algorithm::kv-cache, algorithm::matrix-multiplication, algorithm::scaled-dot-product-attention, algorithm::softmax, application, case, case::transformer-attention-kv-cache, category::developer-infrastructure, chapter::07, chapter::08, chapter::09, chapter::15, leetcode, system::llm-inference, system::transformer]
---
## Q
Transformer self-attention 的公式每一步在做什么？KV cache 省掉了什么、没省掉什么？

## A
`softmax(QK^T/√d + mask)V`：QK 点积算相关性，缩放稳定 softmax，causal mask 禁看未来，权重再混合 V。KV cache 保存各层历史 K/V，decode 只算并追加新 K/V；但新 Q 仍需读取并关注历史 K/V。

**Evidence**

Transformer 原论文定义 scaled dot-product attention；vLLM 官方设计说明以 blocks 管理 KV cache 来降低 serving 碎片。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FTransformer%20Attention%EF%BC%9A%E7%9F%A9%E9%98%B5%E4%B9%98%E6%B3%95%E3%80%81Softmax%20%E4%B8%8E%20KV%20Cache)
