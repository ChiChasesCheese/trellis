# LOOP GUIDE · Abnormal AI · SWE II – Insider Risk（Identity Security）

> 每轮：形式 · 评什么 · 通过线 · 挂点 · 备考动作。每条主张后的括号是证据编号：`inbox`（门户官方原文）· `O-n`（`catalog/raw/official.md`）· `F-n`（`catalog/raw/ai_screen_format.md`）· `Q-n`（`catalog/raw/questions_reported.md`）· `#xxxx`（LeetCode Discuss topicId，`catalog/raw/process_and_rounds.md`）。
> **[推断]** 标记的是从证据推出、没有原话的结论。

## 0. 全景（2026 年的新流程）

| 步 | 官方名（O-14） | 面经里的样子（2026） | Chi 的状态 |
|---|---|---|---|
| 1 | TA Screen | recruiter：经历、最大影响、流程介绍（#8496901） | ✅ |
| 2 | Hiring Manager Interview | 公司与日常工作、背景、为什么换工作、**怎么在日常用 AI**（F-14、Q19） | ✅ |
| 3 | **Skills Assessment** | **AI Technical Screen**：60 min，已有 Python 代码库 + Claude Code，探索 ~10 → 模糊 feature ~35 → walkthrough + 反问（inbox）；报道过的代码库 = security-events 管线（#8335187） | **下一轮（排期中）** |
| 4 | Team Interviews（"cross-functional … values fit, how you collaborate"） | SWE II 2026-09（#8496901）：**Incident + System Design** · **Code Review + System Extensions** · **Manager/Behavioral** · 可能追加 **Technical Deep Dive**；Glassdoor 2026-04："Assignment review · System design & Incident handling · Code review & fix implementation with AI · Engineering manager"；F-13："system-design and incident-management-style conversation plus a PR or code-review discussion where I could use AI agents throughout" | 未知；门户会更新（inbox："It'll update as you move through each stage"） |

**贯穿全程的评分词**：Judgment · Agency（inbox）；VOICE 价值观——Velocity · Ownership · Intellectual honesty · Customer obsession · Excellence（O-10）；"how you maximize your output with AI, and your willingness to own outcomes without waiting for permission"（O-14）。唯一一份详细挂掉原因："lacked sufficient **judgment** in a few areas"（#8496901 deep dive）。

---

## 1. AI Technical Screen（Skills Assessment）—— 下一轮，权重最高

- **形式**（inbox）：浏览器 VS Code + 预装 Claude Code + 代码库；60 min；exploration ~10 min → feature extension ~35 min（"intentionally underspecified"）→ walkthrough + 反问。#8496901 补充：先"explain how it worked"，最后"discuss possible extensions and modifications … mostly discussion-based"。
- **评什么**（inbox 原文）：Judgment（评估方案、拆里程碑、判断什么契合现有系统）· Agency（做决定、说假设、自测、保持推进）· "ship a working v1 that fits the system" · "notice existing abstractions and patterns" · "think about the user" · 对 AI 的 ownership（"explain it, evaluate it, and decide whether it belongs"）。
- **通过线** [推断，来自 inbox + #8335187 反例]：35 分钟内一个**通过真实入口能演示**的 v1，复用了已有扩展点，说出了假设与 known gaps，加了测试；扩展讨论能给出不止一种方案并讲清取舍。
- **挂点**：① 不推进——#8335187 候选人 20 分钟在口头讲 decorator pattern，没有 v1，最后让 Claude 全写（自评 No）；② 照抄 AI——"AI will produce working code. That's not enough"（inbox），F-15 Meta："you can be marked down if you use it as a crutch"；③ 平行造轮子 / 改 legacy（"design slop… rearchitects things instead of following conventions"，F-2）；④ 只有单测没有证据（F-3）；⑤ 沉默或念代码（inbox："Synthesize your observations rather than narrating them"）。
- **备考动作**：`loop/rounds/01_ai_screen/playbook.md`（逐分钟、提示词、口播）→ `python3 loop/ai_screen.py start cb01 t1` 起，按 `catalog/PARETO.md` 顺序做 9 张 ticket，每次 `check` + `reveal` + 复盘表。**cb01 t1、t2 是报道原题形态，各做两遍。**

## 2. Incident + System Design（onsite）

- **形式**：前半段在 **AWS 环境**里排查一个 incident（#8496901："given access to an AWS environment"；#8387564："a production incident that I had to investigate and resolve"），后半段**扩容一个已有系统**（"given an existing system and asked how I would scale it"）。
- **评什么**（#8496901 原话）：What was going wrong · how to identify the root cause · what signals/logs/monitoring tools · immediate mitigation · long-term fixes；"how I approached debugging and how I prioritized short-term mitigation vs. long-term remediation"。SD："Scaling reads · Scaling writes · Identifying bottlenecks · how the existing architecture would behave as traffic increased"。JD 原文要求 "Strong debugging skills with logs, metrics, and behavioral signals"（O-1）。
- **通过线** [推断]：先止血再根因；每个结论有证据（哪张图、哪条日志）；能排除红鲱鱼；SD 里能量化（QPS、分区数、连接数）并指出第一个瓶颈。
- **挂点** [推断]：乱翻控制台无假设；直接说"加机器"（ic01 里扩容反而更糟）；只讲组件不讲行为与极限。
- **备考动作**：`loop/rounds/02_incident_sd/ic01_*`、`ic02_*`（离线 AWS 快照 + `awsim.py`，按 `investigation.md` 说出来）→ `sd01_*`（扩容 cb01 那种管线）→ `study/` 的 AWS 排查速记卡。

## 3. Code Review + System Extensions（onsite）

- **形式**：一个小仓库做 code review（#8496901）；可能**面试前预发链接**（1p3a 1148780，2025-10；Glassdoor 2026-06 "take-home code review"）；可能要求**用 AI 修**（Glassdoor 2026-04 "Code review & fix implementation with AI"）；后半段扩展 + 规模讨论。
- **评什么**（#8496901）：Identify issues · Prioritize them (P0/P1/etc.) · explain why · concrete improvements；扩展："Concurrency · Parallelism · Worker scaling · Message queue scaling · Throughput · Bottlenecks · Failure scenarios"；"go beyond 'add more workers' or 'use a queue.' … reason about the limits of those approaches"。
- **通过线** [推断]：P0 全找到（正确性/数据丢失/安全/租户隔离），排序理由说得出（影响面 × 概率 × 可发现性）；给出可执行的修法；规模讨论里能算吞吐并指出每种扩容手段的上限。
- **挂点** [推断]：一堆 nit 没有排序；漏掉并发与失败路径；"加 worker"不谈下游限流、分区上限、顺序与幂等。
- **备考动作**：`loop/rounds/03_code_review/cr01_*`、`cr02_*`（PR + diff + 隐藏测试 + `REVIEW_KEY.md` + `followups.md`），45 分钟计时，先自己写评论再对答案。

## 4. Manager / Behavioral（+ 可能的 Technical Deep Dive）

- **形式**：过往项目 · 技术决策 · 挑战 · 影响 · 情景题（#8496901 R5）；可能追加 deep dive "into my experience and decision-making"（R6）。HM 已问过 "how you use AI"（F-14），onsite 可能再问。
- **评什么**：Ownership（O-10："No one here says 'that's not my job'"）· 判断力（R6 挂点）· 具体性（O-15："Come with specific examples grounded in real decisions: what you owned, what the result was, where something didn't go as planned"）。
- **挂点**：泛泛而谈、"Generic, polished responses that read like they came straight from a prompt"（O-15）；讲不出取舍与"我当时为什么这么判断"。
- **备考动作**：`loop/rounds/04_manager_deep_dive/questions.md`（每题映射到 [[S1]]–[[S11]]，每个故事准备"决策点 → 备选方案 → 为什么选 → 结果 → 回头看会怎么改"）。

## 5. Team Interviews（跨职能，价值观）

- **形式与评什么**（O-14）："meet a cross-functional group of people … explore values fit, how you collaborate"。VOICE 五条（O-10）；"You might not thrive here if… You need rigid rules instead of flexible frameworks"（O-11）。
- **备考动作**：`loop/rounds/05_team_values/questions.md`（每条 VOICE 一个故事 + 英文 60 秒版）· `06-questions-to-ask.md`（O-15："Prepare questions that show you're evaluating us as carefully as we're evaluating you"）· `fit.md`（Why Abnormal / Why Identity Security）。

## 6. 旧流程题（2024 – 2025，低优先）

图片/文件去重（四帖 1p3a，2024-04 → 2025-07）：`loop/rounds/06_legacy_coding/pc01_image_dedup/`。若 recruiter 说某轮是"不考 LeetCode 的 coding + 讨论"，做这一题。

---

## 7. 时间表（从今天 2026-10-06 到 AI screen）

| 天 | 做什么 | 量 |
|---|---|---|
| D1 | 读 `playbook.md` 两遍；本地 Claude Code 熟悉快捷键；cb01 t1 一遍 | 1 × 60 min |
| D2 | cb01 t2；cb01 t1 第二遍（换设计）；复盘表 | 2 × 60 min |
| D3 | cb02 t1、cb03 t1（换领域练格式） | 2 × 60 min |
| D4 | cb01 t3、cb02 t3；把复盘表里最常见的 0 分项写成一张卡贴屏幕边 | 2 × 60 min |
| D5（面前一天） | cb01 t2 第二遍；口播 §5 模板念三遍；`fit.md`、反问 | 1 × 60 min |
| 之后（onsite 前） | ic01 → cr01 → sd01 → ic02 → cr02 → 行为题库 | 每天 2 项 |
