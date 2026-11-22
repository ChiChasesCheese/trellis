---
id: aie-context-position-matters
node: t01.context-window
type: qa
step: 2
tags: [先修]
---
## Q
**Context window · 位置与长度的坑**｜先修 · 追问

窗口够长，就可以把一份 200 页的文档整份塞进去，让模型自己找答案吗？关键信息放在文档的哪个位置，模型更容易找到？

## A
**结论：** 装得下 ≠ 用得好。研究（Liu et al., 2023）发现，模型对 prompt **开头和结尾**的内容理解得比**中间**好得多。

**怎么测：** needle in a haystack（NIAH）：把一条随机信息（needle）插到长文本（haystack）的不同位置，问模型这条信息是什么，画出位置与正确率的关系。

| 位置 | 模型找得到的概率 |
|---|---|
| 开头 | 高 |
| 中间 | 明显低 |
| 结尾 | 高 |

**做法：**
- 重要指令放 prompt 的开头或结尾。
- 测试用的 needle 要用**私有信息**；用公开事实的话，模型可能是在凭训练时记住的知识回答，而不是真的在读你给的文本。
- 性能随长度变差就缩短 prompt。RULER 等测试也是用来衡量这一点的。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch5 §Context Length and Context Efficiency（Liu et al., 2023；NIAH；RULER）

</details>
