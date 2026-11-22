---
id: aie-token-count-estimate
node: t01.token-tokenizer
type: qa
step: 2
tags: [先修]
---
## Q
**Token · 数量估算**｜先修 · 必会

一篇英文文章约 3,000 个单词。粗估要多少 token？同样意思换成别的语言，token 数一样吗？

## A
**经验换算（GPT-4 的英文）：** 一个 token 平均约 ¾ 个单词，也就是 100 token ≈ 75 词。

**算：** 3,000 ÷ 0.75 = **约 4,000 token**。

**核对一下这个比例：** 《AI Engineering》全文约 120,000 词，对应约 160,000 token；120,000 ÷ 0.75 = 160,000，吻合。

**不同语言不一样：** 同一个 tokenizer 切不同语言，效率差别很大。GPT-4 在一个把短文翻成 52 种语言的数据集（MASSIVE）上，表达同样意思的 token 数中位数：

| 语言 | token 数中位数 |
|---|---|
| 英语 | 7 |
| 印地语 | 32 |
| 缅甸语 | 72（约英语的 10 倍） |

模型的延迟和费用都和 token 数成正比，所以非英语输入常常更慢更贵。

**所以：** 估成本和长度要用你实际用的 tokenizer 去数，英文的 ¾ 只是起点，不能直接套到中文或其他语言上。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch1 §Language models（¾ 词）；ch2 §Multilingual Models（MASSIVE 中位数，Yennie Jun 的测量）

</details>
