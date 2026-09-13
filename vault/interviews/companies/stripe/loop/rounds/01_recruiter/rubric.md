# Recruiter 电话 —— 自评表

> 依据：`loop/LOOP_GUIDE.md` §1、`loop/raw/hr_hm_behavioral.md` §Recruiter 电话。
> Stripe 内部对每轮打 **1–4 分书面反馈**，Hiring Committee 汇总时**"一个 lukewarm 即拒"**
> （Blind vpdsosjj："they want all thumbs up ... even if one interviewer is lukewarm on
> the candidate, they reject."）——recruiter 轮虽然非正式，但 ophyai 明确说
> **"cultural alignment is a hard filter, not a tiebreaker"**，所以这轮也要按 1–4 分自查，
> 不要因为"只是聊聊"就放松。

## 用法

1. 用 `python3 loop/mock.py bq recruiter -n 3` 抽 3 题，对着计时器口头回答（每题 60–90 秒）。
2. 录音回放，或找人听，按下面 5 个维度打分（1–4）。
3. **任何一个维度打 2 分及以下，视为整轮 lukewarm——回去重讲，不要跳过。**

## 评分维度

### 1. 表达清晰度 / 结构化程度
> 来源：Exponent SWE Guide——"clear, structured communication"。

| 分数 | 长什么样 |
|---|---|
| **1 分** | 想到哪说到哪，没有明显的开头/中间/结尾；30–60 秒的目标时长说成了 3 分钟还没说完重点。 |
| **2 分** | 有大致结构，但中间跑题或反复补充遗漏信息。 |
| **3 分** | 结构清楚（背景→做了什么→结果），时长基本控制住。 |
| **4 分** | 一开口就让人知道"接下来要听什么"；30–60 秒内讲完一个完整故事，无需追问就能听懂重点。 |

### 2. Why Stripe 的具体性
> 来源：ophyai——"a specific answer to 'Why Stripe?'... not just 'I want to work at a
> top company'"；TechPrep——要体现"understand its API-first philosophy"。

| 分数 | 长什么样 |
|---|---|
| **1 分** | "Stripe 是家好公司/大公司"，或复述招聘页文案，无个人角度。 |
| **2 分** | 提到了具体产品（Payments/Billing/Connect），但没讲清楚这对你意味着什么。 |
| **3 分** | 能讲出一个你用过/读过的 Stripe API 或文章，并连到自己的经历。 |
| **4 分** | 能具体讲出"increase the GDP of the internet"这个使命对你的实际含义，且举证是你真研究过（读过官方 blog、用过 API、关注过具体产品线）。 |

### 3. 经历叙述的相关性
> 来源：Exponent——"relevant technical experience"；InterviewKickstart 原题库。

| 分数 | 长什么样 |
|---|---|
| **1 分** | 讲的项目和岗位方向（支付基础设施/后端）关系不大，或讲不清自己的角色。 |
| **2 分** | 相关，但停留在"做了什么"，不涉及"为什么重要"。 |
| **3 分** | 讲清楚项目背景、你的角色、一个亮点结果。 |
| **4 分** | 3 分基础上，还能主动连到"这段经历为什么让我适合 Stripe 的这个方向"。 |

### 4. Culture-fit 信号密度
> 来源：Exponent——"signals of ownership, user focus, and craftsmanship"。

| 分数 | 长什么样 |
|---|---|
| **1 分** | 整段回答里挑不出一个 ownership/user focus/craftsmanship 的具体细节。 |
| **2 分** | 有一个信号，但一带而过。 |
| **3 分** | 至少 2 个信号清晰可辨（比如提到了主动修复非本职问题 + 提到了对用户影响）。 |
| **4 分** | 3 个信号都在，且是具体动作而非形容词自夸（不是"我很有责任心"，是"我在 xxx 情况下做了 xxx"）。 |

### 5. 谈判纪律
> 来源：interviewing.io——此阶段不要透露薪资期望，也不要提在面的其他公司。

| 分数 | 长什么样 |
|---|---|
| **1 分** | 主动报出具体薪资数字，或主动列出正在面的其他公司名单。 |
| **2 分** | 被问到时报了具体数字/公司名，但没有意识到这不是最优策略。 |
| **3 分** | 被问到时用"looking for a competitive offer，想先了解完整 package"类似话术带过。 |
| **4 分** | 不仅带过，还借机把话题引回"团队匹配/时间线"这类对自己更有利的信息收集方向。 |

## 打分表（每轮练习填一次）

| 日期 | 抽到的题 | 表达清晰度 | Why Stripe | 经历相关性 | Culture-fit 信号 | 谈判纪律 | 最低分（=整体判定） |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |

**判定规则**：五个维度取**最低分**作为这轮的整体判定——因为真实机制是"一票 lukewarm 即拒"，
不是平均分及格就行。
