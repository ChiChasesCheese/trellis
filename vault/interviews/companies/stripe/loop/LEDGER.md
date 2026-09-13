# LEDGER — loop 套件账本（append-only；每任务验收后一行；commit = 检查点）

| 时间 | 任务 | 代理 | 产物 | 测试 | commit | 备注 |
|---|---|---|---|---|---|---|
| 2026-09-01 | T0a cn_forums | sonnet | loop/raw/cn_forums.md（269 行） | — | 0d8fe08 | 1p3a `__NEXT_DATA__` 拿到 10 道题库原题 |
| 2026-09-01 | T3 tree | fable | loop/tree/interview-loop.yaml + check_tree.py | check_tree: 8 rounds/38 skills/33 ids, 0 err | (this) | 84 warn = 目录未建 |
| 2026-09-01 | T0b raw github+official | sonnet | loop/raw/github_repos.md(251) + stripe_official_and_api.md(338) | — | (this) | femisowems repo; Mako #434/#435; stripe-mock |
| 2026-09-01 | T4 mock.py | sonnet+fable | loop/mock.py, loop/tests/test_mock.py, loop/README.md | 22 | (this) | bs 工作区改为整目录减 solution/ |
| 2026-09-01 | T1 CATALOG | fable | loop/CATALOG.md | check_tree --catalog 0 err | (this) | 33 ID + OA 交叉引用 |
| 2026-09-01 | T2 LOOP_GUIDE | fable | loop/LOOP_GUIDE.md | — | (this) | 8 轮 + 总图 + 4 周计划 |
| 2026-09-01 | T7 ps05 | sonnet | loop/rounds/03_phone_screen/ps05_numeronym_validation | 23 | (this) | Part2/3 契约为重建，已标注 |
| 2026-09-01 | T7 ps06 | sonnet | loop/rounds/03_phone_screen/ps06_receivables_registration | 21 | (this) | 周末顺延/坏行规则为重建 |
| 2026-09-01 | T5 ps01 | sonnet | loop/rounds/03_phone_screen/ps01_transaction_stream_levels | 27 | (this) | 滑窗取闭区间 [t-W,t]（来源样例强制） |
| 2026-09-01 | T5 ps02 | sonnet | loop/rounds/03_phone_screen/ps02_shipping_cost_pricing | 21 | (this) | 3 个定死错误串；incremental gap 仅在跨越时报错 |
| 2026-09-01 | T6 ps03 | sonnet | loop/rounds/03_phone_screen/ps03_brace_expansion | 19 | (this) | 与 qA03 区分：保序不去重 |
| 2026-09-01 | T6 ps04 | sonnet | loop/rounds/03_phone_screen/ps04_data_validation_fraud | 17 | (this) | 与 q15 区分：范围/黑名单/行为匹配/优先级 |
| 2026-09-01 | T13 mockserver | sonnet | loop/mockserver/ (maps, payments, _png, tests, README) | 40 | (this) | 纯 stdlib；管线 限流→fail-every→鉴权→路由 |
| 2026-09-01 | T8 ps07 | sonnet | loop/rounds/03_phone_screen/ps07_redact_card_numbers | 27 | (this) | 品牌表 +Discover +MC 2221–2720；原题仅一句话 |
| 2026-09-01 | T8 ps08 | sonnet | loop/rounds/03_phone_screen/ps08_minmax_comparator | 33 | (this) | 四段形状来自 rampatra，schema 为重建 |
| 2026-09-01 | 检查点 B | fable | 03_phone_screen 全 8 题 | pytest 03_phone_screen 全绿 | (this) | Phase 2 完成 |
| 2026-09-01 | T10 cd03 | sonnet | loop/rounds/06_coding_onsite/cd03_account_scheduler_lru | 18 | (this) | LRU tie-break 构造顺序，与 OA q26 区分 |
| 2026-09-01 | T10 cd04 | sonnet | loop/rounds/06_coding_onsite/cd04_rate_limiter_4part | 21 | (this) | 4-part 仅 TOC 可读，规则为重建；毫秒；回拨 clamp |
| 2026-09-01 | T11 cd05 | sonnet | loop/rounds/06_coding_onsite/cd05_business_account_verification | 21 | (this) | 1p3a 原题规格；三处补全已标注 |
| 2026-09-01 | T11 cd06 | sonnet | loop/rounds/06_coding_onsite/cd06_suspicious_users_window | 19 | (this) | 闭区间 [t-60,t]；perf 1.66s@1e6 |
| 2026-09-01 | T9 cd01 | sonnet | loop/rounds/06_coding_onsite/cd01_subscription_email_scheduler | 23 | (this) | 日历日期 VO 版，与 q07 区分 |
| 2026-09-01 | T9 cd02 | sonnet | loop/rounds/06_coding_onsite/cd02_payment_ledger | 21 | (this) | 类 + partN 薄包装（CONVENTIONS 偏离已注） |
| 2026-09-01 | T14 int01 | sonnet | loop/rounds/05_integration/int01_bikemap | 20 | (this) | 5 part；data 为重建；Part5 CLI 直接 print |
| 2026-09-01 | T14 int02 | sonnet | loop/rounds/05_integration/int02_payments_reconciliation | 29 | (this) | with_retry 只重试 HTTPError（设计选择） |
| 2026-09-02 | T12 cd07 | sonnet | loop/rounds/06_coding_onsite/cd07_transactions_rules_ai | 23 | (this) | AI 轮版规则引擎；代理撞 limit 前已完成 |
| 2026-09-02 | T12 bs01 | sonnet | loop/rounds/04_bug_squash/bs01_mini_template_engine | start: 2 失败 / ref: 17 绿 | (this) | 两个注入 bug（visitor 缺节点、URI 目录穿越）；bs02 未开始 → backlog |
| 2026-09-02 | T15 int03 | sonnet | loop/rounds/05_integration/int03_multi_json_etl | 26 | (this) | 代理撞 limit 前完成 |
| 2026-09-02 | T15 int04 WIP | sonnet | loop/rounds/05_integration/int04_review_assignment_gitdiff | 无测试（缺 starter.py/test/REPORT） | (this) | 半成品，backlog 收尾 |
| 2026-09-02 | R1 ps01–03 | fable(review)+写入 | ps01 29 / ps02 23 / ps03 20 tests + 3 篇文章 | 绿；lint 通过 | (this) | ps04 未做 → 转 sonnet |
| 2026-09-02 | R2 ps05–07 | fable(review)+写入 | ps05 26 / ps06 23 / ps07 29 tests + ps05/06 文章 | 绿；lint 通过 | (this) | ps07 文章、ps08 未做 → 转 sonnet |
| 2026-09-02 | RA ps04/07/08 | sonnet | 3 目录 + 3 篇文章 | 17/29/33 | (this) | 无功能 bug；仅格式化 |
| 2026-09-02 | RB cd01–03 | sonnet | 3 目录 + 3 篇文章 | 23/24/18 | (this) | cd02 Payment dataclass + 逐字样例测试；cd01 handler 拆分；cd03 _lock 复用 |
| 2026-09-02 | RC cd04–07 | sonnet | 4 目录 + 4 篇文章 | 21/21/18/23 | (this) | 空洞 perf 测试、F541、缺失节补齐；文章骨架修至 40 行 |
| 2026-09-02 | stage: coding review 完成 | fable | cd01–07 | — | (this) | push + obsidian + anki |
| 2026-09-02 | R6 bs01 | sonnet | 目录 + 文章 | start 2 fail / ref 17 pass | (this) | 清除 5 处泄题注释；FIX.patch 11 行 |
| 2026-09-02 | R5 int01–03 | sonnet | 3 目录 + 3 篇文章 | 22/30/28 | (this) | int01 NOT_PNG 路径崩溃；int03 Part1→2 反向依赖；int02 _request 收敛 |
| 2026-09-02 | R7 收口 | fable | 全量 | 499 passed；lint OK；tree 0 err | (this) | 19 篇文章；Obsidian + Anki 已同步；遗留 4 篇骨架略超 40 行 |
