---
id: li-transformer-attention-variants-mha-mqa-gqa
node: transformer.attention-variants
type: qa
step: 1
---
## Q
多头注意力（MHA）、多查询注意力（MQA）、分组查询注意力（GQA）有什么区别？以 Llama 2 7B 和 Llama 3 8B 为例，算出它们每个 token 的 KV 缓存大小。

## A
**背景：** 注意力里，每个 token 在每层算出 Q（查询，"我在找什么"）、K（键，"我是什么"）、V（值，"我能提供什么"）三个向量，并分成多个"头"（head），每个头独立做一次注意力。生成文字时，历史 token 的 K、V 不会变，被存成 **KV 缓存**，每生成一个新 token 都要把整份缓存从显存读一遍。

**三种结构的区别在于 K、V 有几组：**
- **MHA（multi-head attention）：** 每个查询头都有自己的 K、V。32 个查询头 → 32 组 K、V。
- **MQA（multi-query attention）：** 所有查询头共用 1 组 K、V。缓存最小，但质量下降较明显。
- **GQA（grouped-query attention）：** 查询头分组，每组共用 1 组 K、V。比如 32 个查询头、8 组 K、V，每 4 个查询头共享一组。质量接近 MHA，缓存是它的 1/4。

**算 KV 缓存（FP16，每个数 2 字节）：** 每 token 字节数 = 2（K 和 V）× 层数 × K/V 头数 × 每头维数 × 2 字节。

| 模型 | 层数 | K/V 头数 | 每头维数 | 每 token |
|---|---|---|---|---|
| Llama 2 7B（MHA） | 32 | 32 | 128 | 2×32×32×128×2 = **512 KB** |
| Llama 3 8B（GQA） | 32 | 8 | 128 | 2×32×8×128×2 = **128 KB** |

一个 8,000 token 的对话：Llama 2 7B 约 4 GB，Llama 3 8B 约 1 GB。同一张卡上，后者能同时服务的长对话数约是前者的 4 倍。

**为什么这对推理关键：** 生成阶段每步要读整份 KV 缓存，缓存小 4 倍，读得也快 4 倍，长上下文时速度明显更快；并发数也受缓存大小限制。

**配置里怎么看：** `config.json` 的 `num_attention_heads`（查询头数）和 `num_key_value_heads`（K/V 头数）。两者相等是 MHA，后者为 1 是 MQA，介于中间是 GQA。更激进的变体如 MLA（multi-head latent attention）把 K、V 压缩成一个低维向量再缓存。

**新进展（2026 年 2 月）。** 阿里发布开源的 Qwen3.5-397B-A17B：60 层里每 4 层只有 1 层是常规注意力，另外 3 层是线性注意力（Gated DeltaNet，只存一份大小固定的状态，不随长度增长）。按本卡的公式，只有那 15 层要算进“层数”，长上下文时缓存比 GQA 还小得多。

<details class="pt"><summary>想一想：按本卡公式，只有 15 层会随长度增长缓存，每个 token 的缓存约是同样规模全注意力模型的几分之几？这种省法的代价最可能在哪？</summary>约 1/4（15/60，忽略固定状态和头数差别）。代价是线性注意力把整段历史压进固定大小的状态，对很远处细节的精确回忆通常较弱，所以仍保留四分之一的全注意力层。</details>
