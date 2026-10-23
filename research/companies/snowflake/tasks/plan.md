# Snowflake kit — 原子任务清单

> 一行一个任务：谁做 · 写哪个目录 · 验收命令。完成打 ✅ 并在 `../LEDGER.md` 记一行、commit。并行子代理 ≤ 3（sonnet），互不共享目录。
> 编排者（Fable）负责：拆任务、验收、合成 CATALOG/LOOP_GUIDE、commit/push。

## P0 骨架（fable）

- [x] T0.1 同步 stripeoa `d36756f` → `companies/stripe/`（1031 文件；`pytest problems -m "not perf"` 绿；`check_tree --strict` 0/0）
- [x] T0.2 复制 kit 骨架 → `companies/snowflake/`（drill.py · loop/mock.py · tools/ · conftest.py · pytest.ini · CONVENTIONS.md · Makefile · check_tree.py）
- [x] T0.3 CLAUDE.md（仓库根）· `.claude/settings.json` · `.gitignore` · pyproject `testpaths` · 用户级 `fallbackModel`
- [ ] T0.4 commit + push 检查点 1

## P1 尽调（sonnet ×3，并行）

- [ ] T1.A `catalog/raw/coding_oa.md` `coding_phone_onsite.md` `ood.md` `TALLY.md` — 验收：每题 URL+日期+置信度；TALLY ≥ 30 行或说明为何不足
- [ ] T1.B `catalog/raw/system_design.md` `bq_hm_recruiter.md` `process_and_jd.md` `sources_index.md` — 验收：SD ≥ 10 题；BQ 映射到 8 条价值观；JD 技能频次表
- [ ] T1.C `catalog/discovery/`（reddit/hn json · mirror_1p3a_snowflake/index.md · README triage 表）— 验收：README 有命令与状态码；triage 表 ≥ 20 行
- [ ] T1.V fable 抽查三路各 5 条 URL 可回溯；LEDGER 记 3 行；commit 检查点 2

## P2 合成（fable）

- [ ] T2.1 `catalog/CATALOG.md`：Table A 编码题（OA/电面/onsite）· Table B OOD · Table C SD · Table D 非编码轮题库 · Table E 仅题名；每行 #refs / 置信度 / 最近日期 / URL；**28 法则**：按 stage 权重 × refs × recency 排序，标出覆盖 80% 出现次数的前 N 行（cut line）
- [ ] T2.2 `loop/LOOP_GUIDE.md`：每轮 形式 · 评什么 · 通过线 · 挂点 · 备考动作 · 练什么；含 AI 轮（引用 03）
- [ ] T2.3 `loop/tree/interview-loop.yaml`：round → skill → problems/study；`check_tree.py`（缺目录 = warning 可接受，errors 0）
- [ ] T2.4 `skills_matrix.md`：测试目标 ↔ 题 ↔ JD 行
- [ ] T2.5 commit 检查点 3

## P3 题库（sonnet ×3，按目录分工，并行）

- [ ] T3.A `problems/qNN_*`：CATALOG cut line 以内的 OA/coding 题，每题 problem.md · starter_template.py · starter.py · solution.py · test_qNN.py · REPORT.md；验收 `python3 drill.py ref qNN` 全绿、空 starter 必红
- [ ] T3.B `loop/rounds/04_ood/odNN_*` + `loop/rounds/03_phone_coding/pcNN_*`：同上结构；验收 `loop/mock.py ref <id>` 绿
- [ ] T3.C `loop/rounds/05_system_design/sdNN_*`：prompt.md · rubric.md · model_answer.md · followups.md（中文，≥ 8 追问）；验收 4 文件齐 + rubric 五维
- [ ] T3.D `loop/rounds/01_recruiter` `06_project_deep_dive` `07_hm_behavioral` `08_team_matching`：bank.json · questions.md · rubric.md · stories.md（stories 指向 `core/stories`）；验收 `loop/mock.py bq <round> -n 3` 可抽
- [ ] T3.V fable 逐目录验收 + `tools/summary.py --run`；LEDGER；commit 检查点 4

## P4 学习面（sonnet ×2 + fable）

- [ ] T4.1 `study/README.md` `INDEX.md` `00-essentials/`（Snowflake 版：分布式系统基础 · OOD 套路 · 并发 · SQL 引擎/存储概念 · 场景题骨架）
- [ ] T4.2 `study/10-rounds/*.md` 每轮准备材料 + `study/30-articles/` 每题一篇（cut line 内必有）
- [ ] T4.3 `loop/tree` 补齐 study 路径；`check_tree.py --strict` 0 错
- [ ] T4.4 commit 检查点 5

## P5 收尾（fable）

- [ ] T5.1 `00-README.md` 重写为总索引（含 AI 轮材料 + 全轮次 kit）；`../../README.md` 更新
- [ ] T5.2 `reports/OVERALL_REPORT.md` + `TEST_SUMMARY.md`（`tools/summary.py --run`）
- [ ] T5.3 `uv run trellis --all validate` 0 错；trellis pytest 绿
- [ ] T5.4 PR → merge → 主 checkout `git pull`
