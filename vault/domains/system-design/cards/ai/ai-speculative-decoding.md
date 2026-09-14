---
id: ai-speculative-decoding
node: ai.inference
type: qa
---
## Q
Speculative decoding runs a *second* model per request yet makes serving faster. Explain the mechanism, why output quality is unchanged, and when it stops helping.

## A
A cheap **draft model** proposes k tokens autoregressively; the target model then scores all k **in one forward pass** (parallel, like prefill) and accepts the longest prefix consistent with its own distribution — rejected positions are resampled from the target. Because decode is **memory-bandwidth-bound** ([[ai-prefill-vs-decode]]), verifying k tokens costs about the same weight-streaming as generating 1, so accepted tokens are nearly free.

Quality: the accept/resample rule is exact rejection sampling — outputs follow the **target model's distribution exactly**; speed is the only variable.

Limits: speedup ∝ acceptance rate (draft must imitate the target well; predictable text like code accepts more), and the win **fades at high batch sizes**, where the GPU is already compute-saturated and there are no idle FLOPs to spend on verification.

## Q zh
推测解码每个请求运行一个 *第二个* 模型，但使服务更快。解释机制，为什么输出质量不变，以及何时停止帮助。

## A zh
便宜的 **draft 模型** 自回归地提议 k 个 token；目标模型然后在 **一次前向通过中** 评分所有 k 个（并行，像 prefill）并接受与其自己的分布一致的最长前缀 — 拒绝的位置从目标重新采样。因为解码是 **内存带宽约束**（[[ai-prefill-vs-decode]]），验证 k 个 token 的成本大约与生成 1 个相同的权重流，所以接受的 token 几乎是免费的。

质量：accept/resample 规则是精确拒绝采样 — 输出完全遵循 **目标模型的分布**；速度是唯一的变量。

限制：加速 ∝ 接受率（draft 必须模拟目标很好；像代码这样的可预测文本接受更多），以及赢 **在高批大小下褪色**，其中 GPU 已经计算饱和，没有空闲 FLOP 用于验证。
