# Sr 工作方法（Senior Engineering Craft）

> 每个叶子都是一条通用原则。卡片统一带：原则 / 怎么做 / 常见错法 / 面试官考什么 / 配哪类故事。`*` = 帕累托核心。

## 一、范围与资深度（Scope & Seniority）
- * 资深到底看什么：范围、自主、影响（Scope, Autonomy, Impact）— 各家职级表（ladder）的共同维度，及 Sr 与 Mid 的本质差别：不是写得更快，而是能处理更模糊、更大的问题
- * 把模糊问题变成计划（Taming Ambiguity）— 澄清目标、列假设、做最小实验、定"做到什么算够"
- * 拥有结果而不是任务（Owning Outcomes）— 对结果负责到上线之后；看指标不看工单关闭
- 技术领导的几种形态（Staff Archetypes）— Larson 四类：Tech Lead / Architect / Solver / Right Hand，各自怎么工作
- 胶水工作（Glue Work）— 看不见的协调工作：何时做、怎么让它被看见、何时停
- 当团队里最强的人（Being the Strongest）— 不做瓶颈：放大别人而不是亲自全做
- 选择战场（Picking Battles）— 哪些值得坚持、哪些值得让步

## 二、写作（Writing）
- * 设计文档（Design Doc）— 目的：在写代码前以低成本发现错误；结构：背景、目标/非目标、方案、替代方案、风险
- * 目标与非目标（Goals & Non-Goals）— 非目标要写成"别人可能合理期待但我们不做"的事
- * 替代方案与取舍（Alternatives Considered）— 至少一个认真的替代方案，写清为什么没选
- * RFC 流程（RFC Process）— 提案、评论期、决议、状态；Rust RFC / Python PEP / K8s KEP 的共同骨架
- * 决策记录（ADR）— 一页：背景、决定、后果；只记难以回退的决定；不可改历史，只能被取代
- 什么时候不该写设计文档（When Not to Write One）— 方案显然、可逆、成本低时
- * 状态更新（Status Updates）— 结论先行、红黄绿的含义、风险与请求放最前
- 文档的评审与生命周期（Doc Review & Lifecycle）— 谁评审、何时关闭、如何保持更新、归档
- 写给高层的一页纸（One-Pager for Leadership）— 问题、建议、代价、需要的决定（需先: 状态更新）
- 倒推工作法 PR/FAQ（Working Backwards）— 先写新闻稿和常见问题再开工

## 三、规划与里程碑（Planning & Milestones）
- * 拆解工作（Work Breakdown）— 按可验证的竖切片拆，而不是按层；每块 1–3 天可交付
- * 估期的真相（Estimation）— 范围而非点；已知/未知；乘数；估期是沟通工具不是承诺
- * 估期常见错法（Estimation Failure Modes）— 规划谬误、忘记评审/发布/联调、被压价后直接点头
- * 里程碑与可见进度（Milestones & Visible Progress）— 先打通最薄的端到端，再加厚
- * 风险登记与先做最难的（Risk First）— 把最不确定的部分前置做 spike
- * 范围谈判（Scope Negotiation）— 铁三角：时间、范围、质量，选择砍什么而非加班
- 依赖与跨团队排期（Dependencies）— 尽早提需求、写明接口与日期、设检查点
- 项目启动与收尾（Kickoff & Closeout）— 启动清单、成功标准、收尾回顾
- 优先级排序框架（Prioritization Frameworks）— 影响/成本、RICE 的用途与局限
- 技术规划与季度路线（Technical Roadmapping）— 把技术债和平台工作放进业务语言

## 四、技术决策（Technical Decisions）
- * 单向门与双向门（One-Way vs Two-Way Doors）— 可逆性决定决策速度和评审重量
- * 自建还是采购（Build vs Buy）— 核心差异化自建；总拥有成本；退出成本
- * 技术债（Technical Debt）— 有意与无意；"利息"才是关键；何时还、何时不还
- * 迁移（Migrations）— 先双写/影子、再灰度、最后下线旧的；不可能一次切完
- * 选型与简单优先（Choose Boring Technology）— 创新预算；团队能运维的才是好技术
- 决策的取舍表达（Articulating Trade-offs）— 说清放弃了什么，而不仅仅选了什么
- 过度工程与过早优化（Over-engineering）— 为未来需求设计的代价
- 重写还是重构（Rewrite vs Refactor）— 为何重写常常失败，何时合理
- 技术战略（Technical Strategy）— 诊断、指导原则、一致的行动（Rumelt 框架；Larson 应用）
- 平台与复用的经济学（Platform Economics）— 何时抽象成共享组件，何时复制

## 五、可靠性与事故（Reliability & Incidents）
- * 事故指挥（Incident Command）— 角色：指挥、通讯、执行；先止血后找因
- * 无责复盘（Blameless Postmortem）— 结构、时间线、贡献因素、行动项；避免"人为错误"作为根因
- * 值班实践（On-Call Practice）— 交接、手册（runbook）、负载上限、疲劳管理
- * SLO 与错误预算（SLOs & Error Budgets）— 用预算来决定发布与可靠性工作的权衡
- 事故沟通（Incident Communication）— 对内对外更新频率、措辞、不确定时怎么说
- 行动项的落实（Postmortem Action Items）— 为什么大多数复盘无效：行动项没有负责人和截止日
- 变更管理与发布风险（Change Risk）— 大多数事故来自变更；灰度、开关、回滚
- 告警质量（Alert Quality）— 可操作、症状导向、减少噪声
- 容量与韧性的预先思考（Pre-mortems）— 事前验尸：假设失败再倒推原因

## 六、协作与影响力（Collaboration & Influence）
- * 无权力的影响（Influence Without Authority）— 先建立信用、对齐动机、让对方赢
- * 建立共识与分歧处理（Alignment & Disagreement）— 先问清真正的分歧点；用数据和实验；升级的时机
- * 分歧后承诺（Disagree and Commit）— 表达、记录、执行；不消极抵抗
- * 跨团队合作（Cross-team Work）— 对方的目标与约束；写下约定；别绕过
- * 向上管理（Managing Up）— 让上级少意外：节奏、期望对齐、带方案提问
- 赞助与导师（Sponsorship vs Mentorship）— 谁在会议室里替你说话
- 反馈：给与收（Feedback）— 具体、行为、影响；接收时先复述
- 困难的人与冲突（Difficult Conversations）— 事实、感受、请求；私下先谈
- 会议与决策机制（Meeting Hygiene）— 目的、议程、结论、负责人
- 异步沟通与远程协作（Async & Remote）— 默认写作；时区约定

## 七、质量与评审（Quality & Review）
- * 代码评审的目的与优先级（Code Review Goals）— 正确性、设计、可读性、风格；速度也是质量（→ 见 low-level-design review）
- * 写和接受评审意见（Giving & Receiving Review）— 提问式、区分必须与建议、小 PR
- * 测试策略（Test Strategy）— 测试金字塔、风险驱动、什么不该测
- * 质量的成本与时机（Cost of Quality）— 越早发现越便宜；左移
- 可观测性是设计的一部分（Observability by Design）
- 技术债的度量（Quality Metrics）— DORA 四项、变更失败率、恢复时间
- 评审他人设计（Design Review as Reviewer）— 提问清单：失败模式、规模、回退

## 八、带人（Growing Others）
- * 指导（Mentoring）— 提问多于给答案；委托而非接管；设定成长目标
- * 新人上手（Onboarding）— 第一周清单、第一个 PR、文档化隐性知识
- * 面试别人（Interviewing Others）— 设计结构化问题、评分表、避免偏差、写评语
- * 委托与放手（Delegation）— 交付结果而非步骤；检查点；承受别人做得不同
- 提升团队而不是自己（Raising the Bar）— 模板、工具、评审标准
- 给出有难度的绩效反馈（Hard Feedback）— 尽早、具体、可改变

## 九、业务与成本（Business & Cost）
- * 把技术工作翻译成业务价值（Business Value Framing）— 收入、成本、风险、速度
- * 云成本意识（Cloud Cost Awareness）— 单位经济、成本归因、何时优化值得
- * 为什么做：问题先于方案（Problem Before Solution）— 先验证需求，再设计
- 度量与实验（Metrics & Experiments）— 先定成功指标，A/B 的陷阱
- 看懂公司的钱（How the Company Makes Money）— 收入模型、毛利、对工程优先级的影响
- 客户与支持的反馈回路（Customer Feedback Loop）

## 不收（out of scope）
- 管理者技能（招聘流程、绩效校准、预算）— 属 EM 路线，非 IC 资深；只收"面试别人"与"带人"的 IC 部分
- 具体技术深度（分布式、数据库）— 已有各技术领域
- 个人故事与经历库 — 面试时由 Chi 自选；本域只给故事"类型"
- 求职谈判与晋升 — 归 `career`
- 沟通与英语表达 — 归 `tech-comm`

## 与已有领域的重叠
- narrative `themes.conflict` / `themes.influence` / `themes.mentoring` / `themes.ambiguity` / `themes.prioritization` / `themes.disagree-and-commit` — go deeper：narrative 讲"怎么讲故事"，本域讲"这样做事的原则"；本域每叶只给故事类型并 link 过去，不重复 STAR 技巧。narrative 已退役（卡片已删），可吸收其 summary。
- narrative `round.seniority-ladder` — link 到"资深到底看什么"，本域负责内容。
- cdn-content `reliability.slos`、`reliability.incidents`、`reliability.alerting` — link：技术细节（SLI 选择、burn-rate）留在那里；本域只讲方法（事故指挥角色、复盘文化、值班负载），go deeper 在人与流程。
- test-release（发布 SLO 一叶）、cdn-content `delivery.canary/rollback` — skip（技术机制）；"变更风险"叶仅 link。
- low-level-design `review.*`（priorities, comments, approval-bar, small-changes）— skip 评审技术叶；本域只留"评审目的与文化 / 评审他人设计"，link 过去。
- sysdesign：设计文档里的"取舍表达"与系统设计面试的取舍叶相近 — link。

## 卡片格式建议
- 正面：一个处境问题（"同事想一周重写服务，你怎么办？"），不要问定义。
- 背面固定五段：**原则**（一句话）/ **怎么做**（3–5 步或清单）/ **常见错法**（2–3 条反模式，各带后果）/ **面试官在考什么**（一个信号：如 scope、judgment、ownership）/ **配哪类故事**（只写类型，如"一次你主动叫停的项目"）。
- 凡含数字（如 SRE 值班负载上限、DORA 基准）必须当场查证并留痕。
- 至少 25% 卡片带图：决策树（单向/双向门）、事故时间线、RFC 生命周期状态机、估期漏斗。
