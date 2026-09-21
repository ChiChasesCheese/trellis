# 02 · Millennium LEaD 面试流程（2026-09）

> 逐条证据与置信度在 `catalog/raw/process_and_rounds.md`（LEaD 专属 L1–L6）与 `catalog/raw/coding_first_round.md`。**high** = 一手 / 官方；**medium** = 一手但只读到摘要，或标了日期的聚合站；**low** = SEO。

## 0. 总图（LEaD，推断自 L1 + L2 + 通用流程）

```
投递（eightfold，2026-08-14）→ 简历筛（批处理拒信 13:0x UTC；其它 req 全拒）
  → 邀约 2026-09-21：R1 45 min · SWE · Webex + HackerRank live coding（← 我在这）
      一手同形态（1p3a 1090775）：~15 min 背景/项目 + ~30 min 一题
  → R2 / R3：更多人（HM / tech leader / 可能 Steve Johnson）；Miami 2026-02 一例"3 轮全 behavioral、每轮很快回音"
  → 决定（通用：R4 后 2 天自动拒；"decision 1–3 weeks" 为 SEO 口径）→ offer（全现金）
```

| 数字 | 值 | 来源 | 置信度 |
|---|---|---|---|
| 投递 → R1 邀约 | 38 天 | 自己的邮件 | high |
| R1 时长 | 45 min | 邀约邮件 | high |
| R1 切分 | 15 + 30（背景 + 一题） | 1p3a 1090775（同公司 45 min 电面） | medium |
| 后续轮数 | 2–3 轮（Miami 2026-02：3 轮总计） | Glassdoor 摘要 | medium |
| 通过线 | 未知；一手：括号漏写未给 debug 时间 → 挂；面试官"几乎不给反馈" | LC 7423863 · 1p3a 1090775 | medium |
| TC | ≈ $210K（Miami 轮岗 new-grad 一例）；Miami SWE 中位 $209K | Blind · levels.fyi | medium |

## 1. R1（当前）：45 min · Webex + HackerRank

- **形式**：一位 SWE（Microsoft 背景，见 `catalog/raw/interviewer.md`）；HackerRank 面试环境（可跑代码；产品自带 AI 助手且**面试官能看到你和 AI 的交互**——默认不用 AI，除非对方明说）。
- **内容（证据权重顺序）**：① 一道实用编码题（分组聚合 / 分页拉取 / 装饰器 / 数据结构设计 / 大数字符串）② 或一道 LC medium（双指针 / 前缀和 / 图 BFS）③ 穿插 Python 内功口头题 ④ 前 15 min 简历与项目 ⑤ SQL 小题概率低。
- **评什么**：官方 "talk through code live"、fundamentals、abstract reasoning、ownership；一手："working and optimized"、自己走样例、复杂度。
- **打法**：`loop/rounds/01_first_round/playbook.md`（逐分钟）。

## 2. R2+（预留）：项目深挖 · behavioral · 可能 SD

| 类型 | 一手报道 | 备注 |
|---|---|---|
| 项目深挖 | "pick a project → objectives, approach, tech stack, design, challenges, database strategy"（LC 6020524）· "explain a project and its hardest engineering challenge"（PracHub 2026-04） | `loop/rounds/03_project_deep_dive/` |
| Behavioral | 官方四条；"explain work to non-technical partners"（PracHub HR 2026-02）；pressure / tech debt / incidents（TechPrep）；"why finance / why Millennium / pod 结构"（recruiter 口径） | `loop/rounds/05_hm_behavioral/` |
| SD / LLD | price data design（一手，R5）· research data pipeline / real-time risk monitor / rate limiter / order book（聚合） | `loop/rounds/04_system_design/` |
| 场景 | "app crashes in prod → RCA"、"how to know what's true in an unfamiliar system" | 直接用 [[S8]] / [[S9]] / [[S3]] |

## 3. 矛盾与未知

1. **45 vs 90 min**：邀约 45（high）；Blind "LEaD 首轮 90 min"（low）。以邀约为准。
2. **写代码 vs 全 behavioral**：邀约明说 live coding；Miami 2026-02 说全 behavioral。两手准备。
3. **LC 式 vs 实用**：两种一手都有。LEaD JD 偏数据/AI → 实用更可能；LC medium 不能掉。
4. **语言**：不限。Python；Java 口答。
5. **后续轮次**：未知——R1 结束反问；回复 recruiter 邮件时也问。
6. **未抓到**：Blind/Glassdoor/1p3a 正文、intern timeline 帖 951597、levels.fyi 页面。

## 亲历（面完填）

| 日期 | 环节 | 实际被问 | 追问 | 自评 / 结果 |
|---|---|---|---|---|
| | R1 45 min（面试官） | | | |
