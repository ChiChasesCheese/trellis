---
nodes: [problems.realtime.llm-chat-service]
url: https://www.usenix.org/conference/osdi22/presentation/yu
---
# Orca: A Distributed Serving System for Transformer-Based Generative Models

值得读：连续/迭代级批处理（continuous / iteration-level batching）与 selective batching
的原始出处（OSDI'22），报告相比 NVIDIA FasterTransformer 在 GPT-3 175B 上 36.9 倍吞吐
提升。[[ai.inference|Inference Serving]] 的概念卡已经覆盖了这个机制本身是什么，本题解
不重复其内容，只在容量估算和「深入探讨」第 2 节引用其数量级作为"批处理价值有多大"的
参照，重点转向 KV 缓存容量和路由这一层。
