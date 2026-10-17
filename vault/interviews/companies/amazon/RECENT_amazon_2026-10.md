# Amazon 近一月面经（2026-09-16..10-16，不含 OA）

> 来源：一亩三分地 39 帖 + 题库 29 条（[[1p3a_2026-10-16]]）、Hello Interview 27 条报告（[[hellointerview_2026-10-16]]）。
> 抓取 2026-10-16，Chi 的账号登录。1p3a 几乎每帖核心段落要「积分 > 188」才可见（Chi 目前 99），下面的题目来自可见文字、
> 楼下回复、站方摘要与题库 slug；看不到的部分标 **（重建）**。置信度：高 = 原文可见；中 = 摘要 / 题库点名；低 = 片段。

## 0. 一句话结论

- **OA 之后的轮次里，本月被点名的题几乎全是熟题或熟题变形**：word ladder、task / course scheduling、LRU、group anagrams、
  sliding window max、LCA、399、472、topo sort；1193105 的楼主原话「备考 Amazon 感觉确实不用紧张，基本不会有非常规题目」。
- **OOD 是最确定的一轮**：本月 10 道 OOD 被点名（火车票价、折扣引擎、Locker、可配置缓存、停车计费、Pub/Sub、find API、
  机器人餐厅、file watcher、增删查最近值），全部写进 LLD deck「10 Amazon 专项」，按由浅入深排好。
- **coding 与 LLD 都是 dry run**（1193105：「都是dry run，不用跑」；Hello Interview：「syntactically correct, although it
  will not be executed」）：练手写 + 手动走查，不要依赖运行。
- **每轮先 LP 10–30 分钟**，BQ 原话见 §4；L6 店面里面试官会要求「换一个更重大的故事」。

## 1. 在哪练（Anki + Obsidian）

| 轮 | Anki deck | Obsidian |
|---|---|---|
| OOD / LLD | `低层设计（LLD）::10 Amazon 专项（Amazon OOD）`（卡片顺序 = 学习顺序） | 每题的题解 `solution-amz-*`、drill `design-amz-*`，入口 [[低层设计（LLD） MOC]] |
| Coding | `LeetCode Tops::22 Amazon 近一月原题（2026-10）`（新题整题召回卡）；本月出现过的老题已在 `20 Amazon 高频 A 档` | `recent/coding/amz_*`，解法 `coding/solutions/` |
| 系统设计 | —（题解，无卡） | [[sd-index]]（`interviews/core/system-design/`） |
| LP | — | §4 的原话 → `lp/question_bank.md`、[[story_matrix]] |

## 2. Coding（店面 / onsite）

| 题 | 报告 | 置信度 | 在哪练 |
|---|---|---|---|
| LC 127 Word Ladder（听过即换题） | 1p3a 1193105 SDE II onsite 2026-10-02 | 高 | A 档已有 |
| LC 621 / 207 / 210（task、course scheduling、DAG 拓扑） | 1193105 onsite；1192714 L5 店面 R1 | 高 | A 档已有；LLD `amz-dag-runner` |
| LC 146 LRU | 1189999 SDE II 店面 2026-09-18；题库 8 源 | 高 | A 档已有；LLD `amz-configurable-cache` |
| LC 239 Sliding Window Maximum（O(k) 空间、结构对比、单调队列） | 1192827 onsite | 高 | A 档已有 |
| LC 49 Group Anagrams（禁止排序签名） | 1191823 NG onsite | 高 | A 档已有 |
| LC 305 / 岛屿逐行流式（并查集） | 1191823 follow-up；题库 3 源 | 高 | deck 22 |
| LC 235 / 236 LCA；组织架构最低共同上级 | 1191548 L6 店面；题库 3 源 | 高 / 中 | A 档已有；deck 22 |
| LC 399 + 缓存追问 | 1191084 L6 店面；题库 | 中 | A 档已有；deck 22（追问卡） |
| LC 472 Trie + DFS 写法 | 1192241 L5 店面 | 中 | deck 22 |
| 棋子最少步数吃王（BFS，重建） | 1192241 L5 店面 | 中 | deck 22 |
| LC 490 + 方向约束 | 1190455 SDE II 店面 | 高 | deck 22 |
| LC 347（流式 follow-up）、LC 474 | Hello Interview 店面 2026-10-01；题库 | 中 | A 档已有 |
| LC 815、3286、2365、332、45（返回路径） | Hello Interview 2026-09-10..10-01 | 中 | deck 22 |
| 多粒度滑动窗口限流 | Hello Interview 店面 2026-10-01 | 中 | deck 22 |

## 3. OOD 与系统设计

OOD 的学习顺序就是 LLD deck 10 的叶子顺序：Amazon LLD 轮怎么打 → 增删查最近值 → 火车票价 → 折扣引擎 → Linux find →
应急 Pub/Sub → 可配置缓存 → 停车计费 → 现场版 Locker → 机器人餐厅 → File Watcher → DAG 执行器。
系统设计七题见 [[sd-index]]：短链接、Amazon Lockers、配送中心库存、跨区域文件复制、疫苗预约、Agentic AI 安全事件平台、外部排序。

## 4. LP / BQ 原话（本月）

映射是 `推断`，依据 [[story_matrix]] 的 P 标记；换故事前先看该故事的 senior 门槛。

| 原话（来源） | LP | 先用 |
|---|---|---|
| a time you made a decision with incomplete information（1191823） | Are Right, A Lot / Bias for Action | S6、S5 |
| a time you disagreed with a teammate or your manager and how you handled it（1191823） | Have Backbone | S3、S6 |
| taking a calculated risk：风险怎么量化、兜底方案、结果、重来会不会改（1191823） | Bias for Action | S7、S6 |
| influencing without authority：用了什么手段、被拒绝过几次、怎么落地（1191823） | Earn Trust | S2、S10 |
| pushed back against a decision that negatively impacted your team（1191754） | Have Backbone | S6、S3 |
| a system was failing intermittently, and the very obvious metrics were all looking good — root cause, how long（1191754） | Dive Deep | S3、S8 |
| a problem that required in-depth thought and analysis — how did you know you were focusing on the right things（1191754） | Dive Deep / Are Right | S4、S10 |
| 如何评估客户体验（1191548 L6） | Customer Obsession | S4、S9 |
| 重大的、未预料到的阻碍——面试官嫌不够重大让换故事（1191548 L6） | Deliver Results | S1、S5 |
| 需要 deep dive 进去找到问题点（1189999） | Dive Deep | S3、S8 |
| identified a customer pain point；customer asked for a requirement that is not feasible（Hello Interview 2026-09-20） | Customer Obsession / Earn Trust | S9、S10 |
| work outside of your comfort area；How would you validate code written by AI?；a time you failed；pushed back on a decision；a complex problem；trade-off between two competing priorities（Hello Interview 2026-09-10，senior / manager） | LBC / GenAI / Ownership / Backbone / Dive Deep / Deliver Results | R2、`lp/genai/`、S3、S6、S4、S5 |
| 20 分钟简历深挖：技术栈选型、trade-off（1190455 SDE II 店面） | — | 简历每一行都要能讲到选型理由 |

## 5. 流程信号（本月）

- SDE II：OA → 店面（1 小时，先 tech 后 LP）→ 四轮背靠背，可选 in person 或 zoom（1193105）。
- 整理帖 1191766：NG 的 OA 2.5–4 小时（coding 2 + Work Simulation + Work Style）；SDE-2 的 OA 有独立 15–20 分钟系统设计；
  挂后冷冻期可能从 6 个月变成 1 年（多方说法，无官方证实）。
- 1p3a 的完整原文要积分 ≥ 188：Chi 登录后发帖 / 回帖攒分，或 VIP，可回来补全本表「隐藏」的格子。
