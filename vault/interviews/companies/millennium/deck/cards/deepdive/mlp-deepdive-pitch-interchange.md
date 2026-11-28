---
id: mlp-deepdive-pitch-interchange
node: deepdive.pitch
type: qa
step: 3
---
## Q
**怎么讲 interchange 数据源切换**｜项目深挖

“Tell me about a migration you led. How did you make sure nothing broke?”

## A
这是“迁移与验证”的项目：技术决定加严格的上线方法。interchange fee（交换费，发卡行收的那部分手续费）是信用卡手续费里占比最大的一类。

- **背景：** 净额结算（net settlement）是把大商户迁到收单行每日净额直连的多季度项目，出款从 T+X 缩到 T+1，项目层面释放约 $450M 每月的垫付。你负责其中费用这一侧最硬的一块：pass-through 费用都来自收单行的 transaction 视图，而它有时在出款截止之后才填好，费用赶不上当天。
- **你的决定：** 把 interchange 的取数源切到更早到达的 settlement 视图。方案 A 是把已有的“哪个视图有数用哪个”回退逻辑做聪明；方案 B 是按费用类型静态划分，你选 B。
- **验证：** 先字段级 discovery，一致率超过 99.9%，0.07% 不匹配全是单侧当日才有的记录；再把即将上线的生产查询当 `count(*)` 跑一整天，约 13.7M 行，差 +0.224%。
- **发布：** 开关默认关，部署不等于发布，先在预生产开，再到生产。

**英文答法。**
- Pass-through fees came from the acquirer's **transaction view**, which sometimes filled **after the disbursement cutoff**; I owned switching credit **interchange** to the earlier **settlement view**.
- I chose a **static split by fee type** behind a toggle, not a smarter fallback: in a revenue path the **source of truth should be a fact, not a runtime decision**.
- Validation: a field-by-field `FULL OUTER JOIN`, **over 99.9% parity**, then the **production query itself as `count(*)`** over about **13.7 million rows**, within a fraction of a percent.
- Shipped **dark**: merged with the toggle off, enabled in pre-prod, then production.

**5 分钟展开。**
- **0:00 业务背景：** 为什么费用赶不上出款截止。
- **1:00 两个方案与选择：** 动态回退对静态拆分。
- **2:15 验证：** discovery，再用生产查询自己做影子核对。
- **3:30 过程里的四个手法：** 幂等 `MERGE`、窗口化 `ON`、trigger-status 连接、商户级功能闸门加 Amex 排除。
- **4:30 发布：** 部署与发布是两步。

**追问。**
- **Are you the sole owner of net settlement?** No, I own the fee side, the interchange track inside the program; the program-level numbers are the business's.
- **Zero regression?** Don't claim it; say shipped dark, enabled in pre-prod, then production.
