---
id: aie-public-benchmark-contamination
node: t02.public-benchmark
type: qa
step: 2
tags: [考点]
---
## Q
**Public benchmark · 高分可信吗**｜考点 · 必会

某模型在司法考试题 benchmark 上拿了高分，销售说「它能做法律咨询」。你要问哪些问题？

## A
**先问是不是 data contamination：** 模型训练时见过测试题，分数就是背出来的，不代表能力。

| 来源 | 例子 |
|---|---|
| 无意 | 训练数据从网上抓，抓到了公开的 benchmark |
| 间接 | 训练用了某本数学教材，别人用同一本教材出题做 benchmark |
| 有意 | 先排除 benchmark 选模型，发布前又把高质量的 benchmark 数据加进训练 |

**怎么检测：**
- **n-gram overlap：** 评测样本里连续 13 个 token 也出现在训练数据里，就认为这条样本「脏」了。准，但要拿到训练数据，也要把每条样本和全部训练数据比。
- **perplexity（模型预测一段文本有多难）：** 评测数据上异常低，说明模型可能见过。便宜但不准。

**对使用者的影响：**
- 大多数人拿不到训练数据，检测不了；通常由模型方披露「干净子集」的得分。
- GPT-3 的分析里，有 13 个 benchmark 至少 40% 的内容出现在训练数据中。
- 一个只训练在 benchmark 数据上的 100 万参数小模型，几乎能拿满分（Schaeffer 2023 的讽刺论文）。

**回到题目：** 要问模型方有没有披露污染比例和干净样本得分；并用自己的、未公开的法律问题测。榜单高分只能说明「值得测」。

**出处：** Huyen《AI Engineering》ch4 §Data contamination with public benchmarks（How data contamination happens、Handling data contamination）
