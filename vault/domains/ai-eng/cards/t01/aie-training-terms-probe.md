---
id: aie-training-terms-probe
node: t01.pre-training-post-training-sft-preference-finetu
type: qa
step: 3
tags: [先修]
---
## Q
**训练相关的词 · 辨析**｜先修 · 追问

下面四件事，哪些真的改变了模型的 weights（参数的数值）？一个人说"我给 ChatGPT 喂了我童年的日记，把它训练成了年轻时的我"，技术上准确吗？

1. 在大量网页文字上从头训练一个 model
2. 拿现成模型，用你公司 5,000 条（问题，理想回答）继续训练
3. 在 prompt 里贴上 5 个示范，要求模型照着写
4. 把权重从 16 位精度压成更低精度来省显存（quantization）

## A
| 做法 | 改 weights？ | 名字 |
|---|---|---|
| 1 | 是 | pre-training |
| 2 | 是 | finetuning（模型厂商做则叫 post-training） |
| 3 | **否** | prompt engineering |
| 4 | 改了数值，但**不算训练** | quantization |

**那个说法：** 日记是通过 **prompt（context）**喂给模型的，模型的 weights 没变，技术上叫 prompt engineering，不是 training。口语里说"训练"没人会误会，但在工程讨论里要分清，因为：

| | prompt 方式 | finetuning 方式 |
|---|---|---|
| 要不要数据 | 很少 | 更多 |
| 门槛 | 低，马上能试 | 高，要训练 |
| 效果上限 | 复杂任务可能不够 | 质量、延迟、成本都可显著改善 |

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch1 §On the Differences Among Training, Pre-Training, Finetuning, and Post-Training、§Model adaptation 段

</details>
