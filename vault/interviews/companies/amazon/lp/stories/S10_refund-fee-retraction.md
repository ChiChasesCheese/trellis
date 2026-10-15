# S10 · 退款费 billing-terms 复盘（推翻自己的数字）

> 来源：`core/stories/S10 退款费 billing-terms 复盘.md`（status: verified）。
> 主 LP：**Earn Trust · Dive Deep · Are Right, A Lot**；副：Insist on the Highest Standards · Customer Obsession · Ownership。
> 一句话：*"My first blast-radius query said 196K rows; before anyone acted I found the predicate was wrong, retracted it, and the real number was 21,923."*

## 1. 数字

| 版本 | 谓词 | 结果 |
|---|---|---|
| 第一版 | credit 计划 monthly ∧ 费用创建当天生效计划 daily/net ∧ 生成的 billing_terms 仍 MONTHLY | 196,274 行 / 61 商户 / $11,123 |
| **修正** | + `ps_curr.created_at <= bf.created_at` | **21,923 行 / 10,330 credits / 30 商户 / $5,854.52** |
| 1,062 个切到 NET 的美国商户里只有 5 个产生 bug 费用 | 爆炸半径收敛 |
| 那家电商：216 行、延迟 214 天 | 积压 → 补跑 |
| 上游"计划写入滞后" 1 小时 32 分 | 第二个脆弱点 |
| $ 口径：`SUM(ABS(amount))/100` | 明确 |
| 回填 PR：TEMU/SHEIN 191,191 笔 sales → 382,382 fee 行 | PR #2246 / #2689 / #2753 / #2763 / #2966 |

## 2. 60–90 秒（口述提纲）

**"My first blast-radius query said 196 thousand rows; before anyone acted, I found the predicate was wrong, retracted it myself, and the real number was 21,923."**

**S · Situation**
- A large e-commerce merchant moved to **net settlement**.
- Some **refund fees** came out tagged with the old **monthly** billing terms.

**T · Task**
- I owned **sizing the blast radius** and finding the root cause.
- Remediation had to be sized off a **correct number**, not a bad predicate.

**A · Action** (in the order it happened)
1. I wrote the sizing query: **about 200K fee rows, sixty merchants**.
2. **Before anyone acted**, I re-read my own predicate and found it was **wrong**.
3. It didn't check the new schedule **existed at fee-creation time**; many were **backfilled months later**, so correct when written.
4. I **added that condition** and re-ran: the real scope was far smaller.
5. **Root cause**: the refund-fee path **copied the credit's historical schedule ID** instead of resolving it at fee time.
6. I also found an **upstream fragility**: a schedule written **an hour and a half** after the stream stamped that day's credits.

**R · Result**
- Real scope: about **22K rows, 30 merchants, under $6K**, instead of 200K and sixty.
- **One fix covers both** fragilities: resolve the effective schedule at fee creation.

**L · Learning / Mechanism**
- I'd rather **retract my own number in public** than size a remediation off a bad predicate.
- Every claim gets a **re-runnable query**; blast-radius predicates must check **time validity**.

<details><summary>逐字稿（参考，不背）</summary>

> After a large e-commerce merchant moved to net settlement, some refund fees came out tagged with the old monthly billing terms. My first blast-radius query said about two hundred thousand fee rows across sixty merchants. Before anyone acted on it, I re-examined the predicate and found it was wrong: it didn't check that the new pricing schedule existed at the time the fee was created. Many of those rows had schedules backfilled months later and were correct when written. Adding that condition took the real scope to about twenty-two thousand rows, thirty merchants, under six thousand dollars.
>
> The root cause was that the refund-fee path copied the credit's historical pricing-schedule ID instead of resolving the effective schedule at fee-creation time. Along the way I found a second, upstream fragility: a schedule written to the database an hour and a half after the transaction stream had already stamped that day's credits. One fix covers both. I'd rather retract my own number in public than have a remediation sized off a bad predicate.

</details>

## 3. 2 分钟（口述提纲）

**"My first blast-radius query said 196 thousand rows; before anyone acted, I found the predicate was wrong, retracted it myself, and the real number was 21,923."**

**S · Situation**
- A large e-commerce merchant moved to **net settlement**.
- Some of its **refund fees** came out with the old **monthly** billing terms.

**T · Task**
- I owned **sizing the blast radius** and the **root cause**.
- Why it mattered: **merchants billed on the wrong terms**, and remediation scoped off my number.

**A · Action** (in the order it happened)
1. **Wrote the query**: credit on a monthly plan, plan at fee date daily or net, billing terms still monthly.
2. It returned **196,274 rows, 61 merchants, ~$11K**.
3. **Before anyone built on it**, I re-read my own predicate: it never checked the schedule **existed when the fee was created**.
4. Many schedules were **backdated months later**, so those fees were right when written.
5. I added **schedule `created_at` <= fee `created_at`** and **corrected the number in the thread, with both queries**.
6. Checked **why the scope is bounded**: after a switch, new credits get the net plan automatically.
7. **Root cause, downstream**: the refund-fee path reused the credit's historical schedule ID.
8. **Root cause, upstream**: one merchant's net plan landed **1 h 32 min** after the stream stamped that day's credits.
9. **Fix direction**: resolve the effective schedule at fee creation; that covers both.

**R · Result**
- **21,923 rows, 10,330 credits, 30 merchants, $5,854.52** (down from 196,274 / 61 / ~$11K).
- Only **5 of 1,062** US merchants moved to net produced buggy fees; the e-commerce merchant had **216 rows delayed 214 days**.
- Backfill PRs covered **191,191 sales into 382,382 fee rows** (TEMU/SHEIN). Fix shipped? 【待 Chi 补：修复是否已上线】

**L · Learning / Mechanism**
- **Every claim has a re-runnable query**; sizing predicates must check **time validity**.
- What I'd do differently: 【待 Chi 补：这次复盘之后团队是否多了"sizing 查询必须带时间有效性条件"的 checklist / 模板？】

<details><summary>逐字稿（参考，不背）</summary>

> **Situation.** A large e-commerce merchant moved to net settlement. Some of its refund fees came out with the old monthly billing terms.
>
> **First answer — and why it was wrong.** I wrote a query to size the blast radius: credit on a monthly plan, merchant's plan at fee-creation date daily or net, generated billing terms still monthly. It returned 196,274 rows, 61 merchants, about eleven thousand dollars.
>
> **The catch.** Before anyone built a remediation on it, I re-read my own predicate. It didn't check that the new schedule physically existed when the fee was created. Many schedules had been backdated months later, so those fees were correct when written. I added `created_at` of the schedule less than or equal to that of the fee. The real number: 21,923 rows, 10,330 credits, 30 merchants, $5,854.52.
>
> **Why I did it in public.** I corrected the number in the thread, with both queries, so scope and remediation were sized correctly.
>
> **Why the real scope is bounded.** After a merchant switches, new credits get the net plan automatically, so the bug stops accumulating. It bites where a backlog of refund fees built up before the switch and ran after: the e-commerce merchant had 216 rows delayed 214 days. Of 1,062 US merchants moved to net, only five produced buggy fees.
>
> **Root causes.** Downstream, the refund-fee path reused the credit's historical schedule ID instead of resolving the effective schedule at fee creation. Upstream, one merchant's net plan was written one hour thirty-two minutes after the stream stamped that day's credits. Resolving the schedule at fee time fixes both.
>
> **What I'd keep.** Every claim has a re-runnable query.

</details>

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Earn Trust** (P) | "I retracted my own number in public before anyone acted on it." | 公开改口；两版查询并排 | 说成"被人抓到"；是我自己发现的 |
| **Dive Deep** (P) | "The difference between 196K and 22K was one missing condition on when a row was created." | 谓词、时间有效性、1h32m 滞后 | — |
| **Are Right, A Lot** (P) | "I treated my own query as a hypothesis to disconfirm." | 重审谓词；`GET_BILLING_TERMS` 数据驱动、先排除美国特判 | — |
| **Insist on the Highest Standards** (S) | "One fix that covers both the downstream and upstream fragility." | 在费用创建时重新解析生效计划 | 修复是否已上线 【待 Chi 补】 |
| **Customer Obsession** (S) | "Thirty merchants had been billed on the wrong terms." | 商户侧影响与回填 | — |
| **Ownership** (S) | "I owned the sizing and the root cause, and followed through to the backfills." | PR 回填 191,191 笔 sales → 382,382 fee 行 | 不点名商户 |

## 5. 追问（≥5）

1. **How did you discover the predicate was wrong?**
   - 【待 Chi 补：触发点（抽样某行发现计划是几个月后回填的？）——被问"错的假设"时需要真实细节】
2. **Who had seen your first number?**
   - 【待 Chi 补：196K 是否已发给他人/进入 ticket？"在任何人据此行动之前"需要你能支持的事实】
3. **Why is the blast radius bounded?**
   - After the switch, new credits get the **NET plan ID** automatically.
   - Only merchants with a **pre-switch backlog run after the switch** are hit.
4. **How do you fix it?**
   - Call **`EFFECTIVE_PRICING_SCHEDULE(maid, date)`** at fee creation.
   - **Don't copy** the credit's historical plan ID.
5. **What about the upstream lag?**
   - The function resolves by schedules **physically present at query time**.
   - Lag can be **systematic in bulk rollouts**.
   - Re-resolving at fee creation **mitigates both**.
6. **How do you know $5,854.52 is right?**
   - Basis is **`SUM(ABS(amount))/100`**.
   - SQL appendix in **Confluence 2946204146**.
7. **What changed in how you work?**
   - **Every claim gets a re-runnable query**.
   - Blast-radius predicates check **time validity**.

## 6. Senior 升级点（bar = senior）

当前档位：**trade-off with data + 自我纠错 是 senior 级**；缺 **influence（谁据此行动）与 mechanism（谓词模板/查询模板）**。
- 【待 Chi 补：这次复盘之后团队是否多了"sizing 查询必须带时间有效性条件"的 checklist / 模板？】
- 【待 Chi 补：这份复盘谁读了、基于它做了什么决定（回填范围、优先级）？】
- 升级句：「I'd rather retract my own number in public than have a remediation sized off a bad predicate.」
