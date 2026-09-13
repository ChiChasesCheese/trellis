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
- [x] T12 cd07 transactions_rules_ai · bs01 mini_template_engine · bs02 mini_http_client
  - cd 题 AC 同 T5–T8；cd04 part4 含线程安全测试（`threading` 并发 1000 次无超发）
  - int 题 AC：目录含 `problem.md`（含 API 文档节）、`data/`（ride-simple.json 约 500 点 / charges 样本）、`starter_template.py`、`solution.py`、`test_intNN.py`（fixture 起 mockserver 于随机端口、结束关闭）、`REPORT.md`；测试覆盖 happy path + 网络错误 + 分页第 2 页 + 429 退避 + 幂等重放
  - bs 题 AC：`src/<pkg>/`（200–600 行）、`tests/`（1–3 个失败用例 + 其余通过）、`README.md`（库用途、跑测试命令）、`solution/FIX.patch`、`REPORT.md`（根因·排查路径·最小修复·真实库对应 issue/PR）；`git apply --check solution/FIX.patch` 通过；打补丁后全绿
  - 验证：同上 + starter 红

### Checkpoint C（Phase 3 后）
- [ ] `pytest loop/rounds/06_coding_onsite loop/rounds/05_integration/int01 loop/rounds/05_integration/int02 loop/mockserver` 全绿；bs01/02 打补丁前红、后绿；commit；LEDGER；CHECKPOINT

## ⏸ BACKLOG（用户 2026-09-01 指示：先 review 已有题，以下暂停）

## Phase 4 · integration 后半 + bug squash 后半 + SD + 非编码轮 + study 前半（5 并行）
- [~] T15 int03 ✓ · int04 半成品（缺 starter.py/test/REPORT）→ BACKLOG（int04 用 `subprocess git` 在 tmp repo 造两分支）
- [ ] T17 bs03 mini_yaml_csv · bs04 config_manager_concurrency · bs05 asyncio_fetch_race
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
