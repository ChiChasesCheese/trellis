---
id: aie-eval-sample-size-ci
node: t05.eval-statistical-power-sample-size-confidence-in
type: qa
step: 1
tags: [考点]
---
## Q
**Eval 统计功效 · 差 2 个点是不是噪声**｜考点 · 必会

两个 prompt 版本在 200 条评测集上得分 82% 和 84%。能说新版更好吗？评测集要多大才够？

## A
**先算误差范围：** 得分是比例，标准误 ≈ √(p(1−p)/n)。

- p = 0.82，n = 200：√(0.82 × 0.18 / 200) ≈ 2.7 个点；
- 95% **confidence interval**（置信区间，真实值有 95% 把握落在其中的范围）约 ±5 个点，即 77%–87%；
- 两个版本的区间重叠很多，2 个点的差**不能当作真实提升**。

**OpenAI 的经验表（要 95% 把握判断哪个系统更好）：**

| 要分辨的差距 | 约需样本数 |
|---|---|
| 30% | 10 |
| 10% | 100 |
| 3% | 1,000 |
| 1% | 10,000 |

规律：差距每缩小到 1/3，样本数多 10 倍。参照：lm-evaluation-harness 里 benchmark 的样本数中位数 1,000；Inverse Scaling 奖的组织者认为 300 条是下限，最好 1,000 条以上。

**非确定性也要算进去：**
- 同一套评测跑两遍结果会不会不同？不同评测集抽样的方差多大？目标是**可复现、低方差**；
- AI judge 的 temperature 设 0，配置固定；
- 用 bootstrap（对评测集有放回地重采样）估计波动范围；
- 随机性大的任务，每条样本跑多次取平均。

**怎么用：**
1. 先估能接受的最小差距，再定样本数；
2. 报告得分时带区间，不只给一个数；
3. 样本不够时，看逐条的变化（由对变错、由错变对），别只看总分。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch4 §Annotate evaluation data（Table 4-7）、§Evaluate your evaluation pipeline；ch2 §Inconsistency；标准误公式为通用统计

</details>
