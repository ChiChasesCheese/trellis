# LP 题库（按 16 条 LP；每题映射到最佳故事）

> 题目写法：按 Amazon 常见问法撰写（**推断**，沿用社区里 "Tell me about a time…" 的固定句式；本次没有逐字抓取面经，所以不当作"真题"引用）。官方只确认：每位面试官通常问 2–3 个行为题，以 STAR + 数据回答（<https://amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep>，2026-10-15）。
> **bar = senior**：每个 LP 前的 *Senior angle* 写明面试官在 senior 档会往哪里深挖：ambiguity、无权威的跨团队影响、超出任务的 ownership、机制（不是一次性英雄行为）、数据权衡、拉高水平、与资深干系人 disagree-and-commit。
> 故事编号见 `story_matrix.md`；开场一句与追问见 `stories/Sx_*.md`。`【待 Chi 补】` 的故事在补完前**不要**口播相关数字。
> 约定：*Best* = 首选；*Backup* = 同一面试官面前已用过 Best 时换；*Fallback* = 没有合适故事时的诚实答法（`00_how_lp_works.md` §7）。

---

## LP1 · Customer Obsession
*Senior angle：你怎么发现客户没说出来的问题？为客户牺牲过短期目标吗？「客户」可以是商户，也可以是下游团队；先说清是谁。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 1.1 | Tell me about a time you went above and beyond for a customer. | **S4** | S9 | "It wasn't my ticket; I owned the answer." 三团队 50 条回复，一条查询结束 |
| 1.2 | Describe a time you had to deal with a difficult customer situation. | **S9** | S4 | ~$4M 出款"不见了"；先区分预期延迟 vs 回归 |
| 1.3 | Tell me about a time you identified a customer problem before the customer reported it. | **S3** | S10 | 我建的健康检查先于商户发现费用静默缺失 |
| 1.4 | Tell me about a time you had to balance a customer's needs against a technical constraint. | **S9** | S5 | revert 快 vs region conditional 稳；净额窗口 vs 费用到达时间 |
| 1.5 | How did you use customer feedback to change what you built? | R3（**需补**） | S4 | 【待 Chi 补：Aiki 用户反馈驱动的具体改动】；补不出就用 S4 |

**Fallback：** "Most of my customers are internal — merchants through downstream teams and the payout service. The clearest case where I worked backwards from a merchant's problem is [S4/S9]."

## LP2 · Ownership
*Senior angle：没人派你的事、跨团队的事、做到「不再复发」而不是修一次。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 2.1 | Tell me about a time you took on something outside your responsibilities. | **S7** | S8 | 无 ticket；两个 agent 撞 DDL；ADR；个人仓库的边界要说清 |
| 2.2 | Describe a project you owned end to end. | **S1** | S5 | stub → 设计 → 上线 → 18 个月 on-call → EU 扩展 |
| 2.3 | Tell me about a time you sacrificed a short-term result for long-term value. | **S3** | S6 | 止血之后继续做结构性修复；S6 叫停短期"快赢" |
| 2.4 | Tell me about a time you took ownership of a problem that wasn't yours. | **S6** | S4 | 接手离职实习生的项目；先救不可再生的标注 |
| 2.5 | Tell me about a time you took responsibility for a mistake. | **S10** | S2 | 公开收回自己的数字 |

**Fallback：** 不需要——LP2 有 5 个 primary。注意同一面试官面前不要连用 S1 和 S3。

## LP3 · Invent and Simplify
*Senior angle：简化的是「机制」（别人不再需要你）而不是一段代码；说出被否决的备选。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 3.1 | Tell me about a time you simplified a complex process. | **S2** | S5 | 每表一个校验 task → 插一行配置 |
| 3.2 | Tell me about something you invented or built that nobody asked for. | **S7** | R1 | 零拷贝克隆池；tech lead of a team of agents |
| 3.3 | Describe a time you challenged the way things had always been done. | **S5** | S2 | 静态拆分 vs 更聪明的运行时 fallback |
| 3.4 | Tell me about a creative solution you found under tight constraints. | **S6** | S7 | Phase 1 纯 SQL 规则推进，ML 放门后 |

**Fallback：** 不需要。

## LP4 · Are Right, A Lot
*Senior angle：不是"我总是对"，而是你如何找反证、如何校准、错了怎么办。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 4.1 | Tell me about a time you made a decision with incomplete information. | **S5** | S6 | discovery → 影子核对 → toggle 默认关，让不确定性可观测 |
| 4.2 | Tell me about a time you were wrong. | **S10** | S2 | 196K → 21,923；自己发现 |
| 4.3 | Describe a time you changed your mind based on new evidence. | **S2** | S10 | 发现自己框架的粒度错了，写 ADR |
| 4.4 | Tell me about a judgment call that others disagreed with. | **S6** | S9 | go/no-go；region conditional |
| 4.5 | How do you seek out views that disconfirm your own? | **S2** | R1 | ADR 四方案；双关卡 + 实验账本 |

**Fallback：** 不需要。

## LP5 · Learn and Be Curious
*Senior angle：你学到的东西是否转成了团队能力？学习路径是系统的还是随机的？*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 5.1 | Tell me about a time you had to learn something new quickly. | **R2**（需补） | S7 | 【待 Chi 补：AI-native 迁移的学习曲线】；S7：零拷贝克隆 + Deployments API |
| 5.2 | Describe something you taught yourself recently and how you applied it. | **R1**（需补） | S11 | purged CV / DSR / PBO；【待 Chi 补：学习路径】 |
| 5.3 | Tell me about a time you improved after feedback. | **S2** | S10 | 对自己的抽象用 review 别人代码的严格度 |
| 5.4 | How do you stay current with technology? | R2 / S7 | — | 并行用 Claude Code / Codex / Cursor 并有 usage 上限意识；AWS DVA-C02 证书（简历） |

**Fallback：** "Most of my learning has been on the job: Snowflake internals — streams, zero-copy clones, micro-partitions — [S7]."

## LP6 · Hire and Develop the Best
*Senior angle：带人的可见产出 + 你让团队标准变高的机制。这条是当前最薄的 LP。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 6.1 | Tell me about a time you mentored someone. | **M1**（需补） | S6（接手实习生项目） | 契约先行；【待 Chi 补：被带者的结果】；**不编 1:1** |
| 6.2 | Describe a time you raised the performance bar on your team. | **S2** | M1 | 框架使"最省事的路径"=标准做法；ADR |
| 6.3 | Tell me about a time you helped someone grow. | **M1** | — | 同 6.1 |
| 6.4 | Tell me about a time you gave tough feedback. | — | — | 【待 Chi 补：无素材】 |

**Fallback：** "I haven't run a formal mentoring program. The way I raise the bar is through mechanisms — the quality-check framework eight subject areas use, the ADRs, and the onboarding doc I've maintained since 2024 — and I've defined the contracts for a newer engineer's three projects. Let me tell you about that last one."（说完就讲 M1，不道歉三次。）

## LP7 · Insist on the Highest Standards
*Senior angle：你的标准高于流程要求；修到「不再复发」，并写下机制。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 7.1 | Tell me about a time you refused to lower your standards. | **S3** | S6 | 不压掉检查；不让 ACH 进排除名单 |
| 7.2 | Describe how you ensured a problem stayed fixed. | **S3** | S8 | 单函数 + versioned DROP + e2e；扫全仓库 |
| 7.3 | Tell me about a time you raised quality standards for a team. | **S2** | R1 | 握手变 SQL 硬条件；strictest wins |
| 7.4 | Tell me about a time you found a defect others missed. | **S10** | S3 | 谓词缺"时间有效性"；e2e 的四个缺口 |

**Fallback：** 不需要。

## LP8 · Think Big
*Senior angle：你提出的方向是否更大、有数据支撑、有人跟着走？当前 employer 证据薄。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 8.1 | Tell me about a time you thought bigger than the task you were given. | **S2** | S8 | 不是 feature，是别人往上接的平台；全仓库扫描 |
| 8.2 | Describe a bold idea you proposed. | **R1**（个人） | S7 | 一个平台、四个市场；【待 Chi 补：employer 里的更大方向】 |
| 8.3 | Tell me about a time you created a vision that others followed. | **S2** | S7 | 【待 Chi 补：谁跟着你的框架/工具走】 |
| 8.4 | How have you looked around corners for your customers? | **S5** | S3 | 费用赶不上净额窗口 → 提前切数据源 |

**Fallback：** "The biggest-scope thing is S2/S5; my boldest independent project is R1 — a platform where a new market is a thin adapter. I want to be honest that R1 is a personal project."

## LP9 · Bias for Action
*Senior angle：不是"快"，是在可逆性分析下的 calculated risk，并说明你如何限制下行。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 9.1 | Tell me about a calculated risk you took. | **S5** | S7 | shipped dark：toggle 默认关 → pre-prod → prod；deploy ≠ release |
| 9.2 | Describe a time you had to decide quickly with limited information. | **S8** | S3 | 7 分钟根因；邻近模块核查 |
| 9.3 | Tell me about a time you acted without waiting for approval. | **S7** | S8 | 个人仓库，无 ticket；S8 问了一句可否推 PR（不是未经批准） |
| 9.4 | Tell me about a time you had to choose between speed and thoroughness. | **S6** | S8 | 反向：叫停快赢；先救标注 |
| 9.5 | How do you decide when to act and when to wait? | **S5** | S6 | 可逆 → 先动；不可逆 → 影子核对 |

**Fallback：** 不需要，但 S7/S8 scope 偏小，senior 面试官会追问更大的风险；用 S5 做主答案。

## LP10 · Frugality
*Senior angle：具体的资源数字（算力、行数、基础设施、人周）。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 10.1 | Tell me about a time you accomplished more with less. | **S2** | S7 | 复用结果表，零新基础设施，只存失败行（~80 万 vs 240 万行） |
| 10.2 | Describe a time you had limited resources or time. | **S7** | S6 | 零拷贝克隆约 2 秒、不拷数据；S6 把 2–3 个月放到门后 |
| 10.3 | Tell me about a time you reduced cost or complexity. | **S1** | S5 | `STREAM_HAS_DATA` 不为空输入起 warehouse；窗口化 ON 使扫描量恒定 |
| 10.4 | Tell me about a time you decided not to build something. | **S6** | S2 | Phase 2 在 gate 之后；否决 VARIANT / 新表 |

**Fallback：** 不需要，但缺成本数字：【待 Chi 补：任何一个 credit / 时间 / 行数的具体节省】。

## LP11 · Earn Trust
*Senior angle：对更资深的人坦率；公开自批；让别人能独立验证你。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 11.1 | Tell me about a time you made a mistake and how you handled it. | **S10** | S2 | 先在公开线程收回数字，并排放两版查询 |
| 11.2 | Describe a time you had to deliver bad news. | **S10** | S9 | "I'd rather retract my own number…" |
| 11.3 | Tell me about a time you earned the trust of people who were skeptical. | **S4** | S5 | 可复跑的查询；影子核对 |
| 11.4 | Tell me about a time you were candid when it was uncomfortable. | **S3** | S2 | 数字写下来，不加排除；对自己的设计写 ADR |
| 11.5 | How do you build trust with other teams? | **S5** | S4 | 把方法沉淀为模板，下次不用重新发明信任 |

**Fallback：** 不需要。

## LP12 · Dive Deep
*Senior angle：你下到哪一层（行、函数、查询）？metrics 与 anecdote 不一致时你做什么？*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 12.1 | Tell me about a time you dove deep to find a root cause. | **S3** | S8 | 切片 → 单笔 → 回溯 → 读两个重载 |
| 12.2 | Describe a time when the data and the anecdote disagreed. | **S4** | S10 | PM 说没有退款费 vs 百万行 vs 0；196K vs 22K |
| 12.3 | Tell me about the most complex problem you've debugged. | **S3** | S1 | NULL 拼接；overload 覆盖 |
| 12.4 | Tell me about a time you audited something and found a problem. | **S10** | S8 | 重审谓词；扫 79 个资源找到 42 |
| 12.5 | How do you verify that a system is correct? | **S1** | S5 | 行/批/对账三层；同一份 SQL 既验证又生产 |

**Fallback：** 不需要。

## LP13 · Have Backbone; Disagree and Commit
*Senior angle：与更资深的人分歧；决定做出后全力执行。这条的"commit"一半目前没有故事。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 13.1 | Tell me about a time you disagreed with a decision made by your manager or a senior stakeholder. | **S3** | S9 | "有人建议加排除名单，我用数字说不"——**要补谁提的、最后怎么定的** |
| 13.2 | Tell me about a time you disagreed with a decision and committed anyway. | 【待 Chi 补】 | S9 | 缺：被否决后全力执行的故事。候选：S5 选 B 时有人倾向 A？S2 评审？S9 revert vs conditional（若方案被采纳则不是 commit） |
| 13.3 | Tell me about a time you pushed back on a deadline or a plan. | **S6** | S3 | 冻结告警/CI 工作，直到 gate 给 go |
| 13.4 | Tell me about a time you stood alone in a room. | **S3** | S6 | 【待 Chi 补：当时是否只有你一人坚持】 |
| 13.5 | Tell me about a time you challenged the team's approach and were not backed. | 【待 Chi 补】 | — | 缺 |

**Fallback（13.2）：** "My strongest examples are cases where I held a position and the group agreed with me. I want to be honest that I don't have a clean story where I lost the argument and then committed. The closest is [S9: I argued for the region conditional over a revert]." ——**只讲真实发生过的**；补到真实素材之前不要编"如果输了我会…"的假设。优先在 Day 1–2 从 S5 / S9 / S2 的评审里挖（见 `drill.md`）。

---

## LP14 · Deliver Results
*Senior angle：带数字，含障碍与代价，"despite setbacks"。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 14.1 | Tell me about your most significant accomplishment. | **S1** | S5 | ~22M 笔、最大单 PR、18 个月 |
| 14.2 | Tell me about a time you overcame obstacles to deliver. | **S5** | S1 | 费用赶不上净额窗口；13.7M 行影子核对；迟到文件教训 |
| 14.3 | Tell me about a time you delivered under a tight deadline. | **S8** | S9 | 7 分钟 → 同天三环境；三天关闭事故 |
| 14.4 | Describe a time you delivered despite ambiguity. | **S5** | S6 | 无需求文档 |
| 14.5 | Tell me about a goal you missed. | **S2** | S10 | 粒度选错，用 ADR 修；【待 Chi 补：是否有真正"错过交付日期"的例子】 |

**Fallback：** 不需要。注意简历 `$600B+` 口径（见 `story_matrix.md` §4）。

## LP15 · Strive to be Earth's Best Employer
*Senior angle：对同事成长/安全/包容的具体机制。无故事。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 15.1 | Tell me about a time you made your team's environment better for others. | **M1** | S7 | onboarding doc；schema pool 让并行开发不踩脚 |
| 15.2 | How do you help a teammate who is struggling? | M1（**需补**） | — | 【待 Chi 补】 |
| 15.3 | Describe how you've contributed to an inclusive team. | — | — | 【待 Chi 补：无素材】 |

**Fallback：** "I haven't led an initiative on this. What I've done in practice is lower the cost of joining and working on the team — the onboarding doc, the schema pool so people and agents don't collide, and blameless-style postmortems like S3's. I'd be glad to learn more about how your teams approach it."——**不要夸大**。

## LP16 · Success and Scale Bring Broad Responsibility
*Senior angle：二阶影响。无故事。*

| # | Question | Best | Backup | 切入点 |
|---|---|---|---|---|
| 16.1 | Tell me about a time you considered the broader impact of a decision. | S10（**需确认**） | S3 | 不按错误谓词过度补偿商户（Chi 需确认真实动机）；NULL 静默 = 对商户账务的二阶影响 |
| 16.2 | Describe a time you left something better than you found it. | **S3** / S1 | S7 | postmortem + 移除整类 bug；工具留给团队 |
| 16.3 | Tell me about a time you had to weigh business results against a wider responsibility. | — | — | 【待 Chi 补：无素材】 |

**Fallback：** "Working on payments, the secondary effects are on merchants' cash: a wrong fee or a late payout lands on someone's operations. That's why I treat silent failures as unacceptable [S3]. I haven't had a case with a wider societal dimension."——**只说真实的**。

---

## 通用问题（常被插入的非 LP 标题题）

| Question | Best | Backup |
|---|---|---|
| Tell me about yourself（≤ 1 分钟） | 简历主线：PayPal 费用平台 → S1 / S5 / S2 → 想做 AWS 数据服务 | — |
| Tell me about a time you failed | **S2**（自己的设计缺陷，ADR 修复） | S10 |
| What is your biggest weakness? | 【待 Chi 补：真实的，与 senior 档相关；例如 influence 的记录太少】 | — |
| Why Amazon / Why AWS Data Services? | 【待 Chi 补：由 `AGENT_RULES.md` 里的 JD 与 Chi 自己的动机组合】 | — |
