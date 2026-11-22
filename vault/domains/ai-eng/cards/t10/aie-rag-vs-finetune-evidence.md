---
id: aie-rag-vs-finetune-evidence
node: t10.prompting-rag-finetuning
type: qa
step: 2
tags: [考点]
---
## Q
**RAG vs finetuning · 看证据**｜考点 · 必会

要让模型回答"最近发生的事件"相关的问题。团队想把新文章微调进模型。Ovadia 等人（2024）的实验怎么说？

## A
**实验（当前事件问答，正确率）：**

| 模型 | 基础模型 | 基础 + RAG | 微调（FT-reg） | 微调（FT-par） | FT-reg + RAG | FT-par + RAG |
|---|---|---|---|---|---|---|
| Mistral-7B | 0.481 | **0.875** | 0.504 | 0.588 | 0.810 | 0.830 |
| Llama 2-7B | 0.353 | **0.585** | 0.219 | 0.392 | 0.326 | 0.520 |
| Orca 2-7B | 0.456 | **0.876** | 0.511 | 0.566 | 0.820 | 0.826 |

**读法：**
- **基础模型 + RAG 最高**：对需要最新信息的任务，RAG 比微调好得多；
- 微调的提升很小，甚至让 Llama 2-7B 变差（0.353 → 0.219）；
- 在微调过的模型上再加 RAG，反而**不如**在基础模型上加 RAG：微调可能让其他方面变差。
- 在 MMLU 的实验里：几乎所有问题类别 RAG 都胜过微调；在微调模型上叠加 RAG，在 43% 的情况下提升表现，57% 的情况下不如单独用 RAG。

**所以：** 缺事实 / 知识更新快，用 RAG，不要把事实"训练进去"。

**例外：** 如果问题是行为类（输出格式、风格、冷门的语法如不常见的 SQL 方言），finetuning 才有用。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch7 §Finetuning and RAG（Table 7-2，Ovadia et al. 2024）

</details>
