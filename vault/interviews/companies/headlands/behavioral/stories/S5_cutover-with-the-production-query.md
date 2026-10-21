# S5 · 用生产查询本身做验证的数据源切换（测试 · 有界扫描 · 默认关的发布）

用于：how do you test a risky change / a performance decision / ship fast safely / biggest system change。

**Hook：「I validated with the production query itself, so there was no gap between what I tested and what I shipped.」**

## 数字

- 字段级一致率 **>99.9%**；不一致的 **0.07%** 全是"单侧当日才有"的记录（时序，不是冲突）。
- 切换前跑生产查询的 `count(*)`：13,737,670 vs 13,768,430，差 **+0.224%**。0.07% 和 0.224% 是两个不同的数。
- 简历口径：13.7M 行切换。

## 60 秒

**S**
- Our **pass-through fees** came from the acquirer's **transaction view**, which sometimes filled **after the payout cutoff**; a **settlement view** arrives earlier.

**T**
- I owned the **interchange-fee track**: move the biggest category, credit interchange, to the **earlier source**.

**A**
1. Option **A**: make the "whichever view has data" **fallback** smarter. Option **B**: a **static split by fee type**.
2. Chose **B**: the fallback had **sticky state** and three CTEs; a **source of truth** should be a **fact**, not a runtime decision.
3. **Compared field by field** with a full outer join and `EQUAL_NULL`: **>99.9%**, every difference explained.
4. Ran the **production query itself** as a `count(*)` on a full day: **+0.224%**.
5. **Bounded the scan** with a **one-month window** on the merge's `ON`.
6. **Idempotent `MERGE`** on a synthetic key; **toggle off by default**; pre-prod first, then production.

**R**
- **13.7M rows** cut over at **>99.9%** parity; **deploy and release** were separate steps.

**L**
- **Validate with the thing you ship; bound the scan; ship dark.**

## 2 分钟（在 60 秒上加）

- **Why a window**: staging only grows, so an equality `ON` scans **all history**; a one-month window lets **zone maps prune** and keeps scan cost **constant**.
- **Its cost**: a record reprocessed **after a month** bypasses dedup; I **documented** that beside the clause.
- **Gating**: the join returns nothing until the **upstream quality status** says the day is validated; **merchant-level** gate; **Amex excluded** (own pipeline).
- **No double counting**: the old task **skips interchange** when the toggle is on; **source filtering**, not MERGE dedup, makes the two paths exclusive.
- **Idempotency**: the task re-runs hourly; the synthetic key (prefix + invoice number) makes re-runs **no-ops**.
- The **backfill SQL** became the team's **CDC backfill template**.

## 追问

- **Why not dual-write?** Two tasks gated in **opposite directions** by one toggle are the exclusion; dual-write without it **double-charges**.
- **What does the window cost?** The one-month dedup blind spot above.
- **How do you know pruning worked?** I'd read the **query profile** (partitions scanned vs total). 【待 Chi 补：是否真的看过；没有就说"I reasoned it from the clustering"】
- **Settlement view late too?** The quality-status join returns **nothing**; fees **wait**, never read half-built.
- **What can still go wrong?** Reprocessing past the window; one-sided same-day records must arrive later; the toggle gives a **fast off**.

## 别说

- "唯一 owner / spearheaded the program"；"merchant by merchant"、"两周"、"零回归"。
- $55B / $450M/月 是项目级数字，不是我的产出。
- 窗口化"快了 N 倍"（没有测过）。

## 待 Chi 补

- 有无资深同事倾向 A；窗口化前后的 partitions scanned。
