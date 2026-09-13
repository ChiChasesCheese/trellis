# 逐题面试手册 · 维度 1（技术深度）+ 维度 2（业务影响）

> Chi Zhang · Braintree Pricing & Settlement · Senior SWE 晋升
> 每题两个答案：A 影响导向（60–90 秒），B 技术深度（可被追问 how/why 时展开）。

---

## Q1. 讲一个你做过的技术上最有挑战的项目——复杂在哪，你是怎么拆解和解决的？

### 答案 A · 影响导向

去年我从零搭了 Amex GRRCN 结算管线——GRRCN 是 Amex 专有的定宽结算文件格式，我们要把它端到端接进 Snowglobe：文件落地 → staging → 解析 → 算 Braintree fee → 聚合 → 交给 Funding 出款。难点是它同时是「新支付集成」和「跨系统迁移」两件事：原来这套逻辑是 Funding 里的一堆 Ruby 脚本，我要把它整体搬成 Snowflake-native 的 SQL 管线，还要在迁移期间保证一分钱都不能错。

我接手的只是前任留下的一个 stub，设计、实现、EU 扩展、到之后 18 个月的生产防御，基本都是我独立 own 的。最终这条管线一年处理了 **21,964,869 笔 Amex 交易、$138.6B 结算 volume**，是我任期内最硬的可辩护影响数字。

### 答案 B · 技术深度

复杂度我拆成三层来讲。

**第一层是格式和正确性**。GRRCN 是定宽记录、多种 record type 混在一个文件里，我用 UDTF 来解析定宽记录，落进 6 条 append-only stream 驱动的增量管线，加上 7 张 staging/target 表。核心设计是 `STAGE_AMEX_GRRCN_FILE` task 做 ingestion，后面每一步都是 stream 驱动、幂等、可重放——因为结算数据错一次的成本极高,我宁可让每一步都能安全重跑，也不做「一次性跑对」的乐观假设。

**第二层是迁移风险**。把 Funding 的 Ruby 逻辑搬到 SQL,最大的坑是「行为等价」——不能只是重写，得证明新旧结果一致。而且迁移期我必须能随时急停,所以我加了 feature flag `AGGREGATED_AMEX_SEPARATE_FLOW`,让 aggregated 和 non-aggregated 两条流可以独立灰度、独立回滚。

**第三层是长期防御**。上线不是终点。这条管线我后面跟了 ~10 个 hardening PR,单个最大的 PR #886 有 1,849 行(我任期最大)。这里我学到的判断是:结算这种系统,「上线」和「可长期维护」是两个 milestone,真正的 Senior 工作量在后者——我为它建了自助监控(Streamlit 的 `NON_AGG_AMEX_TASK_MONITOR`)、修了误报告警,让它不需要我天天盯着也能稳。

> 证据锚点：PR snowglobe #751/#856/#862/#886/#911/#1023 + ~10 hardening PR；Jira DTBTTFOUND-1960/1961/2084/2097/2139，epic DTBTTFOUND-2074；Confluence 2233926829 / 1112867224。

---

## Q2. 你做过的最重要的一次技术决策 / 架构权衡是什么？为什么这么选，放弃了什么？

### 答案 A · 影响导向

我最重要的一次架构决策,是把整个 quality-check 框架从 subject-area 级重构成 merchant 级。

背景:我之前造了一个所有 fee subject area 复用的 quality-check 框架,自己铺开了 ~8 次。用了一段时间后我发现一个设计缺陷——某个 subject area 只要 ~4% 的数据校验失败,就会 block 掉**全部** merchant 的 merge。这对高价值商户是不可接受的:一小撮脏数据能把所有人挡在门外。

我写了一份正式的 ADR(MADR 3.0.0 模板,带正确性证明和 3 个被否掉的备选方案),把它改成 merchant-level——一个商户的数据坏了只 block 那个商户,其他人照常放行。这是从「全有全无」到「按商户隔离」的根本性权衡改变。

### 答案 B · 技术深度

关键权衡在**故障隔离粒度 vs. 实现复杂度**。

原设计用 subject-area 级的 pass/fail,好处是简单、状态少;代价是 blast radius 是整个 subject area。我要把粒度降到 merchant,难点是不能推翻已经铺开 ~8 处的框架,得复用现有工件。所以方案是复用 `QUALITY_CHECK_RESULTS_V1`,加一个 `HAS_MERCHANT_DETAIL` flag——有 merchant 明细的走细粒度隔离,没有的退回旧行为,平滑迁移。

ADR 里我认真写了正确性证明,因为 quality-check 本身是「守门员」,守门员逻辑改错比不改更危险——我必须证明新逻辑不会漏放本该 block 的坏数据。我还显式记录了 3 个被否的备选:比如【预估:一个是按 subject area 加白名单豁免,一个是纯阈值放宽】,以及为什么它们要么治标不治本、要么把复杂度推给下游。

**我放弃了什么**:放弃了旧设计的简单性,也接受了 dense relational rows 带来的存储和查询开销。但对结算 pipeline,「一个商户的问题不该连坐所有商户」这个正确性属性,值这个复杂度。这份 ADR 是我目前最强的架构决策工件,不只是修 bug,是在给团队定「quality-check 该怎么建」的标准。

> 证据锚点：Confluence ADR "[ADR Draft] Merchant-Level Quality Checks Using Dense Relational Rows"(2894288991)，Jira DTBTTFOUND-2749；框架 PR #1997(DTBTTFOUND-2664) + 铺开 #2061/#2069/#2075/#2091/#2106/#2558/#3040/#3237。

---

## Q3. 描述你 debug 过的最难的一个问题（生产事故或诡异 bug），你怎么定位到根因的？

### 答案 A · 影响导向

最难的一次是一条 ACH fee-calc 的 PagerDuty:`CHECK_TRANSACTION_HAS_BRAINTREE_FEES` 报警,大量 ACH 交易没有生成 fee。我自己转发了这条 alert,并当场给出了完整根因。

根因是:Standard ACH(没开 `ACH_FASTER_FUND`)在 promote 进 `TRANSACTIONS` 表时,`payment_instrument_sub_kind` 是 NULL;而 fee-calc 的品类映射是字符串拼接 `'BT_' || NULL`,SQL 里这个结果是 NULL,于是根本不生成 discount/settled fee。影响是 **~196 个商户、~$11.3M/天 GMV、~1.05M 行**,其中 98.9% 是 us_bank_account、100% 归因到 STANDARD_ACH。定位之后我持续 own 了这个问题好几周,不是丢回去就走。

### 答案 B · 技术深度

难点在于它是一个**静默的正确性 bug**,不是崩溃——没有异常、没有报错,fee 就是「悄悄没生成」,而且只影响一个子类别,极容易被当成正常业务波动漏掉。

我的定位路径:先从数据反推,发现缺失 fee 的交易高度集中在 STANDARD_ACH,这把范围一下收窄。然后顺着 fee-calc 逻辑往上游追 `payment_instrument_sub_kind` 是从哪来的,精确定位到 SQL 工件 `R__create-eventstream-to-pending-transactions-with-source-stored-procedure.sql` 里的 `GET_EVENTSTREAM_PAYMENT_INSTRUMENT_SUB_KIND()`——关键是这个函数有 **1-arg 和 2-arg 两个 overload**,change #2941 引入的路径走到了返回 NULL 的那个 overload。SQL 里 `NULL` 参与字符串拼接的传染性(`'BT_' || NULL = NULL`)就是那个把 bug 放大到全品类的隐形放大器。

我踩到的教训:**SQL 的 NULL 语义是这类静默数据 bug 的头号来源**,尤其在字符串拼接做品类映射时。所以修复不止是补这一处,我后面推动把这个 UDF 的两个 overload 做了合并(consolidation),从根上消除「调错 overload」的可能。我还把这次的定量分析沉淀成 postmortem,把 scope 从初估的 196,274 行 / $11,123 精确重算到 21,923 行 / $5,854——因为事故里给出一个能被审计的准确数字,比一个吓人的粗估更有价值。这次之后 Sahar 和 Dylan 都公开致谢了。

> 证据锚点：Slack #snowglobe 2026-07-29 (ts 1785371583.033749)；Confluence "CHECK_TRANSACTION_HAS_BRAINTREE_FEES"(3029344728)、UDF overload 合并(3052036330, DTBTTFOUND-3246)、postmortem "To net or not to net..."(2946204146)；起因 change #2941。

---

## Q4. 你在系统设计 / 架构层面最拿得出手的贡献是什么？

### 答案 A · 影响导向

最拿得出手的是我造的 quality-check & handshake 框架——这不是一个 feature,是一个平台。

Snowglobe 里每个 fee subject area 都需要做数据校验,以前是各写各的。我把它抽象成一个**配置表驱动**的框架:一张集中式 config 表定义校验规则,一组通用 procedure 动态执行这些校验,再用一个 trigger-status handshake 机制告诉下游「这块数据已经验证过、可以安全读了」。建好之后我自己在几乎每个 fee subject area 铺开了 ~8 次,后续别人加新校验也直接复用。这是我从「写 feature」跨到「造别人都在用的平台」的标志性工作。

### 答案 B · 技术深度

架构上我最看重三个设计选择。

**一是 config-driven 而非 code-driven**。校验规则放在数据里(config 表),不是散在各处的 SQL。这样加一条新校验是改配置、不是改代码,降低了每次扩展的边际成本——这也是为什么它能被复用 ~8 次而不腐化。

**二是 handshake 解决的是分布式数据管线里的可见性契约问题**。下游怎么知道上游这批数据「算完了且验过了」?我用 trigger-status handshake 做显式信号,而不是让下游去猜或轮询。本质上这是在给 pipeline 各阶段之间定一个明确的 data-readiness contract。

**三是我事后主动纠正了它的架构缺陷**(和 Q2 是同一条线):原框架是 subject-area 级 block,我发现 ~4% 失败连坐全部 merchant 的问题后,写 ADR 把它演进到 merchant-level 隔离,复用 `QUALITY_CHECK_RESULTS_V1` + `HAS_MERCHANT_DETAIL`。

我想强调的 Senior 信号是:**我不只造了这个平台,我还负责它的长期演进**——发现自己设计的缺陷、写正式 ADR、给出正确性证明、平滑迁移。造一个东西容易,持续为它的架构健康负责才是我在 architecture 层面真正拿得出手的地方。

> 证据锚点：PR snowglobe #1997(DTBTTFOUND-2664) + 铺开 #2061/#2069/#2075/#2091/#2106/#2558/#3040/#3237；ADR 2894288991(DTBTTFOUND-2749)。

---

## Q5. 你今年最大的业务影响是什么？（要带量化数据）

### 答案 A · 影响导向

今年最大的业务影响是 Net Settlement Pricing——我在 Pricing 这一侧端到端唯一 owner,已经持续 2 年多。

背景:Braintree 要把大商户(LE/MM)迁到跟 Fiserv 的直连,商户出款从「gross 结算」改成 Fiserv 的每日净额结算。这件事的量级:它是 **$55B+ 增量 TPV** 的前提——Google $40B、Microsoft $10B、Meta $5–7B 这几个大 logo 都挂在它上面;同时它解决一个 **$450M/月的 float 问题**,因为现在 gross 结算意味着 Braintree 每天要垫付 IC++ 费用。

我负责 Pricing 这侧的全部:plan-code/fee 映射、pass-through fee 计算、schedule 同步、审计,以及对 Fiserv 上报费用的 reconciliation。这是我最能证明「已经在做 Senior 级、收入关键、跨季度 ownership」的项目。

### 答案 B · 技术深度

我讲一个最能体现深度的子任务:Interchange fee 的取数源迁移 + shadow-run。

我们要把 interchange fee 的取数从 Trans View 切到 Settle View(因为 Settle View 才是结算的真实 SOR)。这种「换数据源」在结算系统里是高危操作——数字一旦不一致,直接影响给商户出多少钱。所以我没有直接切,而是先做 **shadow-run 对账**:切换前用 day-level SQL 把新旧两个源在同一天的结果逐字段比,结果是 **13.7M 行上 >99.9% 字段一致,variance 只有 0.224%**。拿到这个数我才有底气切,并且用 feature toggle `US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED` 灰度上线,而不是一把梭。

关键的 trade-off 判断:shadow-run 有额外成本(要跑两遍、要写对账 SQL、要人工审 variance),但对「改变商户实际到账金额」的变更,这个成本是必须付的保险。而且我把这套方法沉淀成了可复用的 "CDC Table Backfilling Template",让团队之后做类似的数据源迁移有现成模板——把一次性的谨慎变成团队的标准做法。

模糊性也是这个项目的一部分:它是多季度、需求随 Fiserv 那边推进不断变化的 P1,我从 DTBTTFOUND-2071 一路 own 到现在的 3126。能长期扛住这种模糊 + 高风险 + 收入关键的组合,是我认为自己 ready for promotion 的核心证据。

> 证据锚点：Jira epic 链 DTBTTFOUND-2071→2074→2232→2541→2879→3126(P1)，parent PSCBU-1645；PR snowglobe #1615；Confluence 2698298357 / 2747965111 / "CDC Table Backfilling Template"(2747848324)。（$55B TPV、$450M/月 float、13.7M 行/0.224% 均为证据确认数字。）

---

## Q6. 你的工作影响半径有多大——只在自己项目，还是跨团队 / 组织级？举例。

### 答案 A · 影响导向

三个层级我都能举出例子。

**项目内**:我是 Snowglobe 主 repo 全时段 #1 committer——615 commits、63 merged PR、17.1K+ 行,领先第二名(467)一大截,是这个平台事实上的核心。

**跨团队**:举个例子,PM Liz Lippow 走正式的 "Request Help" 流程报了个问题,Tejesh 直接点名把它路由给我——所有 AU 商户的 Amex refund fee 从来没生成过。这是跨到 PM 和其他团队的问题,最后是我定位到根因。

**组织级 / 事故权威**:DoorDash 报 Amex 出款延迟的正式事故里,事故指挥 Kiran Patil 点名我做三个 fix owner 之一;SLA 问题上 George Fashho 直接 defer 给我。我在这个领域已经是别人依赖的权威。总的来说,我在 Slack 86 个频道里被全团队按名 ping,是 fee-calc 和结算这块的 go-to person。

### 答案 B · 技术深度

我用 AU Amex refund 那个案子讲影响半径怎么形成的。

那是一个 50 条回复的长 thread,PM 走正式表单、Tejesh 点名给我。根因其实很「领域知识」:所有 AU 商户的 `fee_refund_policy` 是 `'partial'`,从来不是 `'full'`,导致 non-agg Amex refund fee 在 AU 从不生成。我用数据坐实——USA 有 1,079,627 行,AUS 是 0,跨 157 个商户,然后开了 DTBTTFOUND-3269。这里的点是:**我的影响半径不是靠职位,是靠领域权威**——别人遇到 fee-calc 说不清的问题,系统默认路由到我。

为什么会形成这种半径,我自己复盘有两个原因。一是我沉淀知识:我维护的 onboarding doc 从 2024-06 建到现在还在编辑,新人靠它上手;ACH 事故我写了能被审计的 postmortem。二是我造的东西是别人依赖的地基——quality-check 框架、Amex 管线、Net Settlement 的 pricing 侧。当你的产出是别人工作的前提时,影响半径是自然外扩的。

我也把这个信号用在带教上:我的 mentee Ziyang(Leo Huang)做的三块活儿——Snowglobe migrated-merchant exclusion service、Funding→Pricing 的 gRPC journaling sync、scheme fee 估算 ML——**每一块都接入或依赖我拥有的 Snowglobe / fee-calc 领域**。我定 contract、在事故里当他依赖的 fee-calc 权威、在架构方向上把关。【待 Chi 补充:具体 1:1/pairing 细节】。这说明我的影响已经通过别人的产出被放大,这是 Senior 该做的杠杆。

> 证据锚点：AU Amex — Slack #service-pricing 2026-08-03 (ts 1785766795.306709)，DTBTTFOUND-3269；DoorDash — Slack #_inc3743178_... 2026-07-06；#1 committer 数据(615/63/17.1K)；Ziyang 领域接入 — Hari Devulapally 关于 "Leo Huang ... Snowglobe journaled merchants" 的 Slack 记录。

---

## Q7. 举一个你主动发现并解决问题的例子（不是被分配的任务）。

### 答案 A · 影响导向

最纯粹的例子是 snowglobe-tools——一个完全没有 ticket 驱动、我自发建的开发者生产力基建。

问题是:我们越来越多地用 Claude Code agent 并行开发,但多个会话同时在不同分支上跑,会互相撞 Snowflake 的 DDL/migration,谁也没法干净地测。没人分配我这个任务,我自己建了一个独立 repo(100% 我),给 Snowglobe 做隔离的 Snowflake schema pool,让每个会话/分支拿到自己的 schema,并行开发不打架。这是我看到团队(包括我自己)真实的摩擦、主动去消除它的例子。

### 答案 B · 技术深度

技术上最有意思的是处理 Flyway 的边界情况。做 schema pool(SCHEMA_POOL_V2 那次重写)要克隆出可用的隔离 schema,难点全在 migration 的边界:stream 有失效顺序问题、repeatable migration 会重复执行要排除、还有些表只在 prod 存在但迁移依赖它们、得建 stub。这些都不是「跑一遍 Flyway」能解决的,得真正理解 migration 的执行语义。我还为这个工具写了 ADR——一个纯自发的内部工具我也按正式标准记录设计决策。

我想借这个例子讲一个更 staff 级的判断,是另一个主动 owning 的例子:一个实习生建了个 ML fee-anomaly detector,零生产验证——QA 是建在 834M 行 / 6 个合成商户上的,而 prod 是 39B 行 / 18,140 个真实商户。实习生 offboard 后我临时接管。**我没有顺着惯性继续投入**,而是先写了一个 go/no-go 的 ROI gate:量化 prod-scale 风险(per-row numpy serving 在 760M 行/天 大概率 OOM 或 timeout),给出分阶段 cutover 方案,并明确「Phase1/2、CI-CD、Slack 告警都不许动,等这个 gate 说 go 再说」。

这两件事放一起是我对「主动性」的定义:主动不等于「多干活」,而是**主动判断什么该干、什么该先叫停**。snowglobe-tools 是主动造价值,anomaly detector 是主动踩刹车避免把资源投进一个未验证的坑——后者往往更难,也更 Senior。

> 证据锚点：snowglobe-tools — repo czhang17_paypal/snowglobe-tools(100% 他，无 ticket)；anomaly detector — Jira DTBTTFOUND-3254/3255/3256/3257/3259/3260/3261(label anomaly-detector)，Confluence "Fee Anomaly Detector — State, Handoff and Prod-Cutover Plan"(3049697063)。

---

## Q8. 你如何衡量自己工作的价值 / 成功？

### 答案 A · 影响导向

我用三把尺子,从硬到软。

**第一,可辩护的业务量化**:我今年最硬的数字是我的管线处理了 $138.6B 的 Amex volume、21.96M 笔交易;我 own 的 Net Settlement 是 $55B+ 增量 TPV 的前提、解决 $450M/月的 float。这些是能被审计、能对上收入的数字,不是自吹。

**第二,复用次数**:一个东西被复用多少次,说明它是不是真的地基。我的 quality-check 框架被铺开 ~8 次,shadow-run 沉淀成团队复用的 CDC backfilling template。

**第三,go-to 信号**:别人遇到问题第一个想到谁。事故里被点名当 owner、PM 走正式流程点名找我、SLA 问题别人 defer 给我——这些是团队用行动投票的成功指标。

### 答案 B · 技术深度

我刻意不把「写了多少代码」当主要指标——虽然我确实是 #1 committer(615 commits)。commit 数是产出,不是价值。我更看重三个「杠杆」维度。

**一是正确性的可审计性**。在结算这行,价值的反面是「悄悄算错钱」。所以我衡量成功的一个标准是:我的变更能不能被证明是对的。这就是为什么我做取数源迁移要先 shadow-run 到 13.7M 行 / 0.224% variance 才敢切,为什么改 quality-check 我要在 ADR 里写正确性证明,为什么事故 postmortem 我要把 scope 从粗估的 196K 行精算到 21.9K 行。一个能被审计相信的数字,比一个漂亮的估计有价值得多。

**二是我的产出有没有变成别人的地基**。复用次数、别人依赖我的 contract、mentee 的工作全部接进我的领域——这些说明我的影响在被放大,而不是线性地随我一个人的工时增长。这是我判断自己是不是在 Senior 轨道上的核心信号。

**三是「不做什么」也算成功**。anomaly detector 那次我踩刹车、写 ROI gate 拦住一个未验证的 prod cutover——避免的损失不会出现在任何 dashboard 上,但那是真实价值。能识别并叫停错误的投入,和能交付正确的东西,我认为是同一种判断力的两面。

所以总结:我不用工时或代码量衡量自己,我用**可辩护的业务数字 × 被复用/被依赖的程度 × 判断的质量**来衡量。这三者恰好也是我认为区分 Senior 和 mid-level 的地方。

> 证据锚点：$138.6B / 21.96M 笔(Confluence 2750481503)；$55B TPV / $450M float；shadow-run 13.7M/0.224%；quality-check 复用 ~8 次；ADR 正确性证明(2894288991)；anomaly detector ROI gate(3049697063)；#1 committer 615 commits。
