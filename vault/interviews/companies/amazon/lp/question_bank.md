# LP 题库（16 条 LP × 题目 × 框架 × 追问）

- 用法：听到题 → 判断是哪条 LP → 报出故事编号 → 讲 3–4 个要点 → 准备好追问。
- 故事编号：「Amex 结算管线」–「实习：Kafka 事件流」 工作故事，「Quant-Stroller 研究平台」–「Aiki 消费者 App」 个人项目与迁移，「新人 onboarding 与带教」 带教；全文见 [[S1_amex-settlement-pipeline]] 等 `stories/` 笔记。
- 级别：senior。每条 LP 的「听什么」一行写明面试官在 senior 档往哪里深挖。
- 带「需补」的故事：补完 【待补】 之前不要口播它的数字。
- 同一位面试官面前不连用同一个故事；首选用过就换备选。

## LP1 · Customer Obsession

- 听什么：你怎么发现客户没说出来的问题；为客户让过短期目标吗；「客户」是谁（商户，或下游团队）要先说清。

### 1.1 Tell me about a time you went above and beyond for a customer.
- 框架：**「澳洲 Amex 退款费」**（备选 「Amex 出款延迟事故」）
  - 开场：**"It wasn't my ticket; I owned the answer."**
  - 三个团队、约 **50 条**回复互相推诿
  - 我按国家数退款费行：美国 **1,079,627** 行 vs 澳大利亚 **0**
  - 原因是配置（定价计划是 `partial`，逻辑只在 `full` 触发），早于迁移；查询写进文档，当天结束讨论，变成功能票
- 追问：
  - How did you know it wasn't a regression? → 出款服务从来没为 AU direct-Amex 发过退款费；变的只是报表口径。
  - Why pull data instead of discuss? → 争论来自领域知识不对称；数据让所有人当场可验证。
  - What did you do for the merchants meanwhile? → 【待补：是否有临时补偿；没有就说「没有，已立功能票」】
  - How big is the money? → 【待补：AU 漏掉的退款费量级】

### 1.2 Describe a time you had to deal with a difficult customer situation.
- 框架：**「Amex 出款延迟事故」**（备选 「澳洲 Amex 退款费」）
  - 约 **$4M** 出款「不见了」，商户在等
  - 先区分「预期延迟」和「回归」：内部 SLA 是 **T+7**
  - 我是三位 owner 之一，负责 SLA 判定和修复方向
  - 方案选 **region conditional** 而不是 revert，两人部署
- 追问：
  - What exactly did you do vs the others? → 三位 owner 之一；我的是 SLA 判定 + 修复方向；部署是两位队友。
  - Why region conditional over revert? → revert 会连 EU 合规改动一起撤；conditional 让 EU/US 语义独立；代价是 UDTF 多一个分支。
  - Did the merchant get the money? → 【待补：最终出款或补偿；$4M 是延迟不是丢失】
  - Whose PR caused it? → 我们团队的一个 PR（EU 合规的 effective-date 变更）；不点名。

### 1.3 Tell me about a time you identified a customer problem before the customer reported it.
- 框架：**「ACH 费用 NULL 事故」**（备选 「退款费 billing-terms 复盘」）
  - 我建的健康检查「每笔 settled 交易都有 Braintree 费」先于商户发现费用静默缺失
  - 切片：100% 是 `us_bank_account` + standard ACH，约 **196 商户**、**$11.3M/天**
  - 单笔追踪：sub_kind 为 NULL，`'BT_' || NULL` 为 NULL，无类别、无费用、无报错
  - 结果：根因几分钟内定位，重载设计整体移除，新增 e2e
- 追问：
  - Why not exclude ACH from the check? → 数字写下来：检查是对的，费用真丢；不压掉检查。
  - Which part was yours? → 根因、postmortem、重载合并、DROP；止血 PR 是队友的。
  - Money actually lost? → 【待补：缺失费用是否补账、对商户的实际影响】

### 1.4 Tell me about a time you had to balance a customer's needs against a technical constraint.
- 框架：**「Amex 出款延迟事故」**（备选 「Net Settlement 数据源切换」）
  - 「Amex 出款延迟事故」：revert 快 vs region conditional 稳；商户要钱，但不能撤掉 EU 合规
  - 「Net Settlement 数据源切换」：净额结算窗口 vs 费用到达时间，费用赶不上窗口
  - 讲被否决的备选和代价
- 追问：
  - What did it cost? → 「Amex 出款延迟事故」 多一个分支和测试；「Net Settlement 数据源切换」 把一个月外的重处理写成注释里的已知风险。
  - How did you choose? → 先看可逆性，再看影响范围。
  - Who agreed? → 【待补：谁提的备选、最后谁拍板】

### 1.5 How did you use customer feedback to change what you built?
- 框架：**「Aiki 消费者 App」**（需补），备选 「澳洲 Amex 退款费」
  - 【待补：Aiki 用户反馈驱动的具体改动，含数字】
  - 补不出就用 「澳洲 Amex 退款费」：PM 的升级 → 数据 → 功能票
- 追问：
  - Who were the users? → 【待补】
  - What changed in the product? → 【待补】
  - Result? → iOS 应用 **4.5+** App Store 评分；其余【待补】

- 没有合适故事时：
  - "Most of my customers are internal — merchants through downstream teams and the payout service. The clearest case where I worked backwards from a merchant's problem is 「澳洲 Amex 退款费」/S9."

## LP2 · Ownership

- 听什么：没人派你的事、跨团队的事；做到「不再复发」而不是修一次。

### 2.1 Tell me about a time you took on something outside your responsibilities.
- 框架：**「schema pool」**（备选 「Terraform 7 分钟 RCA」）
  - 没有 ticket；多个 agent 同时跑，撞同一套 DDL
  - 我做了 schema pool：零拷贝克隆，约 **2 秒**一个独立环境，**3 篇 ADR**
  - 范围要说清：这是个人仓库，相邻团队采用 on-call copilot
- 追问：
  - Why is a clone 2 seconds? → 不可变微分区 + 元数据指针，不拷数据。
  - What broke in V1? → `PUBLIC` 的状态取决于谁最后跑了什么迁移。
  - Who uses it? → 【待补：团队里其他工程师的使用人数和频率】
  - Why direct-push to main? → 个人仓库，不影响团队代码。

### 2.2 Describe a project you owned end to end.
- 框架：**「Amex 结算管线」**（备选 「Net Settlement 数据源切换」）
  - 接手一张表的 stub → 设计文档 → 上线 → **18 个月** on-call → EU 扩展
  - 六个 append-only stream、每阶段复合键 MERGE、两个校验函数、一个 kill-switch
  - 结果：生产首半年约 **22M** 笔 Amex 交易；最大单 PR 约 **1,800 行**
- 追问：
  - What was yours vs the team's? → stub 起全部设计是我的；设计文档给团队评审。
  - Why Streams/Tasks, not Airflow or Spark? → 数据局部性 + 事务性 MERGE + `STREAM_HAS_DATA` 省算力；代价是编排弱，用监控和告警补。
  - What broke? → 迟到文件（改为扫描所有日期目录 + load history 去重）；拒付标志（复合键）。
  - What would you do differently? → 偏移配置表 + 通用定宽解析，新增记录类型 = 加一行配置。

### 2.3 Tell me about a time you sacrificed a short-term result for long-term value.
- 框架：**「ACH 费用 NULL 事故」**（备选 「费用异常检测器 go/no-go」）
  - 「ACH 费用 NULL 事故」：止血之后继续做结构性修复：单函数 + versioned DROP + e2e
  - 「费用异常检测器 go/no-go」：叫停短期「快赢」，把 Phase 2 放到 gate 之后
- 追问：
  - What did it cost in time? → 【待补：结构性修复比止血多花多久】
  - Who pushed back? → 【待补】
  - How do you know it stayed fixed? → 同类 NULL 拼接在接缝处直接报错；e2e 覆盖从 promote 到费用。

### 2.4 Tell me about a time you took ownership of a problem that wasn't yours.
- 框架：**「费用异常检测器 go/no-go」**（备选 「澳洲 Amex 退款费」）
  - 接手离职实习生的异常检测项目，重新界定范围
  - 先救不可再生的标注并导出；代码、terraform、训练配方（固定 seed）都可重建
  - 给出 go/no-go：Phase 1 纯 SQL 规则推进，ML 放到 gate 之后
- 追问：
  - Who asked you to assess? → 【待补：自己发起还是经理要求】
  - Wasn't that wasted work? → 唯一不可再生的是标注，已导出。
  - How do you know the numbers? → 来自我自己的评估文档，口播用量级。

### 2.5 Tell me about a time you took responsibility for a mistake.
- 框架：**「退款费 billing-terms 复盘」**（备选 「Quality-check 框架」）
  - 我的数字 **196,274** 行是错的，真实是 **21,923** 行；商户 **61 → 30**；金额 **$11,123 → $5,854.52**
  - 自己发现，在公开线程收回，并排放两版查询
  - 机制：每个结论带可重跑查询；影响范围谓词必须检查时间有效性
- 追问：
  - How did you discover it? → 【待补：触发点，例如抽样某行发现计划是几个月后回填的】
  - Who had seen the first number? → 【待补：196K 是否已发给他人或进入 ticket】
  - How do you fix it? → 创建费用时调用 `EFFECTIVE_PRICING_SCHEDULE(maid, date)`，不复制 credit 的历史计划 ID。

- 没有合适故事时：不需要，LP2 有 5 个首选；同一面试官面前不要连用 「Amex 结算管线」 和 「ACH 费用 NULL 事故」。

## LP3 · Invent and Simplify

- 听什么：简化的是「机制」（别人不再需要你），不是一段代码；说出被否决的备选。

### 3.1 Tell me about a time you simplified a complex process.
- 框架：**「Quality-check 框架」**（备选 「Net Settlement 数据源切换」）
  - 每张表一个校验 task → 配置驱动的框架，接入 = 插一行配置
  - 约 **1,500 行**框架，铺开 **8** 个 subject area
  - 否决：VARIANT / 新表（会关闭谓词下推）；用扁平行 + 等值 JOIN
- 追问：
  - Isn't dynamic SQL risky? → 配置经 migration 控制，不是用户输入；失去静态检查，用 exception handler + 结果表健康检查补。
  - Why a status table, not task dependencies? → 下游在不同库、不同账号，`AFTER` 不跨账号。
  - Actual status? → 框架 + 8 次铺开在生产；商户级设计并评审，在一个区域验证（TRANSFERS，16 个月）。

### 3.2 Tell me about something you invented or built that nobody asked for.
- 框架：**「schema pool」**（备选 「Quant-Stroller 研究平台」）
  - 零拷贝克隆池：约 **2 秒**得到一个隔离环境
  - 角色：像带一队 agent 的 tech lead，**3 篇 ADR**
  - 「Quant-Stroller 研究平台」：一个平台，四个市场，新市场 = 一个薄适配器
- 追问：
  - Why GitHub Deployments API, not tags? → 打了 tag 不等于部署；Deployments API 记录生产实际部署的 SHA。
  - Cross-database streams? → 先克隆 APP_DB 再 REPL_DB 会让 stream 失效；固定顺序先 REPL 后 APP。
  - Who adopted it? → 【待补】

### 3.3 Describe a time you challenged the way things had always been done.
- 框架：**「Net Settlement 数据源切换」**（备选 「Quality-check 框架」）
  - 静态拆分 vs 更聪明的运行时 fallback：费用赶不上净额窗口，提前切数据源
  - 两个 task 被同一个 toggle 反向控制，等于互斥
  - 窗口化 ON 使扫描量恒定
- 追问：
  - Trade-off of the time window? → 同一记录超过一个月才重处理时绕开去重；写在注释里的已知风险。
  - Why not dual-write? → 没有显式互斥的 dual-write 就是重复收费。
  - Postgres vs Snowflake? → Postgres 是费率的 system of record，事务原子写；Snowflake 做数十亿行聚合。

### 3.4 Tell me about a creative solution you found under tight constraints.
- 框架：**「费用异常检测器 go/no-go」**（备选 「schema pool」）
  - Phase 1 纯 SQL 规则推进，ML 放门后
  - 理由：大 warehouse 上推理必超时；精确率无 ground truth；告警量每天数百万条
  - 估算 **5–8 人周**、**2–3 个月**
- 追问：
  - Why no-go and not just harder? → 超时 + 无 ground truth + 告警量，三条都是硬约束。
  - What would make you say go? → 业务驱动明确 + shadow 精确率达到阈值；【待补：具体阈值】
  - Pushback? → 【待补：有没有人希望照原计划上线】

- 没有合适故事时：不需要。

## LP4 · Are Right, A Lot

- 听什么：不是「我总是对」，而是你怎么找反证、怎么校准、错了怎么办。

### 4.1 Tell me about a time you made a decision with incomplete information.
- 框架：**「Net Settlement 数据源切换」**（备选 「费用异常检测器 go/no-go」）
  - 没有需求文档：先 discovery
  - 影子核对：**13,737,670** vs **13,768,430** 行，差 **+0.224%**，一致率 **>99.9%**
  - toggle 默认关，上线分两步（deploy ≠ release），让不确定性可观测
- 追问：
  - What would have made you not switch? → 【待补：事先设的不切换门槛；没有就说「我判断 0.224% 可接受」】
  - How did you handle the 0.224%? → 是记录数差异，一侧多 30,760 行；构成【待补】。
  - Did the toggle ever flip back? → 生产在一次 migration 里 prod 关、preprod 开；灰度细节无记录，不编。

### 4.2 Tell me about a time you were wrong.
- 框架：**「退款费 billing-terms 复盘」**（备选 「Quality-check 框架」）
  - 我的影响范围数字是 **196,274** 行，实际 **21,923**
  - 自己发现，在任何人据此行动前收回
  - 原因：谓词缺「时间有效性」
- 追问：
  - How did you discover it? → 【待补：触发点】
  - Why is the blast radius bounded? → 切换后新 credit 自动带 NET 计划 ID；只有切换前积压、切换后才跑的商户受影响。
  - What changed in how you work? → 每个结论配可重跑查询；影响范围谓词检查时间有效性。

### 4.3 Describe a time you changed your mind based on new evidence.
- 框架：**「Quality-check 框架」**（备选 「退款费 billing-terms 复盘」）
  - 发现框架的粒度选错（表级），写 ADR 提出商户级
  - 正确性论证：strictest wins，先判表级失败，再判商户级失败
  - 未改造的 procedure 退化为表级阻塞，等于今天的行为
- 追问：
  - Did anyone disagree? → 【待补：ADR 评审里的异议；没有就说「无实质异议」，不编冲突】
  - Why not VARIANT? → 逐行 UDF / VARIANT 解析会关闭谓词下推；VARIANT 16 MB/cell 上限（约 98K 商户）。
  - What did you learn? → 粒度是随规模要重新审视的设计参数。

### 4.4 Tell me about a judgment call that others disagreed with.
- 框架：**「费用异常检测器 go/no-go」**（备选 「Amex 出款延迟事故」）
  - 「费用异常检测器 go/no-go」：go/no-go；「Amex 出款延迟事故」：region conditional 而非 revert
  - 讲你的判断依据（数字、可逆性），不讲「我对他错」
- 追问：
  - Who disagreed? → 【待补：角色与原话】
  - How did you convince them? → 用数据和可重跑的估算，不靠资历。
  - Were you right? → 「Amex 出款延迟事故」 方案被采纳并部署；「费用异常检测器 go/no-go」 数字来自评估文档，口播用量级。

### 4.5 How do you seek out views that disconfirm your own?
- 框架：**「Quality-check 框架」**（备选 「Quant-Stroller 研究平台」）
  - 「Quality-check 框架」：ADR 写四个方案及否决理由，邀请评审
  - 「Quant-Stroller 研究平台」：双关卡（purged CV、Deflated Sharpe、PBO + 执行重放）+ **340+** 次实验记入 append-only 账本
- 追问：
  - How many ideas did the gates reject? → 【待补：340 个实验中通过双关卡的数量】
  - A case the gate said no? → 【待补：一个被 DSR/PBO 拒绝的具体想法】
  - What's the headline result? → 中国小盘月度策略，两关通过，扣 10 bps 成本后 excess Sharpe **1.39**，paper-trading。

- 没有合适故事时：不需要。

## LP5 · Learn and Be Curious

- 听什么：学到的东西是否转成团队能力；学习路径是系统的还是随机的。

### 5.1 Tell me about a time you had to learn something new quickly.
- 框架：**「AI-native 迁移」**（需补），备选 「schema pool」
  - 「AI-native 迁移」：AI-native 迁移 Ruby/Kotlin → Snowflake/Java；【待补：学习曲线】
  - 「schema pool」：零拷贝克隆 + GitHub Deployments API
- 追问：
  - How did you ramp up? → 【待补】
  - What did you build with it? → 「schema pool」：schema pool，约 2 秒克隆。
  - How did you verify you'd learned it? → 全面测试保证 behavioral parity。

### 5.2 Describe something you taught yourself recently and how you applied it.
- 框架：**「Quant-Stroller 研究平台」**（需补），备选 「实习：Kafka 事件流」
  - purged CV / Deflated Sharpe / PBO，落到双关卡
  - 【待补：学习路径】
  - 「实习：Kafka 事件流」：实习时从零接 Kafka Connect / Snowpipe Streaming；【待补：入职起点和学法】
- 追问：
  - Why did you start it? → 【待补：动机】
  - What did you apply? → 双关卡 + **340+** 次实验账本。
  - What did you get wrong first? → 【待补】

### 5.3 Tell me about a time you improved after feedback.
- 框架：**「Quality-check 框架」**（备选 「退款费 billing-terms 复盘」）
  - 对自己的抽象用 review 别人代码的严格度，写 ADR 修自己的缺陷
- 追问：
  - What was the feedback? → 【待补：谁、说了什么】
  - What changed? → 修自己的缺陷也走正式流程（ADR）。
  - Next time? → 设计任何 gate 先问：失败的爆炸半径是谁。

### 5.4 How do you stay current with technology?
- 框架：**「AI-native 迁移」 / 「schema pool」**
  - 并行用 Claude Code / Codex / Cursor，并知道各自的 usage 上限
  - AWS DVA-C02 证书（简历）
  - 做法：plan with the agent → TDD 每个阶段 → CI 与监控 gate 决定
- 追问：
  - How do you trust AI-written code? → gates 和阈值，不看行数；money code 逐个 diff 读。
  - Last thing you learned? → 【待补】

- 没有合适故事时：
  - "Most of my learning has been on the job: Snowflake internals — streams, zero-copy clones, micro-partitions — 「schema pool」."

## LP6 · Hire and Develop the Best

- 听什么：带人的可见产出 + 你让团队标准变高的机制。这是目前最薄的一条 LP。

### 6.1 Tell me about a time you mentored someone.
- 框架：**「新人 onboarding 与带教」**（需补），备选 「费用异常检测器 go/no-go」
  - 契约先行：我先定义领域边界（哪些商户在什么记账状态下算已迁移）
  - 他的三块工作：Snowglobe exclusion service、journaling-schedule gRPC 同步、scheme fee 估算 ML
  - 我按下游怎么消费同一批事件来审他的设计
  - 事故里我是他依赖的 fee-calc 权威
- 追问：
  - How did you help him grow concretely? → 边界与契约前置；按下游消费审设计；事故里的权威。不编 1:1。
  - What did he own at the end? → 【待补：被带者现在独立 own 的东西】
  - What did he disagree with you on? → 【待补：一次他提出异议、你改了想法的例子】

### 6.2 Describe a time you raised the performance bar on your team.
- 框架：**「Quality-check 框架」**（备选 「新人 onboarding 与带教」）
  - 框架让「最省事的路径」= 标准做法
  - 握手变成 SQL 硬条件；铺开 **8** 次；ADR 展示决策如何被论证
- 追问：
  - How many teams adopted it? → 【待补：除本团队外有无其他团队接入】
  - Did you check others' work? → review 看三件事：正确性、领域边界、strictest wins 式安全论证。
  - Hiring or promotion? → 【待补：是否参与；没有就说「没有，我的影响通过框架和文档」】

### 6.3 Tell me about a time you helped someone grow.
- 框架：**「新人 onboarding 与带教」**
  - 同 6.1：契约先行、设计评审、onboarding doc（2024 年建，至今维护）
- 追问：
  - What's in the onboarding doc? → 【待补：目录结构和使用者反馈】
  - What if someone doesn't improve? → 【待补】
  - Next step for him? → 【待补】

### 6.4 Tell me about a time you gave tough feedback.
- 框架：无素材
  - 【待补：一个真实的反馈场景；没有就用下面的说法】
- 追问：
  - How do you give feedback? → 【待补】
  - Result? → 【待补】

- 没有合适故事时：
  - "I haven't run a formal mentoring program. The way I raise the bar is through mechanisms — the quality-check framework eight subject areas use, the ADRs, and the onboarding doc I've maintained since 2024 — and I've defined the contracts for a newer engineer's three projects. Let me tell you about that last one."
  - 说完立刻讲 「新人 onboarding 与带教」，不道歉三次。

## LP7 · Insist on the Highest Standards

- 听什么：你的标准高于流程要求；修到「不再复发」，并写下机制。

### 7.1 Tell me about a time you refused to lower your standards.
- 框架：**「ACH 费用 NULL 事故」**（备选 「费用异常检测器 go/no-go」）
  - 有人建议把 ACH 加进检查的排除名单；我把数字写下来，检查保留
  - 止血之后继续做结构性修复
  - 「费用异常检测器 go/no-go」：不让「快赢」绕过 gate
- 追问：
  - Who proposed the exclusion? → 【待补：角色、你的原话、谁拍板】
  - Why didn't tests catch it? → 只断言路由；fixture 用卡 payload；pending 行不断言 sub_kind；没有跨 promote→fee 的测试。
  - What did the check cost you? → 【待补】

### 7.2 Describe how you ensured a problem stayed fixed.
- 框架：**「ACH 费用 NULL 事故」**（备选 「Terraform 7 分钟 RCA」）
  - 单函数 + 默认参数，新分支选不到不完整实现
  - versioned migration 显式 DROP 旧签名（删文件不会删已部署对象）
  - e2e 覆盖 promote 到费用；规则：不可映射的工具必须 fail loudly
  - 「Terraform 7 分钟 RCA」：扫全仓库，找到同形风险
- 追问：
  - How do you prevent the class? → 修接缝，不修调用点；NULL 拼接是 SQL 语言属性。
  - Why a versioned DROP? → 删掉 `R__` repeatable 文件不会删已部署对象。
  - Did other teams adopt the e2e pattern? → 【待补】

### 7.3 Tell me about a time you raised quality standards for a team.
- 框架：**「Quality-check 框架」**（备选 「Quant-Stroller 研究平台」）
  - 握手变 SQL 硬条件；strictest wins
  - 约 **1,500 行**框架，**8** 个 subject area，**96.4%** 检查一次通过
- 追问：
  - What did it find? → **50** 个坏商户 / **35,000**。
  - Why a status table? → 下游在不同库、不同账号。
  - Cost to teams? → 接入 = 插一行配置。

### 7.4 Tell me about a time you found a defect others missed.
- 框架：**「退款费 billing-terms 复盘」**（备选 「ACH 费用 NULL 事故」）
  - 「退款费 billing-terms 复盘」：重审自己的谓词，发现缺「时间有效性」
  - 「ACH 费用 NULL 事故」：e2e 的四个缺口
- 追问：
  - Why did others miss it? → 「退款费 billing-terms 复盘」：谓词看起来对；「ACH 费用 NULL 事故」：测试只看路由。
  - How did you confirm? → 可重跑查询，数字对比。
  - What changed? → 每个结论带查询；影响范围检查时间有效性。

- 没有合适故事时：不需要。

## LP8 · Think Big

- 听什么：方向是否更大、有数据支撑、有人跟着走。雇主内证据偏薄，别让 「Quant-Stroller 研究平台」 成为唯一答案。

### 8.1 Tell me about a time you thought bigger than the task you were given.
- 框架：**「Quality-check 框架」**（备选 「Terraform 7 分钟 RCA」）
  - 不是一个 feature，而是别人往上接的平台
  - 「Terraform 7 分钟 RCA」：修完一个资源后扫全仓库，**79** 个资源里找到 **42**
- 追问：
  - Who built on it? → 【待补：谁往框架上接了东西】
  - Why a scan? → 「修完这一次」和「消灭这一类」是两件事。
  - What's the next step? → 全仓库 lint / policy check，把问题前移到 plan 阶段（想法，未落地）。

### 8.2 Describe a bold idea you proposed.
- 框架：**「Quant-Stroller 研究平台」**（个人项目），备选 「schema pool」
  - 一个平台、四个市场（美股、加密、A 股、外汇）；新市场 = 薄适配器，策略代码零改动
  - 四个窄接口：DataSource / Factor / Strategy / Broker
  - 【待补：雇主内更大的方向】
- 追问：
  - Is it a personal project? → 是，先说清楚。
  - Scale? → 66K+ 行、470+ 测试文件、2,300+ 因子目录、9 个数据商。
  - Rejected alternative? → 【待补：一个架构取舍和被否决的备选】

### 8.3 Tell me about a time you created a vision that others followed.
- 框架：**「Quality-check 框架」**（备选 「schema pool」）
  - 框架铺开 8 次，ADR 讲清方向
  - 【待补：谁跟着你的框架或工具走】
- 追问：
  - Who followed? → 【待补】
  - How did you communicate it? → ADR + 评审。
  - What data supported it? → 80 万 vs 240 万行的存储量；50 个坏商户 / 35,000。

### 8.4 How have you looked around corners for your customers?
- 框架：**「Net Settlement 数据源切换」**（备选 「ACH 费用 NULL 事故」）
  - 费用赶不上净额窗口 → 提前切数据源
  - toggle 默认关，pre-prod → prod
- 追问：
  - How did you see it coming? → 【待补】
  - What if you were wrong? → toggle 一次 UPDATE 关回，不需要发版。
  - Risk accepted? → 超过一个月才重处理时绕开去重，写在注释里。

- 没有合适故事时：
  - "The biggest-scope work is 「Quality-check 框架」/S5; my boldest independent project is 「Quant-Stroller 研究平台」 — a platform where a new market is a thin adapter. 「Quant-Stroller 研究平台」 is a personal project."

## LP9 · Bias for Action

- 听什么：不是「快」，而是可逆性分析下的 calculated risk，以及你怎么限制下行。

### 9.1 Tell me about a calculated risk you took.
- 框架：**「Net Settlement 数据源切换」**（备选 「schema pool」）
  - shipped dark：toggle 默认关 → pre-prod → prod；deploy ≠ release
  - 影子核对 **13.7M** 行、**>99.9%** 一致后才切
  - 下行兜底：一个 UPDATE 关回
- 追问：
  - What if the diff had been 5%? → 【待补：事先设的门槛】
  - Who approved the toggle? → 【待补】
  - Why not dual-write? → 没有显式互斥就是重复收费。

### 9.2 Describe a time you had to decide quickly with limited information.
- 框架：**「Terraform 7 分钟 RCA」**（备选 「ACH 费用 NULL 事故」）
  - **7 分钟**根因（Terraform 授权依赖），同天三环境
  - 然后核查邻近模块：**79** 个资源里 **42** 个同形，**2** 个同形风险
- 追问：
  - How did you reach root cause in 7 minutes? → 对仓库 grant 结构有全局图景；错误信息指向依赖授权；provider 有对应参数。
  - Why REVOKE and not COPY? → 【待补：当时是否权衡过】
  - Risk of the fix? → Terraform 无事务；REVOKE 会撤 reviewer 角色的 USAGE，要确认其不依赖。

### 9.3 Tell me about a time you acted without waiting for approval.
- 框架：**「schema pool」**（备选 「Terraform 7 分钟 RCA」）
  - 个人仓库，无 ticket，直接做
  - 「Terraform 7 分钟 RCA」：我先问了一句可否推 PR（不是未经批准）
- 追问：
  - What was the blast radius? → 个人仓库，不影响团队代码。
  - Would you do it on team code? → 不会；走评审。
  - Why direct-push to main? → 个人仓库，如实说。

### 9.4 Tell me about a time you had to choose between speed and thoroughness.
- 框架：**「费用异常检测器 go/no-go」**（备选 「Terraform 7 分钟 RCA」）
  - 反向：叫停快赢；先救不可再生的标注
  - 「Terraform 7 分钟 RCA」：快（7 分钟）+ 全仓库扫描（彻底）两者都要
- 追问：
  - How did you decide? → 可逆性：可逆的先动，不可逆的先核对。
  - Who lost out? → 【待补】
  - What did it save? → 避免 5–8 人周的 Phase 2 在没有 ground truth 时开工。

### 9.5 How do you decide when to act and when to wait?
- 框架：**「Net Settlement 数据源切换」**（备选 「费用异常检测器 go/no-go」）
  - 可逆 → 先动；不可逆 → 影子核对
  - 用 toggle、窗口、门槛把下行限制在可承受范围
- 追问：
  - Example of waiting? → 「费用异常检测器 go/no-go」：Phase 2 放到 gate 之后。
  - Example of acting? → 「Terraform 7 分钟 RCA」：7 分钟定位、同天修复。
  - Who sets the threshold? → 【待补】

- 没有合适故事时：不需要；「schema pool」/S8 范围偏小，senior 面试官会追问更大风险，用 「Net Settlement 数据源切换」 做主答案。

## LP10 · Frugality

- 听什么：具体的资源数字（算力、行数、基础设施、人周）。

### 10.1 Tell me about a time you accomplished more with less.
- 框架：**「Quality-check 框架」**（备选 「schema pool」）
  - 复用结果表，零新基础设施，只存失败行：**80 万** vs **240 万**行
  - 接入 = 插一行配置
- 追问：
  - How did you measure the saving? → 80 万 vs 240 万行存储量的对比。
  - What did you give up? → 只存失败行，通过的行不留痕。
  - Credit/time saved? → 【待补：任何 credit、时间、行数的具体节省】

### 10.2 Describe a time you had limited resources or time.
- 框架：**「schema pool」**（备选 「费用异常检测器 go/no-go」）
  - 零拷贝克隆约 **2 秒**，不拷数据
  - 「费用异常检测器 go/no-go」：把 2–3 个月的工作放到 gate 之后
- 追问：
  - Why 2 seconds? → 不可变微分区 + 元数据指针。
  - What did you cut? → 「费用异常检测器 go/no-go」：Phase 2。
  - Who paid the cost? → 【待补】

### 10.3 Tell me about a time you reduced cost or complexity.
- 框架：**「Amex 结算管线」**（备选 「Net Settlement 数据源切换」）
  - `STREAM_HAS_DATA` 不为空输入起 warehouse
  - 窗口化 ON 使扫描量恒定（「Net Settlement 数据源切换」）
- 追问：
  - Dollar figure? → 【待补】
  - Trade-off? → 编排弱（无分支、无外部回调），用监控补。
  - What did the window cost? → 超过一个月的重处理绕开去重。

### 10.4 Tell me about a time you decided not to build something.
- 框架：**「费用异常检测器 go/no-go」**（备选 「Quality-check 框架」）
  - Phase 2 在 gate 之后；估算 **5–8 人周**、**2–3 个月**
  - 「Quality-check 框架」：否决 VARIANT 和新表
- 追问：
  - How did you decide? → 推理必超时、无 ground truth、告警量每天数百万条。
  - What would change your mind? → 业务驱动明确 + shadow 精确率达标。
  - Pushback? → 【待补】

- 没有合适故事时：不需要；缺成本数字：【待补：任何一个 credit、时间、行数的具体节省】。

## LP11 · Earn Trust

- 听什么：对更资深的人坦率；公开自批；让别人能独立验证你。

### 11.1 Tell me about a time you made a mistake and how you handled it.
- 框架：**「退款费 billing-terms 复盘」**（备选 「Quality-check 框架」）
  - 先在公开线程收回自己的数字，并排放两版查询
  - **196,274 → 21,923** 行；**61 → 30** 商户；**$11,123 → $5,854.52**
  - 机制：每个结论配可重跑查询
- 追问：
  - Who had seen the first number? → 【待补】
  - How do you know $5,854.52 is right? → 口径是 `SUM(ABS(amount))/100`；SQL 附在文档里。
  - What changed? → 影响范围谓词检查时间有效性。

### 11.2 Describe a time you had to deliver bad news.
- 框架：**「退款费 billing-terms 复盘」**（备选 「Amex 出款延迟事故」）
  - 开口句：**"I'd rather retract my own number…"**
  - 「Amex 出款延迟事故」：向商户方说明 $4M 出款延迟的原因和时间
- 追问：
  - How did people react? → 【待补】
  - Why retract publicly? → 让别人别据此行动，比保面子重要。
  - Follow-up? → 修复方案：创建费用时重新解析计划。

### 11.3 Tell me about a time you earned the trust of people who were skeptical.
- 框架：**「澳洲 Amex 退款费」**（备选 「Net Settlement 数据源切换」）
  - 可重跑的查询，让对方自己验证
  - 「Net Settlement 数据源切换」：影子核对，让下游看到并行结果
- 追问：
  - Why did they doubt you? → 三个团队 50 条回复互相推诿，各有领域假设。
  - How did you prove it? → 查询写进文档，所有人当场复跑。
  - What did you say about what you didn't know? → 第二类费用我说 "not sure yet"，给分层假设和验证计划。

### 11.4 Tell me about a time you were candid when it was uncomfortable.
- 框架：**「ACH 费用 NULL 事故」**（备选 「Quality-check 框架」）
  - 数字写下来，不加排除
  - 「Quality-check 框架」：对自己的设计写 ADR，承认粒度错
- 追问：
  - Who was uncomfortable? → 【待补】
  - How did you phrase it? → 用数字，不用「我对他错」。
  - Outcome? → 检查保留，根因修复。

### 11.5 How do you build trust with other teams?
- 框架：**「Net Settlement 数据源切换」**（备选 「澳洲 Amex 退款费」）
  - 把方法沉淀为模板，下次不用重新发明信任
  - 对齐靠数据契约：定价服务、结算平台、出款服务、收单行
- 追问：
  - Which teams? → 定价服务、结算平台、出款服务、收单行。
  - Your PR count? → 【待补：团队规模和我的 PR 数】
  - A conflict? → 「Amex 出款延迟事故」：划清边界，不挤进别人的部署。

- 没有合适故事时：不需要。

## LP12 · Dive Deep

- 听什么：你下到哪一层（行、函数、查询）；metrics 与 anecdote 不一致时你做什么。

### 12.1 Tell me about a time you dove deep to find a root cause.
- 框架：**「ACH 费用 NULL 事故」**（备选 「Terraform 7 分钟 RCA」）
  - 切片 → 单笔 → 回溯 → 读两个重载
  - 排除时序（每个年龄桶覆盖率 0%）和 stream 绕过（**30 of 30** 行到达费用 staging）；快速 ACH 对照组有费用
  - 根因：最终 MERGE 调用无银行账户分支的单参数重载，覆盖了正确值
- 追问：
  - How did you rule out a timing lag? → 时间序列显示每个年龄桶覆盖率都是 0%。
  - How big was the blast radius? → 约 196 商户、$11.3M/天；约 99,700 笔 settled 费 + 约 5,500 笔 discount 费缺失。
  - How do you prevent it? → fail loudly；单函数默认参数。

### 12.2 Describe a time when the data and the anecdote disagreed.
- 框架：**「澳洲 Amex 退款费」**（备选 「退款费 billing-terms 复盘」）
  - PM 说没有退款费 vs 数据：美国 **1,079,627** 行 vs 澳大利亚 **0**
  - 「退款费 billing-terms 复盘」：我的 196K 与重审后的 22K
- 追问：
  - Which was right? → 数据：美国有百万行，AU 为 0；原因是配置，不是回归。
  - Second issue? → AU 专有的 `refund` 费用类型；我说不确定，给分层假设。
  - Your initial hypothesis? → 【待补：被数据推翻的那一半】

### 12.3 Tell me about the most complex problem you've debugged.
- 框架：**「ACH 费用 NULL 事故」**（备选 「Amex 结算管线」）
  - NULL 拼接 + 重载覆盖，两层原因叠加
  - 「Amex 结算管线」：迟到文件与拒付标志的复合键问题
- 追问：
  - Why hard? → 无报错，静默缺失。
  - Alternatives you ruled out? → 时序滞后、stream 绕过。
  - Lesson? → 修接缝，不修调用点。

### 12.4 Tell me about a time you audited something and found a problem.
- 框架：**「退款费 billing-terms 复盘」**（备选 「Terraform 7 分钟 RCA」）
  - 重审自己的谓词，缺时间有效性
  - 「Terraform 7 分钟 RCA」：扫 **79** 个资源，找到 **42**
- 追问：
  - What triggered the audit? → 「退款费 billing-terms 复盘」：【待补】；「Terraform 7 分钟 RCA」：「修完这一次」和「消灭这一类」是两件事。
  - Did you fix the two risky ones? → 【待补：已提 PR 还是只标出】
  - Prevention? → 全仓库 policy check（想法，未落地）。

### 12.5 How do you verify that a system is correct?
- 框架：**「Amex 结算管线」**（备选 「Net Settlement 数据源切换」）
  - 行级：`TRY_TO_DECIMAL/DATE`，坏字段不炸整批，拒收记录保留
  - 批级：健康检查，每笔结算交易都有费用
  - 对账级：费用总额对 Amex 自己的汇总记录；不一致就停 task、page on-call
  - 同一份 SQL 既验证又生产
- 追问：
  - Did you ever lose or double-count money? → 不说 "no accidents"；设计目标是坏了就记录。
  - How does the dual-upstream task stay consistent? → `AFTER` 只保证各跑过一次，不保证同一批；FULL OUTER JOIN 兜底，错位记录下一轮自愈。
  - Parity for migration? → 「Net Settlement 数据源切换」：影子核对 13.7M 行。

- 没有合适故事时：不需要。

## LP13 · Have Backbone; Disagree and Commit

- 听什么：与更资深的人分歧；决定后全力执行。「commit」这一半目前没有真实故事。

### 13.1 Tell me about a time you disagreed with a decision made by your manager or a senior stakeholder.
- 框架：**「ACH 费用 NULL 事故」**（备选 「Amex 出款延迟事故」）
  - 有人建议加排除名单；我用数字说不
  - 【待补：谁提的、你的原话、最后谁定的】
- 追问：
  - What did you say exactly? → 【待补】
  - What if they had insisted? → 【待补】
  - Result? → 检查保留，根因修复。

### 13.2 Tell me about a time you disagreed with a decision and committed anyway.
- 框架：【待补】，备选 「Amex 出款延迟事故」
  - 【待补：被否决后全力执行的故事。候选：「Net Settlement 数据源切换」 选 B 时有人倾向 A？「Quality-check 框架」 评审？】
  - 「Amex 出款延迟事故」：region conditional vs revert，若方案被采纳则不算 commit
- 追问：
  - What did you do after the decision? → 【待补】
  - Did you say "I told you so"? → 【待补】
  - Result? → 【待补】
- 没有真实故事时：
  - "My strongest examples are cases where I held a position and the group agreed with me. I don't have a clean story where I lost the argument and then committed. The closest is 「Amex 出款延迟事故」: I argued for the region conditional over a revert."
  - 只讲真实发生过的；不编假设。

### 13.3 Tell me about a time you pushed back on a deadline or a plan.
- 框架：**「费用异常检测器 go/no-go」**（备选 「ACH 费用 NULL 事故」）
  - 冻结告警和 CI 工作，直到 gate 给 go
  - 理由：推理必超时、无 ground truth、告警量每天数百万条
- 追问：
  - Who set the deadline? → 【待补】
  - What did you offer instead? → Phase 1 纯 SQL 规则。
  - What if they said no? → 【待补】

### 13.4 Tell me about a time you stood alone in a room.
- 框架：**「ACH 费用 NULL 事故」**（备选 「费用异常检测器 go/no-go」）
  - 【待补：当时是否只有你一人坚持】
  - 数字写在线程里，检查不撤
- 追问：
  - Who was in the room? → 【待补】
  - What changed their mind? → 数字。
  - How did you keep the relationship? → 把冲突限定在证据上。

### 13.5 Tell me about a time you challenged the team's approach and were not backed.
- 框架：【待补】
  - 缺故事
- 追问：
  - What did you do next? → 【待补】
  - Would you do it again? → 【待补】

## LP14 · Deliver Results

- 听什么：带数字，含障碍与代价，"despite setbacks"。

### 14.1 Tell me about your most significant accomplishment.
- 框架：**「Amex 结算管线」**（备选 「Net Settlement 数据源切换」）
  - 约 **22M** 笔交易，最大单 PR 约 **1,800 行**，**18 个月**
  - 简历口径：不说 $600B；美元量级【待补：最终口径】
- 追问：
  - Dollar volume? → 【待补】；不口播 $600B。
  - What was yours? → stub 起的全部设计。
  - What broke? → 迟到文件、拒付标志；约十几个加固 PR。

### 14.2 Tell me about a time you overcame obstacles to deliver.
- 框架：**「Net Settlement 数据源切换」**（备选 「Amex 结算管线」）
  - 费用赶不上净额窗口
  - **13.7M** 行影子核对，>99.9% 一致，差 +0.224%
  - 迟到文件教训：改扫所有日期目录 + load history 去重
- 追问：
  - What did you do about 0.224%? → 记录数差异，30,760 行；构成【待补】。
  - 0.07% vs 0.224%? → 是两个不同的数；$55B / $450M 是项目级数字，不是我的。
  - Who else was involved? → 定价服务、结算平台、出款服务、收单行。

### 14.3 Tell me about a time you delivered under a tight deadline.
- 框架：**「Terraform 7 分钟 RCA」**（备选 「Amex 出款延迟事故」）
  - **7 分钟**根因，同天三环境
  - 「Amex 出款延迟事故」：三天关闭事故
- 追问：
  - What else did you find? → 同形风险 2 个。
  - Did you fix them? → 【待补：已提 PR 还是只标出】
  - Result? → 7 分钟定位，同天三环境。

### 14.4 Tell me about a time you delivered despite ambiguity.
- 框架：**「Net Settlement 数据源切换」**（备选 「费用异常检测器 go/no-go」）
  - 没有需求文档；先 discovery，再影子核对，再切
  - 「费用异常检测器 go/no-go」：用评估文档把模糊的 ML 想法变成 go/no-go
- 追问：
  - Who defined success? → 【待补】
  - What did you decide alone? → toggle 默认关、影子核对门槛。
  - Result? → >99.9% 一致后切换。

### 14.5 Tell me about a goal you missed.
- 框架：**「Quality-check 框架」**（备选 「退款费 billing-terms 复盘」）
  - 粒度选错，用 ADR 修
  - 【待补：是否有真正「错过交付日期」的例子】
- 追问：
  - What did it cost? → 商户级未全框架铺开，排在净额结算之后。
  - What changed? → 粒度是要重新审视的设计参数。
  - Status? → 框架 + 8 次铺开在生产；商户级设计、评审、在 TRANSFERS 验证。

- 没有合适故事时：不需要。

## LP15 · Strive to be Earth's Best Employer

- 听什么：对同事成长、安全、包容的具体机制。目前无专属故事。

### 15.1 Tell me about a time you made your team's environment better for others.
- 框架：**「新人 onboarding 与带教」**（备选 「schema pool」）
  - onboarding doc（2024 年建，至今维护）
  - schema pool 让并行开发不互相踩脚
- 追问：
  - Who used the doc? → 【待补：受益人数】
  - What's in it? → 【待补】
  - What else? → blameless 风格的 postmortem（「ACH 费用 NULL 事故」）。

### 15.2 How do you help a teammate who is struggling?
- 框架：**「新人 onboarding 与带教」**（需补）
  - 【待补】
- 追问：
  - A real case? → 【待补】
  - What did you change? → 【待补】

### 15.3 Describe how you've contributed to an inclusive team.
- 框架：无素材
  - 【待补：无素材】
- 追问：
  - 无。

- 没有合适故事时：
  - "I haven't led an initiative on this. What I've done in practice is lower the cost of joining and working on the team — the onboarding doc, the schema pool so people and agents don't collide, and blameless-style postmortems like 「ACH 费用 NULL 事故」's."
  - 不夸大。

## LP16 · Success and Scale Bring Broad Responsibility

- 听什么：二阶影响。目前无专属故事。

### 16.1 Tell me about a time you considered the broader impact of a decision.
- 框架：**「退款费 billing-terms 复盘」**（需确认），备选 「ACH 费用 NULL 事故」
  - 不按错误谓词过度补偿商户：【待补：真实动机】
  - 「ACH 费用 NULL 事故」：NULL 静默 = 对商户账务的二阶影响
- 追问：
  - Who would have been affected? → 影响范围 61 → 30 商户。
  - What did you do? → 收回数字、修正谓词。
  - Mechanism? → 每个结论配可重跑查询。

### 16.2 Describe a time you left something better than you found it.
- 框架：**「ACH 费用 NULL 事故」 / 「Amex 结算管线」**（备选 「schema pool」）
  - postmortem + 移除整类 bug
  - 工具留给团队（框架、schema pool、onboarding doc）
- 追问：
  - What was left behind? → 单函数、versioned DROP、e2e。
  - Who uses it? → 【待补】
  - Mechanism? → fail loudly。

### 16.3 Tell me about a time you had to weigh business results against a wider responsibility.
- 框架：无素材
  - 【待补：无素材】
- 追问：
  - 无。

- 没有合适故事时：
  - "Working on payments, the secondary effects are on merchants' cash: a wrong fee or a late payout lands on someone's operations. That's why I treat silent failures as unacceptable (「ACH 费用 NULL 事故」). I haven't had a case with a wider societal dimension."
  - 只说真实的。

## 通用问题

### Tell me about yourself（不超过 1 分钟）
- 框架：**简历主线**：PayPal 费用平台 → 「Amex 结算管线」 / 「Net Settlement 数据源切换」 / 「Quality-check 框架」 → 想做 AWS 数据服务；按时间顺序，英文
  - 开口句：**"I'm a software engineer at PayPal who owns the Amex fee pipeline end to end, and I'm looking to do that kind of data-platform work on AWS."**
  - **Education**：**NYU MS in CS**（2023–Jan 2025）；之前 **BS in Construction Management**（Tianjin University）
  - **Summer 2024**：PayPal 实习（Chicago）；**Kotlin/Spring Boot**、**Kafka**、**Spark + Airflow**（「实习：Kafka 事件流」）
  - **Feb 2025**：全职 Software Engineer（San Jose）；从 stub 设计并建成 **Amex 结算与费用管线**（Snowflake），**数千万**笔交易、**数十亿美元**年量（「Amex 结算管线」）
  - **Then**：Braintree **net-settlement** 项目内，我 own **interchange-fee** 这条线；**13.7M** 行切换，**>99.9%** 一致（「Net Settlement 数据源切换」）
  - **Alongside**：on-call owner；建 tracing 与 observability；配置驱动的质量检查框架（「Quality-check 框架」）
  - **Recently**：**AI-native 迁移** Ruby/Kotlin 到 Snowflake/Java，保持 behavioral parity（「AI-native 迁移」）；个人 **quant 研究平台**（「Quant-Stroller 研究平台」）
  - **Why here**：**AWS data services**；【待补：Why Amazon / Why AWS Data Services 的真实动机】
- 追问：
  - Why leave? → 【待补】
  - Biggest accomplishment? → 「Amex 结算管线」。

### Tell me about a time you failed
- 框架：**「Quality-check 框架」**（备选 「退款费 billing-terms 复盘」）
  - 自己的设计缺陷：粒度选错，ADR 修复
- 追问：
  - What was the cost? → 商户级铺开推迟。
  - What do you do differently? → 设计 gate 先问失败的爆炸半径是谁。

### What is your biggest weakness?
- 框架：【待补：真实的、与 senior 档相关的；例如 influence 的记录太少】
- 追问：
  - What are you doing about it? → 【待补】

### Why Amazon / Why AWS Data Services?
- 框架：【待补：由职位描述和你自己的动机组合】
- 追问：
  - Which team? → 【待补】

## LP ↔ 故事

| LP | 首选故事 | 备选 |
|---|---|---|
| 1 Customer Obsession | 「澳洲 Amex 退款费」（1.1）/ 「Amex 出款延迟事故」（1.2） | 「ACH 费用 NULL 事故」、「退款费 billing-terms 复盘」、「Aiki 消费者 App」（需补） |
| 2 Ownership | 「Amex 结算管线」 / 「schema pool」 / 「费用异常检测器 go/no-go」 / 「ACH 费用 NULL 事故」 | 「Terraform 7 分钟 RCA」、「Net Settlement 数据源切换」、「退款费 billing-terms 复盘」、「Quality-check 框架」 |
| 3 Invent and Simplify | 「Quality-check 框架」 / 「schema pool」 / 「Net Settlement 数据源切换」 / 「费用异常检测器 go/no-go」 | 「Quant-Stroller 研究平台」 |
| 4 Are Right, A Lot | 「Net Settlement 数据源切换」 / 「退款费 billing-terms 复盘」 / 「Quality-check 框架」 / 「费用异常检测器 go/no-go」 | 「Quant-Stroller 研究平台」、「Amex 出款延迟事故」 |
| 5 Learn and Be Curious | 「AI-native 迁移」、「Quant-Stroller 研究平台」（均需补）/ 「Quality-check 框架」 | 「schema pool」、「实习：Kafka 事件流」 |
| 6 Hire and Develop the Best | 「新人 onboarding 与带教」（需补）/ 「Quality-check 框架」 | 「费用异常检测器 go/no-go」 |
| 7 Insist on the Highest Standards | 「ACH 费用 NULL 事故」 / 「Quality-check 框架」 / 「退款费 billing-terms 复盘」 | 「费用异常检测器 go/no-go」、「Terraform 7 分钟 RCA」、「Quant-Stroller 研究平台」 |
| 8 Think Big | 「Quality-check 框架」 / 「Net Settlement 数据源切换」 / 「Quant-Stroller 研究平台」（个人） | 「Terraform 7 分钟 RCA」、「schema pool」、「ACH 费用 NULL 事故」 |
| 9 Bias for Action | 「Net Settlement 数据源切换」 / 「Terraform 7 分钟 RCA」 / 「schema pool」 / 「费用异常检测器 go/no-go」 | 「ACH 费用 NULL 事故」、「Amex 出款延迟事故」 |
| 10 Frugality | 「Quality-check 框架」 / 「schema pool」 / 「Amex 结算管线」 / 「费用异常检测器 go/no-go」 | 「Net Settlement 数据源切换」 |
| 11 Earn Trust | 「退款费 billing-terms 复盘」 / 「澳洲 Amex 退款费」 / 「ACH 费用 NULL 事故」 / 「Net Settlement 数据源切换」 | 「Quality-check 框架」、「Amex 出款延迟事故」 |
| 12 Dive Deep | 「ACH 费用 NULL 事故」 / 「澳洲 Amex 退款费」 / 「退款费 billing-terms 复盘」 / 「Amex 结算管线」 | 「Terraform 7 分钟 RCA」、「Net Settlement 数据源切换」 |
| 13 Have Backbone; Disagree and Commit | 「ACH 费用 NULL 事故」 / 「费用异常检测器 go/no-go」（commit 半边【待补】） | 「Amex 出款延迟事故」 |
| 14 Deliver Results | 「Amex 结算管线」 / 「Net Settlement 数据源切换」 / 「Terraform 7 分钟 RCA」 / 「Quality-check 框架」 | 「Amex 出款延迟事故」、「费用异常检测器 go/no-go」、「退款费 billing-terms 复盘」 |
| 15 Strive to be Earth's Best Employer | 「新人 onboarding 与带教」（需补） | 「schema pool」 |
| 16 Success and Scale Bring Broad Responsibility | 「ACH 费用 NULL 事故」 / 「Amex 结算管线」（「退款费 billing-terms 复盘」 需确认） | 「schema pool」 |
