# TODO：Stripe 面试 Loop 套件（与 plan.md 同步；完成即在 LEDGER.md 记一行并 commit）

约定：每任务 ≤ 5 文件 × 每题；验证命令统一 `rtk proxy python3 -m pytest <dir> -q`，starter 必须失败：`IMPL=starter rtk proxy python3 -m pytest <dir> -q`。

## Phase 0 · raw 收尾（进行中）
- [x] T0a `loop/raw/cn_forums.md`（commit 0d8fe08）
- [x] T0b `loop/raw/github_repos.md` + `loop/raw/stripe_official_and_api.md`
  - AC：两文件各 ≥ 250 行；每条带来源；`## 附` 列出失败来源
  - 验证：`wc -l`；`grep -c 'http' ` ≥ 80

## Phase 1 · 汇总层（协调者自写）
- [x] T1 `loop/CATALOG.md`
  - AC：按轮次分表（phone / coding / bug squash / integration / SD / 非编码），每行含 ID·题名·别名·part 递进·最近报道·#refs·置信度·与 OA `problems/qNN` 的交叉引用·来源；覆盖 plan.md ID 表全部 33 个 ID；末尾"来源可信度"与"未收录/存疑"节
  - 验证：`grep -c '^| ps\|^| cd\|^| bs\|^| int\|^| sd' loop/CATALOG.md` = 33
- [x] T2 `loop/LOOP_GUIDE.md`
  - AC：流程总图（校招 vs 社招）、每轮 1 页（形式·时长·平台·评分维度·通过线·挂点 top5·备考动作·对应 rounds ID 与 study 章节）、时间线/HC/team match/offer、AI 轮、语言选择结论
  - 验证：8 个 `## ` 轮次节全在；每节含"对应练习"链接且路径存在（`check_tree.py --guide`）
- [x] T3 `loop/tree/interview-loop.yaml` + `loop/tree/check_tree.py`
  - AC：节点 = 轮次 → 技能 → problems（ID）→ study 章节；受限 YAML（2 空格缩进、`key: value`、`- item`）；check_tree.py 校验所有 `rounds/<round>/<id>` 与 `study/...` 路径存在、ID 与 CATALOG 一致
  - 验证：`python3 loop/tree/check_tree.py` 退出码 0（此时允许"目录尚不存在"以 warning 报告）

### Checkpoint A（Phase 1 后）
- [x] CATALOG 33 ID 全覆盖；check_tree 通过；commit；LEDGER 记 T1–T3；CHECKPOINT.md 更新

## Phase 2 · 基建 + phone screen（5 并行）
- [x] T4 `loop/mock.py` + `loop/README.md` + `.gitignore`（loop/work/）
  - AC：`list / show <id> / start <id> [-m] / test <id> [-k] / ref <id> / time <id>`（对齐 drill.py）；bs 题 `start` 拷贝到 `loop/work/<id>/` 并跑失败测试；int 题 `serve <id>` 启动 mockserver；`bq [round] [-n]` 随机抽题计时；默认时长 ps45/cd60/int60/bs60/sd45
  - 验证：`python3 loop/mock.py list` 列出全部 rounds；`python3 loop/mock.py start ps01 -m 45` 生成计时文件；`rtk proxy python3 -m pytest loop/tests/test_mock.py -q` 绿
- [x] T5 ps01 transaction_stream_levels · ps02 shipping_cost_pricing
- [x] T6 ps03 brace_expansion · ps04 data_validation_fraud
- [x] T7 ps05 numeronym_validation · ps06 receivables_registration
- [x] T8 ps07 redact_card_numbers · ps08 minmax_comparator
  - T5–T8 共同 AC：每题 6 文件齐（problem.md / starter_template.py / starter.py / solution.py / test_psNN.py / REPORT.md）；每 part ≥ 3 测试 + edge/fmt/io 各 ≥ 1 + perf 1；problem.md 含 worked example 与来源置信度；REPORT 含"面试官追问"节
  - 验证：solution 全绿；starter 全红；`git status` 无越界文件

### Checkpoint B（Phase 2 后）
- [x] `rtk proxy python3 -m pytest loop/rounds/03_phone_screen -q` 全绿；mock.py 可 start/test 任一 ps 题；commit ×5；LEDGER；CHECKPOINT

## Phase R · Review（Fable 5.1）+ 文章（在 Phase 3 收尾后、Phase 4 之前；用户指示）
- [x] R0 `loop/lint.sh`、`loop/tasks/review_checklist.md`、`loop/study/30-articles/_TEMPLATE.md`；基建 lint 通过
- [x] R1 ps01–ps04：review → 修 → lint → 测试 → 文章 `loop/study/30-articles/psNN_*.md`
- [x] R2 ps05–ps08
- [x] R3 cd01–cd03
- [x] R4 cd04–cd07
- [x] R5 int01–int04
- [x] R6 bs01–bs02
- [x] R7 全量（2026-09-02：499 tests 绿；lint 绿；19 篇文章已同步 Obsidian + Anki；遗留：ps03/05/06/07 文章骨架 41–46 行略超 40）：`pytest loop -q` 绿、`loop/lint.sh` 绿、文章 21 篇同步到 Obsidian `Inbox/Stripe Loop/`（含索引 + `Claude 接力.md` 链接）、LEDGER/CHECKPOINT、commit
  - AC：每题 REPORT.md 有 `## Review（Fable 5.1）` 节；每篇文章 8 节齐、≤40 行核心骨架、无 corner-case 堆砌

## Phase 3 · coding + mockserver + integration 前半 + bug squash 前半（5 并行）
- [x] T13 `loop/mockserver/`（先做，同一代理随后做 T14）
  - AC：`maps.py`（POST /render JSON 坐标 → 返回最小合法 PNG；GET /health）；`payments.py`（GET /v1/charges 带 `limit/starting_after` cursor 分页与 `has_more`；每 N 次返回 429 + `Retry-After`；POST /v1/refunds 支持 `Idempotency-Key` 头：重放返回同响应、body 不同返回 400；POST /webhook 事件带 `Stripe-Signature` t=…,v1=HMAC）；纯 stdlib；`python3 -m loop.mockserver.maps --port 0` 打印端口
  - 验证：`rtk proxy python3 -m pytest loop/mockserver/tests -q` 绿（分页/429/幂等/签名各 ≥ 2 测试）
- [x] T14 int01 bikemap · int02 payments_reconciliation
- [x] T9 cd01 subscription_email_scheduler · cd02 payment_ledger
- [x] T10 cd03 account_scheduler_lru · cd04 rate_limiter_4part
- [x] T11 cd05 business_account_verification · cd06 suspicious_users_window
- [~] T12 cd07 transactions_rules_ai ✓ · bs01 mini_template_engine ✓ · **bs02 mini_http_client 从未落盘**
  - 更正（2026-09-03）：本条原先勾成 [x]，但 git 历史里 `loop/rounds/04_bug_squash/` 只出现过 bs01。bs02 退回 BACKLOG，与 T17 的 bs03–05 一起排。
  - cd 题 AC 同 T5–T8；cd04 part4 含线程安全测试（`threading` 并发 1000 次无超发）
  - int 题 AC：目录含 `problem.md`（含 API 文档节）、`data/`（ride-simple.json 约 500 点 / charges 样本）、`starter_template.py`、`solution.py`、`test_intNN.py`（fixture 起 mockserver 于随机端口、结束关闭）、`REPORT.md`；测试覆盖 happy path + 网络错误 + 分页第 2 页 + 429 退避 + 幂等重放
  - bs 题 AC：`src/<pkg>/`（200–600 行）、`tests/`（1–3 个失败用例 + 其余通过）、`README.md`（库用途、跑测试命令）、`solution/FIX.patch`、`REPORT.md`（根因·排查路径·最小修复·真实库对应 issue/PR）；`git apply --check solution/FIX.patch` 通过；打补丁后全绿
  - 验证：同上 + starter 红

### Checkpoint C（Phase 3 后）
- [ ] `pytest loop/rounds/06_coding_onsite loop/rounds/05_integration/int01 loop/rounds/05_integration/int02 loop/mockserver` 全绿；bs01/02 打补丁前红、后绿；commit；LEDGER；CHECKPOINT

## ⏸ BACKLOG（用户 2026-09-01 指示：先 review 已有题，以下暂停）

## Phase 4 · integration 后半 + bug squash 后半 + SD + 非编码轮 + study 前半（5 并行）
- [x] T15 int03 ✓ · **int04 ✓（2026-09-03 收尾）**：补齐 starter.py / test_int04.py（34 测试）/ REPORT.md；测试在 tmp_path 里真起 git 仓库造 A/M/D/R 变更，无 git 时 skip；solution.py 未改动；lint 绿
- [x] T17 bs02 mini_http_client · bs03 mini_yaml_csv · bs04 config_manager_concurrency · bs05 asyncio_fetch_race
  （T12 里 bs02 原被误勾为已完成，实际从未建过，本轮一并补齐并更正记录）

### Bug Squash 五题实测（2026-09-03）

| 题 | 注入的两个 bug | 补丁前 | 打补丁后 |
|---|---|---|---|
| bs01 minimako | 少 `visit_IncludeNode` · 路径穿越校验漏 | 2 红 15 绿 | 17 绿 |
| bs02 minihttp | 测完长度没 seek 回原位 · `slice_length=None` 未判空 | 2 红 23 绿 | 25 绿 |
| bs03 miniyaml | `"- "` 占两列却按一列算 · 复用 Parser 没重置 `pos` | 2 红 23 绿 | 25 绿 |
| bs04 confmgr | check-then-act 拆成两段独立加锁 · `reload()` 没清缓存 | 2 红 29 绿 | 31 绿 |
| bs05 fetchrace | `release()` 不在 `try/finally` · 异常项被计入成功 | 2 红 14 绿 | 16 绿 |

并发两题（bs04/bs05）**确定性已验**：各连跑 20 次输出完全一致，再在 4 核满载下复跑仍一致。
"flake 不是根因"这条规矩要成立，题本身就不能是 flaky 的。

**注释纪律**（用户要求"注释告诉我代码在讲什么"与"自己找 bug"的平衡）：
`src/` 注释用英文白话讲**机制**（模块职责、数据流、信号量语义、什么受哪把锁保护），
但**没有一个字指向注入行**，注入行的注释密度与文件其余部分一致；根因只在 `solution/NOTES.md` 与 `REPORT.md`。
五题的 bug 都做成"**docstring 写对了契约、代码在下面违约**"这一型——读已经给你的那段文档就能找到。
每题另配中文 `CODE_GUIDE.md` 逐模块导读（开头即声明不会说 bug 在哪，第二遍起别读）。
调试入门见 `loop/rounds/04_bug_squash/DEBUG_101.md`（命令与 pdb 实录均在 bs01 上真跑）。

- [x] C27 Bitfont 三版本各建一题（用户指示"几个版本都来一份"）：
  `cd08_bitmap_ascii_render`（**真实复原**——完整题面藏在 PracHub 页面的 RSC 数据块里，
  上一轮误判为被锁）· `cd09_bitfont_binary_frames`（重建题，唯一来源无法核实）·
  `cd10_bitfont_render_compress_invert`（重建题，仅标题级证据）。
  三题 problem.md 互相交叉引用，说明"不确定的是整个家族，不是某一道"。
  cd09 的 REPORT 建议新增 **S25 二进制帧解码**（字节序 · MSB-first 取位 · RLE 游程），
  现有 S01–S24 / A01–A16 覆盖不到——**仅为建议，未改 `skills_matrix.md`**。
- [ ] T18 sd01–sd06：每题 `prompt.md`（一段业务描述 ≥ 300 字，不给结构）、`rubric.md`（五维 + 主线，可打分 1–4）、`model_answer.md`（≥ 150 行，含 API 契约/数据模型/失败模式/对账/可观测）、`followups.md`（≥ 8 条追问 + 期望要点）；复用 `raw/system_design.md` §4
  - 验证：每题 4 文件；`check_tree.py` 路径通过
- [ ] T19 `loop/rounds/01_recruiter/`、`02_hm/`、`08_behavioral/`：`questions.md`（去重题库，标来源与频次）、`stories.md`（STAR-L 6 故事表模板 + Operating Principles 覆盖矩阵）、`rubric.md`（自评）、`bank.json`（供 mock.py bq 抽题：`{round, q, principle, source}`）
  - 验证：`python3 loop/mock.py bq hm -n 3` 能抽题；bank.json 合法 JSON ≥ 60 题
- [ ] T21 `loop/study/10-rounds/01–04`（recruiter / HM / phone screen / bug squash 各一章）
  - AC：每章含：这轮到底考什么（引 raw 证据）· 评分表 · 时间分配 · 演练脚本（mock.py 命令）· 挂点→对策 · 对应 rounds ID · 自检清单；密度对齐 00-prereq；≥ 150 行/章
  - 验证：链接路径存在（check_tree --study）

### Checkpoint D（Phase 4 后）
- [ ] 全部 rounds 目录存在；`pytest loop -q` 全绿；bq 抽题可用；commit；LEDGER；CHECKPOINT

## Phase 5 · study 后半 + 卡片 + 树渲染 + 审查 + 收口
- [ ] T22 `loop/study/10-rounds/05–08`（integration / coding / SD / behavioral）AC 同 T21
- [ ] T23 `loop/study/20-cards/`：`stripe_api.md`（幂等/分页/expand/版本/429/webhook/PaymentIntent 状态机…≥ 60 卡）、`python_debug.md`（pdb/breakpoint/traceback/logging/bisect ≥ 30 卡）、`http_json.md`（≥ 30 卡）、`patterns.md`（滑窗/状态机/规则引擎/LRU/幂等键 ≥ 30 卡）；格式 `| Q | A | 来源 |`
- [ ] T20 `loop/tree/TREE.md` 渲染 + `check_tree.py` 严格模式（缺路径 = error）
- [ ] T24 `loop/README.md` 完整版 + `loop/study/INDEX.md`
- [ ] T25 审查：`agent-skills:code-reviewer` 审 rounds 抽样（每轮 1 题）；修复；`pytest loop -q` 全绿；`python3 loop/tree/check_tree.py --strict` 0；LEDGER 汇总表；CHECKPOINT 标"完成"

### Checkpoint E（完成）
- [ ] 33 ID × 全部文件；全量测试绿；tree 严格通过；README 可从零上手；commit + push 分支

---

## 2026-09-03 会话（进度追踪 + 二轮排查 + 收尾）

已完成并入库：

- [x] **进度追踪**：`tools/progress.py` + `tools/pytest_progress.py`；`drill.py status` / `loop/mock.py status`
  - 只聚合 `IMPL=starter` 的运行；`ref` 不入账；pytest 没跑起来的运行不记录
- [x] **int04 收尾**（见上 T15）
- [x] **来源登记表**：`catalog/sources.json`（518 URL / 91 站）+ `catalog/SOURCES.md` + `tools/refresh_check.py`
  - 更正：teamblind 换浏览器 UA 即 200（12/12 实测），leetcode 有 GraphQL 端点；**只有 1point3acres 真不可达**
- [x] **Table C 二轮排查**：`catalog/discovery/2026-09/` 三份报告；结论已写回 CATALOG.md Table C 的 Note 列 + 新增「2026-09-03 二轮排查增量」节
- [x] **LOOP_GUIDE §4** 吸收 bug squash 新证据（2–3 个 bug · 5 步流程 · 4 类典型 bug · 明确禁用 AI）

本轮新建的题与轮次（全部已验收合并：参考解全绿 · starter 绝大多数红 · lint 通过）：

| 目录 | 来源等级 | 测试 | starter |
|---|---|---|---|
| `ps09_matching_contacts` | 真实复原（high） | 22 | 16红/6绿 |
| `ps12_hierarchical_task_csv` | 真实复原（high） | 24 | 22红/2绿 |
| `ps13_incident_monitor` | 部分重建（Part 1 有实证） | 29 | 22红/7绿 |
| `ps10_rbac_role_resolver` | 重建题 | 28 | 21红/7绿 |
| `ps11_factory_cost` | 重建题 | 29 | 28红/1绿 |
| `problems/q41_observability_metrics` | 重建题 | 25 | 24红/1绿 |

- [x] T18 sd01–sd06（每题 4 文件；prompt.md 是无结构业务白话，不给需求清单）
- [x] T19 01_recruiter(14) / 02_hm(30) / 08_behavioral(50)，去重 66 题，`mock.py bq` 可用

**全量回归（2026-09-03，容器内）**：`problems` 1033 绿 / 1 红 · `loop`（除 bug squash）661 绿 / 4 红。
四条红分两类，**都不是本轮引入的**：

1. `loop/study/00-prereq/exercises/test_ex02.py` 3 条 —— `ex02_structure.py` 是**留给用户填的作答文件**（满篇 `# TODO`），红是它的正常状态，跟 starter.py 一个道理。
2. perf 预算：`cd06::test_perf_1m_rows` **单独跑是绿的**（3.23s），只在全量并跑时被 CPU 争用挤超时；`q07::test_perf_100k` 单独跑也红（3.40s vs 2.0s 预算），且**本轮开工前就是红的**（改动前实测 3.21s）。本容器 4 核，CPU 基准比开发机慢。**没有放宽预算去掩盖**——预算按用户开发机定的，就该按那个标准。

仍在 BACKLOG：

- [ ] T17 bs02–bs05（素材已备：`catalog/discovery/2026-09/rounds_material.md` 块 1 有 8 条一手可信 bug 候选，Python 5 条）
- [ ] T21/T22 `loop/study/10-rounds/01–08`
- [ ] T23 `loop/study/20-cards/`（stripe_api / python_debug / http_json / patterns）
- [ ] T20 `loop/tree/TREE.md` 渲染 + check_tree 严格模式
- [ ] **C27 Bitfont 故意不建**：三个版本互相矛盾，核实等级 low-medium，编规格会让人背错格式。等能读到 1p3a 原文再定稿
