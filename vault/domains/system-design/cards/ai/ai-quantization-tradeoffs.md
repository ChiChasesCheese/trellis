---
id: ai-quantization-tradeoffs
node: ai.inference
type: qa
---
## Q
Weight-only INT4/INT8 vs FP8 (weights + activations) vs KV-cache quantization: which serving bottleneck does each attack, and where are the quality cliffs?

## A
- **Weight-only (INT8/INT4, e.g. AWQ/GPTQ)**: shrinks weight streaming — attacks **memory-bandwidth-bound decode** and lets bigger models fit per GPU. Compute still runs in higher precision after dequant.
- **FP8 weights + activations**: engages the GPU's low-precision tensor cores — attacks **compute-bound prefill** too; needs hardware support (H100-class on).
- **KV-cache quantization (8/4-bit)**: attacks the **capacity ceiling on concurrency** — more sequences resident per GPU ([[ai-kv-cache]]).

Quality: 8-bit is near-lossless; **4-bit is where cliffs appear** — degradation is task-dependent (reasoning and long-context suffer first) and invisible to perplexity alone, so gate rollouts on your own task evals, not benchmark deltas.

## Q zh
仅权重 INT4/INT8 vs FP8（权重+激活）vs KV-cache 量化：每个攻击哪个服务瓶颈，质量悬崖在哪里？

## A zh
- **仅权重（INT8/INT4，例如 AWQ/GPTQ）**：缩小权重流 — 攻击 **内存带宽约束的解码** 并让更大的模型适应每个 GPU。反量化后计算仍在更高精度下运行。
- **FP8 权重+激活**：利用 GPU 的低精度张量核心 — 也攻击 **计算约束的预填充**；需要硬件支持（H100 级别开启）。
- **KV-cache 量化（8/4 位）**：攻击 **并发容量上限** — 更多序列驻留在每个 GPU 中（[[ai-kv-cache]]）。

质量：8 位接近无损；**4 位是悬崖出现的地方** — 降级是任务相关的（推理和长上下文首先受害）并且对困惑度单独不可见，所以在你自己的任务 eval 上控制推出，而不是基准增量。
