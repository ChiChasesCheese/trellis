# 维度 4 · 带教与协作（Mentorship & Collaboration）

> ⚠️ **诚实说明（面试前 Chi 务必读）**
>
> 这一维度的诚实风险最高，尤其是 Q13（mentor Ziyang / Leo Huang）。请守住三条线：
>
> 1. **没有可举证的 code-review 痕迹**。GitHub / Jira / 公开 Slack 里**找不到**你直接 review、评论、co-author Ziyang PR 的记录。所以这里所有答案都**不讲"我 review 了他哪个 PR / 我在 PR 里写了什么评论 / 某次 1:1 我说了什么"**。一旦面试官追问"能举一条具体 review 评论吗？"而你答不出、或对方事后能查 PR 记录，整个故事崩盘，比不讲带教更糟。
> 2. **可辩护的框定 = domain-ownership / architectural collaboration，不是 code-review trail**。真实且可举证的事实是:你拥有 Snowglobe + fee-calc 的领域与标准;Ziyang 的每一块工作(`SnowglobeExclusionService` 防重复计费、Funding→Pricing gRPC journaling sync 喂 Snowglobe、Scheme Fee ML)都**接入或依赖你的领域**;你定 contract、当 fee-calc 权威、把关架构方向。旁证:Hari Devulapally 在 Slack 说过 "Leo Huang worked on excluding fee calculations for Snowglobe journaled merchants"——即他的活儿是围绕你的 Snowglobe 展开的。这条线你可以放心讲。
> 3. **占位符必须你亲自填真实内容**,别让我替你编。凡是标 `【待 Chi 补充：…】` 的地方(具体 1:1 频率、pairing 场景、口头 unblock 的一次对话),都是真实带教细节——你有就填、没有就删,**不要保留成编造**。数字占位 `【预估：…】` 同理,换成真实值。

---

## Q13. 讲讲你 mentor Ziyang（Leo Huang）的经历——你怎么带他?他因此产出了什么?

> 【核心题。以下两答案是一体两面:A 讲"他在我的领域指导下产出了什么"(影响 + 我的杠杆),B 讲"我具体怎么带"(方法论 + 占位真实细节)。面试时先给 A,被追问 how 再展开 B。**两个答案都不碰 review 痕迹**,只讲 domain ownership / contract / 架构把关。】

### 答案 A · 影响导向(我的领域杠杆放大了他的产出)

Ziyang 是我们团队的 junior,他这一年三块主要工作,**全部落在我拥有的 Snowglobe / fee-calc 领域边界内或依赖它**——我做的是"把我的领域知识和 contract 变成他能安全落地的地基",让他产出远超一个 junior 独立能做的东西。

三块产出:

1. **`SnowglobeExclusionService`——防止对已迁移商户重复计费**。当商户迁到我拥有的 Snowglobe 做清结算后,Pricing 侧不能再对同一笔交易计费,否则重复收费。Ziyang 建了这个 exclusion service(pricing #3054/#3108/#3129/#3159)。这里的关键是"哪些 merchant 算已迁移、以什么 journaling 状态为准"——这个判定标准是我的领域定义的,我给他定了 contract,他照着落地。这是一个直接防生产事故(重复计费=真金白银的客诉)的服务。

2. **Funding→Pricing gRPC journaling-schedule sync**(funding #13724/#13790/#13881/#13992/#14206/#14302/#14386,epic DTBTPRWIZ)。这套 sync 加回填、加 bulk update/delete API,**喂的正是我的 Snowglobe 所需要的 journaling 数据**。数据 schema 和一致性要求由我这边定义,他实现跨系统的同步管道。

3. **Scheme Fee estimation ML**(DTBTPBIL-713,scheme-fee-estimate repo):XGBoost + Snowflake 分布式训练,accuracy 从 V0 的 **90.57% 迭代到 V9 的 98.57%**,prod 验证 95%+。Scheme fee 估算落在我拥有的 fee/pricing 领域内,我是他在 fee 口径、正确性判定上的对接权威。

**我的杠杆点**:这三块任何一块单独交给 junior 都容易翻车(重复计费、跨系统数据不一致、fee 口径错),因为它们都咬在我领域的正确性红线上。我做的不是替他写代码,而是**把领域边界、contract、正确性标准前置定义清楚**,让他在正确的框架内高速落地。旁证是 Hari Devulapally 在 Slack 直接说 "Leo Huang worked on excluding fee calculations for Snowglobe journaled merchants"——他的工作被组织认知为"围绕 Chi 的 Snowglobe 展开"。

### 答案 B · 带教方法论(我具体怎么带)

被追问"你具体怎么带他"时展开。我的带教不是盯代码行,而是**在他依赖我领域的每个接触点上,把我变成他的地基和 unblocker**。四个抓手:

**1. 定 contract、划领域边界(带教的地基)。** Ziyang 的每块活儿都要接入我的 Snowglobe / fee-calc。带他的第一件事不是让他先写代码,而是先和他对齐"边界在哪":对 exclusion service,是"哪些 merchant 在什么 journaling 状态下算已迁移、Pricing 该停止计费";对 gRPC sync,是"Snowglobe 侧需要什么 schema、一致性要求是什么"。我把这些领域定义讲清、变成他能 code against 的 contract,他就不会在错误的假设上盖楼。这是 junior 最容易踩的坑——不理解上游领域就硬做,我用领域知识前置消除它。

**2. 领域知识传授。** 我们团队 fee-calc 的品类映射、Snowglobe 的清结算模型、journaling 语义,这些没有文档能完全替代口头带。我把这套心智模型传给他,让他做 scheme fee ML / exclusion 时知道 fee 口径到底该怎么算、边界 case 在哪。`【待 Chi 补充：具体 1:1 / pairing 细节——比如多久一次 1:1、有没有一起 pair 过某块 fee 逻辑、在哪个场景口头给他讲过 journaling 模型】`

**3. 架构把关(gatekeeping direction, not diffing lines)。** 当他的方案要接入我的领域时,我把关的是**架构方向**——contract 对不对、数据一致性靠不靠得住、fee 正确性有没有保证——而不是逐行 diff。`【待 Chi 补充：具体某次你在方向上纠正/确认他的一次真实对话或讨论,例如某个设计评审里你对 exclusion 判定标准提的意见】`

**4. 在他依赖我领域时 unblock。** 他的三块活都咬在我的领域上,意味着他被卡住时第一个找的就是我——fee 口径存疑、journaling 状态不确定、Snowglobe 侧接口不清。我是他这条路上的 go-to unblocker。`【待 Chi 补充:一次具体的 unblock——他卡在哪、你怎么当场解开的(DM / 口头 / 一次 debug)】`

**为什么这是 Senior 该做的事**:junior 带 junior 是替他写代码;Senior 带 junior 是**用自己的领域 ownership 当放大器**——我不必碰他的键盘,但因为我拥有他所有工作都要接入的领域,我定义的 contract、传授的领域知识、把关的方向,决定了他能不能安全、快速地产出。他这一年的 exclusion service、gRPC sync、90.57%→98.57% 的 ML,都是在我这块地基上盖起来的。

> 证据锚点:Ziyang 真实产出——`SnowglobeExclusionService`(pricing #3054/#3108/#3129/#3159,DTBTPRWIZ-730/714)、Funding→Pricing gRPC sync(funding #13724/#13790/#13881/#13992/#14206/#14302/#14386,epic DTBTPRWIZ)、Scheme Fee ML 90.57%→98.57%(DTBTPBIL-713,scheme-fee-estimate)。领域旁证:Hari Devulapally Slack "Leo Huang worked on excluding fee calculations for Snowglobe journaled merchants";Chi 是 #lep-mentees / #lep-all 成员。**⚠️ 全程无 code-review 痕迹可引用,勿编造。**

---

## Q14. 描述一次你和同事 / 其他团队的技术意见冲突,你怎么解决的?

### 答案 A · 影响导向(S4 AU Amex,用领域证据终结分歧)

情境:PM Liz Lippow 走正式 "Request Help" 表单报了个问题——AU(澳洲)商户的 Amex refund fee 疑似出错,Tejesh 点名把问题路由给我。那条 thread 拉了 50 多条回复,一开始各方对"到底是数据问题、配置问题还是计算逻辑问题"意见不一。

我没有陷进"我觉得 / 你觉得"的口水,而是**直接用数据把分歧收敛掉**:我拉出 USA 1,079,627 行 vs AUS 0 行的对比,再往上游追,定位到根因是**所有 AU merchant 的 `fee_refund_policy` 都是 `'partial'`、从来不是 `'full'`**,导致 non-agg Amex refund fee 在 AU 根本不生成,跨 157 个 merchant。根因一出,分歧当场结束——不是我说服了谁,是数据说服了所有人。这催生了 DTBTTFOUND-3269。

我解决技术冲突的方式:**争议归争议,但谁能拿出可复现的根因和数字,谁就赢**。我拥有这块 fee-calc 领域,所以我总能第一个把讨论从主观意见拉回到可验证的事实。

### 答案 B · 技术深度(S9 DoorDash,冲突在于"SLA 谁说了算")

`【也可用 S9,当面试官想听"跨团队 + 你是被 defer 的权威"那种冲突。】`

情境:DoorDash 报 Amex 出款延迟,开了正式事故频道。冲突点是团队之间对"这个延迟到底违不违反 SLA、该谁负责"有分歧——George Fashho 和其他人在 SLA 口径上说法不一。

事故指挥 Kiran Patil 点名我为三个 fix owner 之一,而在 SLA 这个争议点上,**George 直接 defer 给我**。我给的是权威判定:**"T+7 是我们 US 内部管线的 SLA,但真正的约束是我们必须等 Amex 把钱 settle 到我们账户之后才能出款——所以这不是我们管线违约,是上游资金到账时点决定的。"** 这个回答把"是不是我们的锅"这个争议一锤定音。

我处理这类冲突的原则:**当冲突源于领域知识不对称时,解决冲突 = 由领域权威给出可辩护的事实判定**,而不是各退一步和稀泥。因为我拥有这块结算 / fee 领域,团队在有分歧时把我当作最终裁判——这本身就是 Senior 的信号。踩过的坑教会我一件事:事故里最贵的不是 bug,是各方对"边界在哪"的误解;所以我总是先把边界(内部 SLA vs 上游资金到账)讲清,冲突自然消解。

> 证据锚点:S4——Slack #service-pricing 2026-08-03(ts 1785766795.306709),USA 1,079,627 vs AUS 0 跨 157 merchants,`fee_refund_policy='partial'`,DTBTTFOUND-3269,PM Liz Lippow 正式 Request Help + Tejesh 点名路由。S9——Slack #_inc3743178_doordash_us_amex_disbursement_delays 2026-07-06,Kiran Patil 指定 fix owner,George Fashho SLA 上 defer。

---

## Q15. 你平时如何 unblock 别人 / 成为团队的 go-to person?

### 答案 A · 影响导向(go-to 是既成事实 + 三个快速 unblock)

我在 **86 个 Slack 频道**里,被全团队按名 ping 做 go-to person——这不是我自封的,是团队用行为投票出来的。三个典型:

1. **ACH fee-calc 生产事故(S3)**:一条 `CHECK_TRANSACTION_HAS_BRAINTREE_FEES` PagerDuty,我自己转发并**当场给出完整根因**——Standard ACH promote 进 `TRANSACTIONS` 时 `payment_instrument_sub_kind = NULL`,导致品类映射 `'BT_' || NULL = NULL`、不生成 fee。精确到 UDF 的 1-arg vs 2-arg overload。影响 ~196 merchants、~$11.3M/day GMV。Sahar 和 Dylan 公开致谢。

2. **AU Amex 跨团队问题(S4)**:PM 走正式表单、Tejesh 点名路由给我,50 条 thread 我给出根因(见 Q14)。

3. **Terraform grant-ownership(S8)**:release 被 `GRANT OWNERSHIP` 拒卡住,我 **~7 分钟**定位根因(`FEE_ANOMALIES_REVIEWER` 已持依赖的 USAGE grant,是全 repo 唯一缺 `outbound_privileges` 的资源),出 PR #1326,release 成功部署。

我成为 go-to 的机制:**我拥有 Snowglobe + fee-calc 这块几乎所有下游都要碰的核心领域,而且我解题速度足够快(7 分钟量级)、根因足够硬(精确到 SQL 工件 / overload)**,所以别人卡住时的最优选择就是先找我。

### 答案 B · 技术深度(unblock 的方法论:根因优先、当场闭环、持续 owning)

被追问"你为什么能当场 unblock 而不是踢皮球"时展开。我的 unblock 有三个特征:

**1. 根因优先,不给"可能的原因列表"。** S3 那次我没有说"可能是数据问题也可能是配置问题",而是直接定位到 `GET_EVENTSTREAM_PAYMENT_INSTRUMENT_SUB_KIND()` 的 overload、起因 change #2941。别人来找我,拿到的是可执行的答案,不是待办清单。这是 unblock 和"表示关心"的区别。

**2. 当场闭环 + 持续 owning。** S3 我不是给完根因就走,而是持续 owning 数周,直到 UDF overload 合并收口(DTBTTFOUND-3246)。S8 我不是只说"哦是 grant 问题",而是当场出 PR、跟到 release 部署成功。unblock 别人的信誉是靠"我接手的事一定收口"攒出来的。

**3. 领域 ownership 是速度的来源。** 我能 7 分钟定位 Terraform 那个问题,是因为我对整个 repo 的 grant 结构有全局图景——我知道哪些资源缺 `outbound_privileges`。速度不是天赋,是领域深度的副产品。这也解释了为什么 Ziyang 这样的 junior 卡在我领域相关的活儿上时,第一个找的是我(见 Q13)。`【待 Chi 补充:一次日常(非事故)的口头 / DM unblock 例子,让 go-to 形象更立体】`

> 证据锚点:86 个 Slack 频道被按名 ping;S3——Slack #snowglobe 2026-07-29(ts 1785371583.033749),DTBTTFOUND-3246,Sahar/Dylan 公开致谢;S8——Slack #treasury-services-releases 2026-08-13(parent ts 1786640974.325349),PR snowglobe #1326;S4——见 Q14。

---

## Q16. 你如何做 code review / 传递工程标准?

> ⚠️ **诚实框定**:不要讲"我 review 谁的哪个 PR"这种没证据的话。真实且可举证的是——**你通过"框架 / 标准 / ADR / onboarding doc"这些工件传递工程规范**,让标准可复用、可执行,而不是靠一次次口头 review。这比讲某次 review 更 Senior。

### 答案 A · 影响导向(用框架和标准传递规范,而非逐个 review)

我传递工程标准的方式,是**把标准做成可复用的工件,让它自动传播,而不是靠我一个个去 review**——这是 Senior 和高级工程师的区别。

最强的例子是 **Quality-Check & Handshake 框架(S2)**:我造了一个所有未来 quality-check 都复用的框架(PR #1997,1,489 行)——集中式 config 表驱动、通用 procs 动态执行校验、trigger-status handshake 告诉下游"这块数据已验证可读"。然后我自己在几乎每个 fee subject area 铺开了 ~8 次。这意味着**任何人往后做 quality check,都必须沿着我定义的标准来**——标准写进了框架,不靠人肉 review 把关。

更进一步,当我发现原框架有设计缺陷("某 subject area ~4% 失败就 block 全部 merchant"),我没有临时打补丁,而是写了一份正式 **ADR**(MADR 3.0.0 模板,含正确性证明 + 3 个被否方案),把设计改成 merchant-level。ADR 本身就是最高级的"传递工程标准"——它让团队看到一个决策该怎么权衡、为什么否掉备选。

### 答案 B · 技术深度(标准传递的三层:framework / ADR / onboarding doc)

被追问方法论时展开。我传递工程标准分三层,越往上越 Senior:

**1. Framework 层——把标准编码成代码。** Quality-Check 框架(S2)是典型:与其在每次 review 里提醒"你要加数据校验",不如做一个 config 表驱动的通用框架,让"加校验"变成填一行 config。标准一旦进了框架,就不依赖任何人记得去 review。我铺开 ~8 次,等于把这个标准强制传播到每个 fee subject area。

**2. ADR 层——把决策方法论沉淀下来。** 我那份 merchant-level quality check 的 ADR(2894288991,DTBTTFOUND-2749)不只是记录"改成了什么",而是**展示了怎么做技术决策**:先证明原设计的正确性缺陷,再列 3 个备选方案并逐一说明为什么否掉,最后给出正确性证明。团队读这份 ADR,学到的是"架构决策该有的严谨度"——这比 review 一个 PR 传递的标准高一个量级。

**3. Onboarding doc 层——把领域知识做成新人地基。** 我维护团队的 onboarding doc(Confluence 885424440,2024-06 建、2026-08 仍在编辑)。新人(包括我带的 junior)从这里获得进入 Snowglobe / fee-calc 领域的第一层标准和心智模型。这和 Q13 里我带 Ziyang 是同一套逻辑:**我传递标准的主渠道是"可复用的工件",不是一次性的口头 review。**

关于 code review 本身:`【待 Chi 补充:你日常 review 时的真实原则——比如你 review 时最看重什么(正确性 / 领域边界 / 一致性)、有没有一次你在 review 里拦下过一个会出事的改动。有真实例子就填,没有就只讲上面三层工件,别编。】`

**为什么这是 Senior 信号**:junior 传递标准靠 review 一个个抓;Senior 传递标准靠**做框架、写 ADR、维护 onboarding doc**——让标准脱离个人、可复用、可执行。我这三层都在做,而且都有工件可举证。

> 证据锚点:S2——PR snowglobe #1997(DTBTTFOUND-2664)+ 铺开 #2061/#2069/#2075/#2091/#2106/#2558/#3040/#3237;ADR "[ADR Draft] Merchant-Level Quality Checks Using Dense Relational Rows"(Confluence 2894288991,DTBTTFOUND-2749,MADR 3.0.0,否掉 3 个备选);onboarding doc(Confluence 885424440,2024-06 建、2026-08 仍在编辑)。**⚠️ 不引用任何具体 review PR / 评论记录。**
