# S1 · Amex 结算管线（端到端 owner）

> 来源：`core/stories/S1 Amex 结算管线.md`（status: verified）。只用其中有证据的事实；缺的写 `【待 Chi 补：…】`。
> 主 LP：**Ownership · Deliver Results**；副：Dive Deep · Insist on the Highest Standards · Invent and Simplify · Frugality。
> 一句话（给 Bar Raiser，零术语）：*"I built and ran, for eighteen months, the pipeline that turns American Express's daily settlement file into booked transactions and fees on our Snowflake-based fee platform."*

## 1. 数字（只用这些）

| 数字 | 口径 | 能否口播 |
|---|---|---|
| ~22M 笔 Amex 交易 | 生产 `TRANSACTIONS` 中 `sub_kind = american_express`，2025-05-20 起约半年 | 能：说 "about twenty-two million transactions in the first six months" |
| 18 个月生产 | 2025-04 首个 PR 合并至今 | 能 |
| ~1,800 行（1,849） | 任期内最大单个 PR（PR #886） | 能 |
| 十几个加固 PR | 迟到文件、拒付标志、大小写、错误日志 | 能：说 "about a dozen" |
| 美元金额 | S1 笔记：查询结果页首注明**以分计**，$138.6B 很可能是 $1.386B | **不口播具体美元** 【待 Chi 补：本管线美元量级的最终口径】 |
| **简历写 "$600B+ annual transaction volume"** | 简历第一条 bullet 写在 Amex 系统上 | ⚠️ **与上面 22M 笔 / ~$1.4B 差两个数量级。Dive Deep 追问「$600B 怎么算的」会炸。面试前必须对齐口径：是 Braintree 全量 TPV 还是 Amex 管线？** 【待 Chi 补】 简历已于 2026-10-15 改为证据口径；投递版仍是旧数字，答法见 ../../README.md「面试前必须处理」 |

## 2. 60–90 秒口述提纲

**I inherited a one-table stub and ran the Amex settlement pipeline end to end for eighteen months.**

**S · Situation**
- **Braintree** fee platform on **Snowflake**; Visa and Mastercard settle through near-real-time acquirer views.
- **Amex** is closed loop: **one fixed-width file a day**, so no booking until the file confirms settlement.

**T · Task**
- I **owned** the pipeline from design doc through production; I inherited a **stub with one table**.
- Its output feeds **fee calculation and payouts**.

**A · Action** (in the order it happened)
1. **Designed** six append-only streams, one per record type — each has its own **offset**, none blocks the others.
2. Put a composite-key **MERGE** at every stage — a re-delivered file can't **double-count**.
3. Built two **validation** functions — every mismatch goes to an **error log**, never dropped.
4. Added one **feature flag** as a **kill switch** — one `UPDATE`, no deploy.
5. Stayed **on-call**; shipped about a **dozen hardening PRs** after real failures.

**R · Result**
- **~22M** Amex transactions in the first six months; **18 months** in production.
- Largest PR of my tenure, **~1,800 lines**.

**L · Learning / Mechanism**
- When it breaks, it **records the problem instead of losing data**.

<details><summary>逐字稿（参考，不背）</summary>

> The project I'm proudest of is the American Express settlement pipeline on our Snowflake-based fee platform at Braintree. Amex is a closed-loop network: instead of the near-real-time views we get from our acquirer for Visa and Mastercard, it sends one fixed-width reconciliation file a day. So we can't book an Amex transaction until that file confirms it settled.
>
> I inherited a stub with a single table and owned the pipeline from the design doc through eighteen months of production. I made three design calls. First, six append-only streams, one per record type, so each has its own offset and none blocks the others. Second, a composite-key `MERGE` at every stage, so a re-delivered file or a re-run task can't double-count. Third, two validation functions that send every mismatch to an error log instead of dropping it, and a single feature flag that doubles as a kill switch, so I could stop it with one `UPDATE`, no deploy.
>
> Because I was on-call for it, I shipped about a dozen hardening PRs after real failures. It processed about twenty-two million Amex transactions in its first six months, and it's the largest change I've merged — around 1,800 lines. The part I'm proudest of: when it breaks, it records the problem instead of losing data.

</details>

## 3. 2 分钟口述提纲

**I inherited a one-table stub and ran the Amex settlement pipeline end to end for eighteen months.**

**S · Situation**
- Visa and Mastercard settle through near-real-time acquirer views; **Amex** sends **one fixed-width file a day**, **six record types**.
- An Amex transaction waits in a **pending table** until the file proves it settled — the **good-funds model**.

**T · Task**
- I inherited a **one-table stub** and **owned** design, build and run.
- Output feeds **fee calculation and payouts**.

**A · Action** (in the order it happened)
1. **Wrote the design doc**: topology, six parsing procedures, two validation table functions.
2. Chose **append-only streams** — each record type needs an independent **offset**; accepted that offsets don't advance with my writes.
3. So correctness comes from the **MERGE keys**, not the stream; kept everything inside **Snowflake**, no external orchestrator.
4. Added a **stream-has-data** check so empty input never starts a warehouse; built a **monitoring app and alerting** to cover weaker orchestration.
5. Built the fee-calculation task and the **kill switch** (one flag, one `UPDATE`).
6. In production, Amex dropped files into **yesterday's folder** — I scanned **every date folder** by pattern and deduped on **load history**.
7. The **reject-flag** bug led to the composite key (reference number + reject indicator); later I built the **EU extension** with a second flag and a separate fee ledger.

**R · Result**
- **~22M** transactions in six months; **18 months** in production.
- Largest PR of my tenure, **~1,800 lines**; about **a dozen** hardening PRs.

**L · Learning / Mechanism**
- Correctness in **three layers**: row-level, batch-level, and reconciliation against Amex's own summary record.
- **What I'd do differently:** the six parsers repeat one offset table — I'd use an **offset config table** and one generic parser.
- I did exactly that pattern later in the **quality-check framework**.

<details><summary>逐字稿（参考，不背）</summary>

> **Context.** Visa and Mastercard settle through near-real-time views from our acquirer. Amex is a closed loop — one proprietary fixed-width file per day containing six record types: transactions, pricing, adjustments, chargebacks, fee revenue and a summary. So an Amex transaction arrives and has to sit in a pending table until the file proves it actually settled. We call that the good-funds model, and its output feeds fee calculation and payouts.
>
> **My role.** I inherited a one-table stub. Design doc, topology, six parsing procedures, two validation table functions, the fee-calculation task, the kill switch, and later an EU extension with a second flag and a separate fee ledger — all mine.
>
> **The decisions.** I chose append-only streams over a standard stream because each record type needs an independent offset. I accepted that stream offsets don't advance in the same transaction as my writes, so correctness comes from the `MERGE` keys, not the stream. I also chose to keep everything inside Snowflake rather than adding an external orchestrator: the file's already there, every step is a transactional `MERGE`, and a stream-has-data check stops a task from spinning up a warehouse on empty input. The cost is weaker orchestration, so I built a monitoring app and alerting on top.
>
> **What went wrong, and what I did.** Amex sometimes dropped a file into yesterday's date folder after we'd moved on. I changed ingestion to scan every date folder with a pattern and rely on the load history for dedup. The reject flag bug led to the composite key: reference number plus a reject indicator, so a transaction that's settled and later rejected can coexist as two rows, and the validator decides which wins.
>
> **Result.** About twenty-two million transactions in six months, the largest PR of my tenure, about a dozen hardening PRs. **What I'd change:** the six parsers repeat one offset table six times — I'd move offsets to a config table and write one generic parser. I did exactly that pattern later in the quality-check framework.

</details>

## 4. 适用 LP 与改角度（re-angle）

| LP | 开场一句（把同一个故事从这里切入） | 重点讲 | 避免 |
|---|---|---|---|
| **Ownership** (P) | "I inherited a one-table stub and I'm still the person who gets paged for it eighteen months later." | stub → 设计 → 上线 → 18 个月 on-call；kill switch；EU 扩展不是别人派的 | 说成「团队做的」 |
| **Deliver Results** (P) | "The Amex pipeline went from a stub to about twenty-two million booked transactions in six months." | 22M 笔、最大单 PR、可急停、EU 扩展 | 美元数字（口径未对齐） |
| **Dive Deep** (S) | "Amex files kept landing in yesterday's folder, and finding why meant reading the load history, not the dashboard." | `PATTERN` 迟到文件、拒付标志复合键 | — |
| **Insist on the Highest Standards** (S) | "My bar was: if it breaks, it must record, never drop." | 错误日志永不丢；三层正确性（行/批/对账汇总记录） | 声称「no bugs」——S3 就在下游 |
| **Invent and Simplify** (S) | "One flag routes Amex away from every other card network's path, and one UPDATE stops it." | 单 flag + 急停；我会改成配置表 + 通用解析 | — |
| **Frugality** (S) | "A stream-has-data check means we never start a warehouse for an empty file." | `SYSTEM$STREAM_HAS_DATA` 省算力 | 没有成本数字，别编 |

## 5. 可能的追问（≥5）与答题要点

1. **What exactly was yours vs. the team's?**
   - **Stub** 起，全部设计是我的；写了团队评审的**设计文档**。
   - 最大单 PR **~1,800 行**。
   - Amex 逻辑原来在 Rails 出款服务；我的是接收侧 **Snowflake-native** 替代，**不说**迁了 Funding 的 Ruby 脚本。
2. **Why Streams/Tasks, not Airflow or Spark?**
   - **数据局部性** + 事务性 `MERGE` + `STREAM_HAS_DATA` 省算力。
   - 代价：**编排弱**（无分支/外部回调）。
   - 补法：**Streamlit 监控** + **Datadog 告警**。
3. **How do you know it's correct?**
   - **行级**：`TRY_TO_DECIMAL/DATE`，坏字段不炸整批，拒收记录保留。
   - **批级**：健康检查，每笔结算交易都有费用。
   - **对账级**：费用总额对 Amex 自己的汇总记录；不一致就**停 task、page on-call**。
4. **What broke?**
   - **迟到文件**：改成 `PATTERN` 扫所有日期目录 + load history 去重；代价：那几天下游已出过少数据的版本。
   - **拒付标志**：复合键。
5. **What would you do differently?**
   - **偏移配置表** + 通用定宽解析 UDTF。
   - 新增第七种记录类型 = **加一行配置**。
6. **How does the AFTER A,B dual-upstream task stay consistent?**
   - `AFTER` 只保证两边各跑过一次，**不保证同一批**。
   - **FULL OUTER JOIN** 兜底；错位记录记一次错误，**下一轮自愈**。
   - runbook 区分「会自愈的噪音」。
7. **Did you ever lose or double-count money?**
   - **不说** "no accidents"。
   - 设计目标：**坏了就记录**。
   - S3 的 ACH 事故在这条线**下游**，我拥有那次 RCA（见 S3）。

## 6. 证据边界（BR 追问时别越线）

1. **What exactly was yours vs. the team's?**
   - **Stub** 起，全部设计是我的；写了团队评审的**设计文档**。
   - 最大单 PR **~1,800 行**。
   - Amex 逻辑原来在 Rails 出款服务；我的是接收侧 **Snowflake-native** 替代，**不说**迁了 Funding 的 Ruby 脚本。
2. **Why Streams/Tasks, not Airflow or Spark?**
   - **数据局部性** + 事务性 `MERGE` + `STREAM_HAS_DATA` 省算力。
   - 代价：**编排弱**（无分支/外部回调）。
   - 补法：**Streamlit 监控** + **Datadog 告警**。
3. **How do you know it's correct?**
   - **行级**：`TRY_TO_DECIMAL/DATE`，坏字段不炸整批，拒收记录保留。
   - **批级**：健康检查，每笔结算交易都有费用。
   - **对账级**：费用总额对 Amex 自己的汇总记录；不一致就**停 task、page on-call**。
4. **What broke?**
   - **迟到文件**：改成 `PATTERN` 扫所有日期目录 + load history 去重；代价：那几天下游已出过少数据的版本。
   - **拒付标志**：复合键。
5. **What would you do differently?**
   - **偏移配置表** + 通用定宽解析 UDTF。
   - 新增第七种记录类型 = **加一行配置**。
6. **How does the AFTER A,B dual-upstream task stay consistent?**
   - `AFTER` 只保证两边各跑过一次，**不保证同一批**。
   - **FULL OUTER JOIN** 兜底；错位记录记一次错误，**下一轮自愈**。
   - runbook 区分「会自愈的噪音」。
7. **Did you ever lose or double-count money?**
   - **不说** "no accidents"。
   - 设计目标：**坏了就记录**。
   - S3 的 ACH 事故在这条线**下游**，我拥有那次 RCA（见 S3）。
- 团队规模、上线日期、谁评审：【待 Chi 补：设计文档评审人数/周期（只说角色，不说姓名）】。
- 业务影响的客户侧数字（商户数、出款金额）：【待 Chi 补】

## 7. Senior 升级点（bar = senior，AGENT_RULES "Bar: senior"）

当前档位：**scope 与 mechanism 已到 senior**（stub → 18 个月 owner，kill switch、幂等三层、EU 扩展）；**缺的是 influence / raise-the-bar 的证据**，不补的话会被读成「一个人写了个大管线」。
- 开场加「为什么是我」：没有需求文档、只有 stub、Amex 文件格式靠自己读规格 → 这是 **ambiguity**。
- 补 mechanism 的外溢：这条管线是否已成为团队「onboard 新文件型结算源」的参考实现（S1 笔记的口播版这样说，但证据列表里没有佐证）。
- 【待 Chi 补：是否有第二个文件型结算源按这套模式接入？谁接的？（有 → 说 "someone else onboarded X using my pattern without me"，这是最强的 senior 信号；没有 → 删掉 "reference implementation" 一句，别说）】
- 【待 Chi 补：设计文档评审里，资深同事/他团队提出过哪条反对意见，你怎么回应、是否改了设计？（用作 Have Backbone / disagree-and-commit 的素材）】
- 【待 Chi 补：EU 扩展是你独立做的，还是需要说服另一个团队/合规方？】
- 【待 Chi 补：on-call 轮值里其他人靠你写的 runbook/Streamlit 监控处理过事故吗？（拉高水平证据）】
