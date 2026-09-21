---
title: Millennium Kit · LEaD Program 面试总索引
aliases:
  - Millennium Kit
  - millennium kit
  - LEaD Kit
tags:
  - company/millennium
  - moc
---

# Millennium · Software Engineer – Learning Engineering and Data (LEaD) Program — 面试 kit 总索引

> **Miami, FL · Onsite · REQ-27753** · 邀约 2026-09-21（LEaD recruiter）· 当前阶段：**R1 45 min · Webex + HackerRank live coding · 面试官 SWE**（排期自选）
> LEaD = Millennium 官方 **12–18 个月轮岗**项目（2023-04 启动，cohort 制，结束后进四个技术分部之一）；JD 2–5 YOE，C++/Python/Java，Pandas/NumPy，FastAPI/Spring Boot，LLM 产品经验优先。Miami 轮岗 new-grad offer 一例 ≈ $210K TC（Blind，中）。
> 几个 req 里唯一进面的通道（其余简历筛拒）。

这是一本**按轮次组织、可以从头读到尾的备考书**，也是一个**可以跑的题库**；与 `../snowflake/`、`../stripe/` 同一套方法与骨架。

**全书目录 → [`CONTENTS.md`](CONTENTS.md)**（轮次 → 技能 → 题，按 28 法则排序、★ = cut line）。

## 一图看懂

```
00 Recruiter / 邮件 ─┐
01 R1 45 min ────────┼─ catalog/（证据）→ loop/LOOP_GUIDE.md（每轮打法）→ loop/rounds/（题 + 测试 + 参考解 + 题库）
02 Python 内功 ──────┤                                                     ↓
03 项目深挖 ─────────┤                          study/30-articles/（每题一篇题解，先做后读）· study/20-cards/（速记卡）
04 系统/数据设计 ────┤                                                     ↓
05 HM / BQ ──────────┘                          core/（简历、故事 S1–S11、通用答案，跨公司共用）
```

## 按阶段读（从现在到 offer）

| 你现在在 | 先读 | 再练 | 命令 |
|---|---|---|---|
| **回复邀约**（当前） | `03-reply-email.md` · `02-process.md` | — | eightfold 选 3–4 天后的时间 |
| **R1 45 min** | `loop/rounds/01_first_round/playbook.md`（逐分钟 + 英文口播）· `01-company-brief.md` · `fit.md` | `catalog/PARETO.md` 顺序：pc02 → pc03 → pc09 → pc10 → pc01 → pc05 → pc06 → pc07 → pc04 → pc08；口头题 `02_python_internals` | `python3 loop/mock.py start pc02 -m 30` · `bq py -n 5 -m 2` |
| 项目深挖 | `loop/rounds/03_project_deep_dive/questions.md` · [[S1]] [[S5]] | 14 题 | `python3 loop/mock.py bq exp -n 4 -m 3` |
| R2+ HM / BQ | `loop/rounds/05_hm_behavioral/{questions,stories}.md` · `06-questions-to-ask.md` | 12 题 | `python3 loop/mock.py bq hm -n 5 -m 3` |
| R2+ 设计（若有） | `loop/rounds/04_system_design/sd01_market_data_service/` | prompt → rubric 自评 | `python3 loop/mock.py start sd01 -m 45` |

**三天冲刺日程**：`loop/LOOP_GUIDE.md` §6。**进度板**：`python3 loop/mock.py status`。

## 目录

| 路径 | 是什么 | 规模 |
|---|---|---|
| `catalog/raw/` | 原始证据：`inbox.md`（邀约事实）· `official_lead.md`（官方 LEaD / JD / Miami 组织 / 官方面试建议 / 薪酬）· `github_repos.md`（GitHub 优先：LC 标签源无 Millennium）· `coding_first_round.md`（编码题证据）· `process_and_rounds.md`（流程、矛盾）· `interviewer.md` · `sources_index.md`（可达性台账） | 7 |
| `catalog/CATALOG.md` → `RANK.md` → `PARETO.md` | 题目总表（A 编码 · B 设计 · C 口头 · D 题库 · E 不入库）；**cut line = 第 9 行 / 15 行**（`tools/pareto.py --focus 第一轮`） | 15 行 |
| `loop/LOOP_GUIDE.md` | 每一轮：形式 · 评什么 · 通过线 · 挂点 · 备考动作 + 三天冲刺 | 6 轮 |
| `loop/rounds/01_first_round/` | R1 题集（`problem.md` + starter + solution + tests + REPORT）+ `playbook.md` | 10 题 |
| `loop/rounds/02_python_internals/` | Python / Java 内功口头题 + bank.json | 40 题 |
| `loop/rounds/00_recruiter/` `03_project_deep_dive/` `05_hm_behavioral/` | bank.json + questions（+ stories 映射） | 8 · 14 · 12 |
| `loop/rounds/04_system_design/` | sd01 行情/价格数据服务：prompt · rubric · model_answer · followups | 1 |
| `study/30-articles/` · `study/20-cards/` | 每题一篇题解 · 速记卡（Python 内功 20 · 金融词汇 18） | 10 · 2 |
| `loop/tree/interview-loop.yaml` | 知识树（`check_tree.py --strict`）；`CONTENTS.md` 由它生成 | 6 轮 14 技能 |
| `reports/COVERAGE.md` | 已建题对公开流出题的覆盖（`tools/coverage.py`） | — |
| `01-company-brief.md` · `02-process.md` · `fit.md` · `06-questions-to-ask.md` · `03-reply-email.md` | 公司/项目简报 · 流程与矛盾 · Why Millennium/LEaD（英文口播）· 反问 · 回信草稿 | — |
| `CHECKPOINT.md` · `LEDGER.md` · `tasks/` | 构建进度与账本（换会话从这里接手）· 子代理指令 | — |

## 与 core 的关系

- 故事与数字：[[Core]]（[[S1]]–[[S11]]，诚实红线：不说 $600B）。
- 通用题答案：[[Answers]]。简历：`../../core/resume/`。
- LeetCode：`../../core/leetcode/companies/millennium.md`（LC 标签源无目录；只列报道过的原题）。

## 证据的边界（诚实）

- **LEaD 自己的题目一手报道 = 0**。题库来自 Millennium SWE / Quant Dev-Python 岗（LeetCode Discuss 全文、1p3a 经 Telegram 镜像、Blind/Glassdoor 仅摘要）+ PracHub/StealthCoder/QuantVault 聚合。
- Blind、Glassdoor、1p3a 正文全部被反爬拦截；intern timeline 帖（1p3a 951597）值得 Chi 用浏览器手动读一遍。
- "LEaD 首轮 90 min"（Blind）与本次 45 min 邀约冲突；以邀约为准。

## 面完回写

实际被问的题 + 追问 → `02-process.md` 亲历表；新题进 `catalog/raw/coding_first_round.md` 与 `RANK.md`，挂进 `loop/tree/`，重跑 `tools/pareto.py` · `tools/coverage.py` · `tools/contents.py`；答不上的 → [[Core]]。
