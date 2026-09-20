---
id: problems-llm-chat-service-kv-cache-bytes-per-token
node: problems.realtime.llm-chat-service
type: qa
step: 1
tags: [grown]
---
## Q
For a 70-billion-parameter chat model shaped like Llama 3 70B (80 layers, 8 key-value heads from grouped-query attention, head dimension 128, FP16 weights), how do you compute the KV cache（键值缓存）memory cost of a single token, and why does that number, not GPU compute power, cap how many conversations one GPU replica can serve concurrently?

## A
Per token, each of the 80 layers stores one key vector and one value vector, each sized (KV heads × head dimension): 2 (K and V) × 8 × 128 × 2 bytes (FP16) = 4,096 bytes per layer, times 80 layers = 327,680 bytes ≈ 320 KiB per token. A conversation holding 2,000 tokens of context therefore pins about 0.65 GB of GPU memory for as long as it stays active — memory that no other conversation can use. A serving replica has a fixed pool of GPU memory left over after loading model weights, so however fast its GPUs compute, the number of conversations it can hold open at once is capped by dividing that leftover memory by the per-conversation KV cache size, not by FLOPs.

## Q zh
对于一个 700 亿参数、形状类似 Llama 3 70B 的聊天模型（80 层、8 个分组查询注意力的 KV 头、每头维度 128、FP16 权重），如何计算单个 token 的 KV 缓存（键值缓存）内存开销？为什么这个数字而不是 GPU 算力，决定了一个 GPU 副本能同时服务多少个会话？

## A zh
每个 token，80 层中的每一层都要存一个 key 向量和一个 value 向量，每个的大小是（KV 头数 × 头维度）：2（K 和 V）× 8 × 128 × 2 字节（FP16）= 每层 4,096 字节，乘以 80 层 = 327,680 字节 ≈ 每 token 320 KiB。因此一个持有 2,000 token 上下文的会话，只要保持活跃，就会占用约 0.65 GB 的 GPU 显存——这是其他任何会话都无法使用的显存。一个推理副本在加载完模型权重后剩下固定大小的显存池，无论 GPU 算力多强，它能同时保持多少个会话，都由「剩余显存 ÷ 每会话 KV 缓存大小」决定，而不是由 FLOPs 决定。
