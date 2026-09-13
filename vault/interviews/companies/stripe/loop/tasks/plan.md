# Implementation Plan：Stripe 面试 Loop 套件（OA 之后全部轮次）

> 状态：草案 2026-09-01 · 分支 `worktree-stripe-loop` · 全部产物在 `loop/` 下（不动 `catalog/`、`problems/`）
> 执行方式：编排/理解 = 主会话（Fable 5.1）；产出 = `sonnet` 子代理，**并行 ≤ 5**，每个代理只写自己名下的目录（原子更新），共享文件（CATALOG / tree / LEDGER / CHECKPOINT）只由协调者改。
> 账本：`loop/LEDGER.md`（append-only，每任务一行：id · 代理 · 文件 · 测试数 · commit）。每个任务验收后立即 commit，commit 即检查点。

## Overview

把 OA 之后的 8 个轮次（recruiter → HM → phone screen → bug squash → integration → coding → system design → behavioral）做成可离线 mock 的练习套件：每轮有 **题目/题库 + 参考答案 + 自动测试或评分表 + 中文准备材料**，用 `loop/mock.py` 按真实时长（45/60 min）计时演练。技术轮沿用 OA 套件的 `CONVENTIONS.md`（`partN()` + `main()` + pytest markers + 根 `conftest.py` 的 `impl`/`run_script`），bug squash / integration 因形态不同另定契约（见下）。

## Architecture Decisions

1. **复用 OA 基建，不另起炉灶**：phone screen / coding 题目目录结构与 `problems/qNN_slug/` 完全一致（problem.md · starter_template.py · starter.py · solution.py · test_*.py · REPORT.md），根 `conftest.py` 自动生效（rootdir 级）。`pytest.ini` 的 `testpaths=problems` 不改；跑 loop 用显式路径 `pytest loop/rounds/...`。
2. **Bug squash = 自含小型库 + 注入的真实 bug 模式**（不 vendor requests/mako 等大库）：每题一个 200–600 行的 mini 包（模板引擎 / HTTP 客户端 / YAML+CSV 解析器 / 并发 ConfigManager / asyncio 竞态），`tests/` 里 1–3 个失败用例，`FIX.patch` + `REPORT.md`（根因、排查路径、最小修复）。`mock.py start bsNN` 把包拷到 `loop/work/bsNN/` 让用户在自己 IDE 里调。
3. **Integration = 本地 mock 服务器 + 真实 HTTP**：`loop/mockserver/`（stdlib `http.server`，零依赖）提供 map-render（返回 PNG）、payments（cursor 分页 / 429+Retry-After / Idempotency-Key / webhook 签名）两个服务；题目用 `urllib`/`http.client` 调用。PNG 用 `zlib` 手写最小编码器（无 PIL）。
4. **System design / 非编码轮 = 文档 + 评分表 + 自评脚本**：sd 题有 `prompt.md`（一大段业务描述，模拟真实题面）、`rubric.md`（Exponent 五维 + Stripe 主线）、`model_answer.md`（复用 `raw/system_design.md` §4 的中文模型答案）、`followups.md`（失败模式追问）。recruiter/HM/behavioral 是题库 + STAR-L 故事表 + Operating Principles 对照自评；`mock.py bq` 随机抽题计时。
5. **知识树用受限 YAML**（stdlib 无 yaml）：`loop/tree/interview-loop.yaml` 手写；`loop/tree/check_tree.py` 用正则抽 `id:` / `problems:` / `study:` 字段校验引用的目录与文件存在；`TREE.md` 由代理生成并被同一脚本校验同步。
6. **ID 规范**：`ps01..` phone screen · `cd01..` coding · `bs01..` bug squash · `int01..` integration · `sd01..` system design · `rc/hm/bq` 非编码轮。题目 ID 在本计划里一次性分配（下表），CATALOG / tree / rounds / study 全部引用同一 ID。
7. **不重做 OA 已有题**：与 `problems/` 重叠的（q19 accept-language、q21 currency、q08 closing time、q22 shipping、q32 rebalancing、q28 worker、q23 rate limiter…）在 CATALOG 里做交叉引用；loop 只实现**轮次形态不同**的版本（例如 rate limiter 的 4-part "basics→memory→tricky→threads"、shipping 的 fixed→tiered→mixed 计价版）。

## 题目 ID 分配（一次定死）

| ID | 题 | 轮次 | Part | 主要来源 |
|---|---|---|---|---|
| ps01 | Transaction stream levels（汇总→60s 滑窗→TopK→模式检测） | phone | 4 | cn learncswithus 2025-10-25 |
| ps02 | Shipping cost pricing（fixed→tiered→incremental/fixed mixed） | phone(intern) | 3 | cn learncswithus 2025-10-20；1p3a post/7100079 |
| ps03 | Brace expansion（展开→不匹配/单 token→嵌套） | phone | 3 | LC 5341224；interviewdb |
| ps04 | Data validation / fraud 4-part（非空→范围+黑名单→50% 行为匹配→对齐错误码） | phone | 4 | LC 7384225 |
| ps05 | Numeronym validation（校验 i18n 形式→按词典校验展开→生成最短唯一 numeronym）（invoice reconciliation 已在 OA q25） | phone | 3 | FinalRound；Exponent |
| ps06 | Receivables registration（CSV → merchant+card_type+payout_date 聚合 → 追问） | phone/coding | 2 | csoahelp 2024-10-04 |
| ps07 | Redact card numbers from logs（找候选数字串→Luhn/品牌去误报→保留后 4 位与格式→流式大日志）（Luhn 校验已在 OA q05） | phone/coding | 4 | interviewing.io C8；staffengprep |
| ps08 | Min/Max with comparator + ties | phone | 4 | rampatra 2020 |
| cd01 | Subscription email scheduler（基础→改 plan→续费） | coding | 3 | linkjob；1p3a post/7100084 |
| cd02 | PaymentLedger 类（add_payment/refund/revenue/by_date + 5 追问） | coding | 3 | programhelp intern VO |
| cd03 | AccountScheduler（可用性→acquire→LRU 自动选） | coding | 3 | linkjob 2025-12 |
| cd04 | Rate limiter 4-part（basics→省内存→边界→多线程） | coding | 4 | 1p3a post/7100089 |
| cd05 | Business account data verification（when/requires/one_of 规则引擎） | coding/VO | 2 | 1p3a problems/ad817329 |
| cd06 | Suspicious users sliding window（O(n²)→哈希+滑窗） | coding | 2 | programhelp VO 2025-09 |
| cd07 | Transactions + rules（关键词→AND/OR 布尔）— AI programming exercise 版 | coding(AI) | 3 | interviewdb AI guide |
| bs01 | mini template engine（Mako 型：AST visitor 缺节点 + 路径校验） | bug squash | — | Exponent；1p3a post/7100080 |
| bs02 | mini HTTP client（requests 型：BytesIO body 未 rewind / content-length） | bug squash | — | Blind hkzsddkz |
| bs03 | mini YAML+CSV parser（`flag: on` 布尔解析；RFC4180 引号丢失） | bug squash | — | 1p3a problems/9be00044、3edbdc05 |
| bs04 | ConfigManager 并发（懒加载竞态 / 粗锁 / teardown 残留） | bug squash | — | cn learncswithus 2025-11-17 |
| bs05 | asyncio 数据拉取竞态（stale 结果覆盖新结果，取消/忽略） | bug squash | — | 1p3a problems/977b9f31（React 版移植） |
| int01 | BikeMap（GeoJSON→POST 取 PNG→画路线→最近地标→批处理/缓存 CLI） | integration | 5 | oavoservice；learncswithus；1p3a |
| int02 | Payments reconciliation client（分页→429 退避→幂等键→webhook 验签） | integration | 4 | Simplify；Leon；官方 docs |
| int03 | Multi-JSON ETL（读 3 个 JSON→字典→双向转换→join） | integration | 3 | linkjob 2025-12 |
| int04 | Review assignment via git diff + CSV owners | integration | 3 | 1p3a problems/1eb955cf |
| sd01 | Webhook delivery（10k/s、500、noisy neighbor、SSRF、exactly-once） | SD | — | Medium emily 2026-05 |
| sd02 | Idempotent payment / charge API | SD | — | linkjob；techinterview |
| sd03 | Ledger service（双记账、不可变、point-in-time） | SD | — | programhelp；prachub |
| sd04 | Distributed rate limiter（API 网关） | SD | — | Exponent；Paul Tarjan |
| sd05 | Subscription billing & invoicing | SD | — | ophyai；raw §4.5 |
| sd06 | Connect 分账 / payouts + Feature-flag SDK / Metrics counter（短题 ×3） | SD | — | 1p3a post/7100093、7100094 |
| rc | Recruiter 电话题库 + 反问清单 + 薪酬/时间线速查 | recruiter | — | hr_hm_behavioral §Recruiter |
| hm | HM chat 题库 + Operating Principles 映射 + 故事表 | HM | — | hr_hm_behavioral §HM |
| bq | Behavioral 题库（Stripe 专属 + 跨公司 20 题）+ STAR-L 自评 | behavioral | — | hr_hm_behavioral §Behavioral |

## Dependency Graph

```
raw/*.md (6 份)
  └─ T1 CATALOG.md ─┬─ T2 LOOP_GUIDE.md
                    ├─ T3 tree/interview-loop.yaml (+check_tree.py)
                    │      └─ T20 TREE.md（最后渲染/校验）
                    └─ T4 mock.py + loop/conftest 约定 ─┬─ T5–T8 phone screen ps01–08
                                                      ├─ T9–T12 coding cd01–07
                                                      ├─ T13 mockserver ──┬─ T14–T15 integration int01–04
                                                      ├─ T16–T17 bug squash bs01–05
                                                      ├─ T18 system design sd01–06
                                                      └─ T19 非编码轮 rc/hm/bq
   study/00-prereq（已有）─ T21–T22 study/10-rounds ─ T23 study/20-cards ─ T24 README/INDEX
                                                              └─ T25 review + 全量测试 + LEDGER 收口
```

## Phases & 并行分配（每格 = 一个 sonnet 代理，≤5 同时）

| Phase | 并行槽 1 | 槽 2 | 槽 3 | 槽 4 | 槽 5 | 协调者（Fable） |
|---|---|---|---|---|---|---|
| 0（进行中） | raw: github_repos + stripe_official | | | | | 等待 → commit |
| 1 | — | — | — | — | — | **T1 CATALOG、T2 LOOP_GUIDE、T3 tree.yaml**（理解型，自己写） |
| 2 | T4 mock.py + loop/README | T5 ps01–02 | T6 ps03–04 | T7 ps05–06 | T8 ps07–08 | 验收每份 → commit → LEDGER |
| 3 | T13 mockserver（先）→ T14 int01–02 | T9 cd01–02 | T10 cd03–04 | T11 cd05–06 | T12 cd07 + T16 bs01–02 | 同上 |
| 4 | T15 int03–04 | T17 bs03–05 | T18 sd01–06 | T19 rc/hm/bq | T21 study/10-rounds（01–04） | 同上 |
| 5 | T22 study/10-rounds（05–08） | T23 study/20-cards | T20 TREE.md + check | T24 README/INDEX | code-reviewer 审 rounds | T25 全量测试 + LEDGER/CHECKPOINT 收口 |

## 各任务契约（代理必须遵守）

- **只写自己名下目录**；不得改 `loop/CATALOG.md`、`loop/tree/*`、`loop/LEDGER.md`、`loop/CHECKPOINT.md`、根目录任何文件；不 git commit。
- 每题按 `CONVENTIONS.md`：problem.md（含 Part 1..N、worked examples、edge list、sources+confidence、"what this tests"）→ starter_template.py（+cp starter.py）→ solution.py → test_*.py（markers `partN` + `edge/fmt/perf/io`）→ REPORT.md。**写一题落盘一题**。
- 测试命令：`rtk proxy python3 -m pytest loop/rounds/<round>/<id> -q`；再 `IMPL=starter` 跑一次确认空 starter **失败**。
- 全中文（题名/代码/API 英文）；密度优先，禁水文。
- 完成后返回：文件清单、测试数（按 marker）、未解决点、一行 LEDGER 记录。

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| 子代理撞 session limit 丢工作 | High | 每题落盘；每代理 ≤2 题/≤8 文件；协调者每收一份就 commit |
| 并行代理写到同一文件 | Med | 目录级所有权表（本文）；协调者验收时 `git status` 检查越界改动 |
| Bug squash 题"注入 bug"太假 | Med | 每题必须对应 raw 里报道过的真实 bug 模式 + issue 链接；REPORT 写"真实版在哪个库哪个 PR" |
| Integration 依赖网络/第三方库 | High | 全部走本地 mockserver + stdlib；PNG 用 zlib 手写 |
| 与 OA `problems/` 重复 | Low | ID 表已排除重叠；CATALOG 做交叉引用 |
| YAML 无解析器 | Low | 受限 YAML + 正则校验脚本 |
| catalog/CATALOG.md 有 4 行未提交遗留改动 | Low | 不动、不提交；在 LEDGER 备注 |

## Open Questions（不阻塞，按默认假设推进）

1. mock.py 的 bug squash 工作区放 `loop/work/`（git-ignore）——假设可以。
2. ps 题时长按 45 min、cd/int/bs 按 60 min、sd 按 45 min 计时——按 raw 多数报告取值。
3. study/20-cards 采用 Markdown Q/A 表格（可转 Anki）——不引入工具。
