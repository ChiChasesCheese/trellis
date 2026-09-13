# 维度 3(技术领导力)+ 维度 5(处理模糊性与 Ownership)逐题手册

> Chi Zhang · 晋升 Senior SWE · 面试逐题手册 / promotion review 逐题总结
> 每题两个答案:A 影响导向(60–90 秒,punchy)/ B 技术深度(被追问 how/why 时展开)。
> 数字凡未在证据中确认的,以 `【预估】`/`【待 Chi 更新】` 标注。

---

## 维度 3 · 技术领导力(Technical Leadership)

## Q9. 你如何在没有正式管理权(no authority)的情况下影响他人、推动一个技术决策落地?

### 答案 A · 影响导向

我没有 title 带来的授权,靠的是「在关键领域成为别人绕不开的权威」。最典型的一次:一条 PagerDuty(`CHECK_TRANSACTION_HAS_BRAINTREE_FEES`)炸了,影响 ~196 个 merchant、每天 ~$11.3M GMV 的 ACH 交易没生成 fee。我不是那条告警的 assignee,但我自己转发到 #snowglobe,当场给出完整根因——Standard ACH promote 进 `TRANSACTIONS` 时 `payment_instrument_sub_kind = NULL`,导致品类映射 `'BT_' || NULL = NULL`,fee 直接不生成。因为根因给得干净、可复现、精确到具体 SQL 工件和 change 号,团队直接按我的方向修,后续几周的持续 owning 也默认由我来。Sahar 和 Dylan 在频道里公开致谢。我影响别人的方式不是「说服」,是「先把问题啃到没人比我更清楚」,权威自然就在我这。

> 证据锚点:S3 · ACH fee-calc RCA;Slack #snowglobe 2026-07-29 (ts 1785371583.033749);Confluence "CHECK_TRANSACTION_HAS_BRAINTREE_FEES"(3029344728)、UDF overload 合并 DTBTTFOUND-3246。

### 答案 B · 技术深度

我理解的 no-authority 影响力有两层:一层是「事故里的即时权威」,一层是「架构决策里的书面权威」。两层我都刻意在建。

即时权威那层就是 S3 这类:ACH fee 缺失事故,我把根因追到 `R__create-eventstream-to-pending-transactions-with-source-stored-procedure.sql` 里 `GET_EVENTSTREAM_PAYMENT_INSTRUMENT_SUB_KIND()` 的 1-arg vs 2-arg overload,起因是 change #2941;精确到 98.9% 是 us_bank_account、100% 归因 STANDARD_ACH、~1.05M rows。当你能把「谁、多少、为什么、哪一行代码」一次性讲清,没有人会去质疑你的方向,决策就落地了——这比开会拍板高效得多。事后我还主动把这个 UDF overload 做了 consolidation(DTBTTFOUND-3246),从根上消除这类歧义,而不是修完就走。

书面权威那层是我更看重的、可复制的杠杆。比如我发现自己早先建的 Quality-Check 框架有个设计缺陷——某个 subject area ~4% 校验失败就 block 全部 merchant 的 merge。我没有直接改代码「悄悄修」,而是写了一份正式 ADR(MADR 3.0.0 模板),里面带正确性证明、并显式列出并否掉 3 个备选方案,最后论证应该改成 merchant-level(复用 `QUALITY_CHECK_RESULTS_V1` + `HAS_MERCHANT_DETAIL` flag)。ADR 这个动作本身就是 no-authority 影响力的核心工具:它让决策可审查、可追溯,别人是被论证说服,不是被我这个人说服——这样落地的标准才稳。

一句话总结我的方法论:在自己拥有的领域(Snowglobe / fee-calc)里,把根因深度和书面论证做到别人默认 defer 给我,授权就不需要 title 来给。

> 证据锚点:S3(即时权威);S2 · ADR "[ADR Draft] Merchant-Level Quality Checks Using Dense Relational Rows"(2894288991, DTBTTFOUND-2749);snowglobe 全时段 #1 committer(615 commits)。

---

## Q10. 描述一次你 drive 的跨团队 / 跨职能项目——你怎么对齐各方?

### 答案 A · 影响导向

DoorDash 报了一起 Amex 出款延迟的正式事故(#_inc3743178)。事故指挥 Kiran Patil 点名我做三个 fix owner 之一。跨团队对齐里最关键的一刻是 SLA 争议:当 George 在 SLA 口径上不确定时,他直接 defer 给我,我给出权威答案——「T+7 是我们 US 内部管线的 SLA,但实际出款要等 Amex 把钱 settle 到我们账户才能放,这不是我们能压缩的环节」。这一句把所有人的预期从「BT 卡住了钱」重新对齐到「资金到账的物理约束」,把跨团队的指责转成了对同一事实的共识。对齐各方,我靠的不是协调会,是用领域权威给出一个大家都能接受的、基于事实的 single source of truth。

> 证据锚点:S9 · DoorDash Amex disbursement 事故;Slack #_inc3743178_doordash_us_amex_disbursement_delays 2026-07-06;事故指挥 Kiran Patil 指定 owner,George Fashho defer SLA。

### 答案 B · 技术深度

我讲一个更长周期、更结构化的跨职能例子:Net Settlement Pricing(EPP Phase 4 BT Fiserv Migration),它横跨 Funding、Pricing 两条职能线,是 $55B+ 增量 TPV(Google $40B / Microsoft $10B / Meta $5–7B)的前提,也要解决 $450M/月的 float 问题。我端到端拥有 Pricing 这一侧,持续 2 年+ 是唯一 owner。

跨团队对齐在这种项目里的难点不是「开会」,是「数据契约」和「信任」。核心的一次对齐:interchange fee 的取数源要从 Trans View 切到 Settle View,这直接影响 Funding 侧的出款金额。如果我只是发个「我要切了」的通知,没人敢让我切——因为切错就是真金白银的出款错误。所以我做的是:切换前用 day-level SQL 做完整 shadow 对账,拿出 >99.9% 字段一致 @ 13.7M 行(0.224% variance)的证据,再用 feature toggle `US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED` 灰度上线。对齐 Funding 靠的是「我先自证无回归」,而不是「请你相信我」。

更 senior 的一步是:我把这套跨团队切换的方法论沉淀成可复用的 "CDC Table Backfilling Template"——下一次别的团队要做类似的 SOR 切换,不用重新发明信任机制,直接套模板。跨职能对齐做到最后,不该是靠某个人反复救火,而是把「怎么安全地跨团队改数据源」变成团队的标准动作。

另外补充一个 cross-org 的支撑事实:我 mentee(Leo Huang)的 Funding→Pricing gRPC journaling-schedule sync,喂的正是我 Snowglobe 需要的 journaling 数据;我在这条链上定义 contract、在事故里是他依赖的 fee-calc 权威。这条跨团队数据链是我领域的一部分。

> 证据锚点:S5 · Net Settlement;epic 链 DTBTTFOUND-2071→2074→2232→2541→2879→3126(P1);PR snowglobe #1615;Confluence "Discovery on View Switch"(2698298357)、"CDC Table Backfilling Template"(2747848324)。

---

## Q11. 你如何为团队设定技术方向、标准或最佳实践?

### 答案 A · 影响导向

我设定标准的方式是「造平台,不是提规范」。团队原来每做一个 fee subject area 的 quality-check 都是一次性手写,重复、不一致、没人能保证覆盖度。我造了一个所有未来 quality-check 都复用的框架:集中式 config 表驱动 + 通用 procs 动态执行校验 + trigger-status handshake 告诉下游「这块数据已验证、可以读」。框架建好(#1997,1,489 行)之后,我自己在几乎每个 fee subject area 铺开了 ~8 次——不是发文档让别人遵守,是我先把标准跑通、跑遍,让「用这个框架」成为默认路径。最佳实践只有当它是最省事的那条路时,团队才会真的采纳。

> 证据锚点:S2 · Quality-Check & Handshake 框架;PR #1997(DTBTTFOUND-2664),铺开 #2061/#2069/#2075/#2091/#2106/#2558/#3040/#3237。

### 答案 B · 技术深度

我设定技术方向有三个层次,从重到轻。

第一层是框架化标准(Quality-Check & Handshake)。关键的设计判断是 handshake 那部分:数据管线里最容易被忽略的问题是「下游怎么知道上游这批数据校验过了、能安全读」。我用 trigger-status handshake 把「数据已验证」这个状态显式化,让下游依赖一个明确的信号而不是靠 timing 猜。这就把一个隐性约定变成了系统里的一等公民,别人接管时不会踩坑。

第二层是用 ADR 把重大决策变成团队资产。前面提到我发现原框架 subject-area-level block 的缺陷后,写了正式 ADR 改成 merchant-level(复用 `QUALITY_CHECK_RESULTS_V1` + `HAS_MERCHANT_DETAIL`)。我强调 ADR 的价值不在「记录我做了什么」,而在「用 MADR 模板逼自己列出被否的备选方案 + 正确性证明」——这套书写标准本身就在给团队示范「重大决策该怎么被论证、被 review」。

第三层是自发的开发者生产力基建。我自建了 snowglobe-tools(个人 repo,零 ticket 驱动),给 Snowglobe 做隔离的 Snowflake schema pool,让多个 Claude Code agent 会话能并行在不同分支跑而不撞 DDL/migration——我还为它写了 ADR、处理 Flyway 的边界问题(stream 失效顺序、重复 repeatable-migration 排除、prod-only 依赖的 stub 表)。这条不是任何人要求的,但它定义了「团队该怎么并行开发而不互相踩」的新范式。

我的核心信念:方向和标准不是靠 title 宣布的,是靠「我先把可复用的东西造出来、跑通、写清楚论证」,让团队自然收敛过来。

> 证据锚点:S2(框架 + ADR 2894288991);S7 · snowglobe-tools(SCHEMA_POOL_V2 重写 + ADR + Flyway 边界处理,纯自发)。

---

## Q12. 举一个你说服了团队 / 上级改变技术方案的例子。

### 答案 A · 影响导向

我早先建的 Quality-Check 框架上线后跑得挺好,但我自己发现它有个设计缺陷:某个 subject area 只要 ~4% 的校验失败,就会 block 掉该区所有 merchant 的 merge——一小撮坏数据拖死一大片好数据。这个方案是我自己定的,承认它有问题、并推动全团队改,需要先说服大家「值得动」。我写了一份正式 ADR,里面带正确性证明,并显式列出、逐一否掉了 3 个备选方案,最后论证应该改成 merchant-level 粒度(复用现成的 `QUALITY_CHECK_RESULTS_V1` + `HAS_MERCHANT_DETAIL` flag,不引入新表)。因为论证扎实、且复用现有结构、迁移成本可控,方案被采纳。说服团队最有力的一次,往往是说服他们改掉你自己的旧设计。

> 证据锚点:S2 · ADR "[ADR Draft] Merchant-Level Quality Checks Using Dense Relational Rows"(2894288991, DTBTTFOUND-2749);否掉 3 个备选方案。

### 答案 B · 技术深度

这个例子我想强调的是「怎么说服」而不只是「说服了什么」,因为要改的是我自己拍板的原设计,阻力和信任成本都更高。

背景:原 Quality-Check 框架的失败处理是 subject-area-level 的——某个 fee subject area 里 ~4% 的 row 校验失败,整个 subject area 的 merge 全部 block。这在数据量小的时候没暴露,但随着 merchant 规模上去,「4% 坏数据 block 掉另外 96% 好数据的 merge」成了明显的可用性问题。

我没有走「我觉得不对,我改了」的路子,因为那样别人无法评估我的判断对不对。我走的是 ADR:

一是选粒度。核心决策是把 block 粒度从 subject-area 下沉到 merchant——坏的 merchant 挡住,好的 merchant 照常流通。为了让这个选择可辩护,我在 ADR 里显式列了 3 个备选并逐一否掉(备选的具体形态见 ADR 原文),说明为什么 merchant-level 在正确性和成本上都占优。

二是复用而非新建。方案刻意复用已有的 `QUALITY_CHECK_RESULTS_V1` 和 `HAS_MERCHANT_DETAIL` flag(dense relational rows),不引入新表、不改上游契约——这大幅降低了「说服团队接受迁移」的门槛。一个改动如果既正确又便宜,反对的理由就很少。

三是正确性证明。ADR 用 MADR 3.0.0 模板,带正确性论证,让 reviewer 是被逻辑说服而不是被我说服。

我的体会:说服的本质是「把决策的完整推理外化,让对方能独立验证」。尤其当你要推翻的是自己之前的方案,越要靠透明的书面论证,而不是靠既有的信任余额去硬推。

> 证据锚点:S2 · ADR 2894288991(DTBTTFOUND-2749);原框架 PR #1997。

---

## 维度 5 · 处理模糊性与 Ownership(Ambiguity & Ownership)

## Q17. 描述一个需求模糊、信息不全的项目,你怎么把它推进到落地的?

### 答案 A · 影响导向

Net Settlement Pricing 就是典型的多季度模糊项目:目标很大(把 LE/MM 商户迁到 Fiserv 直连、出款从 gross 改成每日净结算,解锁 $55B+ 增量 TPV、解决 $450M/月 float),但一开始没有清晰的技术需求文档,只有一个方向。我端到端拥有 Pricing 这侧,持续 2 年+ 唯一 owner。推进模糊项目我的做法是「用可验证的小步骤代替等待清晰的需求」:每一块(plan-code/fee 映射、pass-through fee 计算、schedule 同步、审计、对 Fiserv 上报的 reconciliation)我都先做出一个能对账验证的最小版本,用数据证明它对,再往下走。项目就是这样从一句方向,推进成一条 P1 在跑的、真实解锁数十亿 TPV 的管线。

> 证据锚点:S5 · Net Settlement;epic 链 DTBTTFOUND-2071→...→3126(P1);parent solution PSCBU-1645。

### 答案 B · 技术深度

模糊项目的核心风险是:你不知道自己做的对不对,又不能停下来等需求变清晰。我在 Net Settlement 上的方法是把「模糊」转成「可对账的假设」。

最能说明问题的一段是 interchange 取数源切换。需求层面只有一个模糊的方向——「Settle View 要取代 Trans View 成为 SOR」。但没人能事先告诉我切完之后数字会不会一致、误差在哪、能不能接受。面对这种不确定,我不去等一个「确认无误」的批准,而是自己制造确定性:

一是先 discovery、后动手。我先做了正式的 discovery(Confluence "Discovery on View Switch")搞清两个 view 的语义差异,而不是假设它们等价。

二是 shadow-run 用数据消除模糊。切换前我用 day-level SQL 做完整 shadow 对账,结果是 >99.9% 字段一致 @ 13.7M 行、0.224% variance。这个数字把「切了会不会出事」这个模糊问题,变成了「0.224% 的差异分别来自哪、能不能解释」的具体问题。

三是灰度 + 可回退。用 feature toggle `US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED` 灰度上线,把风险切成小份。

四是沉淀成模板。做完我把它抽象成可复用的 "CDC Table Backfilling Template",让下一次的模糊切换有章可循。

补充一个更「烂摊子」型的模糊案例:我临时接管了一个实习生留下的 ML fee-anomaly detector,零生产验证(QA 建在 834M 行 / 6 个合成 merchant 上,而 prod 是 39B 行 / 18,140 merchant),状态、边界、能不能上 prod 全是问号。我做的第一件事不是接着写代码,而是先把模糊状态写清楚——写了一份 State/Handoff/Prod-Cutover 文档,量化 prod-scale 风险(per-row numpy serving @ 760M rows/day 大概率 OOM/timeout),用一份 go/no-go gate 把「模糊」收敛成「明确的决策点」。处理模糊性,先降低不确定性本身,比急着产出更重要。

> 证据锚点:S5(shadow-run 13.7M 行/0.224%,toggle,CDC template,Confluence 2698298357/2747848324);S6 · Fee Anomaly Detector(Confluence 3049697063,DTBTTFOUND-3254~3261)。

---

## Q18. 举一个你承担了端到端 owner 责任的经历(从设计到上线到 on-call)。

### 答案 A · 影响导向

AMEX GRRCN 管线是我从零搭到底、并持续防御 18 个月的端到端项目。我接手前任留的一个 stub,独立出了整套设计——`STAGE_AMEX_GRRCN_FILE` task + 6 条 append-only streams + 解析 Amex 定宽记录的 UDTFs + 7 张 staging/target 表 + 一个 feature-flag 急停开关,把原本在 Funding 里的 Ruby 脚本迁移到 Snowflake-native SQL,再做 EU 扩展。上线不是终点:这条管线至今处理了 21.96M 笔 Amex 交易、$138.6B volume,我持续 on-call、写 hardening PR、建监控。设计、上线、生产防御全在我一个人手上——这是我「端到端 ownership」最完整的证明。

> 证据锚点:S1 · AMEX GRRCN;PR snowglobe #751/#856/#862/#886(1,849 行)/#911/#1023 + ~10 hardening PR;epic DTBTTFOUND-2074;Confluence 2233926829。

### 答案 B · 技术深度

我把「端到端 owner」理解成三段责任,AMEX GRRCN 三段我都扛了,而且第三段(on-call/防御)才是真正体现 ownership 的地方。

设计段:GRRCN 是 Amex 专有的定宽文件格式(Global Reconciliation Report & Chargeback Notification),没有现成解析器。我设计的核心是把「文件 → 可对账的 fee」拆成清晰的 SQL-native 流水:`STAGE_AMEX_GRRCN_FILE` task 负责 ingestion/staging,6 条 append-only streams 保证增量、可重放、不丢数据,UDTFs 解析定宽记录,7 张 staging/target 表分层。关键的架构判断是把逻辑从 Funding 的 Ruby 脚本迁到 Snowflake-native——让计算贴着数据走,消除跨系统搬运的延迟和一致性风险。

上线段:PR #886 单个 1,849 行(我任期最大的 PR),之后做 EU 扩展。上线时我埋了一个 feature-flag 急停 `AGGREGATED_AMEX_SEPARATE_FLOW`——这是 owner 心态的体现:设计的时候就假设它会出问题,预留一个能立刻止血的开关,而不是出了事再想怎么关。

on-call / 防御段(18 个月):这是 ownership 的真正考验。这条线是我持续 on-call 的对象,我写了 ~10 个 hardening PR,还自建了 Streamlit 自助监控 app(`NON_AGG_AMEX_TASK_MONITOR`)做可观测性,并修过一次 31.0M 条 junk 误报的根因(Pinless False-Positive Alarms)来降 on-call 噪音。端到端 owner 不是「上线就交付完成」,是「这条线活多久,我就为它的健康负责多久」。

> 证据锚点:S1(#886 1,849 行,feature-flag `AGGREGATED_AMEX_SEPARATE_FLOW`,21.96M/$138.6B);补充工件 "HC Task Failure — Streamlit App"(2989107333)、"Pinless False-Positive Alarms"(3008530291)。

---

## Q19. 讲一次失败 / 受挫的经历,你从中学到了什么?(成长型思维)

### 答案 A · 影响导向

我最有代表性的一次「失败」是我自己搞砸又自己救回来的:我建的 Quality-Check 框架上线后,我发现它有个我当初没考虑到的设计缺陷——某个 subject area 只要 ~4% 校验失败,就会 block 掉该区所有 merchant 的 merge,一小撮坏数据拖死一大片好数据。这是我拍板的原设计,承认它有问题不舒服。但我没有打补丁遮掩,而是把它当成一次架构级返工:写正式 ADR,列出并否掉 3 个备选,重构成 merchant-level 粒度。我学到的是——你自己造的、被广泛复用的东西,发现缺陷时最该做的不是最小修补,是有勇气推翻重来并把论证写清楚,让团队跟你一起把标准提上去。

> 证据锚点:S2 · ADR 2894288991(DTBTTFOUND-2749);原框架 #1997。

### 答案 B · 技术深度

我讲这个失败是因为它的「失败点」很微妙,是一个只有到规模上去才暴露的设计判断错误,而且犯错的人是当时的我。

失败经过:我设计 Quality-Check 框架时,失败处理选了 subject-area-level 的 block——某个 fee subject area 里有校验失败,就 block 整个 area 的 merge。当初的逻辑是「宁可全挡住,也别放脏数据下游」,在数据量小、merchant 少的时候这个粗粒度没问题。但随着 merchant 规模增长,现实变成了「~4% 的坏 row 挡住了另外 ~96% 好 merchant 的正常流通」——我用一个保守的默认值,牺牲了系统的可用性,而我一开始没预见到这个 trade-off 会随规模反转。

我学到的三件事:

一是「粒度是要随规模重新审视的设计参数」。当初 subject-area 粒度不是错,是它对应的规模假设过期了。Senior 的判断力体现在:不仅要为当下选对,还要预判哪些设计选择会随规模失效。

二是「修自己的缺陷要走和修别人 bug 一样正式的流程,甚至更正式」。我完全可以偷偷把粒度改掉。但我选择写完整 ADR(MADR 3.0.0,正确性证明 + 3 个被否方案),把它重构成 merchant-level(复用 `QUALITY_CHECK_RESULTS_V1` + `HAS_MERCHANT_DETAIL`,不新增表)。因为这个框架被 ~8 个 subject area 复用,它的缺陷是团队级的,修复也必须是团队可审查的。

三是「主动暴露自己的错误反而是建立信任的机会」。这个缺陷是我自己发现、自己升级、自己重构的,没等它变成事故。事后团队对我在这个框架上的判断反而更信任了——因为他们看到我会 own 到底,包括 own 自己的错。

> 证据锚点:S2 · ADR 2894288991;框架复用 ~8 次(#2061/#2069/#2075/#2091/#2106/#2558/#3040/#3237)。

---

## Q20. 你如何在多个高优先级任务间做取舍?

### 答案 A · 影响导向

最能代表我取舍判断的一次:我临时接管一个实习生留下的 ML fee-anomaly detector。惯性做法是顺着他的方向继续投入、把它推上生产——毕竟已经做了不少。但我判断这是错的优先级。它零生产验证(QA 建在 834M 行 / 6 个合成 merchant,prod 却是 39B 行 / 18,140 merchant),盲目上线的期望收益远低于风险。所以我做的取舍是「先停下来立一个 go/no-go ROI gate」:量化 prod-scale 风险(per-row numpy serving @ 760M rows/day 大概率 OOM/timeout),给分阶段 cutover 方案,并明确划线——Phase1/2/CI-CD/Slack 集成在这个 gate 说 go 之前一律不许动。取舍的本质不是「先做哪个」,是「有勇气对一个看起来该继续的任务喊停」。

> 证据锚点:S6 · Fee Anomaly Detector ROI gate;Jira DTBTTFOUND-3254~3261;Confluence "Fee Anomaly Detector — State, Handoff and Prod-Cutover Plan"(3049697063)。

### 答案 B · 技术深度

我做取舍有一条明确的原则:按「风险调整后的期望价值」排,而不是按「已经投入了多少 / 谁在催」排。Fee Anomaly Detector 这个 case 把这条原则体现得最完整。

情境:一个实习生(2026-08-14 offboard)留下一个 ML fee-anomaly detector,状态是「看起来快能上了」。同时我手上还压着 Net Settlement(P1)、AMEX 管线的持续 on-call。表面上,把这个 detector 收个尾推上 prod 是个「快赢」,催我继续的惯性也存在。

我的取舍分析:

一是拆穿「沉没成本陷阱」。实习生已经投入很多,但那不是继续的理由。真正要算的是「从现在起,继续投入的边际风险和收益」。

二是量化 prod-scale 风险,而不是凭感觉。QA 环境是 834M 行 / 6 个合成 merchant,prod 是 39B 行 / 18,140 个真实 merchant——差了两个数量级且数据分布完全不同。更致命的是架构:per-row numpy serving 在 760M rows/day 的规模下大概率 OOM 或 timeout。也就是说「快赢」其实是「大概率在 prod 炸掉、然后占用我更多时间救火」的负期望值任务。

三是把判断制度化成 gate,而不是自己拍脑袋停。我写了一份 State/Handoff/Prod-Cutover 文档,立一个显式的 go/no-go ROI gate,给分阶段 cutover 方案,并明确划出「不许动」的边界:Phase1/2、CI-CD、Slack 集成在 gate 通过前全部冻结。这样做的好处是:取舍的理由是公开、可审查的,别人(包括我的上级)能独立判断我停得对不对,而不是「Chi 觉得不值得做就不做了」。

于是我的时间就腾给了真正的 P1(Net Settlement)。我认为这正是 senior 该有的取舍能力:不是把所有高优先级都塞进日程,而是有能力、也有胆量,把一个看起来该继续的任务判定为「先冻结」,并用数据和文档为这个判断负责。

> 证据锚点:S6(QA 834M 行/6 合成 merchant vs prod 39B 行/18,140 merchant;per-row numpy @ 760M rows/day OOM/timeout;分阶段 gate);对照 P1 = S5 Net Settlement(DTBTTFOUND-3126)。
