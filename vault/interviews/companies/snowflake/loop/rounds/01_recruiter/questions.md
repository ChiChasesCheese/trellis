# Recruiter / HR call —— 题库（含 Chakra AI 轮 6 题）

> 来源：`catalog/raw/bq_hm_recruiter.md` §1、`../../../raw/chakra.md`、`../../../raw/process_research.md` §1.3。形式：15–30 min；早期职业 Infra 岗一例不到 15 min。练习：`python3 loop/mock.py bq recruiter -n 5 -m 2`。
> **这一轮不考技术，但会决定你被送去哪个 org 的电面**——把方向偏好说具体。

## 一、Chakra AI 轮（6 题，标 `round: ai`）

| 问题原文 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|
| "Tell me about yourself and your current role." | 一手 ×3 | 60 s 定位 + 三件事 + hook | 超过 90 s；没有数字 |
| "Walk me through a recent project and your specific contribution." | tryexponent | ownership 证据（"I designed / I wrote"） | 讲成团队做了什么 |
| "What's the hardest technical challenge you've faced?" | tryexponent | 根因 + 验证方法 + 数字 | 讲原理课（theoretical = Not Met） |
| "Describe a technical decision and the trade-offs." | tryexponent | 备选方案 + 为什么弃 + 代价 | 只讲最终方案 |
| 场景题（pipeline 算错 / 计量不重复计费 / 无停机切换…） | 邮件 "applied scenarios" | clarify → 3 步 → 真实例子 → trade-off | 没做过就硬编；不说最接近的真实经验 |
| "Do you have any questions for us?" | 邮件第四段 | 问它能答的 + 一句表态留在 transcript | 问薪资/组/manager |

## 二、Recruiter 电话（12 题）

| 问题原文 | 频次 / 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|
| "Tell me about your background and what you've been working on." | 一手（t.me 29383） | 45–60 s 版自我介绍 | 从大学讲起 |
| "What infra / platform work have you done, and what direction next?" | 一手 ×2（29383, 1p3a 1186534） | **方向偏好决定 org 匹配**：transactions / scheduling / metering | 说"都行" |
| "Why Snowflake?" | 聚合站共识 | 具体到产品与技术方向 + 自己的桥（重度 Snowflake 用户） | "大厂、成长快" |
| "What do you know about Snowflake?" | 聚合站 | 三层架构 + agentic 转向 + 开放/OLTP 上移，一分钟 | 背财报数字堆砌 |
| "Menlo Park or Bellevue?" | GenSWE 官方 | 有偏好但都接受；知道两地 org 分布不同 | 不知道 Bellevue 有工程中心 |
| "Timeline / interviewing elsewhere?" | 聚合站 | 给时间线；不透露他家进度 | 报出其它公司名与阶段 |
| "Compensation expectations?" | 聚合站 | "competitive package，先了解 level 与 scope" | 先报数字 |
| "What level are you targeting?" | Blind down-level 帖 | "按 end-to-end ownership 评估；IC2 目标，尊重流程" | 硬要 IC2 或自贬 IC1 |
| "Visa sponsorship?" | 简历事实 | H-1B 2026-10 生效，需 transfer；一句话说清 | 含糊 |
| "Why leave PayPal?" | 通用 | "拥有一个平台两年，下一步去建原语本身" | 抱怨 |
| "Which teams interest you?" | team matching 前置 | 3 个方向 + 理由（tasks/dynamic tables · billing/metering · FDB/Unistore） | 一个都说不出 |
| "Questions for me?" | 通用 | 问流程矛盾：Chakra = Talent Intake？有无 OA？team matching 时点？headcount？ | 没问题 |

## 三、必备答案清单

- 45 s / 60 s / 90 s 三版自我介绍（`../00_ai_screen/playbook.md` §2 为 60 s 版）。
- Why Snowflake 60 s（`../../../fit.md` §1）。
- 三个方向偏好各一句理由（`../../../fit.md` §5）。
- Level / comp 两句话（`../00_ai_screen/playbook.md` §7）。
