# S10 · 公开撤回自己的数字（low ego · 测量要可复跑 · 读状态的时间点）

用于：a mistake / low ego / data analysis / how do you know your number is right。

**Hook：「I'd rather retract my own number in public than have a remediation sized off a bad predicate.」**

## 数字

| | 第一版 | 修正后 | 倍数 |
|---|---|---|---|
| 费用行数 | 196,274 | 21,923 | 约 9× |
| 商户 | 61 | 30 | 约 2× |
| 金额 | $11,123 | $5,854.52 | 约 1.9× |

- 1,062 个切到新结算的美国商户里只有 5 个产生 bug 费用；上游计划写入滞后 1 小时 32 分。

## 60 秒

**S**
- A large **e-commerce merchant** moved to **net settlement**; some **refund fees** still had the old **monthly** terms.

**T**
- Size the **blast radius** so the team could decide **whether** and **how much** to remediate.

**A**
1. My first query: ~**196K rows**, **61 merchants**, ~**$11K**.
2. **Before anyone acted**, I re-read my **predicate**.
3. It never checked that the **new pricing schedule existed** when the fee was created.
4. Many schedules were **backfilled months later**: those fees were **correct when written**.
5. Added `schedule.created_at <= fee.created_at`.
6. **Root cause**: the refund-fee path **copied the credit's old schedule id** instead of resolving the schedule **at fee time**.
7. Found a second, **upstream** fragility: a schedule written **1.5 hours late**; **one fix** covers both.

**R**
- Real scope: **21,923 rows**, **30 merchants**, **under $6K**: about **nine times** fewer rows.

**L**
- **Retract first**; attach a **re-runnable query** to every number; ask **at what time** state is read.

## 2 分钟（在 60 秒上加）

- **First predicate**: credit's schedule monthly ∧ merchant's schedule net on fee day ∧ fee terms still monthly.
- **Why it shrinks by itself**: after the move, **new credits get the new schedule**, so the bug stops **accumulating**; only a **late backlog** is hit hard (one merchant: 216 rows, 214 days late).
- **Second fragility**: the effective-schedule lookup uses what **physically exists at query time**, so a schedule written after the credit was stamped is **missed permanently**.
- **Different next time**: put the **time condition** in the first draft; say **when** each input is read.

## 追问

- **What was wrong with the predicate?** No check that the **schedule existed at fee-creation time**.
- **Root cause in one sentence?** The path **copied the credit's historical schedule id** instead of **resolving at fee time**.
- **Is the lag a race?** Same shape: two writers, and the **reader's time** decides the answer; fix by **resolving at the event's time**.
- **How do others trust it?** Every claim has a **query**; the logic has **no country hard-coding**, so a "US special case" is ruled out first.
- **What triggered the re-read?** 【待 Chi 补】

## 别说

- 商户名；"零回归"；9× 适用于金额（金额约 1.9×）。
- 修复已上线（除非你确认）。

## 待 Chi 补

- 是什么让你重审谓词；修复是否已合入。
