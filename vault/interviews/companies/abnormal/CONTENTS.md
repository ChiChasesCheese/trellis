# 目录 — 按轮次读，按分数练

> 由 `python3 tools/contents.py` 从 `loop/tree/interview-loop.yaml` + `catalog/RANK.md` 生成，**勿手改**。
> 每个技能下的题按 28 法则分数（#refs × 时效 × 轮次权重）降序；**★ = cut line 以内**（累计 80% 流出次数）。
> 每题：题集目录（题面 + 测试 + 参考解）→ 题解文章（先做后读）。练习代码库（cb）用 `python3 loop/ai_screen.py start <cb> <t>`；Abnormal 在 LeetCode 公司标签源里没有题单（`catalog/raw/github_repos.md`）。

## 01_ai_screen · AI Technical Screen · 60 min · 已有 Python 代码库 + Claude Code（探索 10 / 模糊 feature 35 / walkthrough 15）

先读：[playbook](loop/rounds/01_ai_screen/playbook.md) · [00-essentials](study/00-essentials.md) · [claude_code](study/20-cards/claude_code.md)

通用能力（[[Code Core MOC|code-core]] 卡组与练习）：[[round.reading]] · [[round.ambiguity]] · [[round.time]] · [[round.communication]] · [[transfer.abnormal]]

### 报道原形态：security-events 管线 · 规则抑制 · enrichment 插件化 · 告警去重

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **cb01** Security-events 管线：规则抑制 · enrichment 插件化 · 告警去重 | [`loop/rounds/01_ai_screen/cb01_sentinel/`](loop/rounds/01_ai_screen/cb01_sentinel/) | [walkthrough](loop/rounds/01_ai_screen/cb01_sentinel/walkthrough.md) | 2 | 2026-06 | MED-HIGH |

### 换领域练格式：insider-risk（离职外泄 · 告警归并 · 新数据源）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **cb02** 已有代码库 + 未披露 feature（insider-risk 领域库练格式） | [`loop/rounds/01_ai_screen/cb02_insiderwatch/`](loop/rounds/01_ai_screen/cb02_insiderwatch/) | [walkthrough](loop/rounds/01_ai_screen/cb02_insiderwatch/walkthrough.md) | 5 | 2026-09 | MED |

### 团队真实领域：候选人身份欺诈（关联引擎 · Workday 数据源 · 审核反馈）

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
|  | **cb03** 团队领域：候选人身份欺诈（关联 · 新数据源 · 审核反馈） | [`loop/rounds/01_ai_screen/cb03_vetting/`](loop/rounds/01_ai_screen/cb03_vetting/) | [walkthrough](loop/rounds/01_ai_screen/cb03_vetting/walkthrough.md) | 0 | 2026-09 | — |


## 02_incident_sd · Incident（AWS 环境排查）+ System Design（扩容已有系统）

先读：[LOOP_GUIDE](loop/LOOP_GUIDE.md)

通用能力（[[Code Core MOC|code-core]] 卡组与练习）：[[round.debugging]]

### 假设驱动排查：影响面 → 最近变更 → 指标 → 日志 → 根因 → 止血 vs 长期修复

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|

### 读/写扩展、键控状态、热分区、幂等写、迁移路径

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **sd01** 已有系统扩容：读/写扩展、瓶颈 | [`loop/rounds/02_incident_sd/sd01_scale_event_pipeline/`](loop/rounds/02_incident_sd/sd01_scale_event_pipeline/) | [model_answer](loop/rounds/02_incident_sd/sd01_scale_event_pipeline/model_answer.md) | 4 | 2026-09 | MED |


## 03_code_review · Code Review（P0/P1 排序 + 用 AI 修）+ System Extensions（并发、worker、队列扩容）

先读：[LOOP_GUIDE](loop/LOOP_GUIDE.md)

通用能力（[[Code Core MOC|code-core]] 卡组与练习）：[[model.idempotency]]

### 找问题并按影响面排序：正确性 · 数据丢失 · 安全 · 租户隔离 · 并发

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
| ★ | **cr01** Code review 小仓库：P0/P1 排序 + 用 AI 修 | [`loop/rounds/03_code_review/cr01_alert_fanout/`](loop/rounds/03_code_review/cr01_alert_fanout/) | — | 5 | 2026-09 | MED |


## 04_manager_deep_dive · Manager / Behavioral + Technical Deep Dive（判断力）

先读：[questions](loop/rounds/04_manager_deep_dive/questions.md) · [fit](fit.md)

- **约束 → 备选 → 选择与理由 → 结果证据 → 回头看** — 题库：`loop/rounds/04_manager_deep_dive/`
- **How do you use AI / how do you trust it（[[S7]]）** — 题库：`loop/rounds/04_manager_deep_dive/`

## 05_team_values · Team Interviews · 跨职能 · VOICE 价值观

先读：[questions](loop/rounds/05_team_values/questions.md) · [06-questions-to-ask](06-questions-to-ask.md)

- **Velocity · Ownership · Intellectual honesty · Customer obsession · Excellence** — 题库：`loop/rounds/05_team_values/`

## 06_legacy_coding · 旧流程 coding（2024–2025）：图片/文件去重 · 20 min 讨论 + 30 min 写

先读：[LOOP_GUIDE](loop/LOOP_GUIDE.md)

通用能力（[[Code Core MOC|code-core]] 卡组与练习）：[[toolbox.hash]]

### 按大小分桶 → 分块哈希 → 碰撞时逐字节确认 → 近似重复

| | 题 | 题集 | 题解 | #refs | 最近 | 置信度 |
|---|---|---|---|---:|---|---|
