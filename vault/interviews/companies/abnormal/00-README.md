---
title: Abnormal Kit · SWE II – Insider Risk 面试总索引
aliases:
  - Abnormal Kit
  - abnormal kit
tags:
  - company/abnormal
  - moc
---

# Abnormal AI · Software Engineer II – Insider Risk（Identity Security）— 面试 kit 总索引

> 已过 HR + HM（2026-10-06）。**下一轮 = AI Technical Screen**：60 min，浏览器 VS Code + Claude Code，在一个已有 Python 代码库里——探索 ~10 min → 一个故意说不清楚的 feature ~35 min → walkthrough + 反问。之后几轮官方只说 "Team Interviews"；面经给出的 2026 SWE II 版本是 Incident + SD · Code Review + 扩展 · Manager ·（可能）Deep Dive。
> 团队真实产品：**Infiltration Prevention**（检测求职者里的合成身份 / 国家支持的渗透者）。

这是一本**按轮次组织的备考书**，也是一个**可以跑的练习场**；方法与骨架同 `../stripe/`、`../snowflake/`、`../millennium/`，但主力题型是新的：**陌生代码库 + 模糊 ticket + 隐藏验收测试**（`CONVENTIONS.md`）。

**全书目录 → [`CONTENTS.md`](CONTENTS.md)**（轮次 → 技能 → 题，按 28 法则排序）。

## 先读这三样（30 分钟）

0. **真题复刻** `loop/rounds/01_ai_screen/cb01_sentinel/REAL_QUESTION.md` —— 报道过的原题（规则抑制 + 富化插件化）原帖与错因；逐场脚本与参考答案见 `cb01_sentinel/walkthrough.md` §t2；练：`python3 loop/ai_screen.py start cb01 real`。
1. `loop/rounds/01_ai_screen/playbook.md` —— 逐分钟打法、Claude Code 提示词、英文口播。**报道过的真题形态在它开头。**
2. `study/00-essentials.md` —— 十分钟找到扩展点；七种扩展点该怎么挂；安全产品的四类隐藏期望。
3. `loop/LOOP_GUIDE.md` —— 每轮：形式 · 评什么 · 通过线 · 挂点 · 备考动作，全部带证据编号。

## 然后练（每次 60 分钟，严格计时，出声）

```bash
cd vault/interviews/companies/abnormal
python3 loop/ai_screen.py list                      # 3 个代码库 × 3 张 ticket
python3 loop/ai_screen.py start cb01 t1             # 复制出一个干净 git repo；在那个目录开 VS Code + `claude`
python3 loop/ai_screen.py check cb01 t1 <目录>       # 隐藏验收（core/stretch/regression）+ 自带测试 + 你的 diff + 自评表
python3 loop/ai_screen.py reveal cb01 t1            # 面试官笔记：澄清问答、隐藏期望、追问、打分信号
```

顺序（`catalog/PARETO.md`）：**cb01 t1 → cb01 t2**（报道原题形态，各两遍）→ cb02 t1 → cb03 t1 → cb01 t3 → cb02 t3 → cb03 t2 → cb02 t2 → cb03 t3。

| 代码库 | 领域 | 为什么练它 |
|---|---|---|
| `cb01_sentinel` | security-events 管线：采集 → 硬编码 enrichment → 规则 → 威胁等级/排序 → 告警 → API → DB | **一手报道的面试代码库形态**；t1 规则抑制、t2 enrichment 插件化就是报道的两题，t3 告警去重 (reconstructed) |
| `cb02_insiderwatch` | insider risk：审计日志 → 个人基线 → 信号 → 告警 | 换领域练格式：离职外泄 · 告警归并成 case · 新数据源 |
| `cb03_vetting` | 候选人身份欺诈（团队真实产品） | 关联引擎 · Workday 数据源 · 审核反馈；也是 HM/team 面的领域语言 |

## 按阶段读

| 你现在在 | 读 | 练 |
|---|---|---|
| **AI screen 前**（现在） | playbook · essentials · `study/20-cards/claude_code.md` · `01-company-brief.md` | 上面的 9 张 ticket；`LOOP_GUIDE.md` §7 五天表 |
| Incident + SD | `LOOP_GUIDE.md` §2 · `loop/rounds/02_incident_sd/ic0*/investigation.md` | `ic01`、`ic02`（离线 AWS 快照 + `awsim.py`）· `sd01` |
| Code review | `LOOP_GUIDE.md` §3 | `cr01`、`cr02`（PR + diff + 隐藏测试 + `REVIEW_KEY.md`），45 min |
| Manager / deep dive | `loop/rounds/04_manager_deep_dive/questions.md`（判断力五步）· `fit.md` | `python3 loop/mock.py bq hm -n 5 -m 3` |
| Team interviews | `loop/rounds/05_team_values/questions.md` · `06-questions-to-ask.md` | `python3 loop/mock.py bq team -n 4 -m 2` |

## 目录

| 路径 | 是什么 |
|---|---|
| `catalog/raw/` | 证据：`inbox.md`（门户官方原文）· `official.md`（官网/JD/产品/工程博客，O-n）· `ai_screen_format.md`（VP of AI 博客、同类面试，F-n）· `process_and_rounds.md` · `questions_reported.md`（Q-n）· `github_repos.md`（GitHub 优先：无 Abnormal 题库） |
| `catalog/CATALOG.md` → `RANK.md` → `PARETO.md` | 题族总表 → 打分 → cut line（`tools/pareto.py`） |
| `loop/LOOP_GUIDE.md` | 每轮打法 + 五天表 |
| `loop/rounds/01_ai_screen/` | playbook + 3 个练习代码库（starter/solution/acceptance/interviewer/walkthrough/REPORT） |
| `loop/rounds/02_incident_sd/` · `03_code_review/` · `06_legacy_coding/` | incident 演练 · system design · code review · 旧流程去重题 |
| `loop/rounds/04_manager_deep_dive/` · `05_team_values/` | 题库（bank.json 由 `tools/make_banks.py` 从 questions.md 生成） |
| `loop/ai_screen.py` · `loop/mock.py` | 代码库练习 runner · 其它轮 runner |
| `loop/tree/interview-loop.yaml` | 知识树（`check_tree.py --strict`）；`CONTENTS.md` 由它生成 |
| `study/` | 精要 · 速记卡 · 题解 |
| `01-company-brief.md` · `02-process.md` · `fit.md` · `06-questions-to-ask.md` | 简报 · 流程与矛盾（含面完回写表）· Why Abnormal（英文）· 反问 |
| `reports/COVERAGE.md` | 覆盖率（`tools/coverage.py`），注明分母 |
| `CHECKPOINT.md` · `LEDGER.md` · `tasks/` | 构建进度、账本、子代理指令 |

## 与 core 的关系

故事 [[Core]]（[[S1]]–[[S11]]；本 kit 最常用 [[S6]] 判断力、[[S7]] AI-native、[[S3]] 调试）；通用答案 [[Answers]]；简历 `../../core/resume/`；通用编码能力 `transfer.abnormal`（code-core 域）。

## 证据的边界（诚实）

- AI screen 的代码库与题目只有**一份**一手报道（LeetCode Discuss #8335187，2026-06）；另 5 份只说"已有代码库 + feature + 测试"。你的面试很可能是同一个代码库，也可能不是——所以 cb02/cb03 和 `study/00-essentials.md` 练的是**迁移**。
- 后续轮次只有面经（#8496901 最完整），官方只到 "Team Interviews"。门户会更新，每轮前回去看。
- 1p3a 正文全部 403，只有 Telegram 镜像摘要；PracHub 付费文只有标题。
