# 流程 · 已知、推断、矛盾

## 1. Chi 的流程（亲历）

| 日期 | 轮 | 形式 | 结果 / 记录 |
|---|---|---|---|
| ≤ 2026-10-06 | TA screen（recruiter） | 电话 | ✅ 通过 |
| ≤ 2026-10-06 | Hiring Manager | 视频 | ✅ 通过 |
| 排期中（门户："Based on availability requested on Oct 6"） | **AI Technical Screen**（Skills Assessment） | 60 min，浏览器 VS Code + Claude Code + 已有 Python 代码库 | 待面。面完在下面"亲历表"填一行 |
| 未知 | Team Interviews / onsite | 门户会更新 | — |

### 面完回写（亲历表）

| 轮 | 代码库是什么 | feature 原话 | 我问了什么 / 面试官怎么答 | 追问 | 我觉得哪里好 / 哪里差 |
|---|---|---|---|---|---|
| AI screen | | | | | |

回写之后：新事实进 `catalog/raw/inbox.md`；若代码库与 cb01 不同，把形态写进 `catalog/CATALOG.md` 新行，重跑 `tools/pareto.py` · `tools/coverage.py` · `tools/contents.py`。

## 2. 2026 年 SWE II 的预期 onsite（面经，不是官方）

最完整的一份（#8496901，SWE II，2026-09-02，编排者已核对原文）：

1. Recruiter → 2. **Live coding / codebase walkthrough**（= AI screen）→ 3. **Incident Reporting（AWS 环境）+ System Design（扩容已有系统）** → 4. **Code Review + System Extensions** → 5. **Managerial / Behavioral** → 6.（追加）**Technical Deep Dive**（"lacked sufficient judgment in a few areas" 未过）。

其它报道的变体：Glassdoor 2026-04（take-home 版）"Assignment review & iteration · System design & Incident handling · Code review & fix implementation with AI · Engineering manager interview"；Glassdoor Sr SWE 2026-06 "coding exercise with AI assistant, then a take-home code review"；#8387564 SDE II 2026-07 "AI-Assisted Machine Coding → Incident Management + System Design"（次日被拒）。

## 3. 矛盾与未知（问 recruiter）

| 问题 | 为什么要问 | 怎么问（English） |
|---|---|---|
| onsite 有哪几轮、各多长、是否都允许用 AI | 面经三种版本不一致；官方只说 "Team Interviews" | "Could you share the format of the remaining rounds — which are technical, and is AI tooling available in all of them?" |
| code review 是否提前发链接 | 1p3a 2025-10 与 Glassdoor 2026-06 说提前发；#8496901 没说 | "Will I get the code review repository ahead of time?" |
| incident 环境是真实 AWS 控制台还是只读截图 | 决定练习方式 | "For the incident round, is it hands-on in a console or more of a discussion?" |
| 身份核验 / export-control | 职位页 O-3：EAR 管制技术，"candidates offered employment must be eligible to access controlled technology"；"we … validate applicants at various stages" | 若身份/签证有任何不确定，**现在**就问 recruiter，不要等到 offer |

## 4. 旧流程（2024 – 2025，仅作背景）

"一共 4 轮"：① 图片去重（20 min 讨论 + 30 min 写）② manager chat ③ code review（预发 link）+ system design ④ coding + past project deep dive（自己 present 一个 problem domain）。每轮"一半讨论一半做题"。详见 `catalog/raw/process_and_rounds.md` §2。
