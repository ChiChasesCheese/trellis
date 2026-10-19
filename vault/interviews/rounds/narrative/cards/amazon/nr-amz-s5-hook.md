---
id: nr-amz-s5-hook
node: amazon.s5
type: qa
step: 1
---
## Q
【S5 · Net Settlement · interchange 数据源切换（技术决策 + 零回归迁移）】开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
**I turned "will the numbers match?" from an opinion into a query, and shipped the switch dark.**

**适用 LP**

- 主：**Ownership**、**Deliver Results**、**Are Right, A Lot**
- 副：Dive Deep、Insist on the Highest Standards、Invent and Simplify、Bias for Action、Customer Obsession、Think Big、Frugality

**数字**

- **>99.9%** 字段一致（discovery：FULL OUTER JOIN + EQUAL_NULL）
- **0.07%** 不匹配，都是单侧当日才有 = 时序，不是冲突
- 切换前用生产查询 `count(*)` 跑一整天：**13,737,670 vs 13,768,430**，**+0.224%**（差 30,760 行）
- 两个可解释差异：`FEE_SEQUENCE_CODE`、`ALT_DISPUTE_ID`
- 任务窗口 `CRON 15 6-9 * * * America/Chicago`，按 settle 视图实际就绪 [5:30, 8:15] EST 反推
- 0.07% 与 0.224% 是两种数字（字段一致率 vs 记录数差异），不要混用
- 项目级数字，不是我的产出：**$55B+** 增量 TPV、**~$450M/月** float、2 年+ epic 链；口播用 "I own the fee side / the interchange track inside the net-settlement program"
- 【待补：简历 "hundreds of millions in working-capital savings" 是谁估的、怎么算的，BR 会问 baseline；与项目级 ~$450M/月 float 的关系要说清】
