---
id: nr-amz-s5-hook
node: amazon.outline
type: qa
step: 13
---
## Q
<p class="title">Net Settlement 数据源切换<span class="meta">02 提纲</span></p>

开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
<span class="label">开场</span>

**I turned "will the numbers match?" from an opinion into a query, and shipped the switch dark.**

<span class="label">适用 LP</span>

- 主：**Ownership**、**Deliver Results**、**Are Right, A Lot**
- 副：Dive Deep、Insist on the Highest Standards、Invent and Simplify、Bias for Action、Customer Obsession、Think Big、Frugality

<span class="label">数字</span>

- **>99.9%** 字段一致（discovery：FULL OUTER JOIN + EQUAL_NULL）
- **0.07%** 不匹配，都是单侧当日才有 = 时序，不是冲突
- 切换前用生产查询 `count(*)` 跑一整天：**13,737,670 vs 13,768,430**，**+0.224%**（差 30,760 行）
- 两个可解释差异：`FEE_SEQUENCE_CODE`、`ALT_DISPUTE_ID`
- 任务窗口 `CRON 15 6-9 * * * America/Chicago`，按 settle 视图实际就绪 [5:30, 8:15] EST 反推
- 0.07% 与 0.224% 是两种数字（字段一致率 vs 记录数差异），不要混用
- 项目级数字，不是我的产出：**$55B+** 增量 TPV、**~$450M/月** float、2 年+ epic 链；口播用 "I own the fee side / the interchange track inside the net-settlement program"
- 【待补：简历 "hundreds of millions in working-capital savings" 是谁估的、怎么算的，BR 会问 baseline；与项目级 ~$450M/月 float 的关系要说清】

<div class="sources"><b>表达 · business English</b><br>• <b><i>source of truth</i></b> — 权威数据源<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“In a revenue path I want the source of truth to be a fact, not a runtime decision.”</span><br>• <b><i>parity</i></b> — 两边数据一致的程度<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The two views showed over 99.9 percent field-level parity.”</span><br>• <b><i>within tolerance</i></b> — 在可接受误差范围内<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A full day of production traffic came back within tolerance, about 0.224 percent apart.”</span></div>
