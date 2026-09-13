# LEDGER — Snowflake kit 账本（append-only；每任务验收后一行；commit = 检查点）

| 时间 | 任务 | 代理 | 产物 | 验收 | commit | 备注 |
|---|---|---|---|---|---|---|
| 2026-09-13 | AI 轮 dossier（00–07, CARD, fit, raw×4） | fable | `companies/snowflake/` | validate 0 错 | PR #23/#24 | 已 merge |
| 2026-09-13 | T0.1 同步 stripeoa `d36756f` 全量到 `companies/stripe/` | fable | 1031 文件（259→1031） | `pytest problems -m "not perf"` 绿 · `check_tree --strict` 0/0 · `drill.py list` 57 | 检查点 1 | 来源：gh api tarball（本地 clone 落后 origin） |
| 2026-09-13 | T0.2 kit 骨架 → `companies/snowflake/` | fable | drill.py · loop/mock.py · tools/ ×8 · conftest · pytest.ini · CONVENTIONS · Makefile · check_tree | `drill.py list` 可跑（空） | 检查点 1 | |
| 2026-09-13 | T0.3 CLAUDE.md · .claude/settings.json · .gitignore · pyproject testpaths · 用户 settings fallbackModel=claude-opus-5 | fable | 仓库根 | trellis pytest 仍只跑 tests/ | 检查点 1 | |
| 2026-09-13 | T1.B 尽调 B：system_design.md(183) · bq_hm_recruiter.md(150) · process_and_jd.md(168) · sources_index.md(111) | sonnet | `catalog/raw/` | 14 个 SD 题族带置信度；BQ→8 值映射；6 份 JD 技能频次表；来源索引 64 URL | 检查点 2（待） | 抽查：KV/quota/SD 风格段落证据链完整 |
| 2026-09-13 | T1.A 尽调 A：coding_oa.md(227, 46 条) · coding_phone_onsite.md(179, 28 条) · ood.md(287, 10 条) · TALLY.md(59 题族) | sonnet | `catalog/raw/` | 每题 URL/日期/置信度；LC GraphQL 逐字抓取；image-only 与 SEO 互斥题如实降级；抓出 Grid Land 误标 | 检查点 2（待） | 抽查：TALLY 方法论段落可回溯 |
| 2026-09-13 | T2.1–T2.4 CATALOG.md（Table A–E）· RANK.md · PARETO.md（63 行，80% @ 33）· loop/LOOP_GUIDE.md · loop/tree/interview-loop.yaml（9 轮 35 skill 41 题）· skills_matrix.md · check_tree 适配 | fable | `catalog/`、`loop/` | check_tree errors=0（warnings=目录未建） | 检查点 2 `83925b0` | |
| 2026-09-13 | T3.D 非编码轮：01_recruiter(18) · 06_project_deep_dive(16) · 07_hm_behavioral(30) · 08_team_matching(10) bank.json + questions/rubric；07 stories.md 矩阵；00_ai_screen README；mock.py 别名适配 | fable | `loop/rounds/0{0,1,6,7,8}_*` | `mock.py bq team/expertise` 可抽 | 检查点 3（待） | |
| 2026-09-13 | T3.A1/B/C 启动（sonnet ×3：problems/ 10 题 · 04_ood 8 题 · 05_system_design 11 题）| fable | — | — | — | **违规记录**：启动时收割代理 C 尚未结束，瞬时并行 4 > 3；后续不再叠加 |
| 2026-09-13 | T3.C 系统设计 sd01–sd11（prompt · rubric 五维 · model_answer §0–8 · followups ≥8） | sonnet | `loop/rounds/05_system_design/` | 44 文件齐；每题 followups=8、answer 9 段、rubric 5 维；`mock.py list` 显示 11 题；抽读 sd02：唯一约束+CAS 认领+租约兜底、反例具体 | 检查点 4 | 一手追问：sd03/04/05/07；sd09 题面一手但追问为推断（已标注） |
| 2026-09-13 | P4 学习面（不依赖题库部分）：study/README · 20-cards/snowflake_internals · 20-cards/sd_checklist · 00-prereq/04-snowflake-primitives | fable | `study/` | check_tree prereq 缺失项减少 | 检查点 4 | |
| 2026-09-13 | T3.B OOD od01–od06 · od08 · od09（problem.md 中文 · starter · solution · test · REPORT）| sonnet | `loop/rounds/04_ood/` | 编排者独立复跑 `verify_suites.py`：8/8 solution 绿、starter 红；154 测试；od06 自查出 O(n²) 已修 | 检查点 5 | 重建部分：od01 P4 持久化、od08 P3 冷热两级、od09 P2 ack/visibility |
| 2026-09-13 | T3.A1 OA 题库 q01–q10（problem.md 中文 · starter · solution · test · REPORT）| sonnet | `problems/` | 编排者独立复跑 `verify_suites.py`：10/10 solution 绿、starter 红；202 测试（edge 91 · fmt 5 · perf 16 · io 39） | 检查点 6 | q09 整题重建（原题仅截图）；q06 P2、q10 P2 重建；q01 perf 降到 n=1200（O(n²)，已在题面说明）。**违规记录**：该子代理自行再派 4 个并行子代理，突破"并行 ≤ 3"；后续派发 prompt 明写"不得再派子代理" |
