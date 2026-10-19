# Net Settlement · interchange 数据源切换（技术决策 + 零回归迁移）

**I turned "will the numbers match?" from an opinion into a query, and shipped the switch dark.**

## 适用 LP

- 主：**Ownership**、**Deliver Results**、**Are Right, A Lot**
- 副：Dive Deep、Insist on the Highest Standards、Invent and Simplify、Bias for Action、Customer Obsession、Think Big、Frugality

## 数字

- **>99.9%** 字段一致（discovery：FULL OUTER JOIN + EQUAL_NULL）
- **0.07%** 不匹配，都是单侧当日才有 = 时序，不是冲突
- 切换前用生产查询 `count(*)` 跑一整天：**13,737,670 vs 13,768,430**，**+0.224%**（差 30,760 行）
- 两个可解释差异：`FEE_SEQUENCE_CODE`、`ALT_DISPUTE_ID`
- 任务窗口 `CRON 15 6-9 * * * America/Chicago`，按 settle 视图实际就绪 [5:30, 8:15] EST 反推
- 0.07% 与 0.224% 是两种数字（字段一致率 vs 记录数差异），不要混用
- 项目级数字，不是我的产出：**$55B+** 增量 TPV、**~$450M/月** float、2 年+ epic 链；口播用 "I own the fee side / the interchange track inside the net-settlement program"
- 【待补：简历 "hundreds of millions in working-capital savings" 是谁估的、怎么算的，BR 会问 baseline；与项目级 ~$450M/月 float 的关系要说清】

## S / T / A / R / L

### S
- **Net settlement** 是多季度项目；我 own **费用侧**（不是 epic owner of record）
- 透传费用来自收单方的 **transaction view**，有时在**出款截止后**才填充

### T
- 我 **owner** 把最大类别 **credit interchange** 切到更早到达的 **settlement view**

### A
- 比较**两个方案**：更聪明的动态 fallback，或按费用类型的**静态拆分** + toggle
- 选**静态拆分**：fallback 已有粘性状态和三个 CTE；收入路径的数据源应是**事实**
- **Discovery**：全外连接逐字段比，**>99.9%** 一致，差异全部解释
- 用**生产查询本身**做 `count(*)` 跑整天：~**13.7M 行**，差 **0.224%**
- **暗发布**：toggle 默认关 → 预生产 → 生产；**deploy 和 release 分开**

### R
- 生产流量切换前，一整天 **13.7M 行**验证在 **0.224%** 以内
- 回填 SQL 成了团队的 **CDC 回填模板**

### L
- **验证和生产用同一条 SQL**，不会验证 A 却发布 B
- 收入路径的数据源是事实，不是运行时决定

## 追问与回答

- **What's the trade-off of the time window?**
  - 同一记录**超过一个月**才重处理时绕开去重
  - 可解释、**写在注释里**的风险；换**扫描量恒定**
- **Why not dual-write?**
  - 两个 task 被**同一 toggle 反向控制** = 互斥；没有显式互斥的 dual-write 就是重复收费
- **What would have made you not switch?**
  - 见待补
- **How did you handle the 0.224% difference?**
  - 是记录数差异，一侧多 **30,760 行**；构成见待补
- **Postgres vs Snowflake?**
  - 定价计划在 **Postgres**：OLTP、费率 system of record、唯一约束、header + N 行费用**原子写**
  - **Snowflake** 做数十亿行聚合；应用层**幂等 upsert** 同步，冲突以 `FAILED_PRECONDITION` 暴露
- **Who else was involved?**
  - **定价服务**、**结算平台**、**出款服务**、**收单行**；对齐靠数据契约与信任
- **Did the toggle ever get flipped back?**
  - 一次 migration 里 **prod 关、preprod 开**；灰度执行细节无记录，不编

## 换个 LP 讲

- **Ownership**：费用侧最硬的一块；toggle 灰度；窗口化的 ON 风险写在注释里；别说「唯一 owner」
- **Deliver Results**：数字链 99.9% / 0.224% / 13.7M；模板被复用；不说「零回归」「merchant by merchant」「两周」
- **Are Right, A Lot**：先 discovery 再动手，用数据 disconfirm 自己；讲选 B 的理由
- **Dive Deep**：0.07% 全是时序，0.224% 必须解释；两个可解释差异；别混用两个百分比
- **Insist on the Highest Standards**："Deploy is not release."：toggle 默认关、预生产先放、互补 task 防双计
- **Invent and Simplify**：用静态拆分替换有状态 fallback，去掉运行时判断
- **Bias for Action**：暗发布 = 默认关 + 可回退，所以能在生产完全证明前行动；别夸大成「冒险」
- **Customer Obsession**：费用赶不上净额窗口会影响商户出款金额；未验证的因果别说死
- **Think Big**：这是一个涉及数百亿交易量项目的前置；别把 $55B 说成我的产出
- **Frugality**：一个月窗口让扫描成本在只增不减的表上保持恒定（zone-map 剪枝）

## 待补

- 【待补：你事先设的「不切换」门槛是多少；没有预设门槛，如实说「我判断 0.224% 可接受」】
- 【待补：这 0.224% 的构成，是否逐类解释】
- 【待补：团队规模与你的 PR 数】
- 【待补：选 B 而不是 A 时，评审人里有没有资深工程师倾向 A，你怎么说服的 / 被说服的（Have Backbone / Are Right A Lot 核心证据）】
- 【待补：影子核对结果给谁看（定价服务/出款服务/收单行对接人），他们的反应，谁批准放开 toggle】
- 【待补：CDC 回填模板被谁用过、用了几次】
- 【待补：toggle 打开后至今的线上指标，有无回退/事故；没有就不说「零回归」】

<details><summary>逐字稿</summary>

> Our pass-through fees — interchange, scheme, chargeback — all came from the acquirer's transaction view, and that view sometimes wasn't populated until after the daily payout cutoff, so fees missed the net-settlement window. I owned switching the biggest category, credit interchange, to the settlement view, which arrives earlier.
>
> I had two options. Make the existing "whichever view has data" fallback smarter, or statically split by fee type behind a feature toggle. I chose the static split: the fallback had already grown sticky state and three CTEs, and in a revenue path I want the source of truth to be a fact, not a runtime decision.
>
> Before switching I ran a discovery comparison — a full outer join, field by field — with over ninety-nine point nine percent parity and every difference explained. Then I ran the production query itself as a `count(*)` over a full day: about 13.7 million rows, within 0.224 percent. Validation and production share the same SQL, so I can't validate one thing and ship another. I shipped it dark — toggle off, enabled in pre-prod, then production — because deploy and release are two separate steps. The backfill SQL became the team's template for CDC backfills.

</details>
