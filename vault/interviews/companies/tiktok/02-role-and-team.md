# 02 · 岗位与团队：职位说明逐条拆开

这个岗位在 ByteDance Global Payment 的 Financial Product and Solution（FPS）组，给海外市场做消费金融产品：先买后付（BNPL）、消费信贷、保险、钱包。职位说明里的每一句，背后都是一类具体的工作；面试官会从你的简历里找能回答这句话的证据。这一页先把职位说明逐条拆成「实际在做什么、你哪段经历能回答、没有就学什么」，再用短段落讲五个消费金融的话题，最后说你最可能拿到的级别。你的 PayPal 经历在商户侧（费用、结算、对账）是直接对口的；消费者侧（贷款、计息、授信）要靠这一页和链接的材料补上。

## 1. 职位说明逐条对照

评级：**强** = 有直接证据，能讲 3 分钟 · **部分** = 有相邻经验，缺一层 · **缺口** = 没有证据，诚实说并补课。

### 1.1 职责

| 职位说明 | 实际在做什么 | 你的证据 | 评级 | 没有就学什么 |
|---|---|---|---|---|
| Build overseas consumer financial products | 给东南亚、拉美的 PayLater、信贷、保险、钱包写后端：账户、分期计划、还款、计息、和资金方对接 | 费用计算是「按规则给每笔交易算钱」，和计息、生成还款计划是同一类问题；[[S1 Amex 结算管线\|S1]] 的「先挂起、验真后转正」和授信冻结同构 | 部分 | 第 2 节的五个话题 |
| Architect complex payment systems, considering total cost | 设计时同时算三种成本：机器、渠道手续费、资金占用（垫资） | [[S5 Interchange 数据源切换\|S5]]：净额结算把出款提前到 T+1，释放约 $450M / 月的垫资；[[S6 Anomaly detector go-no-go\|S6]]：单行成本 × 峰值行数，先算再做 | 强 | 渠道路由的成本与授权率：[[sd12-payment-routing]] |
| Solve bottlenecks for experience, performance, stability | 批处理赶不上截止时间、热点账户、慢查询、高峰期降级 | S5：费用数据赶不上出款截止，换到更早到达的数据源；S6：逐行推理在生产规模必然超时 | 部分 | 热点账户：[[sd09-wallet-ledger]]；限流降级：[[tiktok-service-protection]] |
| Design reviews and quality control | 评审别人的设计，定测试和质量闸门 | [[S2 Quality-check 框架\|S2]]：配置驱动的质量检查；[[S3 ACH 费用 NULL 传播事故\|S3]]：复盘写清端到端测试为什么没抓到 | 强 | — |

### 1.2 最低要求

| 职位说明 | 实际在做什么 | 你的证据 | 评级 | 没有就学什么 |
|---|---|---|---|---|
| Highly available distributed systems with **financial security** | 高可用加资金安全：幂等、守恒、对账、审计、权限 | S1：坏数据永不丢，进错误表；复合键 MERGE 保证重跑不重复 | 强 | [[sd01-payment-system]]；`支付系统核心` 的正确性工程分支 |
| Code review | 评审别人的代码，也被评审 | 把 Ruby / Kotlin 逻辑迁到 Java，用 AI 辅助评审和生成测试，靠行为一致性测试保证不回归 | 强 | — |
| Java / Python / Go / C++ / PHP | 日常是 Go，面试任何语言都行 | Java、Python、SQL | 强 | Go 只需读得懂：goroutine、channel、error 返回值 |
| In-depth understanding of distributed, cache, message, search mechanisms | 后端基础（八股）：MySQL、Redis、Kafka、搜索引擎的机制 | 实习用过 Kafka（[[S11 实习期事件流\|S11]]）；Snowflake 的存储与 Stream 原理 | 部分 | [[tiktok-fundamentals]]；搜索（倒排索引）是缺口 |
| Online troubleshooting（线上问题定位） | 值班时几分钟内定位一个线上问题：切片、对照组、找到那一行 | S3：告警到根因几分钟；[[S9 Amex 出款延迟事故\|S9]]：事故里给出 SLA 定论；[[S8 Terraform 7 分钟 RCA\|S8]] | 强 | Linux 层：[[tiktok-linux-troubleshooting]] |
| Cross-team coordination | 推动别的团队配合你的项目 | [[S4 AU Amex 退款费\|S4]]：三个团队 50 条回复，用一条可复跑的查询结束；S9：多 owner 事故 | 强 | — |

### 1.3 优先条件

| 职位说明 | 你的证据 | 评级 | 怎么说 |
|---|---|---|---|
| Minimum 4 years at a large internet company | PayPal 全职约两年，加一段实习 | 缺口 | 不辩解年限，讲范围：「I owned one money pipeline end to end, from file ingestion to fee calculation, plus its on-call.」 |
| Fintech or online payment experience | Braintree 的结算与费用管线 | 强 | 这是你最大的优势，每一轮都主动接上 |
| International team experience | S9：为 EU 合规改的逻辑影响了美国出款，主张按区域分开；S4：澳洲商户 | 部分 | 【待补：和其他时区团队协作的真实例子】 |
| AI in risk control and credit decisioning | 用 AI 工具做代码评审、生成测试、重构 | 部分 | 一句话说清：AI 帮你写和审，但钱的路径上每一条规则都要有确定性的测试和人能读懂的审计 |

### 1.4 一句话画像

你的强项是「**钱的正确性**：费用怎么算、结算怎么不丢不重、对不上时怎么在几分钟内找到那一行」。弱项是「**消费者侧的金融产品**（贷款、计息、授信）」和「**单机与搜索的底层机制**」。面试策略：每个问题先接回你的强项，再用第 2 节的推理补上消费金融的一层，承认没做过，但讲得出机制。

---

## 2. 要准备的五个消费金融话题

支付的基础（钱怎么流、复式账本、幂等键、对账、退款与拒付）在 [[05-payment-domain]]；这一节只讲消费金融这一层，以及跨区域容灾。

### 2.1 贷款与分期的生命周期

一笔先买后付的生命周期是一台状态机：申请 → 授信决策 → 批准并给出额度（credit limit）→ 下单时用信（drawdown，也叫放款）→ 生成还款计划（repayment schedule）→ 按期自动扣款 → 结清；没按时还进入逾期（overdue），经过宽限期（grace period）后收滞纳金、催收，长期收不回就核销（write-off）。每一次状态变化都是账本上的分录，而不是改一个字段：放款时借记「应收本金」、贷记「应付商户」；还款时借记「现金」、贷记「应收本金」和「应收利息」。

难点在边界：一次还款不够还清一期，要按固定顺序冲抵（先费用、再利息、最后本金）；用户提前还款，要重算剩余计划；用户退货，退款先冲减未还的本金，再决定退回已付的部分。资金来源有两种：平台自己放贷（自营），或合作方出资、平台只做技术和导流；后者每天要和资金方对账。

链接：[[domains/payments/map/correctness.state-machines|支付状态机]] · [[domains/payments/map/ledger.double-entry|复式记账]] · [[domains/payments/map/platform.subscriptions|订阅与周期计费]]（按期扣款和失败重试同一套机制）· [[sd09-wallet-ledger]]

### 2.2 利息与费用的计提

计提（accrual）是指：利息每天都在产生，即使用户还没付，账上也要每天记一笔「应收利息」。日利息 = 本金 × 年利率 ÷ 365（这个 365 是计息惯例，day-count convention，有的产品用 360）。舍入的位置决定账对不对得上：本金 $1,200、年利率 12%，日利息是 $0.394520…；每天先舍入到分再累加，30 天是 $11.70；用更细的单位累计、月底只舍入一次，是 $11.84。差的 $0.14 乘上几百万笔贷款，就是对账差错。规则：内部用整数的更小单位累计，记账时只舍入一次，余数结转到下一期。

还款计划有几种：等额本息（每期金额相同，前期利息多）、等额本金（每期本金相同）、BNPL 常见的免息分期（比如分 4 期，用户不付利息，平台向商户收费）。等额本息的例子：本金 $1,200、月利率 1%、12 期，每期 $106.62；因为每期都舍入，最后一期是 $106.60，由最后一期吸收舍入差。计提任务按（贷款，日期）做幂等键，重跑同一天不会记两次。你在 PayPal 写的费用公式（金额 = 费率 × 数量 + 固定费）和这里是同一种计算，面试里可以直接接上。

链接：[[domains/payments/map/correctness.money-representation|金额怎么表示]] · [[domains/payments/map/ledger.accounts-postings|账户、凭证与分录]] · [[domains/payments/map/card-lifecycle.fees|交换费、卡组织费与商户定价]]

### 2.3 授信决策

用户在结账页点「分期付款」，系统要在几百毫秒内决定批不批、给多少额度。决策引擎读 KYC 状态、征信或替代数据、风控模型分数和规则，输出批准、拒绝或转人工。三件事最容易被追问：

- **超时怎么办**：决策服务超时，结果只能是「不批」或「换别的支付方式」，绝不能默认批准。钱放出去收不回，比少做一单贵得多。
- **可解释和可审计**：每次决策都记下模型版本、输入特征、命中的规则和分数。监管要求能说出拒绝的理由，出问题时也要能回放当时为什么批了。
- **额度的并发**：同一个用户同时下两单，都要占用同一个额度。做法和库存扣减、余额冻结一样：带条件的更新（剩余额度 ≥ 本次金额才扣），先冻结（hold），下单成功再确认，失败或超时释放。

把 AI 用进授信时，模型放在规则后面、给出分数，硬性规则（年龄、制裁名单、额度上限）仍由确定性的代码执行，并持续监控模型的分数漂移。

链接：[[domains/payments/map/ledger.balances-holds|余额、可用余额与冻结]] · [[domains/payments/map/risk-compliance.fraud|交易欺诈与风控]] · [[domains/payments/map/risk-compliance.aml-kyc|反洗钱、KYC 与制裁筛查]] · [[domains/payments/map/correctness.unknown-outcomes|超时与未知结果]]

### 2.4 多币种与换汇舍入

每种货币的最小单位不同：美元和欧元是 2 位小数，日元是 0 位，科威特第纳尔是 3 位。所以金额一律存「整数的最小单位 + 币种代码」，不用浮点数。换汇只做一次：先锁定一个报价（汇率、报价编号、有效期），用这个报价把两边金额都算出来并记账；换汇在账本里是两条腿，经过一个换汇清算账户，每个币种各自借贷平衡。舍入方式（四舍五入还是银行家舍入）写死在规则里并全局一致，舍入产生的余数记进一个专门的舍入差额账户，账本才能平。

拆分金额时要保证各部分加起来等于总数：$100.00 分三期是 $33.33、$33.33、$33.34，余下的一分钱按固定规则给某一期。面试里被问「汇率换算」的编码题，也会追问精度和舍入。

链接：[[domains/payments/map/ledger.multi-currency-ledger|多币种账务]] · [[domains/payments/map/cross-border.fx-rates|汇率来源与报价锁定]] · [[domains/payments/map/cross-border.multi-currency-pricing|多币种定价与结算币种]] · [[domains/payments/map/cross-border.fx-risk|汇率风险与对冲]] · 编码：[[tlc-tt-currency-conversion-queries-0-whole|汇率换算查询]]

### 2.5 跨区域容灾

先定义两个数字：RPO（恢复点目标，最多丢多少数据）和 RTO（恢复时间目标，多久恢复服务）。对账本来说，已经确认给用户的分录 RPO 必须是 0，所以同一区域内多可用区同步复制；跨区域复制是异步的，有延迟。为了不让两个区域同时写同一个账户，常见做法是单元化：每个用户和账户有一个归属区域，只在归属区域写，其他区域只读或转发。

切换时三步：先隔离旧区域（fencing，防止它恢复后继续写），再提升备用区域，最后处理切换瞬间「结果未知」的支付：用同一个幂等键向 PSP 查询，而不是重新发起。高峰期和故障时先降级非核心功能（营销、积分、推荐），保住下单和支付的主路径。数据驻留和牌照还会限制副本能放在哪个国家，这一点在消费金融里比在电商里更严格。

链接：[[domains/payments/map/platform.availability|支付系统的高可用]] · [[domains/payments/map/platform.routing-failover|渠道路由与容灾]] · [[sd12-payment-routing]] · [[tiktok-service-protection]]

---

## 3. 你最可能的级别

| 因素 | 指向 |
|---|---|
| 全职年限约两年，岗位偏好 4 年以上 | 1-2 或 2-1 |
| 支付领域完全对口，有生产事故和端到端 ownership | 往上推 |
| 这个 req 的区间从入门覆盖到 senior | 级别由面试决定，不由职位名决定 |
| 没有系统设计轮的面试 | 结果通常封顶在 2-1 |

**结论**：现实的落点是 2-1；冲 2-2 的条件是面试里有一轮系统设计，并且你在设计轮和项目深挖里都讲到 senior 的深度（取舍、失败行为、你自己的决定和数字）。所以：

1. 第一通电话里请招聘官按 2-2 安排，并确认包含系统设计轮，问法见 [[06-questions-to-ask]]。
2. 所有准备按 2-2 的标准做：每个设计决定说出「是什么逼出了它、换来了什么、代价是什么」。
3. 拿到 2-1 也不是失败：同一套面试结果会对照组里的名额定级，入职后一年两次考评，可以靠表现晋升。
