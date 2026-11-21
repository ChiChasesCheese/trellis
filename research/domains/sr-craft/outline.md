# Sr 工作方法（Senior Engineering Craft）

术语规则：技术术语一律用英文原词，正文用中文（Chi 2026-11-20）

> 每个叶子都是一条通用原则。卡片统一带：原则 / 怎么做 / 常见错法 / 面试官考什么 / 配哪类故事。`*` = 帕累托核心。

## 一、Scope & seniority
- * Scope, Autonomy, Impact：资深到底看什么 — 各家职级表（ladder）的共同维度，及 Sr 与 Mid 的本质差别：不是写得更快，而是能处理更模糊、更大的问题 〔出处：se-guidebook Ch.1 §2 Typical Software Engineering Career Paths、§5 Alternative Ways to Think About Career Progress；Part V 引言 Role-Model Staff and Principal Engineers〕
- * Taming ambiguity — 澄清目标、列假设、做最小实验、定"做到什么算够" 〔出处：se-guidebook Ch.15 §2 Prototyping and Proof of Concept；Ch.16 §3 Project Kickoffs and Milestones〕
- * Owning outcomes — 对结果负责到上线之后；看指标不看工单关闭 〔出处：se-guidebook Ch.11 §1 Getting Things Done: Perception and Reality、§4 The Big Picture〕
- Staff archetypes — Larson 四类：Tech Lead / Architect / Solver / Right Hand，各自怎么工作 〔出处：se-guidebook Ch.22 §4 Collaborating with Staff+ Peers（Larson 四类）；Ch.25 §9 Software Architect Traits〕
- Glue work — 看不见的协调工作：何时做、怎么让它被看见、何时停 〔出处：se-guidebook Ch.3 §2 The Power of Habit（"Capture work you do to help others"，引 Reilly《Being Glue》）〕
- Being the strongest — 不做瓶颈：放大别人而不是亲自全做 〔出处：se-guidebook Ch.11 §3 Your Team；Ch.12 §3 Mentoring〕
- Picking battles — 哪些值得坚持、哪些值得让步 〔出处：se-guidebook Ch.22 §1 Internal Politics；Ch.7 §1 Focus on the Most Important Piece of Work（部分）〕

## 二、Writing
- * Design doc — 目的：在写代码前以低成本发现错误；结构：背景、目标/非目标、方案、替代方案、风险 〔出处：se-guidebook Ch.15 §1 Design Documents, RFCs and Architecture Documents〕
- * Goals & non-goals — 非目标要写成"别人可能合理期待但我们不做"的事 〔出处：无书，https://www.industrialempathy.com/posts/design-docs-at-google/（Ch.15 §1 泛讲设计文档，未单列 non-goals）〕
- * Alternatives considered — 至少一个认真的替代方案，写清为什么没选 〔出处：se-guidebook Ch.15 §1（部分）；另见 https://www.industrialempathy.com/posts/design-docs-at-google/〕
- * RFC process — 提案、评论期、决议、状态；Rust RFC / Python PEP / K8s KEP 的共同骨架 〔出处：se-guidebook Ch.15 §1；Ch.19 §2 Team Processes（部分）〕
- * ADR（Architecture Decision Record） — 一页：背景、决定、后果；只记难以回退的决定；不可改历史，只能被取代 〔出处：se-guidebook Ch.15 §1（ADR 段）；另见 https://adr.github.io〕
- When not to write a design doc — 方案显然、可逆、成本低时 〔出处：se-guidebook Ch.15 §1（部分）〕
- * Status updates — 结论先行、红黄绿的含义、风险与请求放最前 〔出处：se-guidebook Ch.16 §5 Day-to-Day Project Management；Ch.18 §4 Keep Them in the Loop〕
- Doc review & lifecycle — 谁评审、何时关闭、如何保持更新、归档 〔出处：se-guidebook Ch.13 §4 Documentation；Ch.15 §1〕
- One-pager for leadership — 问题、建议、代价、需要的决定（需先: Status updates） 〔出处：se-guidebook Ch.18 §4 Keep Them in the Loop（部分）〕
- Working backwards：PR/FAQ — 先写新闻稿和常见问题再开工 〔出处：无书，https://www.amazon.jobs/en/principles（《Working Backwards》为商业书，未入库）〕

## 三、Planning & milestones
- * Work breakdown — 按可验证的竖切片拆，而不是按层；每块 1–3 天可交付 〔出处：se-guidebook Ch.7 §3 Break Down the Work〕
- * Estimation — 范围而非点；已知/未知；乘数；估期是沟通工具不是承诺 〔出处：se-guidebook Ch.7 §4 Estimate the Duration of Your Work；Ch.16 §4 "Software Project Physics"〕
- * Estimation failure modes — 规划谬误、忘记评审/发布/联调、被压价后直接点头 〔出处：se-guidebook Ch.16 §4 "Software Project Physics"；Ch.7 §4〕
- * Milestones & visible progress — 先打通最薄的端到端，再加厚 〔出处：se-guidebook Ch.16 §3 Project Kickoffs and Milestones、§5 Day-to-Day Project Management〕
- * Risk first — 把最不确定的部分前置做 spike 〔出处：se-guidebook Ch.16 §6 Risks and Dependencies；Ch.15 §2 Prototyping and Proof of Concept〕
- * Scope negotiation — 铁三角：时间、范围、质量，选择砍什么而非加班 〔出处：se-guidebook Ch.16 §4 "Software Project Physics"（范围、时间、质量的取舍）〕
- Dependencies — 尽早提需求、写明接口与日期、设检查点 〔出处：se-guidebook Ch.16 §6 Risks and Dependencies〕
- Kickoff & closeout — 启动清单、成功标准、收尾回顾 〔出处：se-guidebook Ch.16 §3 Project Kickoffs and Milestones、§7 Wrapping Up Projects〕
- Prioritization frameworks — 影响/成本、RICE 的用途与局限 〔出处：se-guidebook Ch.7 §1 Focus on the Most Important Piece of Work（部分，书中未讲 RICE）；RICE 另见 https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/〕
- Technical roadmapping — 把技术债和平台工作放进业务语言 〔出处：se-guidebook Ch.21 §1 Northstars, KPIs, OKRs；Ch.25 §7 Architecture Decisions vs Business Priorities（部分）；crafting-engineering-strategy Ch.10 Operations（部分）〕
- Software project physics — 范围、时间、人手的硬约束；与估期、范围谈判呼应 〔出处：se-guidebook Ch.16 §4 Software Project Physics〕
- Prototyping & proof of concept — 什么时候做、做到多粗、怎么丢掉 〔出处：se-guidebook Ch.15 §2 Prototyping and Proof of Concept〕

## 四、Technical decisions
- * One-way vs two-way doors — 可逆性决定决策速度和评审重量 〔出处：se-guidebook Ch.25 §4 One-Way Door vs Two-Way Door Decisions〕
- * Build vs buy — 核心差异化自建；总拥有成本；退出成本 〔出处：crafting-engineering-strategy Ch.22 Developer API and acquisition strategy at Stripe（收购与自建，部分）；另见 https://www.joelonsoftware.com/2001/10/14/in-defense-of-not-invented-here-syndrome/（书中仅 Ch.24 一笔带过）〕
- * Technical debt — 有意与无意；"利息"才是关键；何时还、何时不还 〔出处：se-guidebook Ch.13 §3 Tech Debt；Ch.25 §3 Architecture Debt〕
- * Migrations — 先双写/影子、再灰度、最后下线旧的；不可能一次切完 〔出处：se-guidebook Ch.25 §4（迁移与单向门）、§3 Architecture Debt；Ch.13 §3 Tech Debt（部分）；crafting-engineering-strategy Ch.16 Service migration strategy〕
- * Choose boring technology — 创新预算；团队能运维的才是好技术 〔出处：se-guidebook Ch.25 §1 Keep It As Simple As Possible；Ch.13 §1 Languages, Platforms, and Domains〕
- Articulating trade-offs — 说清放弃了什么，而不仅仅选了什么 〔出处：se-guidebook Ch.25 §7 Architecture Decisions vs Business Priorities；Ch.16 §4（部分）〕
- Over-engineering — 为未来需求设计的代价 〔出处：se-guidebook Ch.25 §1、§6 Scalable Architecture〕
- Rewrite vs refactor — 为何重写常常失败，何时合理 〔出处：se-guidebook Ch.25 §3 Architecture Debt（重写段）；Ch.9 §3 Refactoring〕
- Technical strategy — 诊断、指导原则、一致的行动（Rumelt 框架；Larson 应用） 〔出处：crafting-engineering-strategy Ch.5–12（explore → diagnose → refine → policy → operate）；另见 https://lethain.com/eng-strategies/（Larson 的 Engineering Strategy 系列 lethain.com；Rumelt《Good Strategy Bad Strategy》）〕
- Platform economics — 何时抽象成共享组件，何时复制 〔出处：se-guidebook Ch.5 §2 Platform Teams；Ch.25 §6 Scalable Architecture（部分）；crafting-engineering-strategy Ch.20 Service architecture strategy（部分）〕
- Readable strategy docs — 策略文档怎么写得让人读完：先结论、政策与诊断分开 〔出处：crafting-engineering-strategy Ch.11 Writing readable engineering strategies〕
- Strategy testing — 先在小范围试行策略，再推广 〔出处：crafting-engineering-strategy Ch.13 Strategy testing for iterative refinement〕
- Systems modeling — 用存量与流量的模型推演决策后果 〔出处：crafting-engineering-strategy Ch.14 Systems modeling〕
- Wardley maps — 按演化阶段画价值链，判断该自建还是采购 〔出处：crafting-engineering-strategy Ch.15 Wardley maps〕
- LLM adoption strategy — 团队引入大模型的策略怎么定 〔出处：crafting-engineering-strategy Ch.17 LLM adoption strategy〕
- Blast radius of decisions — 与单向门互补：不可逆之外，影响面也决定评审重量 〔出处：se-guidebook Ch.25 §5 The Blast Radius of Decisions〕
- Architecture debt vs tech debt — 区分代码债与架构债，两者的利息和偿还方式不同 〔出处：se-guidebook Ch.25 §3 Architecture Debt〕
- Simplicity — 为什么简单是可靠性与可维护性的前提；支持“选型与简单优先”与“过度工程” 〔出处：Google SRE book《Simplicity》sre.google/sre-book/simplicity/（未入本地库）〕

## 五、Reliability & incidents
- * Incident command — 角色：指挥、通讯、执行；先止血后找因 〔出处：se-guidebook Ch.24 §6 Incident Management（#2 Fix it：角色与止血）；Google SRE book《Managing Incidents》sre.google/sre-book/managing-incidents/（未入本地库）〕
- * Blameless postmortem — 结构、时间线、贡献因素、行动项；避免"人为错误"作为根因 〔出处：se-guidebook Ch.24 §6（#3 Follow-up、Blameless reviews）；Google SRE book《Postmortem Culture: Learning from Failure》sre.google/sre-book/postmortem-culture/（未入本地库）〕
- * On-call practice — 交接、手册（runbook）、负载上限、疲劳管理 〔出处：se-guidebook Ch.24 §5 Oncall（轮值、手册、烦躁与倦怠）；Google SRE book《Being On-Call》sre.google/sre-book/being-on-call/（未入本地库）〕
- * SLOs & error budgets — 用预算来决定发布与可靠性工作的权衡 〔出处：Google SRE book《Service Level Objectives》sre.google/sre-book/service-level-objectives/（未入本地库）（已在 sources/outlines/sre-book.yaml 列入）；Google SRE book《Embracing Risk》sre.google/sre-book/embracing-risk/（未入本地库）（错误预算）〕
- Incident communication — 对内对外更新频率、措辞、不确定时怎么说 〔出处：se-guidebook Ch.24 §6（Declaring an incident 与角色）；Google SRE book《Managing Incidents》sre.google/sre-book/managing-incidents/（未入本地库）〕
- Postmortem action items — 为什么大多数复盘无效：行动项没有负责人和截止日 〔出处：se-guidebook Ch.24 §6（Incident follow-up actions）；Google SRE book《Postmortem Culture》sre.google/sre-book/postmortem-culture/（未入本地库）〕
- Change risk — 大多数事故来自变更；灰度、开关、回滚 〔出处：se-guidebook Ch.17 §3 Principles and Tools、§4 Additional Verification Layers、§5 Taking Pragmatic Risks〕
- Alert quality — 可操作、症状导向、减少噪声 〔出处：se-guidebook Ch.24 §4 Alerting（precision / recall、Alert noise）；Google SRE book《Monitoring Distributed Systems》sre.google/sre-book/monitoring-distributed-systems/（未入本地库）〕
- Pre-mortems — 事前验尸：假设失败再倒推原因 〔出处：se-guidebook Ch.15 §4 Software Architecture That Ships（pre-mortem 练习）；Ch.24 §7 Building Resilient Systems〕
- Release spectrum — 从直接上线到重重关卡的两个极端，按风险选发布方式 〔出处：se-guidebook Ch.17 §1–§2、§7〕
- Eliminating toil — 识别、度量并自动化重复性运维，是资深工程师的杠杆来源 〔出处：Google SRE book《Eliminating Toil》sre.google/sre-book/eliminating-toil/（未入本地库）〕
- Embracing risk — 可靠性目标为什么不是 100%；与 SLO 与错误预算相连但不等同 〔出处：Google SRE book《Embracing Risk》sre.google/sre-book/embracing-risk/（未入本地库）〕
- Effective troubleshooting — 假设驱动的单人排障方法 〔出处：Google SRE book《Effective Troubleshooting》sre.google/sre-book/effective-troubleshooting/（未入本地库）〕
- Emergency response — 故障案例的经验：先止血、别慌、事前演练 〔出处：Google SRE book《Emergency Response》sre.google/sre-book/emergency-response/（未入本地库）〕
- Tracking outages — 把事故变成可统计的数据来驱动改进 〔出处：Google SRE book《Tracking Outages》sre.google/sre-book/tracking-outages/（未入本地库）〕
- Testing for reliability — 与测试策略相邻，面向生产可靠性 〔出处：Google SRE book《Testing for Reliability》sre.google/sre-book/testing-reliability/（未入本地库）〕
- Release engineering — 与变更管理互补，偏流程与工具 〔出处：Google SRE book《Release Engineering》sre.google/sre-book/release-engineering/（未入本地库）〕

## 六、Collaboration & influence
- * Influence without authority — 先建立信用、对齐动机、让对方赢 〔出处：se-guidebook Ch.22 §2 Influencing Others；Ch.12 §6 Influencing Others〕
- * Alignment & disagreement — 先问清真正的分歧点；用数据和实验；升级的时机 〔出处：se-guidebook Ch.22 §1–§2；Ch.18 §5 Problematic Stakeholders〕
- * Disagree and commit — 表达、记录、执行；不消极抵抗 〔出处：se-guidebook Ch.22 §1 Internal Politics（"Have Backbone; Disagree and Commit"）〕
- * Cross-team work — 对方的目标与约束；写下约定；别绕过 〔出处：se-guidebook Ch.12 §5 Working with Other Engineering Teams；Ch.20 §5 Relationships with Other Teams〕
- * Managing up — 让上级少意外：节奏、期望对齐、带方案提问 〔出处：se-guidebook Ch.2 §5 Make Your Manager an Ally；Ch.22 §3 Collaborating with Managers〕
- Sponsorship vs mentorship — 谁在会议室里替你说话 〔出处：se-guidebook Ch.22 §6 Helping Others（Sponsor others）；Ch.12 §3 Mentoring〕
- Feedback — 具体、行为、影响；接收时先复述 〔出处：se-guidebook Ch.12 §4 Giving Feedback；Ch.2 §4 Ask and Give Feedback〕
- Difficult conversations — 事实、感受、请求；私下先谈 〔出处：se-guidebook Ch.12 §4 Giving Feedback（部分）；Ch.20 §2 Unhealthy Teams（部分）〕
- Meeting hygiene — 目的、议程、结论、负责人 〔出处：无书，https://handbook.gitlab.com/handbook/company/culture/all-remote/meetings/（书中仅零散提及会议）〕
- Async & remote — 默认写作；时区约定 〔出处：无书，https://handbook.gitlab.com/handbook/company/culture/all-remote/asynchronous/〕
- Stakeholder management — 干系人类型、识别、保持知情、难缠干系人；补向上管理与状态更新之外的主线 〔出处：se-guidebook Ch.18 Stakeholder Management〕
- Internal politics — 怎么读组织政治、怎么不被拖进去（“选择战场”之外） 〔出处：se-guidebook Ch.22 §1 Internal Politics〕
- Team health & dynamics — 健康/不健康团队的信号、成长期的痛点、团队流程；Sr 常被要求诊断团队 〔出处：se-guidebook Ch.19–20〕

## 七、Quality & review
- * Code review goals — 正确性、设计、可读性、风格；速度也是质量（→ 见 low-level-design review） 〔出处：se-guidebook Ch.12 §1 Code Reviews〕
- * Giving & receiving review — 提问式、区分必须与建议、小 PR 〔出处：se-guidebook Ch.12 §1 Code Reviews〕
- * Test strategy — 测试金字塔、风险驱动、什么不该测 〔出处：se-guidebook Ch.14 §1–§4（尤其 §4 Mental Models for Automated Testing）〕
- * Cost of quality — 越早发现越便宜；左移 〔出处：se-guidebook Ch.14 §7 Benefits and Drawbacks of Automated Testing；Ch.17 §4 Additional Verification Layers〕
- Observability by design 〔出处：se-guidebook Ch.24 §2 Logging、§3 Monitoring〕
- Quality metrics — DORA 四项、变更失败率、恢复时间 〔出处：se-guidebook Ch.17 §3 Principles and Tools（DORA 段，作者本人对其持保留态度）〕
- Design review as reviewer — 提问清单：失败模式、规模、回退 〔出处：se-guidebook Ch.15 §1（设计文档的反馈与评审）（部分）〕
- Testing in production & specialised testing — 灰度、影子流量、混沌类测试 〔出处：se-guidebook Ch.14 §5–§6〕
- Compliance, privacy & secure development — 资深工程师被默认要懂的合规、隐私与安全开发 〔出处：se-guidebook Ch.23 §5–§6〕

## 八、Growing others
- * Mentoring — 提问多于给答案；委托而非接管；设定成长目标 〔出处：se-guidebook Ch.12 §3 Mentoring；Ch.7 §5 Seek Mentors〕
- * Onboarding — 第一周清单、第一个 PR、文档化隐性知识 〔出处：se-guidebook Ch.13 §4 Documentation、§5 Scaling Best Practices Across the Team（部分）；Ch.6 §6 Onboarding to a New Job（新人视角）〕
- * Interviewing others — 设计结构化问题、评分表、避免偏差、写评语 〔出处：无书，https://rework.withgoogle.com/guides/hiring-use-structured-interviewing/steps/introduction/（Ch.6 §3 只讲应聘者一侧）〕
- * Delegation — 交付结果而非步骤；检查点；承受别人做得不同 〔出处：se-guidebook Part IV 引言与 Ch.16（部分）〕
- Raising the bar — 模板、工具、评审标准 〔出处：se-guidebook Ch.13 §5 Scaling Best Practices Across the Team〕
- Hard feedback — 尽早、具体、可改变 〔出处：se-guidebook Ch.12 §4 Giving Feedback（部分）〕

## 九、Business & cost
- * Business value framing — 收入、成本、风险、速度 〔出处：se-guidebook Ch.21 §1–§3（Northstars/KPIs/OKRs、Your Team and Product、Your Company）〕
- * Cloud cost awareness — 单位经济、成本归因、何时优化值得 〔出处：无书，https://www.finops.org/introduction/what-is-finops/（书中仅 Ch.21/Ch.23 一笔带过）〕
- * Problem before solution — 先验证需求，再设计 〔出处：se-guidebook Ch.21 §2 Your Team and Product；Ch.5 §1 Product Teams and Product-Minded Engineers〕
- Metrics & experiments — 先定成功指标，A/B 的陷阱 〔出处：se-guidebook Ch.23 §2 Helpful Engineering Processes（实验、A/B）；Ch.21 §1〕
- How the company makes money — 收入模型、毛利、对工程优先级的影响 〔出处：se-guidebook Ch.21 §3 Your Company、§4 Public Companies、§5 Startups〕
- Customer feedback loop 〔出处：se-guidebook Ch.21 §2 Your Team and Product；Ch.5 §1〕

## 不收（out of scope）
- 管理者技能（招聘流程、绩效校准、预算）— 属 EM 路线，非 IC 资深；只收"Interviewing others"与"带人"的 IC 部分
- 具体技术深度（分布式、数据库）— 已有各技术领域
- 个人故事与经历库 — 面试时由 Chi 自选；本域只给故事"类型"
- 求职谈判与晋升 — 归 `career`
- 沟通与英语表达 — 归 `tech-comm`

## 与已有领域的重叠
- narrative `themes.conflict` / `themes.influence` / `themes.mentoring` / `themes.ambiguity` / `themes.prioritization` / `themes.disagree-and-commit` — go deeper：narrative 讲"怎么讲故事"，本域讲"这样做事的原则"；本域每叶只给故事类型并 link 过去，不重复 STAR 技巧。narrative 已退役（卡片已删），可吸收其 summary。
- narrative `round.seniority-ladder` — link 到"Scope, Autonomy, Impact"，本域负责内容。
- cdn-content `reliability.slos`、`reliability.incidents`、`reliability.alerting` — link：技术细节（SLI 选择、burn-rate）留在那里；本域只讲方法（事故指挥角色、复盘文化、值班负载），go deeper 在人与流程。
- test-release（发布 SLO 一叶）、cdn-content `delivery.canary/rollback` — skip（技术机制）；"Change risk"叶仅 link。
- low-level-design `review.*`（priorities, comments, approval-bar, small-changes）— skip 评审技术叶；本域只留"Code review goals / Design review as reviewer"，link 过去。
- sysdesign：设计文档里的"Articulating trade-offs"与系统设计面试的取舍叶相近 — link。

## 卡片格式建议
- 正面：一个处境问题（"同事想一周重写服务，你怎么办？"），不要问定义。
- 背面固定五段：**原则**（一句话）/ **怎么做**（3–5 步或清单）/ **常见错法**（2–3 条反模式，各带后果）/ **面试官在考什么**（一个信号：如 scope、judgment、ownership）/ **配哪类故事**（只写类型，如"一次你主动叫停的项目"）。
- 凡含数字（如 SRE 值班负载上限、DORA 基准）必须当场查证并留痕。
- 至少 25% 卡片带图：决策树（单向/双向门）、事故时间线、RFC 生命周期状态机、估期漏斗。

## 书里有、大纲没有

已并入（2026-11-20）。

## 大纲有、书里没有

共 8 叶没有任何一本对应的书覆盖（总 93 叶；另有 15 叶只被书部分覆盖，已在叶尾标"部分"）。

- Goals & non-goals
- Working backwards：PR/FAQ
- Build vs buy
- Technical strategy
- Meeting hygiene
- Async & remote
- Interviewing others
- Cloud cost awareness
