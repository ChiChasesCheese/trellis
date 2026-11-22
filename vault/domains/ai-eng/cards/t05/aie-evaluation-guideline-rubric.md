---
id: aie-evaluation-guideline-rubric
node: t05.evaluation-guideline-scoring-rubric
type: qa
step: 1
tags: [实践]
---
## Q
**Evaluation guideline · 写出能让两个人打同分的标准**｜实践 · 必会

两位标注员给同一批客服回答打分，结果差很多。你怎么写 guideline 才能解决？评测分数 80% 又怎么落到业务上？

## A
**guideline 是评测流水线的骨干，写不清楚，分数就没有意义。** 步骤：

1. **定义「好」，也定义「不该做」：** 哪些输入超出应用范围（如问选举）、怎么识别、怎么回应；
2. **「正确」不一定「好」：** LinkedIn 的经验——对求职评估回答「你完全不合适」可能正确，却没用；好的回答要说明差距和怎么补；
3. **拆成几项 criteria：** 如相关性、与上下文事实一致、安全（LangChain 2023 年的统计：用户平均用 2.3 种反馈维度）；
4. **每项选打分制：** 二元 0/1；1–5；或三值（−1 矛盾、0 中立、1 蕴含）；
5. **写 rubric 并配示例：** 一个 1 分的回答长什么样、为什么值 1 分；
6. **让人验证：** 让自己、同事照着 rubric 打分，难以遵循就改，往返多次是必要的；
7. **与 golden set 互补：** rubric 定义怎么评，golden set 提供评什么。

**挂钩业务指标（示意数字，非实测）：**

| 事实一致性 | 可自动化的客服请求 |
|---|---|
| 80% | 30% |
| 90% | 50% |
| 98% | 90% |

并定出 **usefulness threshold**：低于它就不可用。

**迭代要有节制：** criteria 会随用户行为变，但不能天天改；改的时候做实验追踪，记录评测数据、rubric、judge 的 prompt 和采样参数。

**出处：** Huyen《AI Engineering》ch4 §Step 2 Create an Evaluation Guideline（Define evaluation criteria、Create scoring rubrics、Tie evaluation metrics to business metrics）；§Iterate
