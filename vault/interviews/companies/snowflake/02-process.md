# 02 · Snowflake 面试流程（GenSWE / Backend SWE，2025–2026）

> 来源与逐条置信度在 `raw/process_research.md`；Chakra 机制在 `raw/chakra.md`。**high** = 一手候选人帖或官方页；**medium** = 聚合站但细节一致；**low** = SEO。1point3acres 正文全站 403，其内容经 Telegram 镜像 `t.me/s/usinterview` 读到摘要。

## 0. 总图

```
投递（Ashby）→ [Chakra AI 语音筛选 20 min]（← 我在这）→ HR / HM call 15–30 min（有时在 AI 筛之前）
  → [HackerRank OA 3 题 90–120 min]（2026 全职一手帖多数没有；实习/新毕业为主）
  → 技术电面：常见两轮 back-to-back，各 60 min（1 coding + 1 system design，或 2 coding）；10 min 介绍 / 40 min 题 / 10 min 反问
  → Onsite 4–5 轮 × 60 min：coding ×1–2（可因「coding speed」加一轮）· resume/project deep dive（"expertise"）· system design · BQ/manager；IC2 有 4 h 现场
  → 决定（debrief 几天内；官方「30 天无回音视为不匹配」）→ Team matching（GenSWE 最后一步）→ offer
```

| 数字 | 值 | 来源 |
|---|---|---|
| 端到端 | 官方 2–4 周；一手：内推→HR call→约面仅 4 天（2026-08） | careers/gethired · t.me 29627 |
| 电面→结果 | 3–5 天（Leon，low） | — |
| 通过线 | 前两轮电面「只是 screens」；onsite「remaining ones 全要 Hire」 | Blind 2025-10 |
| 定级 | 1.5 YOE 大概率 IC1；IC1 Bay Area 中位 TC $236K（base $168K）；IC2 $341K；IC2 Seattle $323K | levels.fyi 2026-09-13 |

## 1. Chakra AI 语音筛选（当前）

- **形式（一手 ×3，2026-06 ~ 08）**：约 **20 分钟**；开麦克风 + 摄像头 + **全屏共享**；**禁外接显示器**；界面左侧实时转录双方对话、右侧自己画面；内容 = **BQ + 过去的项目**，AI 会对你说的做总结复述；**无 coding**（三条一手均未提写代码）。有一条帖子标题就是 "Snowflake General SWE AI Interview" —— 与 GenSWE 同通道。
- **HackerRank 侧**：Chakra 2026-07 起支持内嵌代码编辑器；邮件写了 "applied scenarios" → 准备**口头**讲后端场景（`loop/rounds/00_ai_screen/scenarios.md`，12 题），写代码可能性低。
- **打分**：Reporter 只读 transcript，每条 expectation Met/Partially/Not Met/Not Assessed，JD must-have 加权；recruiter 看分数 + 带时间戳的引用 + 视频。人做决定（Ashby 邮件明说）。
- **Snowflake 员工也不清楚这个环节**（Blind 2026-05-12 帖，员工只贴了 chakra.sh 链接）→ 没人能给内部提示，按 `loop/rounds/00_ai_screen/playbook.md` 打。
- **AI 筛后的拒信时间线：无一手数据。**

## 2. 电面 / onsite 题型（为下一轮预留）

| 类型 | 一手报道的题 | 备注 |
|---|---|---|
| Coding（LC medium + 更难 follow-up） | LC 1751 Max Events II 变体（2026-06）· Happy Number O(n)→O(1)（Floyd）· LC 330 Patching Array（旧） | 面试官会给 hint、帮 debug；「人都很好」 |
| **OOD / 类设计（高频）** | `addTask(id, priority, ts)` / `executeTask()`（同 task 可多次 add）· Queue 类（类 deque）→ 扩展成云端 queue service 讨论故障语义 | 两条都是「挂」的帖子 → 重点练 |
| System design（偏 infra / data） | SQL notebook（类 LeetCode 跑 SQL，重点 client 怎么取结果）· KV store · Quota system（多上游服务共用）· "SQL engine running loads of queries as a cron job"（IC1/IC2，面试官很沉默）· password storage · audit log service · dynamic blacklist filter | 与我的背景高度重合：任务调度、配额/计量、结果投递 |
| 项目 / BQ | 技术轮开头 15–20 min「最近的项目 + 技术挑战」；onsite 单独 resume 轮 + BQ 轮；expertise 轮 = 40 min 深挖一个项目的 why/how、替代方案、availability / fault tolerance | 官方 panel 列有 behavioral + collaboration，但早期职业不是纯 STAR 轮 |
| OA（若有） | 3 题 / 90–120 min，HackerRank Proctor（每 15 s 截屏）；题名池：Prime String、Task Scheduling、Paint the Ceiling、Design a Quota System、Parallel Courses III、Cheapest Flights K Stops、Meeting Rooms II… | 聚合站来源，low–medium；Stripe 题库 qA02/qA09 直接可用 |

**下一轮准备清单（收到电面邀请再做）**：`companies/stripe/problems/qA*`（算法组）· OOD：task scheduler with priority+timestamp、deque→分布式队列 · SD：quota/metering、query result delivery、KV store · 系统设计要带上 Snowflake 自己的原语（Execution Anchor、FDB、serverless tasks）当参照。

## 3. 矛盾与未知

1. **两封邮件是一个环节还是两个**：Ashby "Talent Intake"（20–30 min）vs HackerRank "Technical Screening Round"（20 min）。PracHub 记录过候选人「同时收到两个链接」的混乱。**做完 Chakra 后回复 Ashby 邮件问清楚。**
2. **AI 筛是否含 coding**：一手 ×3 说无；平台能力有。按「口头场景题」准备。
3. **AI 筛后顺序**：AI → HR → 电面，或 HR 在前，两种都有。
4. **OA 是否必经**：2026 全职一手几乎没提；实习/新毕业为主。
5. **电面组合**：coding + SD 或 2 coding，取决于 org（product vs cloud/infra）。
6. **难度**：senior/DB org 帖说 "extremely hard LC + follow-up"；Global Platform ICT2 帖说 "Mediums"；早期职业一手多为 medium + OOD。
7. **未能抓取**：1p3a 正文、Glassdoor、LeetCode Discuss、官方博客 "AI Cheat Sheet: How (and When) to Use AI in Your Snowflake Interview"（2026-06-09，正文空）——**这篇值得面前用浏览器手动读一遍**：https://careers.snowflake.com/us/en/blogarticle/ai-cheat-sheet-how-and-when-to-use-ai-in-your-snowflake-interview

## 亲历（面完填）

| 日期 | 环节 | 实际被问 | 追问 | 自评 / 结果 |
|---|---|---|---|---|
| | Chakra | | | |
