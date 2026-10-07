# interviewer.md · cb04_quarantine（面试官视角）

> 本文件包含答案：只在做完某张 ticket 之后再看那一节（`python3 loop/ai_screen.py reveal cb04 tN`）。
> 题型：**fix-the-codebase**——代码库带着埋好的 bug，先找到并修，再按判断力推向 production-ready。三张 ticket 都从同一份 `starter/` 开始（每次模拟只做一张）。
> 面试官开场原话（英文）："This is Quarantine, the backend behind our Report Phishing button. Pick up this ticket. You can use Claude Code. I'll answer questions, but I won't tell you how to fix it."
> 评分原话（官方）：Judgment — "evaluate approaches, scope work into milestones, and decide what fits the existing system"；Agency — "make decisions, state assumptions, test your own work, keep momentum"。
> 本题额外看三件事：**先建反馈回路再修**（Prove-It）、**按影响分级**、**收口**（点名的要么做完，要么写进 known gaps）。

通用的"契合本系统"清单（三张 ticket 都适用）：

| 约定（`CONTRIBUTING.md`） | 对应落点 |
|---|---|
| 一切按租户隔离 | repository 方法都带 `tenant_id` 且 SQL 里真的用到；API handler 只用 `request.tenant` |
| 改 schema = 新 migration | `quarantine/store/migrations/NNNN_*.sql`，不改 `0001_init.sql`；表带 `tenant_id` 索引 |
| 配置优于常量 | `config/default.toml` + `quarantine/config.py` 校验（未知键 = `ConfigError`） |
| 动 mailbox 都走 `ActionService`，并写 `action_log` | 不直接调用 `Mailbox` |
| 错误：service 抛 `QuarantineError` 子类，API 抛 `ApiError` 子类 | 不手写错误 body |
| 跳过/吞掉的都要计数 + 日志 | `quarantine.metrics.incr(...)` |
| 时间一律 aware、按 UTC 比较 | `quarantine/timeutil.py`：`to_utc`、`iso`、`parse_rfc2822` |
| 不碰 `quarantine/legacy/` | 冻结；README 说它"在 analyzers 之前运行"是**过时**的（`legacy/regex_filter.py` 没有任何 import） |
| 新模块有测试 | 放进 `tests/test_intake.py` / `test_analyzers.py` / `test_actions.py` / `test_store.py` / `test_api.py` / `test_cli.py` |

埋点总表（starter 自带 54 个测试全绿，bug 只在 ticket 场景下暴露）：

| # | bug | 位置 | 症状（对应 ticket 的哪句话） | 谁来修 |
|---|---|---|---|---|
| B1 | check-then-insert 竞态：`find_by_message` → 分析（慢）→ `insert`，`reports` 上只有普通索引 | `intake/service.py:IntakeService.submit`、`store/migrations/0001_init.sql` | 同一封邮件被两人几乎同时报告 → 两条 report、两次 quarantine | t1 |
| B2 | 跨租户泄露：`get(tenant_id, report_id)` 接收了 `tenant_id` 却在 SQL 里没用 | `store/repositories.py:ReportRepository.get`（`GET /reports/<id>` 与 `POST .../release` 都走它） | "another customer's report ID" | t1 |
| B3 | 时区：`_sent_at` 用 `.replace(tzinfo=None)` 丢掉偏移（而不是转 UTC），"同一发件人 24 小时内被报告过"的窗口在跨时区时算错 | `intake/parsing.py:_sent_at`、`repositories.py:count_sender_reports` | 邮件留在收件箱：重复发件人的加分没算上 | t1 |
| B4 | 吞异常：`except Exception: return Verdict(self.name, 0, ())`，查询失败的恶意链接被判为干净 | `analyzers/link_reputation.py:LinkReputation.analyze` | "reported phishing emails stay in inboxes"（`fixtures/reports/r006_intel_timeout.json` 就是它） | t1 |
| B5 | `release` 不检查当前状态：重复 release 重复调用 mailbox；从未隔离的邮件也能 release | `actions/service.py:ActionService.release` | 重复点击放行 → 供应商侧重复调用 | t2 |
| B6 | 连接在异常路径不关闭（`app.conn.close()` 不在 `finally`） | `cli.py:main` | 无测试可见；读代码才发现 | t2（加分项） |

---

## t1 · planted bugs（QRN-208）

### ① 好的 v1 长什么样
候选人先建反馈回路：读 `tests/` 的写法，然后**为每个症状先写一个会红的测试**（跨租户 `GET` 应 404；lookup 故障的链接不能 RELEASE；两个并发请求只产生一条 report），再改。他说得出优先级：**B2 跨租户泄露**（数据暴露，最严重）> **B4 吞异常**（钓鱼邮件留在收件箱，support 的第一句话）> **B1 竞态**（重复 quarantine）> **B3 时区**（只影响加分的边界）。修法契合本系统：B2 在 SQL 里加 `tenant_id = ?`（并检查同类的其它查询）；B4 去掉 `except Exception`，让 `AnalyzerRunner` 统一处理（计数 + 日志 + "inconclusive"），`decide` 在有 inconclusive 时至少给 `NEEDS_REVIEW`——**不是**自动 QUARANTINE（误杀成本）也不是 RELEASE；B1 用**唯一约束**（新 migration `0002_*.sql`）+ 捕获冲突后走"已有 report"分支，而不是进程内锁（多进程部署锁没用）；B3 用 `timeutil.to_utc`，存储统一为 UTC。他不碰 `legacy/`，不重构，不引入新依赖，结束时说清"修了哪几个、没修哪几个、怎么验证的"。35 分钟内能做完 B2 + B4（M1），再做 B1（M2），B3 是加分。

### ② 澄清问答
| 候选人可能问 | 面试官答（English line） |
|---|---|
| 怎么知道哪些邮件还留在收件箱？有日志吗？ | "I can't give you production logs. You have the fixtures and the tests — start from there."（→ `fixtures/reports/` 里的 r006） |
| 泄露只发生在 GET 吗？ | "I don't know. That's what I'd like you to find out."（→ release 也走同一个 `get`） |
| 一共几个 bug？ | "I'm not going to tell you. Prioritise by impact."（默认：不回答数量） |
| lookup 失败时消息应该怎么处理？ | "I'd rather a human looked at it than let it through. But don't quarantine everything when the provider blips."（→ NEEDS_REVIEW） |
| 失败要可见吗？ | "We should be able to count how often it happens."（→ `metrics.incr`） |
| 可以加唯一约束 / 新 migration 吗？ | "Yes, follow the migration rules in CONTRIBUTING."（未问：默认加；若问到"已有重复行怎么办"：*"There aren't any in production yet — tell me what you would do if there were."*） |
| 并发修法用锁可以吗？ | "We run several app processes."（→ 唯一约束） |
| 可以顺手重构 / 换框架吗？ | "Not today."（默认：最小改动） |
| 要不要为每个 bug 写测试？ | "I'd be surprised if you didn't."（默认：写，且先红后绿） |
| 时间窗口那块我没理解 | "The sender-repeat bonus: if the same sender was reported again within a day, the score goes up. Ask Claude how it measures a day."（→ 引导去读 `count_sender_reports`） |

### ③ 隐藏期望（文件:符号）
- `quarantine/store/repositories.py:ReportRepository.get`：SQL 漏了 `tenant_id`（其余查询——`find_by_message`、`list`、`count`、`update_outcome`、`set_status`——都带）。**同类检查**：改完后 grep 所有 `WHERE`。
- `quarantine/analyzers/link_reputation.py`：`except Exception` → 吞掉；`quarantine/analyzers/runner.py:AnalyzerRunner.run` 是唯一合适的接缝（所有 analyzer 共用，且 `analyzer.run` 计数就在这里）；`quarantine/decision.py:decide`；`quarantine/metrics.py:incr`。
- `quarantine/intake/service.py:IntakeService.submit`：check-then-insert；`quarantine/store/migrations/`：新增 `0002_*.sql`（`CREATE UNIQUE INDEX ... (tenant_id, message_id)`）；`store/repositories.py:ReportRepository.insert` 捕获 `sqlite3.IntegrityError`。
- `quarantine/intake/parsing.py:_sent_at` + `quarantine/timeutil.py:to_utc/iso`：时间一律 aware、UTC；`repositories.py` 里存取同一格式后字符串比较才成立。
- `quarantine/api/testing.py:TestClient`（测试走它）、`quarantine/actions/mailbox.py:FakeMailbox.calls_of`（断言 quarantine 次数）、`quarantine/app.py:create_app(url_lookup=...)`（注入慢/坏的 lookup 来复现竞态与故障）。
- 不该碰：`quarantine/legacy/regex_filter.py`；`ReportRepository.insert` 之外的存储结构；不新增异常层级。

### ④ 追问
1. "How do you know you have found them all?"（→ 不知道；说出 grep 同类、读每个 `except`、读每个 SQL 的方法；说出没覆盖的区域）
2. "Why a unique index and not a lock around the check?"（→ 多进程；约束是唯一跨进程的串行化点；败者走"已有 report"分支）
3. "You add the unique index. What about duplicate rows that already exist?"（→ 迁移会失败；先去重再建索引；本场景生产无重复）
4. "Why NEEDS_REVIEW rather than QUARANTINE when the lookup is down?"（→ 误杀 vs 漏过的成本；provider 故障期间不应隔离所有带链接的邮件）
5. "How would you find out in production that lookups are failing?"（→ `analyzer.error` 计数 → 告警阈值）
6. "Which of these bugs would you fix first if you had only ten minutes, and why?"（→ B2）

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 按影响排序（跨租户 > 吞异常 > 竞态 > 时区）并说出理由；失败时选 NEEDS_REVIEW 并解释；竞态用约束而非锁 | 找到多数 bug，没有明确优先级；用了锁 | 一个一个随机修；失败时直接 RELEASE 或全部 QUARANTINE |
| Agency | 先复现再修（每个 bug 一个会红的测试）；M1 = 两个最严重的；主动说出没覆盖的区域 | 修了，但事后补测试 | 读代码读到第 30 分钟没有一个红测试 |
| Fit-the-system | 在 `runner` 里统一处理；用 `to_utc`；新 migration；`metrics.incr` | 修在 `link_reputation` 里 `except SomeError`（局部可行） | 加新异常体系；改 `0001_init.sql`；加进程内锁 |
| Testing | 红 → 绿；并发测试用慢 lookup 拉宽窗口；同时跑完整套件 | 只跑单个测试 | 把测试改成适配 bug；没有测试 |
| AI-supervision | 让 Claude 先复现并给 3 个排序假设（T8）；审出"它在 `get` 之外没检查其它查询" / "它把 `except` 改成 `except: pass`" | 接受后再检查 | 让 AI "find and fix all bugs" 然后直接接受 |
| Communication | 收尾按"修了/没修/怎么验证"讲；每个 bug 一句因果 | 只讲修了什么 | 无 |

---

## t2 · production-ready（QRN-231）

### ① 好的 v1 长什么样
这张题刻意开放。好的候选人先用 10 分钟列自己的清单（T3），按"最大客户下周上线会咬人的东西"排序：**(1) 重复/并发 release**（`ActionService.release` 无状态检查，重复调用供应商）→ 条件更新 `UPDATE ... WHERE status IN (...)`，只有赢家调用 mailbox；对从未隔离的邮件返回 409；**(2) 输入校验**（缺 `message_id` 现在是 500）→ `ValidationError`（`QuarantineError` 子类）在 `parse_report` 抛出，路由转成 `BadRequest`；顺手发现 `config.py` 里的 `intake.max_links` **已经定义却从没被使用**，接上；**(3) 回执同步发送在请求路径里**（供应商挂掉 → `POST /reports` 500，且 report 已入库，客户重试就是重复）→ outbox 表（新 migration，照 `ActionLogRepository` 的模式）+ `python -m quarantine drain-outbox`（ticket 点名，复用 `create_app(mailbox=...)` 的注入点，与 `ingest` 同款），失败的留在队列并计数；**(4) 日志里有 PII**（`log.info("... reporter=%s ...")`）→ 只打 id。他明确说**不做**：鉴权模型（任何 token 都能 release）、真实队列（SQS）、限流、退避重试；并把它们写进 known gaps。顺手修 CLI 的连接泄露（B6）是加分。

### ② 澄清问答
| 候选人可能问 | 面试官答（English line） |
|---|---|
| 对这个客户最大的风险是什么？ | "Duplicate reports and the mail provider having a bad hour. Beyond that, use your judgement."（默认：自己排序） |
| 鉴权在范围内吗？ | "Out of scope. Tokens are managed elsewhere — but tell me what you'd worry about."（→ 任何 analyst token 都能 release） |
| 谁能 release？ | "Any analyst token, for now." |
| 供应商挂了一小时，回执怎么办？ | "The report must still succeed. The receipt can be late, not lost." |
| 要重试/退避吗？ | "Not for v1. Count the attempts so we can see it."（→ `attempts` 列） |
| `drain-outbox` 跑在 API 进程里吗？ | "No. Cron, as the ticket says."（→ 独立命令，每次处理一批） |
| release 一个从未隔离的邮件？ | "Tell me what you'd do."（本实现：409） |
| 能引入真正的队列吗？ | "No new infrastructure this week." |
| 日志里什么算 PII？ | "Reporter addresses are personal data. They shouldn't be in our logs."（sender 地址同理，保守起见都不打） |
| 校验到多严？ | "Reject what would 500 today. Don't write a schema language."（→ message_id/reporter/links/attachments 类型 + `max_links`） |

### ③ 隐藏期望（文件:符号）
- `quarantine/actions/service.py:ActionService.release`：加状态检查；`store/repositories.py` 新增条件更新（`set_status_if`）；`api/routes/reports.py:release_report`：`Conflict`（`api/framework.py`）用于 CLEARED。
- `quarantine/intake/parsing.py:parse_report`：校验；`quarantine/errors.py`：`ValidationError`；`quarantine/config.py:IntakeSettings.max_links`（已有、未使用——"已有抽象"）；路由里转 `BadRequest`（不手写错误体）。
- `quarantine/actions/notify.py:send_receipt`（同步，注释就写着）→ 入队；新 migration `0003_*.sql`；`ActionLogRepository` 是 repository 范本；`cli.py:main(argv, out, mailbox)` 的 `mailbox` 注入点让命令可测。
- `quarantine/intake/service.py:IntakeService.submit`：`log.info(... reporter=%s ...)`。
- `quarantine/cli.py:main`：`app.conn.close()` 不在 `finally`（B6）。
- 不该碰：`legacy/`；"顺手加鉴权/角色"；"顺手给 `Mailbox` 加重试装饰器"（会把同步等待藏起来，请求路径依然被拖住）。

### ④ 追问
1. "Two `drain-outbox` processes run at the same time. What happens?"（→ 重复发送；至少一次语义；可用 `UPDATE ... WHERE status='PENDING'` 认领，或保证单实例 cron）
2. "How would you roll this out to the customer?"（→ 先影子/小租户；先 drain 再切；回滚 = 回执回到同步？不——outbox 向前兼容）
3. "What would you put on the dashboard on day one?"（→ `analyzer.error`、`outbox.failed`、`intake.created`、outbox 积压量）
4. "Why not wrap `send_receipt` in a try/except and move on?"（→ 回执丢了；没有可见性；无法补发）
5. "Two admins click release at the same moment."（→ 条件更新；赢家调用 mailbox）
6. "What's missing for a real production launch?"（→ 鉴权/角色、限流、退避与死信、数据保留、供应商侧幂等键）

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 先列清单并排序，说出"不做"的项和理由（鉴权、真实队列）；选 outbox 因为 ticket 点了 cron 命令 | 做了该做的，没说不做什么 | 想做"全部"：加鉴权、重试框架、metrics 平台；35 分钟末一个都没收口 |
| Agency | M1 = 幂等 release + 校验（各自红→绿）；M2 = outbox + drain；收尾 NOTES.md | 做完但没有里程碑 | 一开始就设计 outbox，前 20 分钟没有任何可演示 |
| Fit-the-system | `ValidationError` ← `QuarantineError`、`BadRequest`；migration 照旧；`mailbox` 注入点；接上 `max_links` | 校验写在路由里（可用但分散） | 手写 400 body；`print` 日志；改 `0001_init.sql` |
| Testing | 每项一个测试；失败供应商用 `FakeMailbox(fail_receipts=True)`；通过 CLI 演示 drain | 只有 happy path | 无 |
| AI-supervision | 审出"它加了 retry 装饰器 / 引入 `queue.Queue` 线程"并拒绝；让它先读 `ActionLogRepository` | 事后清理 | 接受 AI 的"重试 + 线程池"方案 |
| Communication | known gaps 一项一句：鉴权、重试/退避、死信、并发 drain | 只讲做了什么 | 无 |

---

## t3 · burst scale（QRN-244）

### ① 好的 v1 长什么样
候选人先复现："2000 个报告人报告同一封邮件"（`message_id` 相同）。他发现去重键 `(tenant, message_id)` **已经**让 report 只有一条，问题出在 `IntakeService._repeat`：**每个**重复报告都重跑 4 个 analyzer（含逐次读 `urls.json` 的 URL lookup）并同步给报告人发回执，而重复的报告人根本没被记录——所以 UI 看不到"有多少人报告"。好的 v1：重复报告**不再重新分析**（分析结果已经存在 `reports.verdicts` 里——那就是"按 message 缓存"）；新增 `report_reporters`（PK = tenant + report + reporter，`INSERT OR IGNORE`），新 migration 并回填已有 report 的首位报告人；`Report.reporter_count` 暴露到 `GET /reports/<id>` 与 `GET /reports`（`to_dict` 复用，路由不改）；每个**新的**报告人都入队回执（若做了 t2 的 outbox；否则仍同步）；同一个人重复报告只计一次。他用 `metrics.get("analyzer.run", ...)` 这个已有钩子证明"analyzer 只跑了一次"，用一个 2000 次的循环测耗时。他还主动说出放弃的东西：重复报告不再触发重新评估（v2：按报告人数/情报更新阈值再评估）。

### ② 澄清问答
| 候选人可能问 | 面试官答（English line） |
|---|---|
| "同一封邮件"怎么定义？ | "Same tenant, same Message-ID. That's what we dedupe on today."（→ 不要自作主张按内容指纹合并；可作为 v2 提出：每个收件人的 Message-ID 可能不同） |
| 每个报告人都要回执吗？ | "Yes. Nobody who clicked the button should be ignored."（→ 入队，不是丢弃） |
| 同一个人点了三次？ | "That's one reporter."（本实现：计一次，不重复回执） |
| 之后的报告会改变判定吗？ | "Not in v1. Tell me if you'd want it to."（→ 说出放弃了重新评估，v2 = 报告人数阈值升级到 QUARANTINE） |
| `reporter_count` 要实时精确吗？ | "Roughly right under load is fine; it must be right when things are quiet."（→ 子查询计数即可） |
| 要把报告人名单也暴露吗？ | "Count only. The list is personal data."（→ 只暴露计数） |
| 性能目标？ | "Two thousand reports in a couple of seconds on a laptop."（→ 验收里的 2 s） |
| 数据量增长后列表会慢吗？ | "Good question. Look at how you count."（→ N+1 计数 vs 子查询/索引） |
| 并发时同时来 2000 个呢？ | "Assume several processes."（→ 唯一约束 + PK 已提供串行化点；没做 t1 时先承认竞态） |

### ③ 隐藏期望（文件:符号）
- `quarantine/intake/service.py:IntakeService._repeat`：现在的"重新评估 + 同步回执"就是慢的原因；删掉重跑，改为记录报告人。
- 去重键本身（`ReportRepository.find_by_message`、t1 的唯一索引）**不用改**——候选人若重做去重键就是没读懂。
- `quarantine/store/repositories.py`：新增 `add_reporter` / `reporter_count`；`_row_to_report` 带出 `reporter_count`；`list` 不能逐行再查一次（N+1）；新 migration `0004_*.sql`（PK 含 `tenant_id`，回填）。
- `quarantine/models.py:Report.to_dict`：增加字段，路由因此不用改（"复用"信号）。
- `quarantine/metrics.py` 的 `analyzer.run` 计数（已有钩子）作为"只跑一次"的证据；`FakeMailbox.calls_of("quarantine")` 作为"只隔离一次"的证据。
- `quarantine/actions/notify.py`（t2 已做则复用 outbox；未做则承认回执仍同步，并写进 known gaps）。
- 不该碰：analyzers 本身；`legacy/`；不引入线程池/异步队列。

### ④ 追问
1. "The campaign sends each recipient a different Message-ID but the same links. What now?"（→ 内容指纹缓存：发件人 + 链接集合 → analyzer 结果，TTL；注意隐私与误合并）
2. "2000 receipts are queued at once. What does `drain-outbox` do?"（→ 批量 `--limit`；退避；供应商限流）
3. "Should the 50th reporter change the verdict?"（→ 配置阈值：N 个独立报告人把 NEEDS_REVIEW 升级为 QUARANTINE；防止攻击者刷报告人——只有租户内独立报告人）
4. "What index serves the count and the list?"（→ `report_reporters` 的 PK；`reports` 的 `(tenant_id, received_at)`）
5. "Why count in SQL instead of keeping a counter column?"（→ 一致性 vs 写放大；热点行；可以讨论计数列的取舍）
6. "What's missing?"（→ 重新评估、报告人刷屏、内容指纹、回执批量/限流）

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 先定位"重复报告在做重复工作"而不是去重键；说出放弃重新评估并给出 v2；只暴露计数 | 做出来了，没讨论放弃的行为 | 改去重键 / 加缓存层但仍逐条分析 |
| Agency | M1 = `reporter_count` 红→绿；M2 = 不重复分析（用 `analyzer.run` 证明）；M3 = 2000 条计时 | 一次做完 | 先写 benchmark 框架 |
| Fit-the-system | 新 migration（PK 含 tenant、回填）；`to_dict` 暴露；路由不改；复用 `metrics` | 计数放在内存 dict（重启丢失、多进程不一致） | 全局 `functools.lru_cache`；线程池；Redis |
| Testing | 小规模语义测试（3 个报告人）+ 2000 条规模测试；同一人重复；跨租户 | 只有规模测试 | 无 |
| AI-supervision | 审出 AI 的"列表里每行再查一次计数"（N+1），或"在 `submit` 里加 `lru_cache`" | 事后发现 | 采用 AI 的缓存装饰器 |
| Communication | 说清"缓存 = 已存的 verdicts"；列出 v2 | 只讲实现 | 无 |
