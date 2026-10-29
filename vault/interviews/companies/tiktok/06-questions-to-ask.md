# 06 · 反问清单（ByteDance Global Payment · FPS）

反问有两个用途：拿到只有对方知道的信息（级别、轮次、团队在做什么），以及表明你懂这个团队的业务。对面是谁决定你该问什么：招聘官管流程和级别，写代码的同事知道日常工作和值班，设计轮的面试官知道系统的真实难点，HM 决定级别和你进组后做什么，HR 管薪酬。这份清单按对象分组，每个问题写了为什么问、好答案和坏答案各说明什么。每场最后只有 3–5 分钟，挑 **2–3 个**；单个回答只是线索，面试官是一个人，不代表整个组。

## 怎么用

- 招聘官的问题要在**第一轮之前**问完：级别和轮次一旦定下，后面很难改。最好的办法是周四晚上发一封邮件（模板在 A 节末尾）。
- 面试官那几轮，至少问一个关于**他自己**经历的问题（「你最近一次……」），比「团队文化怎样」得到的信息多。
- 优先级：招聘官问级别和设计轮；同事问值班和上线；设计面试官问对账和故障；HM 问范围和级别标准；HR 问 RSU 变现。
- 薪资、签证不问面试官和 HM，只问招聘官和 HR。

---

## A · 招聘官（第一轮之前）

### 1. 级别，以及要求按 2-2 面

> "Which level is this requisition open at? I'd like to be considered for 2-2. Could the loop be the 2-2 loop, including a system design round?"

- **为什么问**：这个 req 的区间从入门覆盖到 senior。级别由面试表现和名额决定，而没有系统设计轮的面试，结果通常封顶在 2-1。要 2-2，必须在开始前提出来。
- **好答案**：给出级别区间，并答应安排设计轮。
- **坏答案**：「级别看面试表现」，且不提设计轮。追一句：「Would adding a design round be possible if the first rounds go well?」

### 2. 一共几轮，每轮是什么

> "Could you walk me through the rounds — how many, what each one covers, and who the interviewers are?"

- **为什么问**：这个部门的面试有编码、后端基础（八股）、支付系统设计、类设计、项目深挖、HM 几种组合；轮次一轮一轮地约，有时同一天加轮。
- **好答案**：轮数、每轮类型、每轮的面试官角色（同事、tech lead、HM）。
- **坏答案**：「每个面试官不一样」。那就三类都准备，并在每轮开头问面试官这一小时怎么安排。

### 3. 周一这一轮的形式

> "For Monday's round, which platform will we use — HackerRank or Lark — and should I expect a resume discussion before coding? Will I need to write my own test cases?"

- **为什么问**：编码平台没有现成的测试用例，要自己写、自己跑；开头常有一段简历拷问。知道形式才能按考场条件练。
- **好答案**：平台、时长、是否有简历讨论、是否需要运行代码。
- **坏答案**：说不清。按「HackerRank、没有用例、先聊项目 15 分钟」准备。

### 4. 有没有 AI 辅助编码轮

> "Does any round use an AI-assisted format, where I share my own IDE with an AI tool? If so, what's expected — working code, tests, or both?"

- **为什么问**：有的团队开始用这种形式：用你自己的 IDE 和 AI 工具现场实现一个小系统，评分看能跑的代码和**写完的测试**。没准备的人常常测试写不完。
- **好答案**：明确说有或没有；有的话，说明允许的工具和评分重点。
- **坏答案**：不确定。按「允许 AI，但测试必须写完」准备一次。

### 5. 面试官在哪里，用什么语言

> "Will my interviewers be based in the US, or in Singapore or China? I'm comfortable interviewing in English or Mandarin."

- **为什么问**：在亚洲的面试官更常问八股，轮次可能排在美国晚上；每一轮可以选语言。主动说你两种都可以，是加分项。
- **好答案**：说明面试官的位置和时间安排。
- **坏答案**：回避。那就为晚上的轮次和中文口述各准备一次。

### 6. 雇主实体和团队

> "Is the employer ByteDance Inc.? And within Financial Product and Solution, which product and which markets would I work on — PayLater, credit, insurance, or wallet?"

- **为什么问**：FPS 的产品都在美国以外上线，你要知道自己给哪个市场、哪个产品写系统，才能在面试里把例子说对。合资公司的支付团队是另一条线，不要混。
- **好答案**：实体、具体产品、市场。
- **坏答案**：「进来再定」。说明 req 是一个池子，会有组匹配。

### 7. 换组时通过的轮次保留吗

> "If the team's headcount changes during the process, do the rounds I've passed carry over to another Global Payment team?"

- **为什么问**：req 中途关闭、转到别的组重新面都很常见。
- **好答案**：有明确规则。
- **坏答案**：不确定。心里做好重面的准备。

### 发给招聘官的邮件（周四晚上发）

> Hi [Name], thank you for scheduling Monday's round. A few questions so I can prepare well:
> 1. Which level is this role open at? I'd like to be considered for 2-2 — could the loop include a system design round?
> 2. How many rounds are there in total, and what does each cover?
> 3. For Monday: HackerRank or Lark, and should I expect a resume discussion before coding?
> 4. Is there an AI-assisted coding round in this loop?
> 5. Which product and markets within Financial Product and Solution is this role for?
> Thanks, Chi

---

## B · 写代码的同事（编码、八股、项目深挖）

### 8. 值班

> "What does an on-call week look like for the team, and what was the last incident that was hard to debug?"

- **为什么问**：职位说明写「线上问题定位」；你想知道值班负担，也想听到一个真实的排查。你的值班经历在这里能自然接上。
- **好答案**：轮值方式、一次真实的事故、根因落在哪一层。
- **坏答案**：想不起最近一次。

### 9. 一个改动怎么上线

> "How does a change to the money path go from code to production — reviews, feature flags, how you roll back?"

- **为什么问**：钱的路径上，上线方式就是质量控制。你在 PayPal 用「部署和放开分开」的开关上线，可以接话。
- **好答案**：灰度、开关、对账校验、回滚步骤。
- **坏答案**：「测完就上」。

### 10. 和其他时区怎么协作

> "How does the team split work with colleagues in Singapore and China, and how many evening meetings are typical in a week?"

- **为什么问**：部门的重心在新加坡，汇报线可能在亚洲；强度和边界是真实问题，这样问听起来是在规划。
- **好答案**：固定的重叠时段、文档先行、每周几次。
- **坏答案**：「随时」。

### 11. 技术栈和上手

> "What's the day-to-day stack — mostly Go? How long does it usually take a new engineer who comes from Java to ship their first change?"

- **为什么问**：你主要写 Java 和 Python，入职要上手 Go 和内部中间件。
- **好答案**：语言、框架、新人上手的具体做法。
- **坏答案**：没有上手的安排。

---

## C · 系统设计面试官

### 12. 对账发现差异之后

> "When reconciliation finds a mismatch between your ledger and a PSP or bank, what happens next — who looks at it, and how long until it's resolved?"

- **为什么问**：对账是你的强项，问这个等于告诉对方你知道真正的难点在差异处理，不在匹配。
- **好答案**：差异分类、自动修复的边界、人工队列、时限。
- **坏答案**：「很少出差异」。

### 13. 最近一次推翻的设计

> "What's a design decision the team reversed in the last year, and what made you change your mind?"

- **为什么问**：设计面试官是写系统的人，这能听到真实的取舍。
- **好答案**：具体案例和原因（规模、故障、牌照、成本）。
- **坏答案**：「没有什么大的」。

### 14. 新市场上线

> "When the team launches a product in a new market, what changes in the system — currency, licence, data location, the funding partner?"

- **为什么问**：FPS 的产品按市场逐个上线，每个市场带来新的币种、牌照和资金方。这个问题显示你懂多市场的约束。
- **好答案**：配置化的部分、需要改代码的部分、合规检查。
- **坏答案**：每个市场都重写一遍。

---

## D · Hiring manager

### 15. 前六个月的成功

> "What would success look like for someone in this role after six months, and how would you measure it?"

- **为什么问**：HM 定级别；你想知道他期待的范围是否配得上你的故事。
- **好答案**：具体的交付物和指标。
- **坏答案**：「看你的表现」。

### 16. 2-1 和 2-2 的区别

> "On your team, what separates a 2-1 engineer from a 2-2?"

- **为什么问**：你拿到他的定级标准，同时提醒他你在按 2-2 面。
- **好答案**：范围、独立推进、跨团队影响、设计评审这类具体维度。
- **坏答案**：没有标准。

### 17. 这半年的重点

> "What are the team's top priorities this half — new markets, new products, or stability — and where would this role fit?"

- **为什么问**：把岗位和真实的路线图连起来，也能听出组是在扩张还是在维护。
- **好答案**：两三个具体重点，岗位怎么接上。
- **坏答案**：说不清路线图。

### 18. 美国团队的决策权

> "Which decisions does the San Jose team own, and which are made with the teams in Singapore or China?"

- **为什么问**：决策权决定你的 ownership 空间，也决定晚上要开多少会。
- **好答案**：说清哪些本地决定。
- **坏答案**：「都由总部决定」。

---

## E · HR（薪酬与流程）

### 19. 薪酬结构

> "Could you walk me through the full package — base, target bonus, RSU amount and vesting schedule, and sign-on?"

- **为什么问**：总包由 base、奖金、RSU、签字费组成；RSU 有 4 年和 3 年两种归属方式。
- **好答案**：每一项都给数字，包括归属比例和 cliff。
- **坏答案**：只给 base。

### 20. RSU 怎么变现

> "Since the shares aren't publicly traded, how do buybacks work — what was the most recent price, and is there a cap on how much of each vested tranche I can sell?"

- **为什么问**：股票只能在公司回购时卖出，近年授予的股票可能限制每次可卖的比例。不问清，RSU 的数字没有意义。
- **好答案**：最近一次回购价、频率、可卖比例。
- **坏答案**：说不清。按保守值估算这一块。

### 21. 定级和组匹配

> "How are the level and the team decided after the interviews, and what happens if the team only has headcount at a different level?"

- **为什么问**：这是整个流程最不透明的一步。
- **好答案**：清晰的步骤和时间。
- **坏答案**：「会再通知你」。

### 22. 到岗要求

> "What is the in-office expectation for this team — five days a week? And is the role based in San Jose or Seattle?"

- **为什么问**：TikTok 美国多数员工已经每周 5 天到岗；ByteDance Inc. 的支付组是否一样，要问清。
- **好答案**：天数和地点。
- **坏答案**：「看组里」。

---

## 不问

- 薪资、签证：不问面试官和 HM。
- 合资公司的政治背景、牌照的监管细节：不主动提。
- 支付量、收入这类内部数字：对方不一定能说，问了显得不懂分寸。
- 「需要会中文吗」：不问面试官；你已经在招聘官那里说过两种语言都可以。

## 收尾一句（每轮）

> "Thank you — this was really helpful. What you said about [他真的说过的一件事] makes me even more interested in [具体一点]."

方括号里填他在这一小时里**真的说过**的一件事，不要提前写好。
