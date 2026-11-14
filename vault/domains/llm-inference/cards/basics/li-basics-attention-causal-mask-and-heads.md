---
id: li-basics-attention-causal-mask-and-heads
node: basics.attention
type: qa
step: 3
---
## Q
什么是因果掩码（causal mask）和多头注意力（multi-head attention）？它们分别解决什么问题？

## A
**因果掩码：每个位置只能看自己和前面的位置，不能看后面。**
- 语言模型的任务是预测下一个 token，如果训练时能偷看后面的字，就是作弊，学不到东西。
- 实现：在 softmax 之前，把"后面位置"的分数设为负无穷，softmax 之后权重恰好为 0。对长度 4 的序列，第 2 个位置只能看位置 1、2。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 206" font-family="sans-serif" font-size="11">
<text x="138" y="14" text-anchor="middle" fill="currentColor">被看的位置 →</text>
<text x="4" y="34" fill="currentColor">当前位置 ↓</text>
<text x="87" y="34" text-anchor="middle" fill="currentColor">1</text>
<text x="121" y="34" text-anchor="middle" fill="currentColor">2</text>
<text x="155" y="34" text-anchor="middle" fill="currentColor">3</text>
<text x="189" y="34" text-anchor="middle" fill="currentColor">4</text>
<text x="60" y="61" text-anchor="end" fill="currentColor">1</text>
<text x="60" y="95" text-anchor="end" fill="currentColor">2</text>
<text x="60" y="129" text-anchor="end" fill="currentColor">3</text>
<text x="60" y="163" text-anchor="end" fill="currentColor">4</text>
<rect x="70" y="40" width="34" height="34" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="87" y="61" text-anchor="middle" fill="currentColor">看</text>
<rect x="104" y="40" width="34" height="34" fill="none" stroke="currentColor"/><text x="121" y="61" text-anchor="middle" fill="currentColor">−∞</text>
<rect x="138" y="40" width="34" height="34" fill="none" stroke="currentColor"/><text x="155" y="61" text-anchor="middle" fill="currentColor">−∞</text>
<rect x="172" y="40" width="34" height="34" fill="none" stroke="currentColor"/><text x="189" y="61" text-anchor="middle" fill="currentColor">−∞</text>
<rect x="70" y="74" width="34" height="34" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="87" y="95" text-anchor="middle" fill="currentColor">看</text>
<rect x="104" y="74" width="34" height="34" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="121" y="95" text-anchor="middle" fill="currentColor">看</text>
<rect x="138" y="74" width="34" height="34" fill="none" stroke="currentColor"/><text x="155" y="95" text-anchor="middle" fill="currentColor">−∞</text>
<rect x="172" y="74" width="34" height="34" fill="none" stroke="currentColor"/><text x="189" y="95" text-anchor="middle" fill="currentColor">−∞</text>
<rect x="70" y="108" width="34" height="34" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="87" y="129" text-anchor="middle" fill="currentColor">看</text>
<rect x="104" y="108" width="34" height="34" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="121" y="129" text-anchor="middle" fill="currentColor">看</text>
<rect x="138" y="108" width="34" height="34" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="155" y="129" text-anchor="middle" fill="currentColor">看</text>
<rect x="172" y="108" width="34" height="34" fill="none" stroke="currentColor"/><text x="189" y="129" text-anchor="middle" fill="currentColor">−∞</text>
<rect x="70" y="142" width="34" height="34" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="87" y="163" text-anchor="middle" fill="currentColor">看</text>
<rect x="104" y="142" width="34" height="34" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="121" y="163" text-anchor="middle" fill="currentColor">看</text>
<rect x="138" y="142" width="34" height="34" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="155" y="163" text-anchor="middle" fill="currentColor">看</text>
<rect x="172" y="142" width="34" height="34" stroke="currentColor" fill="currentColor" fill-opacity="0.15"/><text x="189" y="163" text-anchor="middle" fill="currentColor">看</text>
<text x="4" y="198" fill="currentColor">看 = 可以看；−∞ = softmax 之后权重为 0</text>
</svg>

- **对推理的重要后果：** 因为前面的 token 永远看不到后面的 token，**前面位置的计算结果不会因为后面追加了新 token 而改变**。所以生成时，旧 token 的中间结果算一次就可以存起来反复用。这就是 KV 缓存（把旧 token 每层的键、值向量存起来反复用）能成立的前提。

**多头注意力：同时做多组独立的注意力，各自关注不同的关系。**
- 一组注意力只能产生一套权重，但一句话里同时存在多种关系：语法上的主谓、指代、相邻词搭配等。
- 做法：把 4,096 维切成 32 份，每份 128 维，称为 32 个"头"（head），每个头有自己的 Q、K、V，独立算注意力，最后把 32 个结果拼回 4,096 维，再乘一个输出矩阵。
- 计算量和单个 4,096 维的注意力相同，只是分成了 32 个并行的小组。

**7B 模型每层注意力的参数：** Q、K、V、输出四个 `[4096, 4096]` 矩阵，共约 6,700 万个。

**容易被问到的变体：** 让多个查询头共用同一组 K、V（分组查询注意力，GQA），能把需要保存的 K、V 减少数倍。Llama 2 7B 每个头都有自己的 K、V，Llama 3 8B 是 32 个查询头共用 8 组 K、V。
