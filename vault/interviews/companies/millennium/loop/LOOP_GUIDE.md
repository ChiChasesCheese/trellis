# Millennium LEaD 面试 Loop 指南（每一轮：形式 · 评什么 · 通过线 · 挂点 · 备考动作）

> 证据在 `../catalog/raw/`（每条可回溯）；题目主键 `../catalog/CATALOG.md`；练习目录 `rounds/`；演练器 `mock.py`。全书目录 `../CONTENTS.md`。
> 读者：1.5 YOE 后端 + 自建量化研究平台；目标 = LEaD Program（Miami，12–18 个月轮岗）。**结论先行，细节靠证据。**

## 0. 总图

```
简历筛（批处理拒信）→ R1 45 min · SWE · Webex + HackerRank（15 简历/项目 + 30 一题 live coding）← 当前
  → R2/R3 更多人（HM / tech leader；Miami 2026-02 一例 3 轮偏 behavioral）
  → 决定（一手：R4 后 2 天自动拒；每轮回音快）→ offer（全现金，Miami new-grad 轮岗一例 ≈ $210K TC）
```

| 数字 | 值 | 来源 |
|---|---|---|
| 投递 → R1 邀约 | 38 天 | 邮件 |
| R1 | 45 min | 邀约 |
| R1 切分 | 15 + 30 | 1p3a 1090775（同公司 45 min 电面） |
| 后续轮数 | 2–3（未知，R1 后问） | Glassdoor Miami 2026-02 |
| 通过线 | 未知；一手挂点：括号漏写未给 debug 时间 | LC 7423863 |

**贯穿所有轮的评分主线**（官方四条 + 一手）：① talk through code live —— 先讲再写，边写边说 ② fundamentals —— 复杂度、语言机制随时被问 ③ ownership & initiative —— 项目要有"我决定" ④ abstract reasoning —— 能把业务题抽成数据结构 ⑤ handle feedback —— 被指出问题时先接受再修。**面试官几乎不给反馈** → 自己推进、自己验证。

---

## 1. R1 · 45 min · Webex + HackerRank（当前）

- **形式**：一位 SWE；HackerRank 面试环境（可跑代码，自带 AI 助手且面试官可见交互 → 不用）。
- **评什么**：一题写对 + 讲清 + 自测；项目讲到第三层；Python 内功口答。
- **通过线（推断）**：题目主线在 30 min 内跑通样例 + 至少一个 follow-up 讲清；无明显基础错误。
- **挂点**：括号/缩进错误没自查；只会 pandas 不会纯 Python；说不清 GIL/asyncio；项目讲成流水账；$600B 之类不诚实数字。
- **备考动作**：`rounds/01_first_round/playbook.md`（逐分钟）；题库按 `../catalog/PARETO.md` 顺序：pc02 → pc03 → pc09 → pc10 → pc01 → pc05 → pc06 → pc07 → pc04 → pc08；每题 30 min 计时只做 Part 1–2；口头题 `mock.py bq py -n 5 -m 2` 每天 10 题；卡片 `../study/20-cards/`。
- **练习**：`python3 loop/mock.py start pc02 -m 30` · `test pc02` · `ref pc02` · `status`。

## 2. 项目深挖（R1 前 15 min；后续轮可能整轮）

- **形式**："pick a project → objectives, approach, tech stack, design, challenges, database strategy"（一手，Bangalore）；"hardest engineering challenge"（PracHub 2026-04）。
- **评什么**：why · alternatives · failure modes 三层；沟通。
- **挂点**：无 headline、每答 > 90 s（Chakra 复盘教训）；讲不出取舍；数字口径不诚实。
- **备考动作**：首选 Quant-Stroller（`rounds/01_first_round/playbook.md` §2.2），备选 [[S1]]/[[S5]]；题库 `rounds/03_project_deep_dive/`。
- **练习**：`python3 loop/mock.py bq exp -n 4 -m 3`。

## 3. HM / Behavioral（R2+）

- **形式**：30–45 min；官方四维；"explain to non-technical partners"、pressure/incident/tech debt；why finance / why Millennium。
- **评什么**：ownership、teamwork、feedback、fit；对 pod 结构与金融的兴趣是否具体。
- **挂点**：泛泛的 "why finance"；讲不出 pod 结构；贬低现雇主。
- **备考动作**：`rounds/05_hm_behavioral/`（12 题 + 故事映射）；`../fit.md`；`../study/20-cards/finance_vocab.md`。
- **练习**：`python3 loop/mock.py bq hm -n 5 -m 3`。

## 4. 系统 / 数据设计（R2+，可能）

- **形式**：45 min；一手 "price data design"；聚合站 research data pipeline / risk monitor / rate limiter。
- **评什么**：不变量先行（point-in-time、幂等、迟到数据）；API 与数据模型；故障与规模；分层；上线与监控。
- **备考动作**：`rounds/04_system_design/sd01_market_data_service/`（prompt · rubric · model_answer · followups）；限流器直接复用 Snowflake `od04`/`sd07`；场景题（生产崩溃 RCA、陌生系统）用 [[S8]]/[[S9]]/[[S3]]。
- **练习**：`python3 loop/mock.py start sd01 -m 45`。

## 5. Recruiter / 邮件往来

- LEaD 无单独 recruiter call（直接 R1）；回信草稿 `../03-reply-email.md`；题库 `rounds/00_recruiter/`。

## 6. 三天冲刺

| 天 | 上午 | 下午 | 晚上 |
|---|---|---|---|
| D1 | pc02 · pc03（各 30 min 计时）+ 读题解 | pc09 · pc10 | Python 卡 20 张 · `bq py -n 10` |
| D2 | pc01 · pc05 · pc06 | pc07 · pc04 · pc08 | 项目口播 3 遍录音（headline ≤ 15 s、总 ≤ 90 s）· `bq exp -n 5` |
| D3 | 重做 PARETO 前 4 题的 Part 1（不看解）| sd01 白板 45 min · 金融卡 | playbook 通读 · HackerRank 环境试跑 · 反问 2 个背熟 |

## 7. 面完回写

实际被问的题 + 追问 → `../02-process.md` 亲历表；新题进 `../catalog/raw/coding_first_round.md` 与 `RANK.md`，挂进 `tree/`，重跑 `tools/pareto.py` · `tools/coverage.py` · `tools/contents.py`；答不上的 → [[Core]]。
