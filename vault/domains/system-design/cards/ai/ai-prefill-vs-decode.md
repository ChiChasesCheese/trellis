---
id: ai-prefill-vs-decode
node: ai.inference
type: cloze
---
LLM inference has two phases with opposite bottlenecks: **prefill** (process the whole prompt, sets time-to-first-token) is {{c1::compute}}-bound and parallelizes across prompt tokens, while **decode** (one token per step, sets inter-token latency) is {{c2::memory-bandwidth}}-bound — each step streams the weights and KV cache. This is why servers batch aggressively during decode, and why disaggregated serving runs {{c3::prefill and decode on separate GPU pools}} so long prompts don't stall other users' token streams.

## zh
LLM 推理有两个阶段有相反的瓶颈：**预填充**（处理整个 prompt，设置 time-to-first-token）是 {{c1::compute}} 约束并在 prompt token 上并行化，而 **解码**（每个步骤一个 token，设置 token 间延迟）是 {{c2::memory-bandwidth}} 约束 — 每个步骤流式传输权重和 KV 缓存。这就是为什么服务器在解码期间积极批处理，以及为什么分离的服务运行 {{c3::prefill and decode on separate GPU pools}}，因此长 prompt 不会阻塞其他用户的 token 流。
