---
id: aie-attention-why-long-is-costly
node: t01.transformer-attention
type: qa
step: 2
tags: [先修]
---
## Q
**Attention · 为什么上下文越长越贵**｜先修 · 必会

同一个模型，prompt 是 500 token 时回答很快，是 100,000 token 时明显更慢、更贵、更占显存。从 attention 的做法推一推，原因在哪？

## A
**推导：**
1. 每生成一个新 token，当前位置的 Q 要和**前面每一个** token 的 K 做一次点积。前面有 n 个 token，就要做 n 次。
2. 每个前面的 token 都有自己的 K 和 V，必须**算出来并存着**，供之后每一步取用。
3. 所以序列越长：每步的比较越多（更慢），要存的 K、V 越多（更占显存）。

| | 500 token 的 prompt | 100,000 token 的 prompt |
|---|---|---|
| 每步要比较的前文 | 约 500 个 | 约 100,000 个 |
| 要存的 K、V 个数 | 500 组 | 100,000 组 |

**补充：**
- 这是把 context length 做长很难的原因之一，后面的推理优化章节专门处理"怎么高效算和存 K、V"。
- 模型的**参数总数不受 context length 影响**，但运行时的显存占用会。
- 慢和贵体现在账单和延迟上：输入越长，费用与延迟越高（后面成本、延迟的卡再细讲）。

**出处：** Huyen《AI Engineering》ch2 §Attention mechanism（"the longer the sequence, the more key and value vectors need to be computed and stored"）、§Transformer block（Table 2-4 前的说明）
