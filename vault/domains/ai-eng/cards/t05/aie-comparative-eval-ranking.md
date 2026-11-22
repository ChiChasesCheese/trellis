---
id: aie-comparative-eval-ranking
node: t05.comparative-evaluation-pairwise-ranking
type: qa
step: 1
tags: [摘要]
---
## Q
**Comparative evaluation · 两两比较怎么变成排名**｜摘要 · 追问

Chatbot Arena 让用户在两个匿名回答里投票。这和给每个模型单独打分有什么不同？票怎么变成排名？它有什么瓶颈？

## A
**pointwise vs comparative：**

| | pointwise | comparative |
|---|---|---|
| 做法 | 每个模型独立打分再排序 | 模型之间比，由比赛结果算排名 |
| 适合 | 有客观标准 | 质量主观时更容易：判断哪首歌好，比给每首打分容易 |

- 每次比较叫一场 **match**；A 胜过 B 的概率叫 **win rate**；平局要允许，避免随机选边；
- 用 **rating algorithm** 把比赛结果换算成分数：Elo、Bradley–Terry、TrueSkill。Chatbot Arena 先用 Elo，后改为 Bradley–Terry，因为 Elo 对评审和 prompt 的顺序敏感；
- 排名是否正确：任意一对中，排名高的赢排名低的概率应超过一半。

**不是所有问题该投票：** 「手机辐射和脑瘤有没有关系」要看对错，不是偏好；用户不懂时让他选，既沮丧也会得到错误信号。投票只对**懂行的评审**有效（AI 当助手加速用户本来会做的事）。

**和 A/B 测试不同：** A/B 中用户一次只看一个候选；comparative 里同时看多个。

**三个瓶颈：**
- **规模：** 模型对数随模型数二次增长。2024 年 1 月 LMSYS 用 244,000 次比较评了 57 个模型（1,596 对），平均每对约 153 次；
- **transitivity 假设**（A 胜 B、B 胜 C，则 A 胜 C）不一定成立；
- **新模型、私有模型：** 加入新模型会改变已有排名；私有模型要自己收集比较信号；
- 还有标准化和质量控制：志愿者不会核对事实，可能偏爱听起来好但错的回答。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch3 §Ranking Models with Comparative Evaluation（Challenges of Comparative Evaluation）

</details>
