# HM 轮 —— 题库（去重，30 题）

> 来源：`loop/raw/hr_hm_behavioral.md` §HM 轮。三种形态：① HM screen（onsite 前，30 min）
> ② HM chat（onsite 后终面，30–45 min，"更像 behavioral 面试，也会在这一步被拒"）
> ③ Team-match HM chat（30 min，vibe check）。练习：`python3 loop/mock.py bq hm -n 3`。
> **重要**：不写代码，但会深挖技术决策的推理过程——少用术语（Blind kt6bwgwv 有人因此被拒）。

## 一、项目深挖（8 题）

| 问题原文 | 频次 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|---|
| "Tell me about any significant project you worked on and the technical challenges you faced while working on it." | 1（转述） | Blind giqtwim6，2024-10-21 | Ownership、技术判断 | 讲不清自己具体做了什么 vs 团队做了什么 |
| "Tell me about a project: how did you ideate it, pitch it, break it down, minimize risk, and manage stakeholder relationships and deadlines?" | 1（转述） | Glassdoor Stripe SWE[搜索摘要]，访问 2026-09-01 | 端到端 ownership、风险管理、干系人沟通 | 只讲技术实现，不讲怎么"pitch"和管理干系人 |
| "Walk me through a complex technical decision you made" | 1 | codinginterview.com，访问 2026-09-01 | Rigor：决策推理过程 | "感觉应该这样做"，没有 alternatives |
| "Walk me through a complex decision you made and how you evaluated alternatives" | 1 | Dataford[搜索摘要，页面 429] | Rigor：明确要求列出被放弃的选项 | 只讲最终方案，不讲比较过程 |
| "Talk about a recent project you led. How did you uphold a high quality bar?" | 1 | Exponent 博客，2026 | Craft：具体质量手段（测试/review/监控） | "能跑就行"式回答 |
| "Tell me about a time you solved your most complex problem." | 1 | Exponent 博客，2026 | Rigor + perseverance | 选的问题技术含量不够 |
| "Tell me about a time you had to make a technical trade-off to meet a deadline. How did you handle the technical debt later?" | 1 | Dataford[搜索摘要，页面 429] | Urgency vs craft 的平衡，且要交代后续还债 | 只讲了"赶了deadline"，没讲技术债怎么处理 |
| "What is something you would have done differently in a project?" | 1 | Prepfully，2026-08-13 | Humility、反思 | 说"没有什么要改的"——反而扣分 |

## 二、分歧 / 协作（7 题）

| 问题原文 | 频次 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|---|
| "Discuss a time when you disagreed with a team decision. What did you do about it?" | 1 | Prepfully，2026-08-13 | Collaborate egolessly | 把团队决定说成"愚蠢的" |
| "Talk about a time when you had to resolve a difficult situation within the team." | 1 | Prepfully，2026-08-13 | 协作、冲突管理 | 只讲结果好，不讲过程中你具体做了什么 |
| "Tell me about a time you had conflict with your manager." | 1 | Blind kt6bwgwv，访问 2026-09-01 | 沟通、egoless；**有真实案例因在此题用技术术语被 candidate review 拒** | 堆砌技术术语；把 manager 描述成不讲理 |
| "Describe a time when you had conflict and how you worked to resolve it." | 1 | Exponent 博客，2026 | Collaborate egolessly | 冲突"消失了"没解决，只是回避 |
| "Tell me about a disagreement with another engineer–how did you handle it?" | 1 | codinginterview.com，访问 2026-09-01 | Collaborate egolessly | 讲分歧时把对方描述成笨蛋 |
| "Tell me about a time you disagreed with a technical decision." | 1 | The Interview Guys，2026-05-31 | Backbone + egoless 的平衡 | 只有 backbone 没有"最后怎么达成一致" |
| "Tell us about a time you had a difference of opinion with a team member. How did you resolve it?" | 1 | InterviewKickstart，2024-12-22 | 协作 | 同上 |

## 三、错误 / 反思 / 反馈（5 题）

| 问题原文 | 频次 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|---|
| "Tell me about a time you made a mistake. What did you learn from it?" | 1 | Prepfully，2026-08-13 | Humility、learning | 归因于外部因素，不是自己 |
| "Tell me about a failure–what happened, and what did you learn?" | 1 | codinginterview.com，访问 2026-09-01 | Resilient | 选的"失败"太轻，不痛不痒 |
| "How do you handle negative feedback?" | 1 | InterviewKickstart，2024-12-22 | Seek feedback | 说自己"从不需要被指正" |
| "Tell me about a time you changed your mind after gathering new information" | 1 | codinginterview.com，访问 2026-09-01 | Rigor、humility | 说"我从来没改变过想法"（=固执信号） |
| "Tell me about a time you changed your mind after digging into the data." | 1 | Dataford[搜索摘要，页面 429] | Rigor | 没有具体数据，只是"直觉告诉我" |

## 四、Ownership / 紧迫感 / 模糊性（7 题）

| 问题原文 | 频次 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|---|
| "Tell me about a time you owned a project from start to finish" | 1 | codinginterview.com，访问 2026-09-01 | Deliver outstanding results：端到端 | "我负责的那一部分做完了"——不是端到端 |
| "Describe a moment where something broke, and you stepped in, even though it wasn't your responsibility" | 1 | codinginterview.com，访问 2026-09-01 | Users first、主动性 | 讲成"被要求"去修，不是主动 |
| "Tell me about a time you made a decision with incomplete information" | 1 | codinginterview.com，访问 2026-09-01 | Ambiguity、urgency | 假装当时信息很完整 |
| "Describe a situation where everything felt urgent—how did you prioritize?" | 1 | codinginterview.com，访问 2026-09-01 | Urgency & focus | 没有明确的排序逻辑，只是"都做了" |
| "Tell me about a time you took full ownership of a project from start to finish." | 1 | The Interview Guys，2026 | Deliver outstanding results | 同上 |
| "Describe a time when you had to make a high-stakes decision with incomplete information." | 1 | The Interview Guys，2026 | Ambiguity、urgency | 案例赌注不够"high-stakes" |
| "Tell me about a time you managed competing priorities under a tight deadline." | 1 | The Interview Guys，2026 | Urgency & focus | 没讲清楚"competing"体现在哪 |

## 五、Why Stripe / 反问（1 题）

| 问题原文 | 频次 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|---|
| "Why Stripe? And do you have any questions for me?" | 1（转述） | Blind giqtwim6，2024-10-21，原文 "Why stripe? And any question to HM." | 动机 + 反问质量 | 没有准备反问，或反问全是薪资/福利 |

## 六、EM 岗题目（供 senior IC 参考，2 题）

| 问题原文 | 频次 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|---|
| "Describe your last strategic hire. What made them the strategic hire?" | 1 | Exponent 博客，2026 | Obsess over talent | IC 若被问到，可换成"参与面试/内推"经历 |
| "How would you handle shifting a top performer off a project they love, or resolving a conflict between two engineers?" | 1（转述） | Taro EM SF，2025-07-01 | Leadership judgment | IC 若被问到，可换成"影响他人但无正式权力"的经历 |

---

## 打分与挂点（不是题目，是评分机制，练习时对照）

- 每位面试官提交 1–4 分书面反馈；Hiring Committee 4–7 天开会。（Leon Consulting）
- **"一票 lukewarm 即拒"**：即便其他轮全 hire/strong hire，一轮 lean-no 也可能被否决（真实案例：L3 全过仍被 C-level 否决）。（Blind vpdsosjj、pGMZbjds）
- HM 会不断打断换问题——准备可被打断、能快速切换的短故事（90 秒版）。（Blind wexjj3xy）
- 拒后 recruiter 通常不给具体理由。
