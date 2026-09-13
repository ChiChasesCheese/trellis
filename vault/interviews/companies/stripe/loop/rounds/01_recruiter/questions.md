# Recruiter 电话 —— 题库（去重，14 题）

> 来源：`loop/raw/hr_hm_behavioral.md` §Recruiter 电话。形式：30 分钟电话，非技术 fit check；
> senior 岗有时由 HM 直接打；onsite 前还有第二次 30 min informational call。练习：
> `python3 loop/mock.py bq recruiter -n 5`。

## 一、动机 / Why Stripe

| 问题原文 | 频次 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|---|
| "Why Stripe?" / "What about Stripe makes you want to work here?" / "What does Stripe's mission mean to you personally?" | 3+（多站点复现） | InterviewKickstart(2024-12-22)、Prepfully(2026-08-13)、The Interview Guys(2026-05-31) | 是否只是"想进大厂"，还是真的理解 API-first 哲学和"increase the GDP of the internet"这个使命 | "I want to work at a top company" 这类空答案不够（ophyai 明确指出）；不要只说崇拜创始人 |
| "What do you know about Stripe?" / "What is your understanding of Stripe?" | 2 | Prepfully(2026-08-13)、InterviewKickstart(2024-12-22) | 对业务/产品的研究深度（Payments API、Billing 等） | 只说"处理支付的公司"这种表面回答 |
| "How did you hear about Stripe?" | 1 | InterviewKickstart(2024-12-22) | 渠道/内推信息，附带核实动机是否真实 | — |

## 二、自我介绍 / 经历

| 问题原文 | 频次 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|---|
| "Tell me about yourself." / "Walk me through your resume." | 2 | The Interview Guys(2026-05-31)、多家 prep 站汇总[搜索摘要] | 结构化表达能力（30–60 秒版本） | 讲成流水账；超过 90 秒还没讲到重点 |
| "Talk about a project you're most proud of." | 2 | Prepfully(2026-08-13)、InterviewKickstart(2024-12-22) | 讲项目的基本能力，为后续 HM 深挖埋伏笔 | 挑一个太浅的项目，后面 HM 深挖时接不住 |
| "Tell me about your background, your distributed-systems experience, why Stripe, and your salary expectations and timeline." | 1 | InterviewQuery[搜索摘要]，访问 2026-09-01 | 一次性打包考察背景、技术方向、动机、谈判信息 | 把"薪资期望"部分回答得过细（见下方"红旗"） |

## 三、职业目标 / 自省

| 问题原文 | 频次 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|---|
| "What are your career aspirations?" | 2 | Prepfully(2026-08-13)、InterviewKickstart(2024-12-22) | 长期匹配度，是否只是过渡跳板 | 目标模糊或与 Stripe 业务方向不搭 |
| "What's your greatest weakness?" | 1 | The Interview Guys(2026-05-31) | Humble：能否诚实说出局限并说明在补什么 | 用"我太追求完美"这种伪装优点的假弱点 |

## 四、谈判信息（红旗区）

| 问题原文 | 频次 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|---|
| "What are your salary expectations?" | 1（据描述转述） | interviewing.io，访问 2026-09-01；codinginterview.com，访问 2026-09-01 | 收集谈判筹码信息 | **官方建议此阶段不要报具体数字**——回答"looking for a competitive offer，想先了解完整 package"（interviewing.io） |
| "Are you currently interviewing with other companies?" | 1（据描述转述） | interviewing.io，访问 2026-09-01 | 判断你的紧迫度和竞争 offer 筹码 | **官方建议不要透露在面的其他公司**（interviewing.io） |

---

## 红旗 / 踩坑实录（不是题目，是流程事故，练习时要心里有数）

- 面试官口头**允许**的事（查语法、integration 轮不用做完）事后被 recruiter 标记为 "red flag"——**一切以书面 prep 材料为准**，不要轻信面试官口头的"没关系"。（Taro，2025-07-01）
- recruiter ghost、拒信只打电话不发邮件、headcount 临时收回都有多起报道——被拒不代表你答得差，可能是 headcount 问题。（Blind wtplzrfs / gq0xjlif / t6bahgt3）
- Stripe 有 "very heavy writing/documentation culture"，沟通/写作弱可能是这一步就被过滤掉的 dealbreaker。（Blind wexjj3xy，2021-12-23）

## 时间线速查

| 阶段 | 时长 | 来源 |
|---|---|---|
| 投递 → recruiter screen | 1–3 周 | Leon Consulting，2026-03-12 |
| recruiter screen → technical screen | 1–2 周 | 同上 |
| 全程 | 4–8 周（内推 2 周） | interviewing.io；Exponent；The Interview Guys |
