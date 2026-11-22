---
id: aie-code-assertions-pass-at-k
node: t05.code-based-assertions-verifiable-evals
type: qa
step: 2
tags: [考点]
---
## Q
**Code-based assertions · pass@k**｜考点 · 必会

一个代码生成基准有 10 道题。每题让模型生成 k = 3 份代码，任何一份通过全部测试，就算这题解决。模型解决了 5 题。pass@3 是多少？pass@1 与它的关系？为什么不能直接拿 pass@10 与别人的 pass@1 比？

## A
**pass@k** = 解决的题数 ÷ 总题数；一题"解决"指 k 份样本中**至少有一份**通过该题全部测试用例。

- 回到题目：5 ÷ 10 = **50%**。
- 生成的样本越多，每题解决的机会越大，所以期望上 **pass@1 < pass@3 < pass@10**。
- 不能直接比：k 不同，机会数不同，必须在**同一个 k** 下比较。

| 指标 | 含义 | 回答的问题 |
|---|---|---|
| pass@1 | 一次生成就对 | 用户拿到第一份答案就能用的概率 |
| pass@k（k>1） | k 次里至少一次对 | 允许多次尝试 / 有验证机制时的上限 |

**在应用里：** 如果你的系统能**自动验证**（跑测试、检查 SQL 是否合法）并在失败时重新生成，pass@k 反映的就是你系统的真实能力；如果没有自动验证，用户只看到一份答案，应看 pass@1。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch3 §Functional Correctness（pass@k 的定义和 10 题解决 5 题的例子）

</details>
