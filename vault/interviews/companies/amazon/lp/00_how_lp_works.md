# LP 面试：现场规则

Amazon 的 16 条领导力准则（Leadership Principles，LP）同时是日常决策语言、绩效标尺和面试评分表。每位面试官被分配几条 LP，问你过去的真实经历，把你的行为写成「证据」，之后在汇总会上逐条讨论。Bar Raiser（来自招聘团队之外的面试官）可以否决，所以每一轮都按他的标准答。编码好、LP 弱，一样被拒。下面是你在现场执行的规则。

## 一轮长什么样

- 一次 loop 是多位面试官逐一单独面谈；每轮约 55 分钟。
- 每位面试官通常问 2–3 个行为题；常见是 2 个，每个 5–10 分钟含追问。
- 4 轮约 8 个 LP 问题，覆盖 6–8 条不同的 LP。
- 一轮的时间分配：
  - 0–5 分钟：寒暄 + 自我介绍（不超过 1 分钟）
  - 5–30 分钟：LP 题 1–2 个
  - 30–50 分钟：编码或设计题（顺序不固定）
  - 50–55 分钟：你问面试官
- 题目几乎全是过去式：`Tell me about a time when…` / `Give me an example of…` / `Describe a situation where…`。
- 遇到假设题（`What would you do if…`），把答案落到「我以前遇到类似情况时…」。
- 不会有脑筋急转弯；答案里要有 metrics、风险、失败、成长。

## 答题结构：STAR + L

- **S + T**：合计不超过 **20%**，两三句，只交代让决策变难的事实。第一句话就是点题。
- **A**：约 **60%**；你具体做了什么，主语用 I；点名**你做的那个决定**和**你否决的备选**。
- **R**：约 **20%**；带数字的结果 + 代价。
- **L**（Learning）：一句话说现在系统或流程里多了什么机制。
- 时长：
  - 90 秒版：60–90 秒
  - 2 分钟版：不超过 2:15
  - 追问：每个故事准备 5 条以上
- 90 秒模板：
  - 1 句点题：`This is a time I [LP 关键行为], on [系统一句话，零术语].`
  - 2 句 S + T：为什么难、谁的问题、为什么是我
  - 3–4 句 A：我的决定（否决了什么）+ 2–3 件具体的事
  - 1–2 句 R：数字 + 代价
  - 1 句 L：机制化的收获
- Bar Raiser 来自别的团队，不了解你的项目：开场用一句零术语介绍，例如 "Snowflake-native fee pipeline for card-network settlement"，不要一上来讲 `MERGE` / `Stream`；对方想下钻会自己问。

## 面试官在做什么（Bar Raiser 习惯）

- 逐字记笔记；只有笔记里写下的东西才进汇总会。故事要「好记录」：开头一句点题、一个数字、一个清晰的决定。
- 追问 2–5 层，是真实性检验：
  - "What exactly did **you** do?"
  - "How did you measure that? What was the baseline?"
  - "What was the alternative? Why didn't you pick it?"
  - "What would you do differently?"
  - "What did the other person say?"
- 编出来的数字和故事会死在第三层追问。
- 评分看证据强度：具体行动 > 泛泛价值观；有数字 > 没数字；你是主体 > 团队是主体；诚实的代价与失败 > 完美故事。
- 你不会被告知谁是 Bar Raiser：每一轮都按最高标准答（有深度、有数字、有代价、有反思）。

## 「I」而不是「we」

- 评分对象是你个人：动作句的主语用 I（I scoped / I wrote / I argued / I decided），动作句里 I 不少于 80%。
- 团队做的部分用准确的句子划边界：
  - "The stopgap was merged by a teammate; I owned the root cause and the hardening."
- 主动划线比被追问出来强。
- 给别人 credit，同时清楚说出你那一份。
- 不点名同事、商户、实习生：用 "a teammate"、"a large marketplace merchant"。

## 数字

- 每个故事至少 1 个数字；没有就用可数的事实；不知道精确值就说量级，绝不编。
- 一个数字要经得住 5 个追问：
  - 基线（from what）
  - 测量工具（how measured）
  - 时间窗口
  - 混杂因素
  - 你的底线（what would make you revert）

## 失败与错误的故事

- 至少备 2 个有代价的失败或错误：S2（自己的设计缺陷）、S10（收回自己的数字）、S3（e2e 的缺口）。
- 结构：主语是 you，不甩锅；讲你造成的部分；以机制化的改进收尾。
- 不要以 "but it worked out" 收尾，它会抵消整个答案。
- 冲突里用证据说服，不说「我对他错」；不把别人当反派。

## Senior 与 junior 的差别

- **Scope**：senior 自己看到问题（没人派）；范围跨团队、跨季度；含模糊性。
- **Influence**：senior 要说服没有汇报关系的人，甚至更资深的人；disagree and commit 的对象是资深干系人。
- **Mechanism**：senior 修一类（框架、模板、gate、ADR、runbook），别人不靠你也能复用。
- **Trade-off with data**：senior 说明放弃了什么、被否决的备选，并用数据选。
- **Raising the bar**：senior 让别人因此做得更好（带教、标准、onboarding、审核习惯）。
- 把任何故事提到 senior 档：
  - Action 里加「我否决的备选」
  - Result 里加「机制：现在流程里多了什么」
  - 开场说清「为什么是我（没人派 / 跨团队）」
- 示例（S4 AU 退款费）：
  - Junior："I found the config was `partial`, told the PM, a ticket was created." 任务驱动，一个行动者，无数字，无机制。
  - Senior："A PM's escalation had bounced across three teams for about fifty replies. I owned the answer though it wasn't my ticket. I counted refund-fee rows by country: over a million in the US, zero in Australia. The cause was configuration, and it predated our migration, so nobody had to defend a regression. I put the queries in the write-up so others could verify me; that ended the thread the same day and became a funded feature ticket. On a second fee kind I said 'not sure yet' and gave a verification plan."
  - 差异：Scope（三个团队、50 条回复）· Influence（无权威，用可重跑证据）· Data（百万行 vs 0）· Mechanism（可重跑查询 → 功能票）· Humility（not sure yet + 计划）。

## 没有故事的时候

- 步骤按顺序：
  - 停 3 秒，**换角度**：同一个故事换一个决定点开讲（S3 默认讲 Dive Deep；被问 Have Backbone 就从「有人建议把 ACH 加进排除名单，我坚持不压掉检查」开讲）。
  - **缩小题目**：把规模调到你真有的规模（Think Big → 你把范围从「修这一个」放大到「改框架」的那一刻）。
  - **诚实坦白 + 最近的相邻经历**："I haven't been in exactly that situation — the closest I have is [X]. Can I tell you that one?" 说完就讲，不道歉三次。
  - 讲到一半发现偏题：land it and pivot，不要道歉重来。
- 绝对不要：编一个、把别人的故事当自己的、硬凹一个无关的故事。
- 每个 LP 的坦白句写在 `question_bank.md` 的「没有合适故事时」。

## 红线

- 用 "we" 叙述 → 面试官看不到你的证据，当作没有证据。
- 没有数字 → 无法评分。
- Situation 讲太长 → 面试官走神；S + T 不超过 20%。
- 故事太虚（"improved the platform"）→ 点具体名词：表、函数、PR、时间。
- 只讲成功 → 至少备 2 个有代价的失败。
- 把别人当反派 → Earn Trust 失分。
- 假故事或夸大 → 被追问抓到，整轮作废；只讲有把握的事实。
- 同一个故事讲 3 次 → 每轮用不同故事；同一故事最多换 LP 角度用 2 次，且不在同一面试官面前。
- 泄漏机密或点名同事 → 用 "a teammate"。
- 只讲 disagree，不讲 commit → 决定后你怎么全力执行（LP13 的 commit 半边目前缺素材，见 `question_bank.md`）。
- 答非所问 → 先判断是哪条 LP，再选故事。

## 16 条 LP

| # | LP | 一句话含义 | 面试官追问什么 | 你的故事 |
|---|---|---|---|---|
| 1 | Customer Obsession | 从客户的痛倒推，为客户信任付额外代价 | 谁是客户（商户或下游团队，先说清）；你为他牺牲了什么 | S4 / S9 |
| 2 | Ownership | 没人派你也去做，做到长期不再出问题，从不说 "not my job" | 没有 ticket 的事；修一次还是修一类 | S1 / S7 / S3 |
| 3 | Invent and Simplify | 造新东西，把复杂的变简单 | 简化的是机制还是代码；被否决的备选 | S2 / S7 |
| 4 | Are Right, A Lot | 判断力 + 主动找反证（disconfirm） | 你怎么发现自己可能错；错了怎么办 | S5 / S10 / S2 |
| 5 | Learn and Be Curious | 不断学习，并用上 | 学了什么、怎么学的、用在哪 | R2 / R1（需补）、S7 |
| 6 | Hire and Develop the Best | 提高团队水平，带出下一批 leader | 带的人独立 own 了什么；你的机制 | M1（需补）、S2 |
| 7 | Insist on the Highest Standards | 标准高于流程要求，问题修到不复发 | 根因 + 防复发机制 | S3 / S2 / S10 |
| 8 | Think Big | 提出更大、有数据支撑的方向 | 方向的数据；有没有人跟着走 | S2 / S5 / R1 |
| 9 | Bias for Action | 速度重要，可逆的决定先动，calculated risk | 可逆性分析；下行怎么兜 | S5 / S8 / S7 |
| 10 | Frugality | 用更少做更多 | 具体资源数字（算力、行数、人周） | S2 / S7 / S1 |
| 11 | Earn Trust | 倾听、坦率、公开自批 | 对资深者的坦率；别人如何独立验证你 | S10 / S4 / S3 |
| 12 | Dive Deep | 下到细节，数字与直觉不符时追查 | 你下到哪一层（行、函数、查询） | S3 / S4 / S10 |
| 13 | Have Backbone; Disagree and Commit | 不舒服也提异议，决定后全力执行 | 分歧对象的资历；你怎么 commit（目前缺） | S3 / S6 |
| 14 | Deliver Results | 抓关键输入，障碍面前仍交付 | 数字、障碍、代价 | S1 / S5 / S8 |
| 15 | Strive to be Earth's Best Employer | 让同事的环境更安全、更高效、更包容 | 具体机制（onboarding、文档） | M1（需补） |
| 16 | Success and Scale Bring Broad Responsibility | 考虑行动的二阶影响，留下比发现时更好的东西 | 对用户、团队、社区的副作用 | S3 / S1 |
