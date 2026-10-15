# stories · Headlands 的故事与自我介绍

> 只用两种材料：[core/resume/resume.tex](../../core/resume/resume.tex)，和 [core/stories/](../../core/stories/) 里已有的故事笔记（总表见 [core/Core.md](../../core/Core.md)）。**没有新增任何经历。** 简历里太薄的地方留成**填空模板**（故事 5 的后半、故事 6），由 Chi 用真实经历填，不要让别人（包括我）替你编。
> 完整英文口播稿在各故事笔记里，这里不复制，只给"Headlands 角度"的改写、该强调的点和**不能说的话**。
> JD 价值词出处：[catalog/raw/official_and_process.md](catalog/raw/official_and_process.md) §C2、§G（`〔O-C2〕`、`〔O-G〕`）。公司背景：[01-company-brief.md](01-company-brief.md)。逐条匹配：[fit.md](fit.md)。
> 面试形式：一小时技术视频，一道基础题被一路追问为主〔loop/LOOP_GUIDE.md §1〕。**行为故事多半只会在开头 5–10 分钟或结尾出现**，所以每个故事练到 60 秒、能被打断。

---

## A. 60 秒自我介绍（Headlands 版）

### 结构（中文骨架）

1. **一句定位**：谁、多久、做什么（8 秒）。
2. **旗舰工作**：一件"正确性很严"的事 + 你是 on-call 的人（15 秒）。
3. **兴趣证据**：自己做的研究平台（15 秒）。
4. **为什么是这个岗**：Java 岗 = 研究平台的基础设施，你为什么在意这一层（12 秒）。
5. **诚实的一句 + 想学什么**（10 秒）。

### 60 秒（口述提纲）

**Hook：「I'm a software engineer at PayPal, and what I'm best at is correctness and testing.」**

**1 · 定位（8 秒）**
- **Software engineer at PayPal**, about **twenty months** full-time, after an **internship on the same team**.
- I work on the **fee platform** for a payments product.

**2 · 旗舰工作（15 秒）**
- I **built** the **American Express settlement pipeline** and the **fee calculation** on top of it.
- Mostly **Snowflake** and **PostgreSQL**, and more and more **Java** as we migrate **Ruby and Kotlin** logic with **parity tests**.
- I own production reliability as **on-call**: **root-causing** quiet data bugs, writing the tests that would have caught them.

**3 · 兴趣证据（15 秒）**
- Outside work I **built** a multi-market **research and backtesting platform**.
- **Point-in-time data**, **purged cross-validation**, a **ledger** of every experiment, a **paper-trading** loop.
- I wanted to see how much of a good-looking backtest **survives realistic costs**.

**4 · 为什么是这个岗（12 秒）**
- This role is the **infrastructure under a research platform**: **storage, compute, monitoring**.

**5 · 诚实的一句 + 想学什么（10 秒）**
- My strength is **correctness and testing**; I'm deliberately building depth **below the JVM**: caches, networking, performance.
- I'd like a **small team** where changes reach production in **weeks**.

<details><summary>逐字稿（参考，不背）</summary>

英文稿（约 155 词，慢速读 60–65 秒）：

> I'm a software engineer at PayPal — about twenty months full-time, after an internship on the same team. I work on the fee platform for a payments product: I built the American Express settlement pipeline and the fee calculation on top of it, mostly Snowflake and PostgreSQL, and more and more Java as we migrate older Ruby and Kotlin logic with parity tests. I also own production reliability as an on-call engineer, so I spend a lot of time root-causing quiet data bugs and writing the tests that would have caught them.
>
> Outside work I built a multi-market research and backtesting platform — point-in-time data, purged cross-validation, a ledger of every experiment, and a paper-trading loop — because I wanted to see how much of a good-looking backtest survives realistic costs.
>
> That's why this role appeals: it's the infrastructure under a research platform — storage, compute, monitoring. My strength is correctness and testing; I'm deliberately building depth below the JVM — caches, networking, performance — and I'd like to do that on a small team where changes reach production in weeks.

</details>

### 取舍与诚实线

- 没说交易总量的具体数字（红线：数字只说量级，[core/Core.md](../../core/Core.md)）；"twenty months"从简历 2025-02 起算，到 2026-10 约 20 个月。
- "built the Amex pipeline"出自 [S1](<../../core/stories/S1 Amex 结算管线.md>)（从 stub 建起）；不要加"#1 committer"之类被红线禁止的说法。
- "in weeks"对应官方视频 16〔O-G 与 Big Tech 的区别〕。**不要说读过他们的博客以显得内行**，除非被问"你为什么选我们"，那时可以提一篇并说清楚你理解了什么（见 §E）。
- 如果面试官打断问 Java：`More and more Java` 要有后续——准备好"迁移里最难的一个行为差异是什么"（自己回忆，别编）。

---

## B. 故事表（JD 价值词 → 故事）

| JD 价值词〔O-C2 / O-G〕 | 主故事 | 备选 |
|---|---|---|
| **"Low ego"** / 协作与独立 | 故事 2（撤回自己的数字） | 故事 4（Terraform 之后扫全仓库）· [S2 的 ADR](<../../core/stories/S2 Quality-check 框架.md>)（Answers Q24） |
| **"fully automated, scalable, maintainable … extensive testing"** | 故事 1（ACH NULL + 跨阶段 e2e） | 故事 5（Quant-Stroller 的 470+ 测试与 dual-gate） |
| **性能工作** "Address performance limitations" | 故事 3（S6 的容量推理）——**设计期，不是剖析** | 故事 6（待填：真实的性能排查） |
| **好奇心** "Genuine interest … ever curious" | 故事 5（Quant-Stroller） | 故事 4；[S7 schema pool](<../../core/stories/S7 Schema pool.md>) |
| 监控与主动发现 "proactive detection" | 故事 1 | 故事 3 |
| 数据分析做决策 "basic data analysis" | 故事 2 | 故事 3 |
| 跨团队沟通 | [S9](<../../core/stories/S9 Amex 出款延迟事故.md>)、[S4](<../../core/stories/S4 AU Amex 退款费.md>) | — |
| 分布式 / 吞吐 | [S11](<../../core/stories/S11 实习期事件流.md>)（只讲消费 / 落库 / 校验侧） | — |

---

## 故事 1 · ACH 费用静默丢失（自动化 · 测试 · 监控 · fail loudly）

**标签**：`fully automated + extensive testing` · `monitoring / proactive detection` · 次要 `curiosity`（顺着数据一层层往回走）
**素材**：[S3 ACH 费用 NULL 传播事故](<../../core/stories/S3 ACH 费用 NULL 传播事故.md>)（完整 90 秒英文稿与追问版在该笔记 §4–5）· Answers [Q3](../../core/Answers.md)

### 60–90 秒（口述提纲）

**Hook：「An unmappable instrument must fail loudly, not emit nothing.」**

**S · Situation**
- A daily **health check I built** alerted: "every settled transaction has a **fee**".
- Fee code builds the category as `'BT_' || sub_kind`, and **no exception** was thrown.

**T · Task**
- I owned the **root cause**: why ~**200 merchants**, ~**$10M a day** of bank-account volume, got **no fee**.
- A teammate's **stopgap** landed first; the **RCA and hardening** were mine.

**A · Action** (in the order it happened)
1. I **sliced** the missing fees: **100%** `us_bank_account`, **100%** the new **standard ACH** path.
2. On one row, `sub_kind` was **NULL**.
3. I traced back through the **promote procedure**: one UDF had **two overloads**.
4. The final **`MERGE`** used the overload with **no bank-account branch**, overwriting the correct value with NULL.
5. In SQL, **NULL concatenation is NULL**, so no category matched and the fee was **silently not generated**.
6. I ruled out "just delayed" with a **control group** and **days-since-promote buckets**.
7. I wrote the **postmortem**, including **four reasons** e2e missed it.
8. Then I removed the two-overload design: **one function**, default parameter, versioned **`DROP`** of the old signature.
9. I added an **e2e** spanning promote to fee generation.

**R · Result**
- **Root cause** within minutes.
- No future branch can pick the **incomplete implementation**; the new **e2e** covers the chain.

**L · Learning / Mechanism**
- **Rule**: an unmappable instrument must **fail loudly**; fix the **seam**, not the call site.

<details><summary>逐字稿（参考，不背）</summary>

原 S/T/A/R 表（中文）。完整 90 秒英文稿在 S3 笔记 §4：

| | 内容 |
|---|---|
| **S** | 我自己建的每日健康检查"每笔已结算交易都有对应费用"报警。费用计算用 `'BT_' || sub_kind` 拼出品类，没有任何异常抛出。 |
| **T** | 找到为什么大约两百个商户、每天约一千万美元量级的银行账户交易没有生成费用。 |
| **A** | 先**切片**（100% 是 us_bank_account、100% 是新的标准 ACH 路径）→ 看单笔字段（sub_kind 是 NULL）→ 回溯 promote procedure，发现同一个 UDF 有两个重载，最后一步 `MERGE` 用了没有 bank-account 分支的那个，把前面算对的值覆盖成 NULL；SQL 里 NULL 拼接得 NULL → 品类匹配不到 → **费用静默不生成**。用对照组与"按 promote 后天数分桶"排除"只是延迟"。写 postmortem，列出 e2e 为什么没抓到的**四个原因**；然后移除双重载设计（单函数 + 默认参数 + versioned `DROP` 旧签名）并补跨"promote → 费用生成"的 e2e。 |
| **R** | 根因几分钟内给出；设计层面不会再选到不完整的实现；新增的 e2e 覆盖这条链。 |

</details>

**Headlands 角度**：这是"系统自己发现自己坏了"（proactive detection）+"测试覆盖不到的地方我补了什么"。讲到测试时说**具体**：断言了路由但没断言费用；fixture 用的是信用卡 payload 所以字段从不为 NULL；pending 行没断言 sub_kind；没有测试跨 promote 到费用。

**不能说**（S3 证据边界）：止血 PR 不是我的，我的是根因、postmortem、重载合并与 DROP；不要说"我 backfill 了"，说 "fix forward with a backfill if needed"。

**追问备弹**
- **为什么不把 ACH 加进排除名单** — 检查是对的，**费用真的丢了**。
- **为什么 `DROP` 要放进 versioned migration** — 删掉 `R__` 文件**不会删已部署对象**。
- **如何避免同类** — an unmappable instrument must **fail loudly**。

---

## 故事 2 · 撤回自己的数字（Low ego · 定量分析）

**标签**：`Low ego` · `basic data analysis for decisions` · 次要 `maintainable`
**素材**：[S10 退款费 billing-terms 复盘](<../../core/stories/S10 退款费 billing-terms 复盘.md>) · Answers [Q8](../../core/Answers.md)、Q19

### 60–90 秒（口述提纲）

**Hook：「I'd rather retract my own number in public than have a remediation sized off a bad predicate.」**

**S · Situation**
- A large **e-commerce merchant** moved to **net settlement**.
- Some **refund fees** still came out with the old **MONTHLY** billing terms.

**T · Task**
- Size the **blast radius**, and decide whether to **remediate** and how much.

**A · Action** (in the order it happened)
1. My first query said ~**200K rows**, ~**60 merchants**, about **$11K**.
2. **Before anyone acted** on it, I **re-examined the predicate**.
3. It never checked that the **new pricing schedule existed at fee-creation time**.
4. Many schedules were **backfilled months later**, so those rows were **correct when written**.
5. I added `schedule.created_at <= fee.created_at`.
6. **Root cause**: the refund-fee path **copied the credit's historical** `pricing_schedule_id` instead of resolving the effective schedule at fee time.
7. I also found an **upstream 1.5-hour schedule-write lag**; one fix covers **both**.

**R · Result**
- Real scope: ~**22K rows**, **30 merchants**, under **$6K**.
- **One fix** covers both fragile points.

**L · Learning / Mechanism**
- **Every claim** has a re-runnable **query**; I **retract my own number first**.

<details><summary>逐字稿（参考，不背）</summary>

原 S/T/A/R 表（中文）。完整 60 秒英文稿在 S10 笔记 §4：

| | 内容 |
|---|---|
| **S** | 一家大型电商商户切到 net settlement 后，部分退款费带着旧的 MONTHLY billing terms。 |
| **T** | 估算影响范围，决定要不要补救、补多少。 |
| **A** | 第一版查询给出约二十万行、约六十个商户、约一万美元。**在任何人据此行动之前**我重审谓词，发现没有检查"新定价计划在费用创建时已存在"——很多行的计划是几个月后才回填的，写入时本来是对的。加上 `schedule.created_at <= fee.created_at`。根因是退款费路径复制了 credit 的历史 `pricing_schedule_id`，而不是在费用创建时解析生效计划；顺带发现上游一个 1.5 小时的计划写入滞后。 |
| **R** | 真实范围约两万二千行、三十个商户、不到六千美元；一处修复覆盖两个脆弱点。 |

</details>

**Headlands 角度**：Low ego 的最硬证据不是"我接受批评"，是**没人逼我时，我自己公开推翻自己的数**。一句收尾："I'd rather retract my own number in public than have a remediation sized off a bad predicate."

**备弹**
- **每条断言都配一个可复跑的查询**。
- **`GET_BILLING_TERMS` 纯数据驱动**，先排除"美国特判"这类假设。

**边界**：不点商户名，说 "a large e-commerce merchant"。

---

## 故事 3 · 异常检测器的 go/no-go（性能推理 · 判断力）

**标签**：`performance work`（设计期容量推理）· `data analysis` · `Low ego`（不顺着惯性接手别人的项目，愿意先叫停）
**素材**：[S6 Anomaly detector go-no-go](<../../core/stories/S6 Anomaly detector go-no-go.md>) · Answers [Q7、Q17、Q20](../../core/Answers.md)

### 60–90 秒（口述提纲）

**Hook：「I'd rather stop a project than ship one that pages the team at 3 a.m.」**

**S · Situation**
- A departing intern left an **ML fee-anomaly detector** that had **only run in QA**.
- QA: **6 synthetic merchants**, under **1B rows**. Production: ~**18K merchants**, up to ~**760M rows** on a peak day.

**T · Task**
- Decide **continue or stop**, and how long **production** would take.

**A · Action** (in the order it happened)
1. I wrote a **State / Handoff / Prod-Cutover** assessment.
2. I found the serving design was a **per-row numpy forward pass**: it would **time out** on a big warehouse.
3. QA could **never expose** that.
4. I split what **disappears** with the departure from what is **rebuildable**.
5. Only the **analyst labels** were irreplaceable, so **export them first**.
6. **Phase 1**: only the deterministic rule `abs(amount) = rate × qty + fixed`, as **pure SQL pushdown**.
7. **Phase 2**: model retrain and inference redesign, **behind a go/no-go gate**.
8. I **froze** the Slack alerting and CI/CD until the gate says go.

**R · Result**
- A risky "might wake the team at night" launch became a **reviewable, phased plan**.

**L · Learning / Mechanism**
- Before writing serving code, ask: **per-row cost times peak row count**.

<details><summary>逐字稿（参考，不背）</summary>

原 S/T/A/R 表（中文）。完整 60 秒英文稿在 S6 笔记 §3：

| | 内容 |
|---|---|
| **S** | 实习生离职前留下一个只在 QA 跑过的 ML 费用异常检测器。QA：六个合成商户、不到十亿行；生产：约一万八千个商户、峰值一天最多约七亿六千万行。 |
| **T** | 决定接着做还是先停，上线要多久。 |
| **A** | 写了 State / Handoff / Prod-Cutover 评估。发现服务设计是逐行 numpy 前向计算——在大仓库上必然超时，而 QA 永远暴露不了这一点。拆成：离职会丢什么（只有分析师标注不可再生，先导出）vs 可重建的；Phase 1 只上确定性规则 `abs(amount) = rate × qty + fixed`，**纯 SQL pushdown**；Phase 2 模型重训 + 推理重构放在 go/no-go 门后；冻结 Slack 告警与 CI/CD。 |
| **R** | 把"可能上线一个半夜叫醒团队的东西"变成可审查的分阶段计划。 |

</details>

**Headlands 角度（性能）**：这个故事能证明的是 *"我会在系统上线前，用数据规模估算识别出逐行方案撑不住，并改成 set-based"*。**不能证明**的是*"我剖析过运行中的系统"*。开口就说清楚：

> "This was capacity reasoning before anything shipped — I couldn't profile it because production scale had never been exercised. The principle I took from it is to ask what the per-row cost times the peak row count is, before writing the serving code."

**这是性能这条价值词上最弱的一环**——见 [fit.md](fit.md) D3；故事 6 就是为了补它。
**边界**：S6 的四个量级来自我自己的评估文档，尚未从生产复核；只说"under a billion vs tens of billions"、"six vs eighteen thousand"、"up to about 760 million on a peak day"。不点名实习生。

---

## 故事 4 · Terraform 的 7 分钟 RCA，以及之后的全仓库扫描（好奇 · 低自我）

**标签**：`curiosity`（修完还去扫整个仓库）· `Low ego`（纠正自己说过的过宽表述）· `maintainable`（消灭一类，不只修一处）
**素材**：[S8 Terraform 7 分钟 RCA](<../../core/stories/S8 Terraform 7 分钟 RCA.md>) · Answers [Q15](../../core/Answers.md)

### 60–90 秒（口述提纲）

**Hook：「I'd rather own "here's the next one" than just the one that paged.」**

**S · Situation**
- An **infra-repo release** failed in **QA**: Snowflake rejected `GRANT OWNERSHIP`.
- Another role already held a dependent **`USAGE`** grant. Someone else was named; I was **cc'd**.

**T · Task**
- **Unblock** the release.

**A · Action** (in the order it happened)
1. In **7 minutes** I posted the **root cause**: the ownership resource had no **`outbound_privileges`**, so Terraform didn't revoke dependents.
2. I posted the **fix**, `= "REVOKE"`, and a **check of neighboring modules**.
3. I asked permission and pushed the **PR**; **QA, pre-prod and prod** deployed that day.
4. **Afterwards** I scanned the **whole repo**: **42 of 79** similar resources lack the parameter.
5. Most are harmless **`future_*`** variants; **two** in another module have the **same shape** and haven't fired.
6. I **flagged** those two.

**R · Result**
- Release **unblocked the same day**.
- The **next failure** was flagged **before it fired**.

**L · Learning / Mechanism**
- Fixing **this one** and eliminating the **class** are different jobs; keep claims **as narrow as what I checked**.

<details><summary>逐字稿（参考，不背）</summary>

原 S/T/A/R 表（中文）。完整 60 秒英文稿在 S8 笔记 §3：

| | 内容 |
|---|---|
| **S** | 基础设施仓库的发布在 QA 挂了：Snowflake 拒绝 `GRANT OWNERSHIP`，因为另一个角色已持有依赖的 `USAGE`。被点名调查的是别人，我只是被 cc。 |
| **T** | 让发布解除阻塞。 |
| **A** | 7 分钟后贴出根因（ownership 资源没设 `outbound_privileges`，Terraform 没有先撤销依赖授权）、修法（`= "REVOKE"`）和对相邻模块的核查，征得同意后推 PR。**事后**我扫了整个仓库：79 个同类资源里 42 个缺该参数；多数是无害的 `future_*` 变体，但另一个模块有两个与出事那个形状完全相同、尚未触发。我把它们标了出来。 |
| **R** | QA、pre-prod、prod 当天部署完；下一个雷被标出来而没有爆。 |

</details>

**Headlands 角度**：JD 说 "Address performance limitations within our own software, open-source libraries …"，其精神是**不满足于修眼前这一个**。这里的技巧是"消灭这一类"。
**Low ego 的加分点**（S8 证据边界）：我曾在一次面试里说过"the only resource in the whole repo missing it"，事后的扫描证明这不成立。**现在的说法**：

> "I checked the neighboring modules that day; afterwards I scanned the whole repo and found dozens missing it, mostly harmless future grants, but two real ones in another module that haven't fired yet."

不要把这句话说宽。不要用"7 分钟"当炫耀，用来说明"全局图景"的价值。

---

## 故事 5 · Quant-Stroller：为了搞懂回测而造的研究平台（好奇 · 自动化 · 研究基础设施）

**标签**：`curiosity` · `fully automated + extensive testing` · 与 JD "research platform" 同构
**素材**：**只有简历**（[resume.tex](../../core/resume/resume.tex) Projects 第一条）。`core/stories/` 里没有这个项目的故事笔记 → 下面只写简历明说的事实，其余留空等 Chi 填。

### 已有事实（逐条出自简历）

- 面向美股、加密、A 股、外汇的研究与回测平台；Python，66K+ 行，470+ 测试文件。
- DataSource / Factor / Strategy / Broker 四个窄接口（seams）：接入一个新市场或数据商 = 一个薄适配器，策略代码不改。
- "Dual-gate" 流水线：purged cross-validation、Deflated Sharpe Ratio、PBO，加 NautilusTrader 上的执行重放；340+ 次实验记入 append-only ledger；每个市场校准了交易成本模型。
- 一个 A 股小盘月度策略通过两道门（扣除 10 bps 成本后的超额 Sharpe 1.39），部署到 live paper-trading 循环（Alpaca / CCXT 路由、事前风控、5 因子风险报告）。
- Point-in-time 数据平面（raw → bars → panel，DuckDB / Parquet），9 个数据商的 2,300+ 因子目录；5,500 只 A 股面板；8-GPU 服务器上的 PyTorch 训练 + 自托管 CI；FastAPI + React 研究控制台。

### 60–90 秒（口述提纲）

> 下面只放简历明说的事实；`【待 Chi 补】` 由 Chi 用真实经历填，空着就不讲。

**Hook：「I built a research platform to see how much of a good-looking backtest survives realistic costs.」**

**S · Situation**
- I wanted to know how much of a **good-looking backtest** survives **realistic costs** and **out-of-sample** checks.
- （这句来自 [../millennium/fit.md](../millennium/fit.md) 里你自己的说法，请确认仍是你的真实动机。）
- 【待 Chi 补：[ ] 触发它的那件具体的事是什么？第一个让你"被自己骗了"的回测？】

**T · Task**
- Build a platform where **adding a market or a strategy** never touches **core code**.
- Every experiment leaves an **immutable record**.
- 【待 Chi 补：[ ] 为什么选 append-only ledger？它防的是什么具体错误？】

**A · Action**
1. **Four narrow interfaces**: DataSource / Factor / Strategy / Broker.
2. A **dual-gate** pipeline plus per-market **cost models**.
3. A **point-in-time** data plane.
4. 【待 Chi 补：[ ] 有没有一个策略被门拦下来？拦在了哪一道？这最能证明"门是真的"。】
5. 【待 Chi 补：[ ] 哪个测试曾经救了你（抓到一个你以为正确的数据泄漏）？】

**R · Result**
- One strategy passed **both gates** and runs in **paper trading**.
- 【待 Chi 补：[ ] paper trading 跑了多久？实际和回测的偏差是多少（有数就说，没有就说"还没足够样本"）？】

**L · Learning / Mechanism**
- **Point-in-time**: a backtest must not use data that wasn't yet known, or results are **inflated**.
- 【待 Chi 补：这个项目留给你的一条规则 / 机制是什么？】

<details><summary>逐字稿（参考，不背）</summary>

原故事骨架表（含填空提示）：

| | 骨架 | 填空提示 |
|---|---|---|
| **S** | 我想知道一个看起来很好的回测有多少能扛住真实成本和样本外检验（这句来自 [../millennium/fit.md](../millennium/fit.md) 里你自己的说法，请确认仍是你的真实动机）。 | [ ] 触发它的那件具体的事是什么？第一个让你"被自己骗了"的回测？ |
| **T** | 造一个让"加一个市场"和"加一个策略"都不会碰核心代码的平台，并让每次实验都留下不可改的记录。 | [ ] 为什么选 append-only ledger？它防的是什么具体错误？ |
| **A** | 窄接口 + 双门 + 成本模型 + point-in-time 数据平面。 | [ ] 有没有一个策略被门拦下来？拦在了哪一道？这最能证明"门是真的"。<br>[ ] 哪个测试曾经救了你（抓到一个你以为正确的数据泄漏）？ |
| **R** | 一个策略通过了双门并跑 paper trading。 | [ ] paper trading 跑了多久？实际和回测的偏差是多少（有数就说，没有就说"还没足够样本"）？ |

</details>

**Headlands 角度**：这是离 JD "research platform" 最近的真实经验，所以别一笔带过。讲"为什么要 point-in-time"（回测里不能用当时还不知道的数据，否则结果虚高）能体现你理解研究员需要基础设施提供什么。**明说它是个人项目**，PayPal 的才是雇主工作。
**不要说**：任何延迟 / 吞吐数字，简历没有。若被问性能 → 引到故事 6 的模板，或诚实说"这个项目的瓶颈在 [ ]"（只在你真的测过时）。
**为什么没有硬数字也无妨**：官方说金融知识要得很少，更要的是 problem-solving 与好奇〔O-G 视频 17、12〕。

---

## 故事 6 · 填空：一次真实的性能排查（简历里没有）

**为什么留空**：JD 有一整条性能（"Address performance limitations …"），评分点也是"性能直觉"〔loop/LOOP_GUIDE.md §1〕，但简历和 `core/stories/` 里**没有**一个"从现象 → 剖析 → 根因 → 前后对比"的故事。故事 3 是设计期推理，不够。不要用故事 3 冒充。

**候选素材（请 Chi 确认哪个是真的，只填真的）**

- 一次在 Snowflake / PostgreSQL 里读 query profile 或 `EXPLAIN` 并改写查询的经历（PayPal 的费用管线里有吗？）
- Quant-Stroller 里某次面板 / 因子计算从"太慢"变"可用"（改了什么：向量化？分区？缓存？列裁剪？）
- 实习期 Spark 作业或 Kafka 消费者吞吐的一次调优（[S11](<../../core/stories/S11 实习期事件流.md>) 只写了并行度公式，没写调优过程）

**口述提纲骨架（时间顺序；全部待填，空着就不讲，不要用故事 3 冒充）**

**Hook：【待 Chi 补：一句话钩子，带一个数字】**

**S · Situation**
- 【待 Chi 补：**现象**——什么慢了？一个**数字**（耗时 / 吞吐 / 延迟 / 内存）；谁发现的？】

**T · Task**
- 【待 Chi 补：你负责排查什么、为什么重要】

**A · Action**
1. 【待 Chi 补：**怎么测**——你真用过的工具，它告诉了你什么】
2. 【待 Chi 补：**假设**——怀疑过哪几个原因，为什么排除其他】
3. 【待 Chi 补：**根因**——在哪一层（算法 / 数据布局 / IO / 锁 / 网络 / GC / 配置）】
4. 【待 Chi 补：**修复**——改了什么】

**R · Result**
- 【待 Chi 补：**前后各是多少**；有没有回归测试守住】

**L · Learning / Mechanism**
- 【待 Chi 补：**下一步**——如果还要更快，先看哪里；加一句"为什么这样会更快"的底层解释】

**填空模板**

| | 提示 |
|---|---|
| **现象** | 什么慢了？用一个**数字**：耗时 / 吞吐 / 延迟 / 内存。谁发现的（你 / 告警 / 用户）？ |
| **怎么测** | 用了什么工具（你**真用过**的：query profile、`EXPLAIN ANALYZE`、JFR、async-profiler、py-spy、`top`/`htop`、Datadog 指标……）？它告诉了你什么？ |
| **假设** | 你怀疑过哪几个原因？为什么排除了其他的？ |
| **根因** | 在哪一层（算法 / 数据布局 / IO / 锁 / 网络 / GC / 配置）？ |
| **修复与对比** | 改了什么？前后各是多少？有没有回归测试守住？ |
| **下一步** | 如果还要更快，你会先看哪里？（这一问最能暴露性能直觉。） |

填好后，对照 [study/00-foundations/cpu_cache_locality.md](study/00-foundations/cpu_cache_locality.md) 与 [kq_language_depth](loop/rounds/01_video/kq_language_depth/questions.md) [A]，补一个"为什么这样会更快"的底层解释。

**同样留空：一次真实的 code review 经历**（JD D9）。简历只写了用 Claude Code 评审 AI 产出；[core/Core.md](../../core/Core.md) 红线禁止编评审记录。提示：你评审过谁的代码？你拦下了什么？对方怎么反应？没有就不讲，说 "I read every diff — including the AI's — in money code"。

---

## C. 预备素材（不是主角，被问到时用）

| 场景 | 用 |
|---|---|
| "有没有意见不一致" | [S4 AU Amex 退款费](<../../core/stories/S4 AU Amex 退款费.md>) · [S9](<../../core/stories/S9 Amex 出款延迟事故.md>) |
| "接受批评" | Answers [Q24](../../core/Answers.md)（[S2](<../../core/stories/S2 Quality-check 框架.md>) 的 ADR） |
| "主动做的事" | [S7 schema pool](<../../core/stories/S7 Schema pool.md>)（个人仓库，说 "I built it, the team adopted it"） |
| "分布式 / Kafka" | [S11](<../../core/stories/S11 实习期事件流.md>)，证据边界：消费 / 落库 / 校验侧，没运维过集群 |
| "用 AI 工具" | S7 的 AI 工具题完整版 |

## D. 练习方式

1. 每个故事先写出 **90 秒版**，再压到 **45 秒版**（面试官可能只给这么久）。
2. 每个故事准备 3 个追问：「你个人做了什么 vs 团队」「什么没做好」「再来一次你会怎么改」。
3. 对着 `core/debrief/`（[说明](../../core/debrief/README.md)）自己录一次，看语速和填充词。
4. 讲完每个故事，用一句话连回 Headlands：故事 1 → "24 小时自动化的系统必须自己发现自己坏了"；故事 2 → "独立判断、公开纠错"；故事 3 → "规模估算先于代码"；故事 4 → "消灭一类问题"；故事 5 → "研究员需要什么样的基础设施"。

## E. 如果被问 "Why Headlands?"（30 秒草稿）

> "Three things I can point to from your own materials. One, you say engineers can see the impact of a change in production within weeks, not quarters — I want that loop. Two, the Java role is the research platform and its infrastructure: storage, a compute farm, monitoring — which is the layer my own backtesting project made me care about. Three, you hire for curiosity and say financial knowledge is learned on the job; I'd rather be hired for how I debug than for what I've memorized."

出处：官方视频 16、17、12〔O-G〕；JD 〔O-C2〕。**不要加**没读过的东西。
