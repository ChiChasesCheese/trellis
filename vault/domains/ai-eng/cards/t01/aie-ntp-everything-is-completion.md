---
id: aie-ntp-everything-is-completion
node: t01.llm-next-token-prediction
type: qa
step: 2
tags: [先修]
---
## Q
**LLM · 一切任务都是补全**｜先修 · 追问

模型只会"接着往下写"，为什么它能做翻译、判断垃圾邮件、写摘要？拿到下面这个 prompt，它的输出为什么常常是"Likely spam"？

```
Question: Is this email likely spam? Here's the email: <email content>
Answer:
```

## A
**原理：** 翻译、分类、摘要、写代码都可以改写成"给出开头，让模型补全结尾"。在训练里见过无数"问题 → 回答"的文字格式，最自然的下文就是答案。

| 任务 | prompt 的写法 | 模型补全的内容 |
|---|---|---|
| 翻译 | `How are you in French is …` | `Comment ça va` |
| 垃圾邮件分类 | 上面那段，结尾是 `Answer:` | `Likely spam` |
| 续写 | `To be or not to be` | `, that is the question.` |

**两个重要的后果：**
- **补全是"预测"，不保证正确。** 模型输出的是概率最高（或按概率抽到）的接续，不是查出来的事实。这就是同一个问题多次问可能不同、有时一本正经地错的根源。
- **补全 ≠ 对话。** 刚训练完的模型被问"How to make pizza"，可能接一句"for a family of six?"（补全了问题本身），而不是给步骤。让它学会"回答"需要后面的 post-training（再调成会听指令的助手），见 pre-training（先读海量文本学会语言） 与 post-training 那张卡。

**对比：** 还有一种 masked language model（BERT 这一类），训练时是"填空"，能同时看空格前后的文字，常用于分类这类理解任务；生成文字用的是 autoregressive 模型。本题库里说的 LLM 都指后者。

**出处：** Huyen《AI Engineering》ch1 §Language models（completion machine、masked vs autoregressive）
