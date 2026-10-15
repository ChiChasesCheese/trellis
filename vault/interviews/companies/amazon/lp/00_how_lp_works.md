# 00 · Leadership Principles 面试是怎么运作的（教科书版，从零）

> 目标岗位：SDE I，AWS Data Services（job 10414316）；**但 Chi 的要求是永远按 senior（SDE II/III）标准准备**（`../AGENT_RULES.md` 的 "Bar: senior"），本目录所有故事和题库按 senior scope 写。Onsite 约 2026-10-20/21（推断，见 `../AGENT_RULES.md`）。
> 为什么这份是最高杠杆：Amazon 每一轮（每个面试官）都会问 LP 题，编码题之外几乎所有「软」分数都来自这里；Bar Raiser（见 §4）可以一票否决。**编码好、LP 烂 = 拒信。**
> 来源标注：`[官]` = Amazon 官方页面（抓取日 2026-10-15）；`[三方]` = 第三方转述，官方页面没有，需要保留怀疑；`推断` = 我的推论。

---

## 1. 先搞清楚：LP 是什么

Leadership Principles（LP，领导力准则）是 Amazon 公开的 16 条行为准则。它们同时是：**日常决策语言**、**绩效评估标尺**、**面试评分表（rubric）**。面试官被分配「你负责考察哪几条 LP」，然后问你过去的真实经历，从你的叙述里找「这个人的行为是否符合这条 LP」的**证据**。

- 官方页面：<https://www.amazon.jobs/content/en/our-workplace/leadership-principles>（2026-10-15 抓取，列出 16 条标题）；全文措辞见 <https://www.aboutamazon.com/about-us/leadership-principles>（仓库内存档 `vault/interviews/rounds/code-core/clippings/amazon-leadership-principles-clip.md`，clipped 2026-08-27）。
- **第 15、16 条是 2021 年新增**（推断：此前是 14 条；旧版网上面经仍会提 14 条，不影响你，只要你知道现在是 16 条）。

### 16 条官方原文 + 中文白话 + 面试官在找什么

| # | LP（官方标题） | 官方原文（节选核心句） | 白话：面试官想听到的证据 |
|---|---|---|---|
| 1 | **Customer Obsession** | "Leaders start with the customer and work backwards. They work vigorously to earn and keep customer trust." | 你从**客户的痛**倒推做事；为客户信任付出了额外代价。Chi 的「客户」= 商户 + 下游团队（出款服务等），要明说是谁。 |
| 2 | **Ownership** | "Leaders are owners. They think long term and don't sacrifice long-term value for short-term results... They never say 'that's not my job.'" | 没人派你，你也去做；做到「事情长期不再出问题」，不止修眼前这一次。 |
| 3 | **Invent and Simplify** | "Leaders expect and require innovation and invention from their teams and always find ways to simplify." | 你把复杂的东西变简单 / 造了新东西；不是「我们用了 X 技术」。 |
| 4 | **Are Right, A Lot** | "Leaders are right a lot. They have strong judgment and good instincts. They seek diverse perspectives and work to disconfirm their beliefs." | 判断力 + **主动找反证**。关键词是 disconfirm：你怎么发现自己可能错了。 |
| 5 | **Learn and Be Curious** | "Leaders are never done learning and always seek to improve themselves. They are curious about new possibilities and act to explore them." | 你主动学了一个不会的东西，并**用上了**。 |
| 6 | **Hire and Develop the Best** | "Leaders raise the performance bar with every hire and promotion... Leaders develop leaders and take seriously their role in coaching others." | 你带过人 / 提高过团队水平；senior 档要求：你做的机制让别人变强，而不只是你教过谁。 |
| 7 | **Insist on the Highest Standards** | "Leaders have relentlessly high standards... Leaders ensure that defects do not get sent down the line and that problems are fixed so they stay fixed." | 别人觉得够了你觉得不够；**问题修到不复发**（root cause + 防复发机制）。 |
| 8 | **Think Big** | "Thinking small is a self-fulfilling prophecy. Leaders create and communicate a bold direction that inspires results." | 你把范围想得比任务本身大，并提出了更大的方案；senior 档要求有数据支撑的大方向，且有别人跟着做。 |
| 9 | **Bias for Action** | "Speed matters in business. Many decisions and actions are reversible and do not need extensive study. We value calculated risk taking." | 信息不全时你敢先动；关键是**可逆**的决定先动，并说明风险怎么兜。 |
| 10 | **Frugality** | "Accomplish more with less. Constraints breed resourcefulness, self-sufficiency and invention." | 在资源/时间/预算限制下用更少做更多；省了什么（算力、行数、基础设施）。 |
| 11 | **Earn Trust** | "Leaders listen attentively, speak candidly, and treat others respectfully. They are vocally self-critical, even when doing so is awkward or embarrassing." | 你**公开认错**、坦诚沟通、让别人信你的数。 |
| 12 | **Dive Deep** | "Leaders operate at all levels, stay connected to the details, audit frequently, and are skeptical when metrics and anecdote differ." | 你下到最底层（具体的行、函数、查询）找到根因；数字与直觉不符时你追查。 |
| 13 | **Have Backbone; Disagree and Commit** | "Leaders are obligated to respectfully challenge decisions when they disagree, even when doing so is uncomfortable or exhausting... Once a decision is determined, they commit wholly." | 你在不舒服时提出异议，**决定做出后全力执行**（两半都要）。 |
| 14 | **Deliver Results** | "Leaders focus on the key inputs for their business and deliver them with the right quality and in a timely fashion. Despite setbacks, they rise to the occasion and never settle." | 在障碍面前仍然交付，且有数字。 |
| 15 | **Strive to be Earth's Best Employer** | "Leaders work every day to create a safer, more productive, higher performing, more diverse, and more just work environment. They lead with empathy..." | 你让同事的工作环境更好、让别人成长（onboarding、文档、安全的 on-call 环境）。 |
| 16 | **Success and Scale Bring Broad Responsibility** | "We must be humble and thoughtful about even the secondary effects of our actions... Leaders create more than they consume and always leave things better than how they found them." | 你考虑过行动的二阶影响（对用户/社区/团队的副作用）。 |

> 引用原文时以官方页面为准；上表原文节选自仓库存档，白话列是我的解释（推断）。

---

## 2. 一场 LP 面试是怎么跑的

### 2.1 形式（官方事实）

- Onsite 叫 **interview loop**：与多位在职员工**逐一单独面谈**，「each person will assess different aspects of your skills and experience」。[官] <https://amazon.jobs/content/en/how-we-hire/interview-loop>（2026-10-15）
- 官方 SDE II 备考页的写法（SDE I 页面没找到，**推断**结构相同）：loop 含 **four 55-minute interviews**；非技术能力「based off of our Leadership Principles, which different interviewers will be assigned to evaluate」；每位面试官「will typically ask two or three behavioral-based questions」；不出 brain teaser；「Use the STAR method」；答案里放 **metrics or data**，并包含 risks taken、failures、growth。[官] <https://amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep>（2026-10-15）
- 回答期待：每个 LP 题你讲一个**真实的、你亲身经历的**故事，面试官追问 5–15 分钟。

### 2.2 一轮 55 分钟里大概怎么分（推断，基于上述官方事实 + 社区常见说法）

| 时段 | 内容 |
|---|---|
| 0–5 min | 寒暄、自我介绍（往往 1 分钟 pitch，不超过 1 分钟） |
| 5–30 min | **LP 题 1–2 个**：每个故事 3–4 分钟讲述 + 追问 |
| 30–50 min | 编码 / 设计题（SDE 轮次几乎每轮都有）。有的轮次编码在前、LP 在后，顺序不固定 |
| 50–55 min | 你问面试官问题 |

**所以：每轮约 2 道 LP 题，4 轮 ≈ 8 个 LP 问题，覆盖 ≈ 6–8 个不同 LP（推断）**；面试官之间会分配不同 LP，但分配对你不可见。你的故事要能「横向复用 + 同一轮内不重复讲同一故事」。

### 2.3 题目长什么样

几乎全是**过去式行为题**：
- "Tell me about a time when you…"（最常见）
- "Give me an example of…"
- "Describe a situation where…"
- 偶尔假设题（"What would you do if…"）——Amazon 偏爱真实经历，遇到假设题，把答案落到「我以前遇到类似情况时…」。

### 2.4 STAR：结构与它的局限

**STAR** = Situation（情境）· Task（任务）· Action（行动）· Result（结果）。

- S+T 合计 **≤ 20%** 篇幅（两三句，只交代让决策变难的事实）。
- A 占 **~60%**：你**具体做了什么**，用 "I"。
- R 占 **~20%**：**带数字**的结果 + 你学到/改变了什么机制。
- 仓库里已有的叙事卡片提醒：STAR 的缺陷是「把 setup 讲太长、判断被埋没」，所以在 Action 里点名**你做的那个决定**与**你否决的备选方案**（`rounds/narrative/cards/story/nr-decision-spine.md`）。

### 2.5 追问（drilling）：为什么故事必须是真的

面试官讲完你的故事后会往下钻 2–5 层：
- "What exactly did **you** do?"（区分你和团队）
- "How did you measure that?"/"What was the baseline?"
- "What was the alternative? Why didn't you pick it?"
- "What would you do differently?"
- "What did the other person say?"

这是**真实性检验**（authenticity check）。能经得住的东西：具体的工具、你亲眼见过的数字、你先追过的错误假设、令你意外的事（`nr-deep-dive-were-you-there.md`）。**编出来的数字和故事会死在第三层追问。**

### 2.6 "I" 而不是 "we"

被评分的是**你个人**的行为。"We decided…" 让面试官无从判断你做了什么。规则：
- 团队做的事，用准确的句子**划边界**：「The stopgap was merged by a teammate; I owned the root cause and the hardening.」——主动划线比被发现夸大强（`nr-deep-dive-were-you-there.md`）。
- 动作主语用 I：I scoped / I wrote / I argued / I decided。
- 但不贬低团队：给别人 credit，同时清楚说你自己那一份。

### 2.7 数据与指标

官方明确要求「metrics or data」。一个数字要能经得住 5 个追问：基线（from what）、测量工具（how measured）、时间窗口、混杂因素（confound）、你的底线（what would make you revert）（`nr-number-survives-followup.md`）。**不知道精确值时，说量级或可数的事实，绝不编。**

---

## 3. 怎么被评分（谁、按什么、怎么汇总）

官方只说了「不同面试官评估不同方面」和「assigned LPs」。评分细节如下，**多为社区/三方说法，视为 推断**：

1. 面试官面谈中做**逐字笔记**，写成「证据」：你在每个故事里的具体行为。
2. 面试后（通常当天）面试官独立提交书面反馈 + 每个所分配 LP 的评级 + 总体 hire / no-hire 建议，先不看其他人的意见 [三方 推断]。
3. **Debrief**（汇总会）：全体面试官 + hiring manager + Bar Raiser，逐 LP 讨论证据，达成决定。
4. 评分对象是**证据的强度**：具体行动 > 泛泛的价值观；有数字 > 没数字；你是主体 > 团队是主体；有代价/失败的诚实 > 完美故事。

**对你的实际意义（因果链）**：面试官只有笔记里写下来的东西才能进 debrief → 你的故事要「容易被记录」：开头一句点题、一句数字、一个清晰的决定 → 它才能被转述给不在场的 Bar Raiser。

---

## 4. Bar Raiser 是什么

- 官方招聘页只在导语里提到 Bar Raisers（"From details on loop interviews to Bar Raisers to Candid Chats…"），没有定义。[官] <https://www.amazon.jobs/en/landing_pages/interviewing-at-amazon>（2026-10-15）
- 三方转述（**非官方，使用前请自行核对**，2026-10-15 搜索）：Bar Raiser 是受过专门训练的面试官，来自**招聘团队之外**，核心问题是「这个人会不会拉高目标团队的平均水平」；在 debrief 里被描述为**拥有否决权**（有来源说是单方否决，也有来源说是与 hiring manager 共同决定，说法不一）；他主要考察 LP 与行为能力，而不是岗位技术细节。来源：<https://www.designgurus.io/answers/detail/what-is-an-amazon-bar-raiser>、<https://www.carrus.io/blog/all-about-bar-raisers-amazons-essential-element-to-the-hiring-process>、<https://jobsbyculture.com/blog/bar-raiser-interview-process-guide-2026>。
- **你不会被告知谁是 Bar Raiser**（推断）。实操：**每一轮都按 Bar Raiser 的标准答**——故事有深度、有数字、有代价、有反思。
- 因为 BR 来自团队外，他对你的项目背景一无所知 → 你的开场必须**零术语自洽**（见 §6）。

---

## 5. 常见失败模式（以及原因 → 对策）

| 失败模式 | 为什么扣分（因果） | 对策 |
|---|---|---|
| **"We" 叙述** | 面试官看不到你个人的证据 → 无法打分 → 当作 no evidence | 每句动作用 I；团队贡献显式划线 |
| **没有数字** | 「It went well」无法评分（官方明说要 metrics） | 每个故事 ≥1 个数字；没有就用可数事实；绝不编 |
| **Situation 讲太长** | 占用你最好的注意力窗口，面试官已经走神 | S+T ≤ 20%，第一句话就是决定 |
| **故事太大、太虚（"improved the platform"）** | 无法追问 → 被怀疑是编的 | 点具体名词：表、函数、PR、时间 |
| **只讲成功** | 官方要求包含 failures、growth；没失败故事读起来像没经验或不反思 | 至少 2 个有代价的失败/错误，讲「我造成的」+「机制化改进」（S2/S10/S3） |
| **把别人当反派** | Earn Trust 失败 | 失败里主语是 you；冲突里证据说服，不是「我对他错」（`nr-conflict-ending.md`） |
| **假故事 / 夸大** | BR 的追问专门挖这个；一次被抓，整轮作废 | 只讲有证据锚点的；知道自己的 evidence boundary（各故事笔记里的 warning） |
| **同一个故事讲 3 次** | 面试官交叉比对笔记，显得库存薄 | 每轮用不同故事；同一故事最多换 LP 角度用 2 次，且不在同一面试官面前 |
| **泄漏机密 / 点名同事** | 违反信任；仓库规则也禁止 | 「a large marketplace merchant」「a teammate」 |
| **不懂 disagree and commit 的后半** | 只讲「我据理力争」，没讲「决定后我怎么全力执行」 | 见 `question_bank.md` LP13 与 `drill.md` 的补故事任务 |
| **答非所问** | 故事不在 LP 的轴上 | 先判断 LP，再选故事；答到一半发现偏了，用「Land it and pivot」（`nr-recover-wrong-story.md`） |

---

## 6. 我的 90 秒模板（Chi 版）

```
[1 句] 点题：This is a time I [LP 关键行为], on [系统一句话，零术语].
[2 句] S+T：为什么难 / 谁的问题 / 为什么是我。
[3–4 句] A：我的决定（我否决了什么备选）+ 我具体做的 2–3 件事。
[1–2 句] R：数字 + 代价。
[1 句] 机制化的收获：现在系统/流程里多了什么。
```

Bar Raiser 来自别的团队：用「Snowflake-native fee pipeline for card-network settlement」这种一句话，不要一上来讲 `MERGE` / `Stream`。面试官想往技术下钻，会问；那时才展开。

---


## 6.5 Senior 答案和 junior 答案差在哪（本目录统一标准）

Chi 的 bar 是 senior。LP 面试官在 senior 档找的不是「更难的技术」，而是五个维度上的**放大**（和 `rounds/narrative/cards/round/nr-same-story-two-levels.md` 一致）：

| 维度 | Junior 答案 | Senior 答案 |
|---|---|---|
| **Scope（范围）** | 完成分配的任务 | 自己看到问题（没人派）；范围跨团队/跨季度；含**模糊性**（没有需求文档） |
| **Influence（影响力）** | 一个行动者（我） | 需要说服**没有汇报关系**的人、甚至更资深的人；Disagree and commit 对象是 senior stakeholder |
| **Mechanism（机制）** | 修了这一次（英雄式） | 修一类：框架、模板、门禁、ADR、runbook，别人不靠你也能复用 |
| **Trade-off with data（数据权衡）** | 结果全是好处 | 明说放弃了什么、被否决的备选、用数据选；承认代价 |
| **Raising the bar（拉高水平）** | 自己做得好 | 别人因此做得更好：带教、标准、onboarding、审核习惯 |

### 并排示例（同一件事：S4 AU 退款费）

**Junior 版**
> A PM asked why Australian merchants weren't seeing Amex refund fees. I looked into it and found the pricing config was set to `partial`, so the refund logic never ran. I told the PM and a ticket was created.

问题：任务驱动、一个行动者、没有数字、没有机制、没有代价、没有影响力。

**Senior 版**
> A PM's escalation had bounced across three teams for about fifty replies, each pointing at the others. I owned the answer even though it wasn't my ticket. Instead of debating ownership I counted refund-fee rows by country: over a million in the US, zero in Australia. The cause was configuration — every Australian pricing schedule had `partial`, and the logic only fires on `full` — and I showed it predated our migration, so nobody had to defend a regression. I put the queries in the write-up so the other teams could verify me, which ended the thread the same day and became a funded feature ticket. In the same thread I said "not sure yet" on a second fee kind and gave a verification plan rather than guess.
>
> 差异：Scope（三个团队、50 条回复）· Influence（没有权威，用可复跑证据说服）· Data（百万行 vs 0）· Mechanism（写成可复跑的证据，变成功能票）· Trade-off/humility（not sure yet + 计划）。

**怎么把任何 Chi 的故事提到 senior 档：** 在 Action 里加一句「我否决的备选」、在 Result 里加「机制 / 现在流程里多了什么」、在开场说清「为什么是我（没人派/跨团队）」。每个 `stories/Sx_*.md` 末尾有 **Senior 升级点** 区块，写明这个故事目前停在哪个档、缺哪个细节（【待 Chi 补】）。

---

## 7. "I don't have a story for that" 怎么办

这是**常态**，不是失败（Chi 的覆盖空洞见 `story_matrix.md`：LP15 / LP16 无故事，LP6 / LP8 / LP5 偏薄）。按顺序用：

1. **停 3 秒，换角度（re-angle）**：同一个故事换一个决定点开讲。例如 S3 默认讲 Dive Deep，被问 Have Backbone 就从「有人建议把 ACH 加进排除名单、我坚持不压掉检查」开讲（`nr-recover-wrong-story.md`：re-aim the same story）。
2. **缩小题目**：把问题的 scale 调小到你真有的规模。「Think Big」→ 讲你把一个任务的范围从「修这一个」放大到「改框架」的瞬间。
3. **诚实坦白 + 最近的类似经历**（官方不禁止；对 BR 是正信号）：「I haven't been in exactly that situation — the closest I have is [X]. Can I tell you that one?」说完就讲，不要道歉三次。（`delivery.dont-know` 的原则：saying you have not faced that, in a way that still produces signal。）
4. **绝对不要**：编一个、把别人的故事当自己的、或说一个与问题无关的故事硬凹。

练习：每个 LP 都准备好「一句坦白 + 一个最近的相邻故事」备用答案，写在 `question_bank.md` 每个 LP 下的 "fallback" 里。

---

## 8. 自测（答案折叠）

**Q1. 一场 55 分钟的 SDE 轮次，LP 题大概占几个、时间怎么分？**
<details><summary>答案</summary>每位面试官通常 2–3 个行为题（官方 SDE II 备考页，推断 SDE I 同样），实际常见 ≈ 2 个，每个 5–10 分钟含追问，其余时间用于编码/设计和你的提问。</details>

**Q2. 下面哪一句更好？(a) "We migrated the pipeline and latency dropped." (b) "I wrote the migration plan, ran the shadow comparison, and found 0.224% row difference." 为什么？**
<details><summary>答案</summary>(b)：主语是 I，有具体行动，有数字，且数字有来源（可被追问）。(a) 面试官无法判断你做了什么。</details>

**Q3. Bar Raiser 来自哪里？为什么这对你开场的写法有影响？**
<details><summary>答案</summary>来自招聘团队之外（三方来源，非官方），不了解你的项目 → 开场必须一句话说清系统，零术语，否则他无法转述给 debrief。</details>

**Q4. "Tell me about a time you failed." 你讲了一个「最后其实结果不错」的故事。问题在哪？**
<details><summary>答案</summary>没有可命名的代价、没有你是直接原因、没有机制化改进；以 "but it worked out" 收尾会抵消整个答案（`nr-failure-or-excuse.md`）。</details>

**Q5. 被问到你完全没有故事的 LP，第一步是什么？**
<details><summary>答案</summary>换角度：从你已有故事里找一个对应该 LP 的决定点重新开讲；其次才是坦白 + 最近的类似经历。不编。</details>

**Q6. 一个数字要经得住哪几个追问？**
<details><summary>答案</summary>基线、测量工具、时间窗口、混杂因素、你的撤销底线（`nr-number-survives-followup.md`）。</details>
