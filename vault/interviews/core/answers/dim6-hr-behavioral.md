# 维度 6 · HR 行为题（HR Behavioral / Fit）

> 逐题面试手册 / promotion review 逐题总结。每题两个备选答案：A = 影响导向（精简，60–90 秒），B = 技术深度（叙事展开）。数值占位处 Chi 面试前替换真实值。

---

## Q21. 你为什么 ready for promotion？你怎么定义 Senior 这个 level，以及你已经在做哪些 Senior 该做的事？

### 答案 A · 影响导向（STAR 精简版）

我对 Senior 的定义是四条：**scope 超出个人项目、造平台化的杠杆、事实上的 on-call owner、放大别人**。这四条我现在都在做，不是"准备做"。

- **Scope 超出个人项目**：我端到端拥有 Net Settlement Pricing —— 这是 Braintree 把 LE/MM 商户迁到 direct-Fiserv 的前提，撬动 **$55B+ 增量 TPV**（Google/Microsoft/Meta），解决 **$450M/月的 float** 问题。这不是一个 feature，是一条跨 Pricing/Funding/Fiserv 的收入关键路径,我做了 2 年+ 的唯一 owner。
- **平台化杠杆**：我没有一个个手写 quality-check，而是造了一个 config 表驱动 + handshake 的框架，全团队后续复用了 ~8 次（S2）。
- **事实 on-call owner**：ACH fee-calc 生产事故、AU Amex refund、DoorDash 出款事故，都是全团队按名把我 ping 进去、我给出权威根因（S3/S4/S9）。我是 snowglobe repo 全时段 **#1 committer**（615 commits，领先第二名 467）。
- **放大别人**：我带 Ziyang（Leo Huang），他做的 exclusion service、gRPC journaling sync、scheme-fee ML 全部接入或依赖我拥有的 Snowglobe/fee-calc 领域,我定 contract、把关架构方向。

Senior 是"团队因为你而运转得更好",不是"你自己产出多少"。我已经在这个位置上了,promotion 只是把 title 对齐现实。

### 答案 B · 技术深度（叙事展开版）

我不想用"我很努力"来论证 ready。我用 Senior 这个 level 该有的**行为定义**逐条对齐我的实际工作,你可以逐条 challenge。

**定义 1 —— scope 超出单个项目,进入收入/风险关键路径。**
Net Settlement Pricing（S5）是最硬的例子。BT 要把大商户迁到 direct-Fiserv,出款方式从 gross 结算改成 Fiserv 每日净额结算(T+X → T+1)。我拥有 Pricing 这一侧的全部:plan-code/fee 映射、pass-through fee 计算、schedule 同步、审计、对 Fiserv 上报费用的 reconciliation。它是 $55B+ 增量 TPV 的前提,解决 $450M/月的 float。它跨 Pricing、Funding、Fiserv 三方,是多季度、多次迁移、有 shadow-run 的工程(epic 链 DTBTTFOUND-2071→…→3126,现在 P1 进行中)。一个 mid-level 会拥有一个明确边界的项目;我拥有的是一条模糊、跨团队、随业务演进的**能力线**。

**定义 2 —— 造平台化杠杆,而不是造 feature。**
Quality-Check & Handshake 框架(S2)。团队原来每个 fee subject area 都要单独写校验逻辑。我建了一个集中式 config 表驱动 + 通用 procs 动态执行 + trigger-status handshake 告诉下游"这块数据已验证可读"的框架(#1997,1,489 行),然后自己在几乎每个 fee subject area 铺开 ~8 次。更能说明问题的是:后来我发现原框架有个设计缺陷 —— 某 subject area ~4% 失败就 block 全部 merchant。我写了正式 ADR(MADR 3.0.0 模板,含正确性证明和 3 个被否方案),把它重构成 merchant-level 粒度。**发现自己造的东西有缺陷、写正式决策工件、否掉备选方案、改对**,这是 Senior 的自我修正闭环。

**定义 3 —— 事实上的 on-call / 领域 owner,团队的 go-to person。**
证据不是我自己说的,是团队行为:ACH fee-calc 那条 PagerDuty(S3),我自己转发并当场给出完整根因 —— 精确到 `GET_EVENTSTREAM_PAYMENT_INSTRUMENT_SUB_KIND()` 的 1-arg vs 2-arg overload 导致 `'BT_' || NULL = NULL`,影响 ~196 merchants / ~$11.3M/day GMV,然后持续 owning 数周还合并了 UDF overload(DTBTTFOUND-3246)。AU Amex refund(S4)是 PM 走正式 "Request Help" 表单、Tejesh 点名路由给我。DoorDash 出款事故(S9)事故指挥点名我做 fix owner 之一、别人在 SLA 问题上 defer 给我。**别人在压力下把不确定性交给谁,谁就是那个 level 的人。**

**定义 4 —— 放大别人的产出。**
我带 Ziyang(Leo Huang)。这里我说实话,我不靠"我 review 了他多少 PR"来讲 —— 我讲领域所有权:他做的 SnowglobeExclusionService(防止对已迁到我 Snowglobe 的 merchant 重复计费)、Funding→Pricing 的 gRPC journaling sync(喂的正是我 Snowglobe 需要的数据)、scheme-fee ML,**每一块都接入或依赖我拥有的领域**。我定义这些接口的 contract,在事故里是他依赖的 fee-calc 权威,在架构方向上把关。他的工作能落地,是因为我这条领域线稳。【待 Chi 补充:一次具体的 1:1 / pairing / unblock 细节】

我还做了没有 ticket 驱动的事:snowglobe-tools(S7),给团队做隔离 schema pool 让多 agent 并行开发,纯自发。这是 craft,是"我看到团队的痛就去解决",不是等分配。

综合起来:我不是在为 promotion 攒证据,我是已经在 Senior 的行为空间里运行了。

> 证据锚点:S5 Net Settlement(epic DTBTTFOUND-2071→…→3126 P1、$55B TPV / $450M float);S2 Quality-Check 框架(#1997)+ ADR "[ADR Draft] Merchant-Level Quality Checks Using Dense Relational Rows"(Confluence 2894288991, DTBTTFOUND-2749);S3 ACH RCA(DTBTTFOUND-3246);S4 AU Amex(DTBTTFOUND-3269);S9 DoorDash 事故;#1 committer(615 commits);带 Ziyang(SnowglobeExclusionService / gRPC journaling sync);S7 snowglobe-tools。

---

## Q22. 你最大的优势是什么？(挑 2–3 个核心竞争力,各配一个证据)

### 答案 A · 影响导向(STAR 精简版)

三个:

1. **平台化 / 系统思维** —— 我倾向于造复用杠杆而不是一次性 feature。Quality-Check 框架建一次、团队复用 ~8 次(S2)。
2. **端到端 ownership + 领域权威** —— 从零搭 AMEX GRRCN 全管线(file ingestion → parse → fee 计算 → 出款),处理了 21.96M 笔 / $138.6B volume(S1);团队出事故第一个 ping 我,我给根因(S3/S4)。
3. **业务影响的规模感** —— 我知道自己的代码在撬动什么钱。Net Settlement 是 $55B+ 增量 TPV 的前提、解决 $450M/月 float(S5)。我做技术决策时是带着这个量级在做的。

### 答案 B · 技术深度(叙事展开版)

**优势一 · 平台化 / 系统思维 —— 我造杠杆,不造一次性代码。**
面对一个反复出现的需求,我的第一反应是"这个抽象的正确边界在哪",不是"先把这次做完"。Quality-Check & Handshake 框架(S2)是典型:我没有在每个 fee subject area 里 copy-paste 校验逻辑,而是建了一个 config 表驱动、通用 procs 动态执行、handshake 通知下游的框架,一次建成、~8 次复用。而且我对自己造的抽象有 review 能力 —— 发现它 "~4% 失败 block 全 merchant" 的粒度错误后,我用 ADR 把它降到 merchant-level。同一条线上还有 snowglobe-tools(S7),自发造的隔离 schema pool 基建。系统思维不只是"设计得漂亮",是**能持续对自己的设计做正确性判断和修正**。

**优势二 · 端到端 ownership + 领域权威 —— 我拥有一整条链,并且团队信任这个所有权。**
AMEX GRRCN(S1):我从前任留的 stub 接手,独立出设计(`STAGE_AMEX_GRRCN_FILE` task + 6 条 append-only streams + 解析定宽记录的 UDTFs + 7 张表 + feature-flag 急停),实现、EU 扩展、18 个月生产防御,还把原本在 Funding 里的 Ruby 脚本迁到 Snowflake-native SQL。这条链处理了 21.96M 笔 Amex 交易 / $138.6B volume。所有权的另一面是**领域权威**:ACH fee-calc 事故我能一眼定位到 UDF overload(S3);AU Amex refund 我定位到 `fee_refund_policy='partial'` 的全域规律(S4);DoorDash 事故我是 SLA 问题上团队 defer 的对象(S9)。拥有一条链、并且成为别人遇到这条链上任何问题时找的人 —— 这两件事加起来才是真正的 ownership。

**优势三 · 业务影响的规模感 —— 我做技术决策时脑子里有钱的量级。**
很多工程师的视野停在"这段 SQL 对不对";我的视野是"这段 SQL 错了会漏算/垫付多少钱"。Net Settlement(S5)我能讲清楚它为什么是 $55B+ 增量 TPV 的前提(Google $40B / Microsoft $10B / Meta $5-7B)、为什么它解决的是 $450M/月的 float(gross 结算让 BT 垫付 IC++ 费用,改成 Fiserv 每日净结算后就不用垫)。这种规模感直接影响我怎么做技术取舍 —— 比如 interchange 取数从 Trans View 切到 Settle View 时,我不是切完就上,而是先 day-level shadow 对账到 **>99.9% 一致 @ 13.7M 行(0.224% variance)**、feature toggle 灰度、再沉淀成可复用的 CDC backfilling template。因为我知道这条链上错一个字段是什么量级的钱。

如果只能留一个:第二个(端到端 ownership + 领域权威),因为它最难被替代 —— 平台能力可以学、规模感可以培养,但"团队出事第一个想到你"是长期积累的信任。

> 证据锚点:S2 Quality-Check 框架(#1997)+ merchant-level ADR(Confluence 2894288991);S1 AMEX GRRCN(PR #886 单个 1,849 行、epic DTBTTFOUND-2074、21.96M 笔 / $138.6B);S3 ACH RCA / S4 AU Amex / S9 DoorDash;S5 Net Settlement($55B TPV / $450M float、interchange 切换 shadow-run 13.7M 行 / 0.224%、CDC backfilling template)。

---

## Q23. 你未来 6–12 个月的职业规划?你打算为团队 / 组织创造什么价值?

### 答案 A · 影响导向(STAR 精简版)

三条主线,都是把现有的高价值工作收尾并放大:

1. **收尾 Net Settlement**(DTBTTFOUND-3126,P1 进行中)—— 把这条 $55B+ TPV / $450M float 的链推到全量上线,这是团队今年最大的收入杠杆。
2. **Fee Anomaly Detector 的安全 cutover**(S6)—— 我已经写了 go/no-go ROI gate,接下来按分阶段方案把它从"实习生 QA 验证"推到 prod-scale(39B 行 / 18,140 merchant)可用,给团队一个真正能用的 fee 异常防线。
3. **放大 mentee 杠杆** —— 继续把 Ziyang 以及后续新人的工作接入我拥有的领域,让我不再是唯一 owner,把领域知识沉淀成团队能力(我一直在维护的 onboarding doc 就是基底)。

一句话:从"团队的关键单点"变成"团队的关键 multiplier"。

### 答案 B · 技术深度(叙事展开版)

我的规划不是"学个新技术栈",是**把我已经在做的高杠杆工作,从单点收尾成组织能力**。

**主线一 · Net Settlement 收尾上线(DTBTTFOUND-3126,P1)。**
这是团队最大的收入关键路径。接下来 6 个月我要把 Pricing 这一侧的剩余环节推到全量:pass-through fee 计算的边界 case、对 Fiserv 上报费用的 reconciliation 稳态、schedule 同步的容错。价值很直接 —— 它是 $55B+ 增量 TPV 能落地的前提,也把 $450M/月的 float 从 BT 账上拿掉。做 owner 2 年+,我要的是看它真正跑在全量商户上。

**主线二 · Fee Anomaly Detector 的负责任 cutover(S6)。**
这是我想强调的一条,因为它体现的是 staff 级判断而不是执行。一个实习生建的 ML fee-anomaly detector,QA 只在 834M 行 / 6 个合成 merchant 上跑过,prod 是 39B 行 / 18,140 merchant。我接管时没有顺着惯性继续投入,而是写了 go/no-go ROI gate,量化 prod-scale 风险(per-row numpy serving @ 760M rows/day 大概率 OOM/timeout),给分阶段 cutover 方案。未来半年我要按这个 gate 把它推过去 —— 如果 ROI 成立,团队就多了一条自动 fee 异常防线;如果不成立,我也会诚实叫停。**创造的价值不只是一个工具,是一个"什么值得投入"的判断范式。**

**主线三 · 把领域从"我"扩成"团队"—— 放大 mentee 杠杆。**
现在的风险是我在 Snowglobe / fee-calc 上太单点。未来 6–12 个月我要主动把这个所有权分出去:继续把 Ziyang 的工作(exclusion service、journaling sync、scheme-fee ML)以及新人的工作接进我定义的 contract 里,让他们能独立在我的领域上推进;把事故 RCA 的模式、quality-check 框架的用法、onboarding 知识沉淀成文档和标准(我从 2024 就在维护 onboarding doc)。目标是**让团队在没有我在场时也能处理 fee-calc 事故**。这对组织的价值比我个人再多写 10K 行代码大得多。

把这三条串起来:今年我从"团队最可靠的单点"转型成"团队的 multiplier"—— 这本身就是 Senior 之后往 Staff 走的方向。

> 证据锚点:S5 Net Settlement(DTBTTFOUND-3126 P1 进行中);S6 Fee Anomaly Detector(Confluence "Fee Anomaly Detector — State, Handoff and Prod-Cutover Plan" 3049697063、DTBTTFOUND-3254~3261);带 Ziyang(SnowglobeExclusionService / gRPC journaling sync / scheme-fee ML);自维护 onboarding doc(Confluence 885424440)。

---

## Q24. 描述一次你收到批评性反馈的经历,你怎么消化和改进的?(挑一个已解决的,成长叙事)

### 答案 A · 影响导向(STAR 精简版)

我的 Quality-Check 框架(S2)上线后,在一次设计讨论里有人指出了一个我没预料到的缺陷:框架是 subject-area 粒度的 gate —— 某个 subject area 只要 ~4% 的数据失败,就会 block 掉**全部** merchant 的下游读取,包括那 96% 完全正常的。这个反馈一开始不好接受,因为这是我自己造的、还铺开了 ~8 次的框架。

但我认下来了:粒度选错了。我没有打补丁,而是写了一份正式 ADR(MADR 3.0.0 模板,含正确性证明 + 3 个被否方案),把 gate 从 subject-area 级重构成 merchant-level(复用 `QUALITY_CHECK_RESULTS_V1` + `HAS_MERCHANT_DETAIL` flag)—— 坏数据只 block 受影响的 merchant,好数据照常流。

我学到的:**对自己造的抽象要有和对别人代码一样的 review 严格度**。现在我设计任何 gate/校验时第一个问的就是"失败的爆炸半径是谁"。

### 答案 B · 技术深度(叙事展开版)

我讲 Quality-Check 框架这个,因为它是我自己的东西被指出缺陷 —— 这比讲别人给我改代码风格更能说明我怎么处理批评。

**情境。** 我造了 Quality-Check & Handshake 框架(S2),config 表驱动、通用 procs 执行校验、handshake 通知下游"这块数据已验证"。我自己很满意,在几乎每个 fee subject area 铺开了 ~8 次,它已经是团队的既成事实。

**反馈。** 在一次相关讨论里,问题被摆出来:我的 handshake 是 **subject-area 粒度**的 —— 一个 subject area 内只要有 ~4% 的行没通过校验,handshake 就不 flip,整个 subject area 对所有 merchant 都不可读。也就是说 4% 的坏数据会连坐 96% 的好数据。这个反馈刺,因为(a)是我设计的,(b)已经复用了 8 次,推翻它意味着承认我在一个基础决策上错了,而且改动面不小。

**我怎么消化。** 我第一反应当然是想辩解"这样更安全"。但我逼自己把它当成别人的代码来 review:如果这是同事写的,我会不会 approve 这个粒度?不会。安全和可用性之间,我选错了默认 —— 一个 pricing 数据平台,让好 merchant 因为别的 merchant 的坏数据而拿不到结算,这不是"更安全",这是把可用性问题伪装成正确性问题。反馈是对的。

**我怎么改。** 我没有就地打个 flag 补丁糊过去。我写了正式 ADR("[ADR Draft] Merchant-Level Quality Checks Using Dense Relational Rows",MADR 3.0.0 模板),因为这是个需要被团队记住的决策:里面有正确性证明(为什么 merchant-level 不会漏掉真正的系统性错误)、有我评估并否掉的 3 个备选方案(为什么不用简单加白名单、为什么不做 subject-area 内部分档等)。最终方案复用已有的 `QUALITY_CHECK_RESULTS_V1` + `HAS_MERCHANT_DETAIL` flag,把 gate 降到 merchant 粒度 —— 坏数据只 block 它自己那个 merchant。

**我学到什么。** 两条,都改了我后来的行为:
1. **对自己的抽象要用 review 别人代码的严格度**。我最容易放过的 bug 是我自己设计里的 bug,因为我对它有 sunk cost。现在我设计任何 gate 都先问"失败的爆炸半径是谁、是不是最小连坐单元"。
2. **推翻自己 8 次复用过的设计,用 ADR 而不是 hotfix**。承认设计错了不丢人,丢人的是打补丁把错误埋深。写 ADR 强迫我把"为什么原来错、为什么新的对、为什么不选别的"讲清楚,这对团队是资产。

这次反馈没让我防御,反而让我拿到了全库最强的一份架构决策工件。这就是我处理批评的方式 —— 把它当成升级设计的输入,不是对我个人的攻击。

> 证据锚点:S2 merchant-level 重构 ADR "[ADR Draft] Merchant-Level Quality Checks Using Dense Relational Rows"(Confluence 2894288991, DTBTTFOUND-2749);原框架 #1997 + 铺开 ~8 次(#2061/#2069/#2075/#2091/#2106/#2558/#3040/#3237);复用 `QUALITY_CHECK_RESULTS_V1` + `HAS_MERCHANT_DETAIL`。
>
> 【备用/替换选项:若面试想讲一个更"外部人给的"批评而非自己发现的缺陷,用占位 `【待 Chi 补充:一次真实的、来自 reviewer/manager 的批评性反馈 —— 情境 / 反馈原话 / 你最初的情绪反应 / 你如何验证反馈是对的 / 你具体改了什么 / 后续行为变化】`,套用上面 B 的五段结构即可。】
