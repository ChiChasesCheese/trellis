# LEDGER — Snowflake kit 账本（append-only；每任务验收后一行；commit = 检查点）

| 时间 | 任务 | 代理 | 产物 | 验收 | commit | 备注 |
|---|---|---|---|---|---|---|
| 2026-09-13 | AI 轮 dossier（00–07, CARD, fit, raw×4） | fable | `companies/snowflake/` | validate 0 错 | PR #23/#24 | 已 merge |
| 2026-09-13 | T0.1 同步 stripeoa `d36756f` 全量到 `companies/stripe/` | fable | 1031 文件（259→1031） | `pytest problems -m "not perf"` 绿 · `check_tree --strict` 0/0 · `drill.py list` 57 | 检查点 1 | 来源：gh api tarball（本地 clone 落后 origin） |
| 2026-09-13 | T0.2 kit 骨架 → `companies/snowflake/` | fable | drill.py · loop/mock.py · tools/ ×8 · conftest · pytest.ini · CONVENTIONS · Makefile · check_tree | `drill.py list` 可跑（空） | 检查点 1 | |
| 2026-09-13 | T0.3 CLAUDE.md · .claude/settings.json · .gitignore · pyproject testpaths · 用户 settings fallbackModel=claude-opus-5 | fable | 仓库根 | trellis pytest 仍只跑 tests/ | 检查点 1 | |
| 2026-09-13 | T1.B 尽调 B：system_design.md(183) · bq_hm_recruiter.md(150) · process_and_jd.md(168) · sources_index.md(111) | sonnet | `catalog/raw/` | 14 个 SD 题族带置信度；BQ→8 值映射；6 份 JD 技能频次表；来源索引 64 URL | 检查点 2（待） | 抽查：KV/quota/SD 风格段落证据链完整 |
| 2026-09-13 | T1.A 尽调 A：coding_oa.md(227, 46 条) · coding_phone_onsite.md(179, 28 条) · ood.md(287, 10 条) · TALLY.md(59 题族) | sonnet | `catalog/raw/` | 每题 URL/日期/置信度；LC GraphQL 逐字抓取；image-only 与 SEO 互斥题如实降级；抓出 Grid Land 误标 | 检查点 2（待） | 抽查：TALLY 方法论段落可回溯 |
