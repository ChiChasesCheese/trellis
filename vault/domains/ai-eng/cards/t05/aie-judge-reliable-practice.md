---
id: aie-judge-reliable-practice
node: t05.llm-as-judge
type: qa
step: 3
tags: [实践]
---
## Q
**让 LLM-as-judge 可信 · 实践**｜拓展 · 加分

另一个团队负责维护 judge，你负责应用。上个月 coherence 分是 90%，这个月是 92%。你怎么判断应用真的变好了？长期该怎么把 judge 管起来？

## A
**原则：** judge 也是一个会变的 AI 应用。**看不到它的 model 和 prompt，就不要信它的分数。**

**怎么做：**
1. **把 judge 当代码管：** judge 的 model 名、版本、prompt、采样参数都进版本控制，每个分数都标上 judge 的版本号。
2. **换 judge 就重跑基线：** judge 一变，用新 judge 把上个月的输出也重评一遍，再比较。
3. **定期和人对一次：** 抽一小批样本请人标注，看 judge 和人的一致率，掉了就回头修 judge 的 prompt。
4. **标准写成 rubric 加例子：** 比如"faithfulness"，MLflow、Ragas、LlamaIndex 的定义和打分尺度各不相同，分数不能互相比较。写清楚你自己的定义，配上每个分数档的例子。
5. **控制成本：** 生产上不必每条都评，用 spot-checking 抽查；评得越多越有把握，也越贵。

**回到题目：** 先确认两个月用的是同一个 judge。不是的话，90% 和 92% 不能比；用新 judge 重评上个月的输出后再下结论。

**常见错法：** 应用团队把分数变化归功于自己的改动，其实是 judge 团队悄悄换了 model。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch3 §Criteria ambiguity、§Increased costs and latency（含 Tip：不信看不到 model 和 prompt 的 judge）

</details>
