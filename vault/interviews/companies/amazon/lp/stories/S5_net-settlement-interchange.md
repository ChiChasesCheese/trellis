# S5 · Net Settlement · interchange 数据源切换（技术决策 + 零回归迁移）

> 来源：`core/stories/S5 Interchange 数据源切换.md`（status: **partial**）。
> 主 LP：**Ownership · Deliver Results · Are Right, A Lot**；副：Dive Deep · Insist on the Highest Standards · Invent and Simplify · Bias for Action · Customer Obsession · Think Big · Frugality。
> 一句话：*"I owned the fee side of a multi-quarter net-settlement program and switched the biggest fee source with a shadow comparison that used the production query itself."*

## 1. 数字（区分项目级与我的）

| 数字 | 口径 | 谁的 |
|---|---|---|
| >99.9% 字段一致 | discovery：FULL OUTER JOIN + EQUAL_NULL | 我 |
| 0.07% 不匹配（单侧当日才有） | 时序，非冲突 | 我 |
| 13,737,670 vs 13,768,430 → **+0.224%** | 切换前用生产查询 `count(*)` 跑当天全量 | 我 |
| 影响面 | 两个可解释差异：`FEE_SEQUENCE_CODE`、`ALT_DISPUTE_ID` | 我 |
| 任务窗口 `CRON 15 6-9 * * * America/Chicago` | 按 settle 视图实际就绪 [5:30, 8:15] EST 反推 | 我 |
| $55B+ 增量 TPV · ~$450M/月 float · 2 年+ epic 链 | **项目级业务数字，不是我的管线产出** | 项目 |

⚠️ 0.07% 与 0.224% 是**两个不同性质**的数字（字段一致率 vs 记录数差异），不要混用。
⚠️ 简历写 "Spearheaded Braintree's net settlement project ... an estimated hundreds of millions in working-capital savings"；S5 证据边界：epic owner of record 不是我 → 口播用 "I own the fee side / the interchange track inside the net-settlement program"。简历 "hundreds of millions" 与项目级 ~$450M/月 float 的关系 【待 Chi 补：这个 estimated savings 是谁估的、怎么算的——BR 会问 baseline】。

## 2. 60–90 秒口播版（≈ 215 词）

> Our pass-through fees — interchange, scheme, chargeback — all came from the acquirer's transaction view, and that view sometimes wasn't populated until after the daily payout cutoff, so fees missed the net-settlement window. I owned switching the biggest category, credit interchange, to the settlement view, which arrives earlier.
>
> I had two options. Make the existing "whichever view has data" fallback smarter, or statically split by fee type behind a feature toggle. I chose the static split: the fallback had already grown sticky state and three CTEs, and in a revenue path I want the source of truth to be a fact, not a runtime decision.
>
> Before switching I ran a discovery comparison — a full outer join, field by field — with over ninety-nine point nine percent parity and every difference explained. Then I ran the production query itself as a `count(*)` over a full day: about 13.7 million rows, within 0.224 percent. Validation and production share the same SQL, so I can't validate one thing and ship another. I shipped it dark — toggle off, enabled in pre-prod, then production — because deploy and release are two separate steps. The backfill SQL became the team's template for CDC backfills.

## 3. 2 分钟版（≈ 330 词）

> **Context.** Net settlement is a multi-quarter program to move large merchants to a daily net payout directly from the acquirer, which shortens payout from T+X to T+1 and frees around 450 million dollars a month of float. That's the program-level number — I'm not the epic's owner of record. I own the fee side of it.
>
> **The problem.** Pass-through fees came from the acquirer's transaction view, which sometimes filled in after the payout cutoff. Credit interchange is the biggest category, so I owned moving it to the settlement view, which arrives earlier.
>
> **The decision.** Option A: make the dynamic fallback smarter. Option B: split statically by fee type — interchange from settlement, everything else unchanged — behind a toggle. I chose B because the fallback had grown stateful and I wanted a revenue-path source of truth to be a fact. I accepted weeks of running two things in parallel and more SQL.
>
> **How I validated.** Discovery: a full outer join with null-safe equality across two normalized shapes, field by field. Over 99.9 percent parity; the 0.07 percent mismatches were all records present on one side only that day, which is timing, not conflict; two differences I could explain. Then pre-cutover, I took the production query that was about to ship, turned it into a `count(*)`, and ran a full day: 13,737,670 against 13,768,430, plus 0.224 percent, which I judged acceptable.
>
> **Mechanics.** The procedure merges on a synthetic key from the invoice number so hourly reruns can't double-bill; the merge condition has a one-month window so it keeps partition pruning on an ever-growing staging table — the trade-off, which I documented, is that reprocessing a record more than a month later bypasses dedup; it joins the quality-gate status so we never read a settlement day that hasn't passed checks; and a feature gate plus an Amex exclusion. The old task excludes interchange only when the toggle is on, so the two can't double-count.
>
> **Release.** Toggle default off, pre-prod on, then production. The backfill SQL became the team's CDC template.

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Ownership** (P) | "I own the fee side of net settlement — specifically the interchange track." | 费用侧最硬的一块；toggle 灰度；窗口化 ON 风险写在注释里 | 说成「唯一 owner」 |
| **Deliver Results** (P) | "The switch was verified on a full day of 13.7M rows before any production traffic moved." | 数字链：99.9% / 0.224% / 13.7M；模板被复用 | 说「零回归」「merchant by merchant」「两周」——无证据 |
| **Are Right, A Lot** (P) | "I tested the decision before betting a revenue path on it: field-level discovery, then the production query as count(*)." | 先 discovery 再动手；用数据 disconfirm 自己；选 B 的理由 | — |
| **Dive Deep** (S) | "A 0.07 percent mismatch was all timing; a 0.224 percent difference had to be explained." | 两个数字性质不同；两个可解释差异 | 混用两个百分比 |
| **Insist on the Highest Standards** (S) | "Deploy is not release." | toggle 默认关；预生产先放；互补 task 防双计 | — |
| **Invent and Simplify** (S) | "I replaced a stateful fallback with a static split." | 去掉运行时判断，选事实 | — |
| **Bias for Action** (S) | "I shipped it dark so I could move before it was fully proven in production." | 默认关 + 可回退 = reversible | 夸大成「冒险」 |
| **Customer Obsession** (S) | "Fees that miss the payout cutoff come out of the merchant's net payout." | 费用赶不上净额窗口 = 对商户出款金额有影响 | 推断；未验证的因果别说死 |
| **Think Big** (S) | "The change is a prerequisite for a program that moves tens of billions in volume." | 项目级背景 | 把 $55B 说成我的产出 |
| **Frugality** (S) | "The one-month window keeps scan cost constant on a table that only grows." | zone-map 剪枝 | — |

## 5. 追问（≥5）

1. **Trade-off of the time window?** → 同一记录超过一个月才重处理时绕开去重；可解释、写在注释里的风险敞口，换取扫描量恒定。
2. **Why not dual-write?** → 两个 task 被同一 toggle 反向控制，这就是互斥；没有显式互斥的 dual-write 就是重复收费。
3. **What would have made you not switch?** → 【待 Chi 补：你事先设的"不切换"门槛是多少？若没有预设门槛，如实说「我判断 0.224% 可接受」】
4. **How did you handle the 0.224% difference?** → 记录数差异；一侧比另一侧多 30,760 行（13,768,430 − 13,737,670，自行算）；是否逐类解释 【待 Chi 补：这 0.224% 的构成】
5. **Postgres vs Snowflake?** → 定价计划在 Postgres（OLTP、费率 system of record、唯一约束、header + N 行费用原子写）；Snowflake 做数十亿行聚合；应用层幂等 upsert 同步，冲突以 `FAILED_PRECONDITION` 暴露。
6. **Who else was involved?** → 定价服务、结算平台、出款服务和收单行；对齐靠数据契约与信任（Answers Q10）。【待 Chi 补：团队规模与我的 PR 数】
7. **Did the toggle ever get flipped back?** → 证据：生产在一次 migration 里 prod 关、preprod 开；灰度执行细节**无记录**，不编。

## 6. 证据边界

不说「唯一 owner」「merchant by merchant」「两周」「零回归」。PR #1615（+634）、#1939、#1833（CDC 回填模板）；Confluence 2698298357 / 2747965111 / 2747848324；Jira DTBTTFOUND-2461 / 2640。

## 7. Senior 升级点（bar = senior）

当前档位：**ambiguity、trade-off with data、mechanism（可复用模板）已到 senior**；**cross-team 对齐与"向 senior 干系人说服"的细节缺失**。
- 【待 Chi 补：选 B 而不是 A 的时候，评审人里有没有资深工程师倾向 A？你怎么说服的 / 被说服的？（这是 Have Backbone / Are Right A Lot 的核心证据）】
- 【待 Chi 补：影子核对结果是给谁看的（定价服务/出款服务/收单行对接人？）他们的反应是什么，谁批准放开 toggle？】
- 【待 Chi 补：CDC 回填模板被谁用过、用了几次（"someone else used my template" = raising the bar）】
- 【待 Chi 补：toggle 打开后至今的线上指标（有无回退/事故）——没有就不说 "零回归"】
- 升级句：「I turned 'will the numbers match?' from an opinion into a query, and the method became the team's template.」
