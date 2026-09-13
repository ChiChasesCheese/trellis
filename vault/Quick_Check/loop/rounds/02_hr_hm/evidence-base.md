# Evidence Base — Chi Zhang 晋升/面试素材库（canonical，所有下游 agent 的单一输入）

> 本文件是 6 个来源（snowglobe/pricing/funding repo + Jira + Slack + Confluence）的合成。
> Wave A（简历→证据地图）agent：读本文件 + 深挖真实 repo/代码。
> Wave B（逐题答案）agent：只读本文件 + question-bank.md 的答案规格即可，不必再读 6 份原始证据。
> 同目录原始证据：repo-snowglobe.md / repo-pricing.md / repo-funding.md / jira.md / slack.md / confluence.md

---

## 0. Chi 画像（一句话定位 + 硬指标）

- **定位**：Braintree Pricing & Settlement 团队，Snowglobe（Braintree 基于 Snowflake 的清结算/对账平台，Java 17 + Gradle + Snowflake SQL）的事实核心。2025-02 入职（returning intern → FT），2024 夏在芝加哥实习。
- **硬指标**：snowglobe 主 repo **全时段 #1 committer**（615 commits / 63 merged PRs / 17.1K+ 行，领先 #2 的 467）。Slack 86 个频道，被全团队按名 ping 的 go-to person。工作几乎全在 Jira prefix **DTBTTFOUND**（自有 team backlog，非零散跨团队打杂）。
- **自量化影响**（Confluence "Appendix of 2025 Impact Summary" 2750481503）：**21,964,869 笔 Amex 交易 / $138,630,471,670 volume** 经他的管线处理。← 这是最硬的可辩护数字。

---

## 1. 核心故事组合（Story Portfolio）—— 5-6 个旗舰故事，一题多用

每个故事：一句话 → 关键动作 → 量化 → 证据锚点。所有答案从这些故事里取材，同一故事可服务多道题（STAR 复用）。

### S1 · AMEX GRRCN 管线（从零搭端到端新支付集成 + 跨系统迁移）★旗舰
- **是什么**：从零搭 Amex 结算文件（GRRCN = Global Reconciliation Report & Chargeback Notification，Amex 专有定宽文件格式）的端到端管线：file ingestion → staging → parse → BT fee 计算 → aggregate 迁移 → 交给 Funding 出款。把原本在 **Funding 里的 Ruby 脚本迁移到 Snowflake-native SQL**。
- **动作**：接手前任（Simrandeep Singh）留的 stub，独立出设计（`STAGE_AMEX_GRRCN_FILE` task + 6 条 append-only streams + 解析定宽记录的 UDTFs + 7 张 staging/target 表 + feature-flag 急停 `AGGREGATED_AMEX_SEPARATE_FLOW`），实现、EU 扩展、18 个月生产防御。
- **量化**：21.96M 笔 / $138.6B volume；PR #886 单个 1,849 行（他任期最大 PR）。
- **锚点**：PR snowglobe #751/#856/#862/#886/#911/#1023 + ~10 hardening PR；Jira DTBTTFOUND-1960/1961/2084/2097/2139，epic DTBTTFOUND-2074；Confluence "AMEX GRRCN File Processing Flow Design & Implementation"(2233926829)、"Aggregated Amex in Snowglobe"(1112867224)。
- **可答题**：技术最难项目 / 端到端 ownership / 迁移 / 业务影响。

### S2 · Quality-Check & Handshake 框架（平台化，不是 feature）★平台工程信号
- **是什么**：造一个所有未来 quality-check 复用的框架——集中式 config 表驱动、通用 procs 动态执行校验、trigger-status handshake 告诉下游"这块数据已验证可读"。
- **动作**：#1997（1,489 行）建框架，然后自己在几乎每个 fee subject area 铺开 ~8 次。后来发现原框架"某 subject area ~4% 失败就 block 全部 merchant"的设计缺陷，写正式 ADR（MADR 3.0.0 模板，含正确性证明 + 3 个被否方案）改成 merchant-level（复用 `QUALITY_CHECK_RESULTS_V1` + `HAS_MERCHANT_DETAIL` flag）。
- **量化**：框架复用 ~8 次；ADR 否掉 3 个备选方案。
- **锚点**：PR #1997(DTBTTFOUND-2664) + 铺开 #2061/#2069/#2075/#2091/#2106/#2558/#3040/#3237；Confluence **ADR "[ADR Draft] Merchant-Level Quality Checks Using Dense Relational Rows"(2894288991)** ←全库最强架构决策工件，Jira DTBTTFOUND-2749。
- **可答题**：技术决策/架构权衡 / 系统设计贡献 / 定标准与最佳实践 / 说服团队改方案。

### S3 · ACH fee-calc 生产事故 RCA（go-to person + 深度 debug + 持续 owning）★
- **是什么**：一条 PagerDuty（`CHECK_TRANSACTION_HAS_BRAINTREE_FEES`），Chi 自己转发并当场给出完整根因。
- **根因**：Standard ACH（`ACH_FASTER_FUND` 关）promote 进 `TRANSACTIONS` 时 `payment_instrument_sub_kind = NULL` → fee-calc 的品类映射 `'BT_' || NULL = NULL` → 不生成 discount/settled fee。精确定位到 SQL 工件 `R__create-eventstream-to-pending-transactions-with-source-stored-procedure.sql` 的 `GET_EVENTSTREAM_PAYMENT_INSTRUMENT_SUB_KIND()` 1-arg vs 2-arg overload，起因 change #2941。
- **量化**：~196 merchants，~$11.3M/day GMV，~1.05M rows，98.9% us_bank_account，100% 归因 STANDARD_ACH。持续 owning 数周。
- **锚点**：Slack #snowglobe 2026-07-29 (ts 1785371583.033749) + #treasury-pricing_app 复盘；Confluence "CHECK_TRANSACTION_HAS_BRAINTREE_FEES"(3029344728)、UDF overload 合并 "GET_EVENTSTREAM..._SUB_KIND UDF Overload Consolidation"(3052036330, DTBTTFOUND-3246)。Sahar/Dylan 公开致谢。
- **可答题**：最难的 bug / on-call ownership / 影响他人（无授权）。

### S4 · AU Amex refund fees RCA（跨团队，被 PM 正式 escalate）
- **是什么**：PM Liz Lippow 走正式 "Request Help" 表单，Tejesh 点名把问题路由给 Chi，50 条回复的长 thread。
- **根因**：所有 AU merchant 的 `fee_refund_policy='partial'`（从来不是 `'full'`）→ non-agg Amex refund fee 在 AU 从不生成。
- **量化**：USA 1,079,627 rows vs AUS 0，跨 157 merchants；催生 DTBTTFOUND-3269。
- **锚点**：Slack #service-pricing 2026-08-03 (ts 1785766795.306709)。
- **可答题**：跨团队冲突/协作 / 影响半径 / go-to person。

### S5 · Net Settlement Pricing（旗舰，多季度，收入关键 + 迁移 + shadow-run）★业务影响
- **是什么**：Braintree 把 LE/MM 商户迁到 direct-Fiserv 直连（EPP Phase 4 BT Fiserv Migration）。Net Settlement 让商户出款从 gross 结算改成 Fiserv 的每日净额结算（T+X → T+1 方向）。Chi 端到端拥有 Pricing 这一侧：plan-code/fee 映射、pass-through fee 计算、schedule 同步、审计、对 Fiserv 上报费用的 reconciliation。
- **迁移 + shadow-run（对应 resume bullet 4）**：Interchange fee 取数从 Trans View 切到 Settle View，切换前用 day-level SQL 做 shadow 对账——**>99.9% 字段一致 @ 13.7M 行（0.224% variance）**，feature toggle `US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED` 灰度，并把这套沉淀成可复用的 "CDC Table Backfilling Template"。
- **量化业务**：Net Settlement 是 **$55B+ 增量 TPV** 的前提（Google $40B / Microsoft $10B / Meta $5-7B），解决 **$450M/月 float** 问题（Fiserv 每日净结算，当前 gross 结算让 BT 垫付 IC++ 费用）。2 年+ 持续唯一 owner。
- **锚点**：Jira epic 链 DTBTTFOUND-2071→2074→2232→2541→2879→**3126(P1, 进行中)**，parent solution PSCBU-1645；PR snowglobe #1615（interchange 取数切换）；Confluence "Discovery on View Switch..."(2698298357)、"Settle View to replace Tran View as SOR..."(2747965111)、"CDC Table Backfilling Template"(2747848324)。
- **可答题**：最大业务影响/规模 / 端到端 ownership / 处理模糊性 / 为什么 ready for promotion。

### S6 · Fee Anomaly Detector 接管 + ROI gate（staff 级判断）
- **是什么**：一个实习生（Lakshay Soin，2026-08-14 offboard）建的 ML fee-anomaly detector，零生产验证（QA 建在 834M 行 / 6 个合成 merchant 上，prod 是 39B 行 / 18,140 merchant）。Chi 临时接管。
- **动作**：不是顺着实习生惯性继续投入，而是写 go/no-go ROI gate——量化 prod-scale 风险（**per-row numpy serving @ 760M rows/day 大概率 OOM/timeout**），给分阶段 cutover 方案，明确"Phase1/2/CI-CD/Slack 都不许动，等这个 gate 说 go"。
- **锚点**：Jira DTBTTFOUND-3254/3255/3256/3257/3259/3260/3261（label anomaly-detector）；Confluence "Fee Anomaly Detector — State, Handoff and Prod-Cutover Plan"(3049697063)。
- **可答题**：staff 级判断 / 多优先级取舍 / 主动 owning / 处理模糊性。

### S7 · snowglobe-tools（自发的开发者生产力基建）
- **是什么**：Chi 自建的个人 repo（czhang17_paypal/snowglobe-tools，100% 他），给 snowglobe 做隔离的 Snowflake schema pool，让多个 Claude Code agent 会话能并行在不同分支上跑而不撞 DDL/migration。
- **动作**：SCHEMA_POOL_V2 重写、写 ADR、处理 Flyway 边界（stream 失效顺序、重复 repeatable-migration 排除、prod-only 依赖的 stub 表）。**没有任何 ticket 驱动，纯自发**。
- **可答题**：主动发现并解决问题（非分配任务） / 超出 backlog 的贡献 / craft。

### S8 · Terraform grant-ownership 7 分钟 RCA（快速 unblock 团队）
- **根因**：`GRANT OWNERSHIP` on `FEE_ANOMALIES_DB` 被 Snowflake 拒，因为 `FEE_ANOMALIES_REVIEWER` 已持依赖的 USAGE grant；确认这是全 repo 唯一缺 `outbound_privileges` 的 `snowflake_grant_ownership` 资源。~7 分钟定位并出 PR #1326，release 成功部署。
- **锚点**：Slack #treasury-services-releases 2026-08-13 (parent ts 1786640974.325349)。
- **可答题**：快速 debug / unblock 他人 / 生产压力下的判断。

### S9 · DoorDash Amex disbursement 事故（被指定 owner + SLA 权威）
- **是什么**：DoorDash 报 Amex 出款延迟的正式事故频道。事故指挥 Kiran Patil 点名 Chi 为三个 fix owner 之一；George Fashho 在 SLA 问题上 defer 给 Chi，Chi 给出权威答案（"T+7 是 US 内部管线 SLA，我们要等 Amex 把钱 settle 到我们账户才出款"）。
- **锚点**：Slack #_inc3743178_doordash_us_amex_disbursement_delays 2026-07-06。
- **可答题**：incident/on-call ownership / 跨团队 / 领域权威。

### 补充可用工件（次级，按需引用）
- "To net or not to net..." postmortem(2946204146)：把某 bug scope 从 196,274 行/$11,123 精确重算到 21,923 行/$5,854，附完整 SQL——最强定量推理工件。
- "HC Task Failure — Streamlit App"(2989107333)：自建 Streamlit 自助监控 app `NON_AGG_AMEX_TASK_MONITOR`——可观测性工具。
- "Pinless False-Positive Alarms"(3008530291)：31.0M 条 junk 误报根因修复——降 on-call 噪音。
- Chi 自己维护的 onboarding doc（885424440，2024-06 建、2026-08 仍在编辑）——知识沉淀/带教基底。

---

## 2. Ziyang（Leo Huang）带教框架 —— ⚠️ 诚实红线，重点看

**真实事实**：Ziyang 是 Chi 的 mentee（同团队、Chi 是领域 owner）。Ziyang 的真实工作：
- Scheme Fee estimation ML（DTBTTPBIL-713 / repo scheme-fee-estimate）：XGBoost + Snowflake 分布式训练（GPU/Ray），accuracy V0→V9 从 90.57% 迭代到 98.57%，prod 验证 95%+。与 co-intern Joseph Loeffler 合作。**这个项目正落在 Chi 拥有的 fee/pricing 领域内。**
- Snowglobe Migrated Merchant Exclusion（DTBTPRWIZ-730/714）：建 `SnowglobeExclusionService`，防止 Pricing 对已迁到 **Chi 的 Snowglobe** 的 merchant 重复计费。pricing #3054/#3108/#3129/#3159。
- Funding→Pricing gRPC journaling-schedule sync + 回填 + bulk update/delete API（funding #13724/#13790/#13881/#13992/#14206/#14302/#14386，epic DTBTPRWIZ）。这套 sync **喂的正是 Chi 的 Snowglobe 需要的 journaling 数据**。
- Bulk Pricing Update / Trinity（DTBTPRWIZ-1037）+ 自发架构文档 "PMS Architecture" / "batch-pricing-correction Architecture"（senior 信号）。

**⚠️ 诚实约束（所有带教答案必须遵守）**：
- **GitHub / Jira / 公开 Slack 里没有 Chi 直接 review / 评论 / co-author Ziyang PR 的痕迹**。不要编造 PR review 记录、不要编造具体的 review 评论内容或 1:1 对话细节。
- **正确框定 = domain-ownership / architectural collaboration，不是 code-review trail**：Chi 拥有 Snowglobe 和 fee-calc 的标准与领域知识；Ziyang 的每一块工作（exclusion service、gRPC sync、scheme fee ML）都要接入或依赖 Chi 的领域；Chi 定义 contract、在事故里是 Ziyang 依赖的 fee-calc 权威、在架构方向上把关。这条线是**真实可辩护**的（Ziyang 的工作确实全部整合进 Chi 的 domain）。
- 日常带教的细节（1:1、DM、pairing、口头 unblock）**留占位** `【待 Chi 补充：具体 1:1/pairing 细节】`，让 Chi 自己填真实内容，不要替他编。
- 可用的真实连接点：Slack 里 Hari Devulapally 提到 "Leo Huang worked on excluding fee calculations for Snowglobe journaled merchants"（即 Ziyang 的活儿是围绕 Chi 的 Snowglobe 展开的）；Chi 是 #lep-mentees / #lep-all 成员（leadership/mentee program）。

---

## 3. 全局诚实红线（Wave A & B 都遵守）

- **数字占位**：未在证据中确认的具体数字用 `【预估：xxx】` 或 `【待 Chi 更新：xxx】`，给合理预估。已确认的数字（$138.6B、21.96M、$55B TPV、$450M/月 float、196 merchants/$11.3M/day、13.7M 行/0.224%）直接用。
- **不能编造**：不存在的项目、不存在的 review 记录、不存在的对话。只放大真实工作的影响面和难度表述（适度包装 OK）。
- **简历里需要标注的三处 gap**（Wave A 必须点出，Wave B 答案回避不确定数字）：
  1. **$600B annual volume**：证据里可辩护的是 **$138.6B**（2025 Amex volume，Chi 自己的 impact doc）。$600B 可能是全 BT 年交易量或年化口径——标 `【待 Chi 确认口径：$600B 是否为全平台/年化，否则用 $138.6B】`。
  2. **Sentry**：全部 6 个来源里**只找到 Datadog（+ 自建 Streamlit 监控 + Splunk）**，没找到 Sentry。标 `【待 Chi 确认：Sentry 是否实际使用，否则改为 Datadog】`。
  3. **Kafka in Kubernetes（intern bullet）**：intern 有据的是 "REST Log Module" + "Spark Validators"（Confluence 966206164/966731781）。Kafka-in-K8s 是最弱的一条，需 Wave A 专门查证（本地有 repo `kafka-snowflake-connector` / `event_protos` 可查），查不到就诚实标注。

---

## 4. 本地 repo / 资源位置（Wave A 用）

- 主 repo 克隆：`/Users/czhang17/Code/snowglobe`（Java17+Snowflake SQL）、`/Users/czhang17/Code/pricing`（Kotlin/Spring+gRPC）、`/Users/czhang17/Code/funding`（Ruby on Rails+gRPC）、`/Users/czhang17/Code/snowglobe-terraform`。
- 可能含 intern / 补充证据的本地 repo：`/Users/czhang17/Code/kafka-snowflake-connector`、`event_protos`、`amex_settlement_parser`、`business_date`、`PassthroughFee-HealthCheck-Dashboard`、`snowglobe-tools`。
- EMU 身份：Chi = `czhang17_paypal`（czhang17@paypal.com）；Ziyang = `ziyhuang_paypal`，GitHub/Jira/Slack 显示名均为 **"Leo Huang"**。
- rtk 注意：`git log` 多行输出会被截断到 ~50 行；用 `git rev-list --count` 等单行输出命令，或 `rtk proxy git ...` 绕过。`find` 只支持简单谓词（不支持 `-not`/`-exec`）。
