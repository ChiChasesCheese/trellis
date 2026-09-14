# Snowflake 面试 Loop 指南（每一轮：形式 · 评什么 · 通过线 · 挂点 · 备考动作）

> 每轮的**全部题目**（按 28 法则排序、★ = cut line）见 [`../CONTENTS.md`](../CONTENTS.md)；本文件讲每轮怎么考、怎么备，题号只举例。

> 证据全部来自 `catalog/raw/`（每条可回溯）与 `../raw/`（AI 轮 dossier）；题目主键见 `catalog/CATALOG.md`；练习目录 `loop/rounds/`；演练器 `loop/mock.py`（OA 用根目录 `drill.py`）。
> 面向读者：1.5 YOE 后端（PayPal Braintree Snowflake-native 结算平台 owner），目标 IC1 争 IC2。**结论先行，细节靠证据。**

## 0. 总图

```
投递（Ashby）→ Chakra AI 语音筛 20 min（BQ + 项目，无 coding；人看记录）
  → HR / HM call 15–30 min（有时在 AI 筛之前）
  → [HackerRank OA 2–3 题 / 90–135 min]（实习/NG 为主；2026 全职一手几乎没有）
  → 技术电面 ×2 back-to-back，各 60 min（1 coding + 1 SD，或 2 coding）
  → Onsite 4–5 轮 × 60 min：coding ×1–2（"coding speed" 可能加一轮）· expertise/resume · SD · HM/BQ
  → Team matching（GenSWE 最后一步，真实门槛）→ offer
```

| 数字 | 值 | 来源 |
|---|---|---|
| 端到端 | 官方 2–4 周；一手内推→HR→约面 4 天（2026-08） | careers/gethired · t.me 29627 |
| 电面→结果 | 3–5 天（聚合站，low） | Leon |
| 通过线 | 电面"只是 screens"；**onsite 每轮都要 Hire** | Blind 2025-10 |
| 定级 | 1.5 YOE ≈ IC1（Bay Area 中位 $236K）；IC2 $341K；down-level 有报道 | levels.fyi 2026-09-13 · Blind |
| 拒信 | 两轮电面后无 onsite 直接拒、无反馈的案例 | Blind 2025-03 |
| Team match | 全过后因 headcount 被搁置 10+ 天的一手案例；offer 后被推去换组再失联（HN 2026-07） | Blind 2025-06 · HN 49061416 |
| NDA | onsite 需签 NDA（与 Databricks、Stripe 同） | HN 42580120（2025-01） |

**贯穿所有技术轮的评分主线**：① 先讲清 approach 再写（面试官会给 hint，但沉默型也存在）② 每题至少准备一个更难 follow-up（O(n)→O(1)、加并发、加持久化、加多副本）③ OOD 题默认有**并发 / 分布式正确性**追问（5/10 OOD 题明确）④ SD 题是 infra/data 题不是 Twitter 题，先说不变量再画图 ⑤ 每轮前 15–20 min 可能先讲项目——项目故事要能被追问三层（why · alternatives · availability/fault tolerance）。
**语言**：Python 最快；JD 里 Java 4/6、C++ 2/6，电面用 Python 无报道被扣分；OA 历史上曾限 Java/C++（2022 实习），开考前看语言列表。

---

## 1. Chakra AI 语音筛（20 min）

- **形式 / 评分 / 剧本**：见 `../03-chakra-playbook.md`（逐分钟英文稿）、`../../core/playbooks/ai-voice-screen.md`（机制）、`../raw/chakra.md`（证据）。
- **一句话**：Reporter 只读 transcript；每个 expectation 要有 clarity / ownership / structured reasoning / specific examples 的**具体证据**；theoretical = Not Met；没说到 = 0。
- **练习**：`../07-mock.md`（20 min 计时）；关键词卡 `../CARD.md`。

## 2. Recruiter / HR call（15–30 min）

- **形式**：背景、infra 经验、平台项目、方向偏好、why Snowflake、时间线/地点（Menlo Park vs Bellevue）。Infra 岗一例 15 min 结束。
- **评什么**：能否具体讲出 Snowflake 的产品/技术方向（不是"大厂"）；沟通清晰。
- **挂点**：此阶段报薪资数字；讲不出具体的 why。
- **备考动作**：`../fit.md` 的 Why Snowflake（Execution Anchor 博客 + 37% 增速 + CoCo/CoWork + Postgres 上移）；level 只说"看 team 与 scope 再谈"。
- **练习**：`python3 loop/mock.py bq recruiter -n 5` · 题库 `loop/rounds/01_recruiter/`。

## 3. HackerRank OA（2–3 题 / 90–135 min，若有）

- **形式**：HackerRank，Proctor（截屏）；2–3 题 medium–hard；2025 Infra 实习为 2 DP + 1 回溯；题在 OA 与电面池之间复用。
- **题型**：DP（元音游程、paid/free server、加权区间调度、2D DP）· 图（拓扑、Wiki BFS、valid tree）· 树（高度压缩）· 区间（merge、最小覆盖区间）· 计数/双指针（Paint the Ceiling、login codes）· 大量 LC 原题（56/94/210/261/484/1639/1851/1962/2002/2050/2062）。
- **通过线**：无一手分数线；聚合站"拒信可在数小时内"。
- **挂点**：DP 状态设计慢；n ≤ 6e6 的生成题用 O(n log n) 超时；LC 原题没刷过。
- **备考动作**：`catalog/CATALOG.md` Table A cut line 内的 OA 题全部用 `drill.py` 计时做一遍（每题 30–40 min）；LC 原题直接刷原题；Stripe 库 qA01–qA13 里的图/DP 题顺带过。
- **练习**：`python3 drill.py list / start q02 -m 40 / test q02 / ref q02 / status`。

## 4. 技术电面（60 min = 10 介绍 + 40 编码 + 10 反问；两轮 back-to-back）

- **形式**：CoderPad；一轮 coding（LC medium + 更难 follow-up，或 OOD 类设计）+ 一轮 SD，或两轮 coding；开头 15–20 min 可能先讲项目。senior 版一轮内 coding + design 二合一。
- **题型**：**RBAC/DAG 权限继承**（#1，4 阶段递进，含反向查询）· 多源 BFS 网格 · 事件流滑窗 · 分布式树计数状态机 · 树高压缩 · Wiki BFS · LC 1751 变体 · Happy Number O(1) · Word Search II · OOD（文件系统、事务 KV、多规则限流、Throne Inheritance）。
- **评什么**：思路先行、正确性、能接住 follow-up、代码整洁；"人都很好、会给 hint"是多数，但也有沉默型。
- **通过线**："只是 screens，不 signal"——但两轮后可直接拒。
- **挂点 top5**：① follow-up 接不住（O(n)→O(1)、并发）② 项目讲 20 min 讲不出 why ③ 类设计没先定 API 契约 ④ 反向查询（"谁拥有某权限"）没想到倒排 ⑤ 沉默面试官下自己不说话。
- **备考动作**：每题 40 min 计时；先写接口与 3 个自测；讲 trade-off；`03_phone_coding/pc01` RBAC 四阶段必做；`04_ood` 每题做完加"并发版"口述。
- **练习**：`python3 loop/mock.py start pc01 -m 40` … `test pc01 -k part1` … `ref pc01`；材料 `study/10-rounds/03-phone-coding.md`。

## 5. Onsite · Coding（60 min，1–2 轮）

- **形式**：同电面但更长；一手：Task Scheduler addTask/executeTask（重复 ID 变体，挂经）、Parallel Courses III 原题、滑窗限流器、LRU、Meeting Rooms II（实习）。
- **评什么**：同电面 + "coding speed"（有因速度被加第三轮 coding 的一手）。
- **备考动作**：`04_ood` 全部 + Stripe `problems/qA*` 算法组；每题 45 min 内做完 base + 一个 follow-up。

## 6. Onsite · System Design（45–60 min）

- **形式**：一段业务描述；白板工具未证实（Stripe 用 Whimsical，Snowflake 无报道）；面试官两极。
- **题型**（Table C）：**PB 级数据库间同步（IC2 一手：不允许需求澄清，直接设计）** · KV store（含 time travel / Raft）· cron/job scheduler / "SQL engine as cron"· SQL notebook 结果分发 · quota · audit log · rate limiter · distributed queue · Jira→PR 自动化 · DAG cache（≈ Dynamic Tables）· password storage · web crawler。
- **评什么**：需求与不变量抽取 → API/数据模型 → 失败模式与规模 → 分层 → rollout/监控（沿用 Stripe 五维 rubric）；**能把 Snowflake 自己的原语当参照**（Execution Anchor 单写者、FDB 元数据、serverless Tasks、Streams offset、Dynamic Tables 增量刷新）是差异化加分。
- **挂点**：面试官不给澄清时停住——要自己口头声明假设再推进（sd22 一手）；直接画框图不说不变量；exactly-once 说成能做到；沉默面试官下不自问自答；quota/rate limiter 说不清强一致 vs 本地缓存。
- **备考动作**：`05_system_design/sd01–sd11` 每题 45 min 口述 + 对照 rubric 自评 + followups 逐条能脱口而出；`../05-applied-scenarios.md` 的六个骨架先背熟。
- **练习**：`python3 loop/mock.py start sd01 -m 45`（打印 prompt，rubric 作提示）。

## 7. Onsite · Expertise / 项目深挖（早期职业：嵌在 coding 前 15–20 min + 一轮 resume；IC3 独立 40 min）

- **问什么**：选一个项目讲透——为什么这个架构/这个库、备选方案、可用性/容错、现在看有什么问题、会怎么重做。
- **评什么**："depth of knowledge in your domain"；每个设计决策的 why；senior 级 trade-off 表达。
- **挂点**：只讲做了什么；被问"还有什么选项"卡壳；停在功能层不谈系统属性。
- **备考动作**：S1（AMEX 管线）与 S5（net settlement shadow-run）各准备 15 min 深挖版：架构图口述 → 3 个决策各带 2 个被否方案 → 失败模式与监控 → 重做清单。素材 `../../core/stories/evidence-base.md`、`resume-evidence-map/01、02`。
- **练习**：`loop/mock.py bq expertise -n 3`（`06_project_deep_dive/`）。

## 8. Onsite · HM / Behavioral（30–45 min，逐题记笔记）

- **问什么**：mistake · ownership · 陌生团队协作 · teamwork · conflict · pushback（disagree-and-commit）· prioritize · customer first · raise the bar；8 条价值观逐条对应。
- **评什么**：Own It / Get It Done / Integrity Always 最常；有具体数字与"我"的动作。
- **挂点**：把分歧对方说成不讲理；讲不出自己改了什么流程；术语堆砌。
- **备考动作**：`../04-answer-bank.md` §3 + §5 价值观矩阵；`../../core/answers/` Q1–Q24；每故事 90 s / 3 min 两版。
- **练习**：`loop/mock.py bq hm -n 3 -m 3`（`07_hm_behavioral/`）。

## 9. Team Matching（GenSWE 最后一步，HM 30–45 min）

- **形式**：HM 介绍团队、问匹配度；候选人按经验/技能/偏好被配对。
- **评什么 / 风险**：团队要不要你 + headcount 是否还在。一手：技术全过后 HM 对话 → headcount 被占 → 新 HM 重面 → 10+ 天无回音。
- **备考动作**：面试过程中就问 recruiter 在匹配哪些 org（Product Experience / Database Engineering / Query Processing / Cloud Services / Billing / AI Platform）与 headcount；准备 3 个偏好方向（transactions/scheduling/metering）与理由；反问见 `../06-questions-to-ask.md` §C/§D。
- **练习**：`loop/mock.py bq team -n 3`（`08_team_matching/`）。

## 10. 一页备考日程（收到电面邀请起，5 天）

| 天 | 做什么 |
|---|---|
| D1 | CATALOG 读一遍；pc01 RBAC 四阶段 + od01 task scheduler 计时做完；sd01 KV 口述一遍 |
| D2 | q02/q03/q01 三个 OA 题族；od02 文件系统 + 并发版；sd02 scheduler、sd03 notebook |
| D3 | pc02/pc03/pc04/pc10；od03 事务 KV；sd04 quota、sd06 audit、sd07 rate limiter |
| D4 | LC 原题组（484/94/210/2050/1751/Happy Number）；od04/od05/od09；sd05/sd11/sd08/sd09 |
| D5 | expertise 15 min 深挖 ×2；bq hm ×6；team matching 反问；复盘 status 板 |
