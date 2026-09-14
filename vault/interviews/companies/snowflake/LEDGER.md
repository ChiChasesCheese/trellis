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
| 2026-09-13 | T1.C 收割：Reddit 6 板块×17 查询（416 命中，35 帖全文+评论，其余 429 限流仅元数据）· HN 6 条相关 · 1p3a Telegram 镜像 21 帖 · TRIAGE.md 46 行 | sonnet | `catalog/discovery/`（1.3 MB） | README 有命令与状态码；1p3a `__NEXT_DATA__` 直连 3/3 次 403（Stripe 时期的绕行已失效） | 检查点 7 | |
| 2026-09-13 | 收割回写：q19 Maximize OR-Sum、od10 Student/Result OOP 升级一手；新增 sd22 PB 级数据库同步（IC2，不许澄清需求）；Table D 加 offer 后换组失联；格式事实加 onsite NDA；PARETO 重跑 66 行 80% @ 35 | fable | `catalog/`、`loop/LOOP_GUIDE.md` | pareto 输出与 CATALOG 一致 | 检查点 7 | sd22、q19、od10 尚未建题（第二批） |
| 2026-09-13 | P4 每轮准备章节 study/10-rounds 00–08（事实层引用 LOOP_GUIDE，本层写练法、时间分配、挂点对策、命令） | fable | `study/10-rounds/` | 9 章齐 | 检查点 7 | |
| 2026-09-13 | T3.C2 sd22 PB 级数据库同步（prompt · rubric · model_answer · followups 8，追问标注推断）| fable | `loop/rounds/05_system_design/sd22_*` | 4 文件齐；`mock.py list` 可见 | 检查点 8 | 一手仅题面 + "不许澄清需求" |
| 2026-09-13 | **中断**：3 个 sonnet 子代理（题解、电面 coding、essentials）同时撞会话用量上限（429，10:30am 重置） | — | — | — | — | 已落盘保留：题解 17/18；essentials 01–05 + README；prereq 01–03；pc01–pc04（pc04 缺 REPORT）；pc05/pc06/pc10 未开始。剩余由主会话（Opus 5）顺序补，不并行 |
| 2026-09-13 | T3.D 电面 coding pc01–pc04 验收 | sonnet（中断前）+ opus 补 | `loop/rounds/03_phone_coding/pc0[1-4]*` | `verify_suites.py` 4/4 OK；pc04 测试侧边数笔误已修；pc04 REPORT 由编排者补写 | 检查点 9 | pc01 P4 反向查询重建 |
| 2026-09-13 | T4.1/4.2 部分：study/30-articles 17 篇（缺 od09）· 00-essentials 01–05 + README · 00-prereq 01–03 | sonnet（中断前） | `study/` | 行数 98–283；essentials 05 结尾完整（54 行，偏短但闭合） | 检查点 9 | |
| 2026-09-13 | T3.D pc06 Happy Number（集合 → Floyd O(1) → 任意进制/幂次的环信息） | opus（主会话） | `loop/rounds/03_phone_coding/pc06_*` | `verify_suites` OK；1–200000 两法一致；Part 3 与暴力找环 3000 组一致；25 测试 | 检查点 10 | P3 重建 |
| 2026-09-13 | T3.D pc10 Distributed Tree Count（FIFO 消息协议逐行轨迹 + 丢失/重试/放弃的部分计数） | opus（主会话） | `loop/rounds/03_phone_coding/pc10_*` | `verify_suites` OK；来源 9 行轨迹逐字复现；3000 棵随机树不变量 0 失败；22 测试 | 检查点 11 | P2 重建；REPORT 格式自定 |
| 2026-09-13 | T3.E cut line 补齐：q19 Maximize OR-Sum（一手逐字题面 + 大 k 取模重建）· od10 Student/Result OOP（一手骨架 + 规则重建） | opus（主会话） | `problems/q19_*`、`loop/rounds/04_ood/od10_*` | `verify_suites` 2/2 OK；q19 与"任意拆分 k 次"穷举 3000 组一致、取模与精确值 3000 组一致 | 检查点 12 | q11 Generating Login Codes 只有标题+标签，不建（CATALOG 注明） |
| 2026-09-13 | 知识树修正：check_tree 的 study/prereq 路径改按 kit 根解析；移除未建的 pc07；新增 loop/rounds/02_oa 指针；study/20-cards/patterns.md | opus（主会话） | `loop/tree/`、`study/20-cards/` | `check_tree --strict`：errors=0 warnings=0 | 检查点 12 | 此前 24 条警告都是解析基准错误，不是缺文件 |
