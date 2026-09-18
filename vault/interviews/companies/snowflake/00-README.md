---
title: Snowflake Kit · GenSWE 面试总索引
aliases:
  - Snowflake Kit
  - snowflake kit
tags:
  - company/snowflake
  - moc
---

# Snowflake · GenSWE (Software Engineer - Backend) — 面试 kit 总索引

> **GenSWE - Menlo Park, CA / Bellevue, WA** · Ashby 邮件 "Software Engineer - Backend" · 邀请 2026-09-11 · 当前阶段：**Chakra AI 语音筛（20 min）** · 截止 **2026-09-24 21:36 PDT**
> GenSWE = Snowflake 官方 **General Software Engineering Program**：早期职业统一 loop → team matching。1.5 年经验大概率 IC1（Bay Area 中位 TC ≈ $236K）；IC2（≈ $341K）要电面 + onsite 全 Hire。

这是一本**按轮次组织、可以从头读到尾的备考书**，也是一个**可以跑的题库**。和 `../stripe/` 同一套方法与骨架。

**全书目录 → [`CONTENTS.md`](CONTENTS.md)**：9 轮 → 技能 → 每道题（题集 + 题解 + 来源数 + 最近报告），轮内按 28 法则排序、★ 标出 cut line。

## 一图看懂

```
00 AI 语音筛 ─┐
01 Recruiter ─┤
02 OA ────────┼─ catalog/（证据）→ loop/LOOP_GUIDE.md（每轮打法）→ study/10-rounds/（怎么练）
03 电面 coding┤                                                      ↓
04 OOD ───────┤                          problems/ + loop/rounds/（题 + 测试 + 参考解）
05 系统设计 ──┤                                                      ↓
06 项目深挖 ──┤                          study/30-articles/（每题一篇题解，先做后读）
07 HM / BQ ───┤
08 Team match ┘                          core/（简历、故事、通用答案，跨公司共用）
```

## 按阶段读（从现在到 offer）

| 你现在在 | 先读 | 再练 | 命令 |
|---|---|---|---|
| **Chakra AI 筛**（当前） | `loop/rounds/00_ai_screen/README.md` → `playbook.md` · 故事 [[Core]] · [[ai-voice-screen\|core/playbooks/ai-voice-screen]] | `loop/rounds/00_ai_screen/questions.md`（79 题）· `scenarios.md` · `07-mock.md` · `CARD.md` | `python3 loop/mock.py bq ai -n 5` |
| Recruiter call | `study/10-rounds/01-recruiter.md` · `fit.md` · `06-questions-to-ask.md` | recruiter 题库 | `python3 loop/mock.py bq recruiter -n 5 -m 2` |
| OA（若有） | `study/10-rounds/02-oa.md` · `study/00-essentials/02-dp-patterns.md` | `CONTENTS.md` §02_oa（★ 优先） | `python3 drill.py start q02 -m 40` |
| 技术电面 | `study/10-rounds/03-phone-coding.md` · `04-ood.md` · `05-system-design.md` | `CONTENTS.md` §03–§05（★ 优先） | `python3 loop/mock.py start pc01 -m 40` |
| Onsite | `loop/LOOP_GUIDE.md` §5–§8 · `study/10-rounds/06-project-deep-dive.md` · `07-hm-behavioral.md` | expertise / HM 题库 | `python3 loop/mock.py bq hm -n 5 -m 3` |
| Team matching | `study/10-rounds/08-team-matching.md` | team 题库 | `python3 loop/mock.py bq team -n 3` |

**五天冲刺日程**：`loop/LOOP_GUIDE.md` §10。**进度板**：`python3 drill.py status` · `python3 loop/mock.py status`。

## 目录

| 路径 | 是什么 | 规模 |
|---|---|---|
| `catalog/CATALOG.md` | 全部题目总表（Table A 编码 · B OOD · C 系统设计 · D 非编码轮 · E 仅题名 · F GitHub 蒸馏补充）；每行 #refs / 置信度 / 最近日期 / 来源 | 90 行 |
| `catalog/RANK.md` → `PARETO.md` | 28 法则打分输入与输出；**cut line = 第 49 行（累计 80%）** | 90 行 |
| `catalog/raw/` · `catalog/discovery/` | 原始证据（每条 URL + 日期，含 `github_repos.md` GitHub 优先蒸馏）· Reddit / HN / 1p3a 镜像收割与 46 行 triage | 9 + 收割 |
| `loop/LOOP_GUIDE.md` | 每一轮：形式 · 评什么 · 通过线 · 挂点 · 备考动作 | 9 轮 |
| `problems/` | OA 题（`drill.py`） | 23 题 |
| `loop/rounds/03_phone_coding/` · `04_ood/` | 电面 coding · 类设计（`mock.py`） | 28 + 15 题 |
| `loop/rounds/05_system_design/` | prompt · rubric 五维 · model_answer · followups | 21 题 |
| `loop/rounds/00_ai_screen/` | Chakra 一站式：playbook · stories（[[S1]]–[[S10]]）· scenarios（12）· questions + bank.json · rubric · CARD | 79 题 |
| `loop/rounds/01_recruiter/` `06_project_deep_dive/` `07_hm_behavioral/` `08_team_matching/` | bank.json · questions · rubric（· stories） | 12 · 16 · 30 · 10 题 |
| `study/00-prereq/` · `00-essentials/` · `10-rounds/` · `20-cards/` · `30-articles/` | 前置课 · 通用精华 · 每轮练法 · 速记卡 · 每题题解（LeetCode 原题指向 LC） | 4 · 5 · 9 · 3 · 55 |
| `skills_matrix.md` · `loop/tree/interview-loop.yaml` | 技能 ↔ 题 ↔ JD；知识树（`check_tree.py --strict` 0/0）；`CONTENTS.md` 由它生成 | 59 skill · 91 题 |
| `reports/COVERAGE.md` | 已建题对公开流出题的覆盖（`tools/coverage.py`；全集含 GitHub 蒸馏）| 175/178 = 98% |
| `reports/TEST_SUMMARY.md` | 66 个编码题集、1421 个测试全绿；空 starter 全红 | — |
| `debrief/<date>-<round>/` | 面后复盘：本机转写 + `report.md`（语速/填充词/语法/题库覆盖/rubric）+ `REVIEW.md`（人工逐题评审）；工具在 [[interviews/core/debrief/README\|core/debrief]] | 1 场 |
| `01-company-brief.md` · `02-process.md` · `fit.md` · `raw/` | 公司尽调 · 流程 · Why Snowflake · AI 轮原始调研 | — |
| `CHECKPOINT.md` · `LEDGER.md` · `tasks/plan.md` | 构建进度与账本（换会话从这里接手） | — |

## 与 core 的关系

- 故事与数字：[[Core]]（[[S1]]–[[S9]]，诚实红线：不说 $600B，说 $138.6B / 21.96M）
- 通用题答案：[[Answers]]（[[Answers#Q1]]–[[Answers#Q24]]）
- 简历：`../../core/resume/`

## 面完回写

实际被问的题 + 追问 → `02-process.md` 末尾「亲历」；新题进 `catalog/raw/` 与 `RANK.md`，挂进 `loop/tree/`，重跑 `tools/pareto.py` · `tools/coverage.py` · `tools/contents.py`；被追到答不上的 → [[Core]]；通用教训 → `core/playbooks/`。
