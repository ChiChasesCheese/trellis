---
id: aie-stack-probabilistic-testing
node: t02.ai-engineering-stack
type: qa
step: 2
tags: [考点]
---
## Q
**输出是概率性的 · 为什么单元测试断言不够**｜考点 · 必会

你给"自动评分作文"的功能写单元测试：`assert score == 4`。同一篇作文跑两次，一次 3 分、一次 5 分，测试时过时不过。这是你代码的 bug 吗？怎么办？

## A
**不是 bug，是模型的性质。** 模型生成时按概率抽 token（见 sampling 那张卡），所以：

| 现象 | 例子 |
|---|---|
| **相同输入，不同输出** | 同一个 prompt 跑两次，评分 3/5 和 5/5 |
| **输入稍变，输出大变** | 不小心把一个字母大写，回答就变了 |

**能做的缓解：**
- 缓存答案，同样的问题直接返回上次的结果；
- 固定 temperature、top-p、top-k，甚至固定 seed（随机数起点）；
- 但**即使全固定，也没有 100% 保证**：运行输出的硬件不同也会影响结果。

**所以测试的做法变了：**

| 传统后端 | AI 应用 |
|---|---|
| 断言：输出 == 期望值 | eval（对模型输出做系统化测试）：在一批样本上给输出打分，看通过比例 |
| 一次失败就是 bug | 看**比例**和**失败类型** |
| "正确"来自规格 | "好"要自己先定义标准（relevance、factual consistency、safety 等） |

开放式输出没法穷举所有"标准答案"来比对，这是 evaluation 在 AI 工程里分量更重的原因。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch2 §The Probabilistic Nature of AI → Inconsistency；ch1 §Application development → Evaluation

</details>
