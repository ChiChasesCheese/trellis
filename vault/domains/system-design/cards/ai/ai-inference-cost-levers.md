---
id: ai-inference-cost-levers
node: ai.inference
type: qa
---
## Q
Latency on an LLM endpoint feels fine but the GPU bill is too high. Name four levers that cut cost per token without swapping hardware.

## A
- **Quantization** (weights and/or KV cache to 8- or 4-bit): shrinks memory and bandwidth needs → bigger batches per GPU, minor quality cost.
- **Right-size the model**: route easy requests to a small/distilled model, escalate hard ones (model cascade/router).
- **Prompt/prefix caching**: stop re-prefilling the shared system prompt on every call.
- **Speculative decoding**: a draft model proposes several tokens, the big model verifies them in one pass — more tokens per weight-load, same output distribution.

(Streaming, by contrast, is a perceived-latency lever — it doesn't reduce cost.)

## Q zh
LLM 端点上的延迟感觉不错但 GPU 账单太高。列举四个不更换硬件就降低每 token 成本的杠杆。

## A zh
- **量化**（权重和/或 KV 缓存到 8 位或 4 位）：缩小内存和带宽需求 → 每个 GPU 更大的批次，小质量成本。
- **适当调整模型大小**：将容易的请求路由到小/蒸馏模型，升级困难的（模型级联/路由器）。
- **Prompt/前缀缓存**：停止在每次调用上重新预填充共享系统提示。
- **推测解码**：draft 模型提议几个 token，大型模型一次通过验证它们 — 更多 token 每权重加载，相同输出分布。

（相比之下，流是一个感知延迟杠杆 — 它不降低成本。）
