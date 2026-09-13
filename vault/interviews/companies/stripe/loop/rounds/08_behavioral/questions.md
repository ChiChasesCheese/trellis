# Behavioral 轮 —— 题库（去重，50 题：28 Stripe 一手 + 22 跨公司迁移练习）

> 来源：`loop/raw/hr_hm_behavioral.md` §Behavioral/Culture 轮 + §其他公司行为面框架。
> 形式：45–60 分钟，HM 或 "Leveler"（类比 Amazon Bar Raiser）主持；"behavioral 评估贯穿每一轮"。
> 练习：`python3 loop/mock.py bq behavioral -n 5`。
>
> **两个题库分区说明**：第一部分（28 题）是 Stripe 一手报道的原题，直接来自求职网站/Blind 面经，
> 权重最高，必须全部覆盖。第二部分（22 题）是 Amazon/Google/Meta/通用行为面框架里的题目，
> `loop/raw/hr_hm_behavioral.md` 把它们和 Stripe 题目并列收录在同一张"题库总表"里，作为
> **跨公司迁移练习**——同样的 STAR-L 故事换个问法练一遍，能检验故事是否够灵活。**这些不是
> Stripe 一手报告的原题**，bank.json 里每条都标了真实来源（如 DesignGurus/ophyai/interviewing.io
> Meta），不会跟第一部分混淆。

## 一、Stripe 一手题库（28 题，按主题分组）

### Ownership / 端到端负责（4 题）

| 问题原文 | 来源 | 考什么 | 踩雷点 |
|---|---|---|---|
| "Tell me about a time you owned a project from start to finish" | codinginterview.com | Deliver outstanding results | "我负责的那部分完成了"≠端到端 |
| "Tell me about a time you took full ownership of a project from start to finish." | The Interview Guys(2026) | 同上 | 同上 |
| "Describe a moment where something broke, and you stepped in, even though it wasn't your responsibility" | codinginterview.com | Users first + 主动性 | 讲成"被要求"而非主动 |
| "Tell me about a project: how did you ideate it, pitch it, break it down, minimize risk, and manage stakeholder relationships and deadlines?" | Glassdoor[搜索摘要] | 端到端 + 干系人管理 | 漏讲 pitch/风险控制环节 |

### 模糊 / 紧迫（4 题）

| 问题原文 | 来源 | 考什么 | 踩雷点 |
|---|---|---|---|
| "Tell me about a time you made a decision with incomplete information" | codinginterview.com | 模糊决策 | 假装信息完整 |
| "Describe a time when you had to make a high-stakes decision with incomplete information." | The Interview Guys | 同上，且要求"高风险" | 案例赌注不够大 |
| "Describe a situation where everything felt urgent—how did you prioritize?" | codinginterview.com | 排序逻辑 | 没有明确排序标准 |
| "Tell me about a time you managed competing priorities under a tight deadline." | The Interview Guys | 同上 | "competing"体现不出来 |

### 技术判断 / Rigor（4 题）

| 问题原文 | 来源 | 考什么 | 踩雷点 |
|---|---|---|---|
| "Walk me through a complex technical decision you made" | codinginterview.com | trade-off 推理 | 无 alternatives |
| "Walk me through a complex decision you made and how you evaluated alternatives" | Dataford[搜索摘要] | 同上，明确要 alternatives | 只讲结论 |
| "Tell me about a time you changed your mind after gathering new information" | codinginterview.com | Rigor + humility | "从没改变过想法" |
| "Tell me about a time you changed your mind after digging into the data." | Dataford[搜索摘要] | 数据驱动 | 没有具体数据点 |

### 冲突 / 分歧（6 题）

| 问题原文 | 来源 | 考什么 | 踩雷点 |
|---|---|---|---|
| "Tell me about a disagreement with another engineer–how did you handle it?" | codinginterview.com | Collaborate egolessly | 把对方说成笨蛋 |
| "Describe a time when you had conflict and how you worked to resolve it." | Exponent 博客 | 同上 | 冲突"消失"而非解决 |
| "Discuss a time when you disagreed with a team decision. What did you do about it?" | Prepfully | 同上 | 团队决定被说成愚蠢 |
| "Tell us about a time you had a difference of opinion with a team member. How did you resolve it?" | InterviewKickstart | 同上 | 无最终共识 |
| "Tell me about a time you disagreed with a technical decision." | The Interview Guys | Backbone + egoless | 只有 backbone 没有共识 |
| "Tell me about a time you had conflict with your manager." | Blind kt6bwgwv | 沟通方式；**真实案例因用术语被拒** | 堆砌技术术语 |

### 失败 / 反思 / 反馈（4 题）

| 问题原文 | 来源 | 考什么 | 踩雷点 |
|---|---|---|---|
| "Tell me about a failure–what happened, and what did you learn?" | codinginterview.com | Resilient | 失败案例太轻 |
| "Tell me about a time you made a mistake. What did you learn from it?" | Prepfully | Humble | 归因外部 |
| "How do you handle negative feedback?" | InterviewKickstart | Seek feedback | "我不需要被指正" |
| "What is something you would have done differently in a project?" | Prepfully | 反思 | "没什么要改的" |

### 质量 / 技术债（2 题）

| 问题原文 | 来源 | 考什么 | 踩雷点 |
|---|---|---|---|
| "Talk about a recent project you led. How did you uphold a high quality bar?" | Exponent 博客 | Craft | "能跑就行" |
| "Tell me about a time you had to make a technical trade-off to meet a deadline. How did you handle the technical debt later?" | Dataford[搜索摘要] | Urgency vs craft | 没讲后续还债 |

### 其他（4 题）

| 问题原文 | 来源 | 考什么 | 踩雷点 |
|---|---|---|---|
| "Tell me about a time you solved your most complex problem." | Exponent 博客 | Rigor + perseverance | 问题深度不够 |
| "What does Stripe's mission mean to you personally?" | The Interview Guys | Macro-optimistic | 空喊口号，无具体细节 |
| "Describe your last strategic hire. What made them the strategic hire?" | Exponent 博客（EM 岗） | Obsess over talent | IC 可换成面试/内推经历 |

---

## 二、跨公司迁移练习（22 题，非 Stripe 一手；每题已标真实来源）

### Amazon 16 Leadership Principles（每条 1 题，覆盖全部 16 条）

| 问题原文 | 对应 LP | 来源 |
|---|---|---|
| "Describe a time when you went above and beyond for a customer." | Customer Obsession | DesignGurus(2026-04-08) |
| "Tell us about a time when you took ownership of a project and its outcome." | Ownership | DesignGurus |
| "Tell us about a time when you simplified a complex process." | Invent and Simplify | DesignGurus |
| "Give an example of when you admitted to being wrong and learned from it." | Are Right, A Lot | DesignGurus |
| "Describe a time you learned a new skill or technology to solve a problem." | Learn and Be Curious | DesignGurus |
| "Describe a situation where you mentored or coached a team member." | Hire and Develop the Best | DesignGurus |
| "Describe a time when you raised the bar for your team." | Insist on the Highest Standards | DesignGurus |
| "Give an example of a calculated risk that paid off." | Think Big | DesignGurus |
| "Describe a time when you had to make a quick decision with limited information." | Bias for Action | DesignGurus；Exponent Amazon Guide |
| "Describe a project where you had to accomplish more with less." | Frugality | DesignGurus |
| "Tell us about a situation where you had to repair a damaged professional relationship." | Earn Trust | DesignGurus |
| "Give an example of when you identified the root cause of a complex issue." | Dive Deep | DesignGurus |
| "Describe a time when you disagreed with a decision and voiced your concerns." | Have Backbone; Disagree and Commit | DesignGurus |
| "Describe a time when you delivered a significant result under challenging circumstances." | Deliver Results | DesignGurus |
| "Tell us about a situation where you prioritized employee well-being." | Strive to be Earth's Best Employer | DesignGurus |
| "Describe a time when you made a decision that took into account the broader implications." | Success and Scale Bring Broad Responsibility | DesignGurus |

### Google / Meta / 通用（6 题）

| 问题原文 | 框架 | 来源 |
|---|---|---|
| "Tell me about a time you had to make progress on something with no clear direction." | Google Googleyness | ophyai(2026-07-24) |
| "Walk me through how you approached a problem you had never seen before." | Google GCA | ophyai(2026-07-24) |
| "Tell me about a time you influenced a decision without authority." | Google Leadership | ophyai(2026-07-24) |
| "Tell me about a time you needed to overcome external obstacles to complete a task or project." | Meta Perseverance | interviewing.io Meta |
| "Tell me about a person or team who you found most challenging to work with." | Meta Resolving Conflicts | interviewing.io Meta |
| "Why do you want to leave your current/last company?" | 通用 | Tech Interview Handbook |

---

## 真实失败案例（练习时对照，不是题目）

- Amazon 员工 $270K TC，技术轮都好，behavioral 讲的故事"not that good"、HM 频繁打断换题 → 被拒。（Blind wexjj3xy）
- L4 技术全过，behavioral **用了技术术语** → candidate review 拒。（Blind kt6bwgwv）
- Adaptability 轮"举的例子面试官无法理解/共鸣" → 拒。
- 全程 vibe 很好仍被拒——"一票 lukewarm 即拒"是真实机制，不是传说。（Blind vpdsosjj）
