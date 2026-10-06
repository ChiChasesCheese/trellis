# cb02_insiderwatch · 面试官手册

> 代码库：`starter/`（Insider Risk 检测后端，纯标准库）。每次模拟 = 10 分钟探索 + 一张 ticket（35 分钟）+ walkthrough。
> 评分的核心不是"功能能不能跑"，而是 *"AI will produce working code. That's not enough. The bar is whether the code fits the existing system."*
> 面试官口头说话时保持"一个忙碌的 PM / tech lead"的口吻：只回答被问到的问题，不主动剧透。

通用约定（三张 ticket 都适用）：

- 用户 = 小写 email；时间 = UTC aware；CLI 入口 `python -m insiderwatch`；验证数据 `fixtures/raw` 回放到 `--until 2026-09-30`。
- 数据里的"主角"（候选人用 `replay` + `alerts` 就能自己发现，不需要你告诉他）：

| 用户 | 故事 | 与哪张 ticket 相关 |
|---|---|---|
| carol.diaz | 09-11 递辞呈，09-26 最后一天，最后一周把文件外享到个人 gmail、设置转发 | t1 必须抓到 |
| erin.walsh | 被裁（last day 10-05，无辞呈日期），09-28~30 外享 + 转发 + Slack 全量导出 | t1 必须抓到 |
| bob.martin | 重度下载者（~200MB/天），已辞职，行为一切如常 | t1 不能误报 |
| dave.kim | 合作伙伴经理，每天外享 2-4 次，被裁，行为如常 | t1 不能误报 |
| frank.okafor | 没有任何 HR 离职信息，却从 09-21 开始每天外享 4 次 | t1 不该产生离职告警 |
| gina.park | 09-18 已离职，账号 09-22/23 仍在使用 | t1 stretch |
| henry.ross | "夜间爆发"的坏人：09-02/03 与 09-27 各一次，共 ~70 条告警 | t2 |
| alice.nguyen | 三个旧信号各触发一次（volume_spike / off_hours / 新国家登录） | 回归 |
| jack.lee / kim.sato | 只出现在 `fixtures/raw/gdrive/` | t3 |

---

## t1 · departing_exfil（"Flag employees who are taking data on their way out"）

### ① 好的 v1 长什么样

一个新的 `@signal("departing_exfil")`（`signals/departing_exfil.py`），在 `signals/__init__.py` 里 import 注册；从 `ctx.roster`（`hr/roster.py`）读 `termination_date` / `resignation_submitted` 判断某天是否处于"离职窗口"；窗口长度、"算作带走数据的动作"、权重都进 `config.py`（`departure_window_days`、`signal_weights["departing_exfil"]`）；对窗口内的每个相关动作，用 `ctx.baselines.get(user, action, ctx.day)` 取**本人**基线，只有明显超出本人基线才产出 `Finding`（strength 0..1），**不在 signal 里决定要不要告警**（那是 `scoring` + `alert_threshold` 的事）。冷启动（`get` 返回 `None`）有明确的说法；离职日之后仍有活动单独处理且更严重。自带 `tests/test_<x>.py`，在 fixtures 上回放，用 `alerts --user carol...` 验证。

不是好 v1：在 `pipeline.py` 里加 `if emp.termination_date: ...`；写一个全局阈值（"下载 > 500MB 即告警"，这恰好是 deprecated 的 `legacy/dlp_rules.py` 的做法）；把逻辑塞进 `volume_spike`；绕过 scoring 自己构造 `Alert`。

### ② 澄清问答（面试官怎么答 / 没问时的默认）

| 候选人问（Q） | 面试官答（A） | 没问的默认 |
|---|---|---|
| "How early before leaving should we start watching?" | "Customers talk about the last two weeks, but make it tunable." | 14 天；要求进 config |
| "What counts as 'taking data'?" | "Downloads, sharing outside the company, forwarding mail to a personal address. Slack workspace export too if you think it belongs." | 下载 / 外部分享 / 外部转发 |
| "Compared to what — a global threshold or the person's own normal?" | "Their own normal. Some people legitimately move a lot of data." | 本人基线（bob、dave 是考点） |
| "What if we have no baseline (new hire)?" | "Your call. Tell me what you picked and why." | 对外部分享/转发保守地标出，对下载不标 |
| "Where does the HR data come from? What if only a resignation date exists?" | "Roster file; `termination_date` is the last day when known. Notice period is usually two weeks." | 辞呈日 + 2 周当最后一天 |
| "What about activity after the last day?" | "That would be bad. Handle it however you think is right." | 视为最高严重度 |
| "Should this alert or just score?" | "Analysts only look at alerts. Use whatever the system already uses for scoring/alerting." | 走 scoring + threshold |
| "Who is this for — the analyst or the manager?" | "The analyst. They need to know why it fired." | reasons 里写清动作、次数、与基线对比、距离最后一天几天 |
| "Do I need to backfill / re-evaluate old days?" | "No. Replay already processes day by day." | 不需要 |

### ③ 隐藏期望（文件:符号）

- `signals/base.py:signal`、`signals/__init__.py`（**必须在这里 import**，否则装饰器从未执行，replay 里静悄悄没有这个 signal）。
- `baselines/store.py:BaselineStore.get`（返回 `None` = 冷启动；对"从未做过的动作"返回真实的 0 基线，`p95_count` / `p95_bytes` 可直接用）。
- `hr/roster.py:Employee.termination_date / resignation_submitted`（`ctx.roster.get(user)`；用户不在名册里要处理）。
- `config.py:Config.signal_weights`（漏了会走 `scoring.score_finding` 的 `default_signal_weight=0.2` + 一条 warning，分数偏低可能跌破 `alert_threshold` → 一个告警都没有）。
- `events.py:Action`（用已有枚举：`FILE_DOWNLOAD / FILE_SHARE_EXTERNAL / EMAIL_FORWARD_EXTERNAL / MESSAGE_EXPORT`，不自造字符串）。
- `timeutil` / `events.day_end`（日期比较用 `date`，不拿 naive datetime 比）。
- 不碰：`legacy/dlp_rules.py`（deprecated 且 README 里仍写着"每个事件都经过它"——README 已过时，现在是 signals）。

### ④ 追问（4–6 个）

1. "What if we ingest 10x the events? Where would this signal get slow?"（每用户每天每动作一次 `get` 查询；可批量预取 / 缓存基线）
2. "How would you roll this out to customers without flooding their analysts on day one?"（先 shadow 模式只写不通知；按租户 flag；`config.flag`）
3. "Dave shares externally every day and is being laid off. Walk me through why he doesn't alert, and what would make him alert."
4. "What's missing from your v1?"（没有 manager 信号、没有"在职但已提交辞呈前的异常"、冷启动策略粗糙、没有按部门调权重）
5. "A user's `termination_date` gets pushed back after you've already alerted. What happens?"（replay 是增量的，历史告警不会重算——这是已知局限）
6. "How do you know the signal isn't just firing on everything?"（看他有没有用 fixtures 的 bob / dave 当反例）

### ⑤ 打分信号

| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 先问窗口/动作/基线/冷启动/离职后活动；主动指出"全局阈值会误伤 bob"；选相对本人基线 | 问了 2-3 个问题，选了合理默认 | 不问直接写；用全局阈值或照搬 `legacy` 的 500MB 规则 |
| Agency | 明说 5 条假设并写进 reasons/注释；M1（只抓 carol）在 15 分钟内可演示；自己跑 replay 验证 | 有假设但没说出口；做完才验证 | 等面试官确认每一步；没验证就宣布完成 |
| Fit-the-system | `@signal` + `__init__` 注册 + config 字段 + 权重；复用 `BaselineStore.get`/roster/`Action`；返回 `Finding` | 复用了大部分，但阈值硬编码在 signal 里 | 在 pipeline 里加分支；自己建 sqlite 表/JSON；改 `volume_spike`；碰 `legacy/` |
| Testing | 新增 `tests/test_*.py` 覆盖：窗口内/外、heavy user、冷启动、离职后；并用 fixtures 回放看真实人物 | 有 1-2 个单测 | 只跑现有测试；没有新增测试 |
| AI-supervision | 先让 Claude 读 `signals/` + `baselines/` + `config.py`，提示里点名要复用的符号；审 diff 时发现并删掉重造的统计函数/硬编码阈值 | 接受了大部分输出，修了明显问题 | 整段粘贴 AI 输出；没发现 AI 写了全局阈值或忘了 import 注册 |
| Communication | 开场一分钟讲清心智模型；收尾说清 known gaps；用 bob/dave 举例解释误报 | 能讲清做了什么 | 只念代码；说不出为什么 |

---

## t2 · alert_cases（"Group them so an analyst sees one thing per incident"）

### ① 好的 v1 长什么样

新增 `alerts/cases.py`：`Case` + `CaseStore(conn, config)`，**新迁移** `migrations/0005_cases.sql`（cases + case_alerts 两张表，**不改** `0002_alerts.sql`）；`pipeline._process_day` 在 `AlertStore.add` 之后调用 `CaseStore.assign(alert)`，**只有 case 新建或严重度升级时才 `notifier.notify`**（复用既有 `Notifier` 协议，不改 `notify/slack_webhook.py` 去重）；窗口 `case_window_hours` 进 config；case 严重度用 `scoring.severity_label` 对成员最大分数求，而不是自己发明 low/medium/high；`cli.py` 新增 `cases [--user] [--json]` 与 `cases close <id>`，输出键 `id/user/status/severity/alerts`。已关闭的 case 不重开，之后的告警开新 case。

不是好 v1：在 `alerts` 表上加 `case_id` 列并改 0002；每次 CLI 调用时在内存里现算分组（没有持久状态、`cases close` 无处存）；把 case 当成新通知渠道；用平均分当严重度；窗口写死在代码里。

### ② 澄清问答

| Q | A | 默认 |
|---|---|---|
| "What defines one incident?" | "Same person, close together in time. Different people are different incidents." | 同用户 + 时间窗口 |
| "How close in time?" | "A day or two. Make it configurable." | 48 小时（相邻告警间隔，滚动） |
| "How severe is a case — max of its alerts, or sum?" | "Analysts triage by the worst thing in it." | 成员最大分数（对应 `severity_label`） |
| "What happens when an analyst closes a case and a new alert arrives?" | "That's a new incident." | 关闭后开新 case，不重开 |
| "Do I notify per case or per alert? When?" | "When an incident starts, and again if it gets worse. Not for every alert in it." | 新建 + 升级时各一次 |
| "Should the existing `alerts` command change?" | "No. Analysts still use it." | 不改，每条告警仍单独可查 |
| "Do I need to backfill cases for alerts already in the DB?" | "No, new replays are enough." | 不回填（说明为 known gap） |
| "How does an analyst close one?" | "`cases close <id>` is fine." | 同 ticket 文字 |
| "Is there a case status beyond open/closed?" | "Not for now." | 仅 open/closed |

### ③ 隐藏期望

- `db.py:migrate` + `migrations/NNNN_*.sql` 约定（CONTRIBUTING 写明："Never edit an applied migration"）。
- `alerts/store.py:AlertStore`（`conn` 注入、`with self._conn:` 事务风格）；`CaseStore` 同风格。
- `scoring.py:severity_label`（`Config.severity_medium/high`）。
- `config.py`（新键 `case_window_hours`，`load_config` 已能覆盖）。
- `notify/__init__.py:Notifier`、`pipeline.py` 中的 `self._notifier.notify(alert)` 调用点（改调用条件，而不是改 notifier）。
- `cli.py:COMMANDS` 注册表 + `--json` 约定；`errors.InsiderWatchError`（`cases close 99` 应走 exit code 2 的统一错误路径）。
- 不碰：`notify/slack_webhook.py` 的 outbox（"看起来是该去重的地方"）、`alerts` 表结构、`legacy/`。

### ④ 追问

1. "Henry has two bursts three weeks apart and a third later the same night. Show me how your window handles that."
2. "What if 10x the alerts: what query runs per alert in `assign`, and what index does it use?"（`idx_cases_user_status`）
3. "Replay stops at 09-02, an analyst closes the case, replay continues. Walk me through what the analyst sees."（stretch 验收即此场景）
4. "How would you roll this out? Customers already have scripts reading `alerts`."（保持 `alerts` 不变；case 只增不改；flag）
5. "What's missing?"（case 合并/拆分、分配给分析师、case 评论、回填、跨用户关联如同一 IP）
6. "Why max and not sum? When would sum be right?"

### ⑤ 打分信号

| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 先问"incident 怎么定义/窗口/严重度/关闭后/通知时机"；明确选 max + 滚动窗口并说出代价 | 问了窗口和通知 | 不问；每天一个 case 或每用户永远一个 case |
| Agency | 15 分钟内先让 `cases` 能列出分组（M1），再做通知，再做 close；每步用 henry 验证 | 一次性写完再测 | 写到最后一分钟才第一次运行 |
| Fit-the-system | 新迁移文件 + `CaseStore(conn, config)` + `severity_label` + 复用 `Notifier`，config 里放窗口 | 新表但把 DDL 写进 Python 的 `CREATE TABLE IF NOT EXISTS` | 改 0002 迁移 / 在 `alerts` 加列 / 在 notifier 里去重 / 现算分组无持久化 |
| Testing | 单测覆盖窗口边界、关闭后新 case、升级通知；回放 fixtures 看 henry 与 alice | 有基础单测 | 无新增测试；只肉眼看输出 |
| AI-supervision | 提示里点名 `db.py`/`alerts/store.py`/`scoring.py`；审 diff 时拒绝 AI 自建的 JSON/文件存储和自造严重度 | 修了 AI 的部分偏差 | 照单全收 AI 生成的独立存储和平均分 |
| Communication | 讲清"为什么通知只在新建/升级"；列出 known gaps（不回填、无合并） | 能说明做了什么 | 说不清通知行为变化对分析师意味着什么 |

---

## t3 · gdrive_connector（"Add Google Drive audit logs as a source"）

### ① 好的 v1 长什么样

`connectors/gdrive.py`：`@register_connector` 的 `Connector` 子类，`source = "gdrive"`；`parse_page` 把 `items[].events[]` **逐事件**展开成记录并返回 `nextPageToken`；`normalize` 映射到**已有** `Action`（`download`→`FILE_DOWNLOAD`；`change_document_visibility` 为 `people_with_link`/`public_on_the_web`→`FILE_SHARE_EXTERNAL`；`change_user_access` 且 `target_user` 为外部域→`FILE_SHARE_EXTERNAL`）；其余用 `self.drop("<reason>")` 丢弃并计数；时间用 `timeutil.parse_ts`（带偏移的 RFC3339 → UTC）；外部域用 `events.is_external` + `config.internal_domains`；在 `connectors/__init__.py` import 才会被 replay 发现。自带 `tests/test_gdrive.py`，并在 `replay --json` 看到 `gdrive`。

### ② 澄清问答

| Q | A | 默认 |
|---|---|---|
| "What counts as an external share?" | "Link sharing or public on the web, or sharing with someone outside our domains." | 同左 |
| "What about `view`, `edit`, `rename`?" | "We don't model them. Don't lose track of how many we skip." | 丢弃并计数 |
| "Do I add new `Action` values?" | "Only if you can justify it; the detections speak the existing ones." | 复用已有枚举 |
| "Sizes? The API doesn't always give them." | "Use `file_size` when present, else zero." | 缺省 0 |
| "One log item can contain several events?" | "Yes." | 每个 event 单独成事件 |
| "Time zones?" | "Google sends RFC3339, sometimes with an offset." | 全部转 UTC |
| "An actor with no email (external viewer)?" | "Skip it, count it." | drop `no_user` |
| "Do I touch detections?" | "No, this is only ingestion." | 不碰 signals |
| "Does it need a CLI flag?" | "Replay should just pick it up." | 无新增 flag |

### ③ 隐藏期望

- `connectors/base.py`：`Connector.parse_page / normalize / drop / events`，分页（token = 下一页文件名）、`ConnectorStats` 都在基类里，**不要重写 `fetch`**。
- `connectors/__init__.py`（import 即注册；忘了就是"replay 没有任何 gdrive 事件"）。
- `timeutil.parse_ts`；`events.is_external` / `Config.internal_domains`；`Action`。
- `pipeline.build_connectors`（按注册表 + 目录是否存在发现）；`replay --json` 的 `dropped` 来自 `ConnectorStats`。
- 不碰：`slack_audit.py`（epoch 时间戳的写法不适用）、`okta.py`、`legacy/`。
- Google 的坑：`intValue` 是字符串；`parameters` 是 name/value 列表；一条 item 多个 event；`actor.email` 可能缺失/大小写混杂。

### ④ 追问

1. "A customer has 50M Drive events a day. Where does `replay` break first?"（全部读入内存再排序；基类 `events()` 是生成器，但 pipeline 把全部事件 `list` 化）
2. "How would you onboard this customer safely?"（`insiderwatch check <raw_dir>` 先 dry-run；看 drop 原因分布）
3. "What if Google adds a new event type tomorrow?"（落入 `unmapped_event` 并计数，不崩）
4. "What did you decide about internal-domain sharing, and who might disagree?"
5. "What's missing?"（真实 API 拉取/游标持久化、`since`、组织单元、shared-drive 级别的事件、`copy`/`print` 动作）

### ⑤ 打分信号

| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 问"什么算外部分享/未知事件怎么办/要不要新枚举"；先看 fixtures 里真实形状（`intValue` 字符串、多 event item） | 看了 fixtures 再写 | 凭对 Google API 的记忆写，不看 fixtures |
| Agency | 先只做 `download`（M1，能在 replay 里看到），再做分享映射，再做 drop 计数 | 一次写完再跑 | 到最后才发现没被 replay 发现 |
| Fit-the-system | 继承 `Connector`、`@register_connector`、`__init__` import、`self.drop()`、`parse_ts`、`is_external` | 复用基类但重写了时间解析 | 自己写 `fetch` 循环/分页、`datetime.fromisoformat` 直接用、新增 Action 值、从 `slack_audit` 复制 epoch 逻辑 |
| Testing | `tests/test_gdrive.py`：分页、drop 计数、偏移、多 event item、`replay` 自动包含 | 有 1-2 个测试 | 无测试，只肉眼看 |
| AI-supervision | 让 AI 先读 `connectors/base.py` 和两个现有 connector；审出 AI 忽略 `intValue` 字符串/忘注册 | 修了主要问题 | 接受 AI 写的"通用 Google API 客户端" |
| Communication | 清楚说明映射表和丢弃策略，诚实说明内部分享的取舍 | 能讲 | 讲不清哪些事件被丢了 |
