# cb02_insiderwatch · 60 分钟参考走法

> 官方评分原话：*Judgment*（evaluate approaches, scope work into milestones, decide what fits the existing system）、*Agency*（make decisions, state assumptions, test your own work, keep momentum）。
> "AI doesn't know what's already in the codebase unless you tell it to look." 所以整场的节奏是：**先让 AI 读，再让 AI 写，最后你来审。**
> 每张 ticket 独立从 `starter/` 开始。练习：`python3 loop/ai_screen.py start cb02 t1`（在 kit 根目录）。

## 0. 探索 10 分钟

先自己 90 秒：`cat README.md CONTRIBUTING.md`，`git log --oneline | head`（如有），`find insiderwatch -name '*.py' | head -50`，`ls fixtures/*`。注意 README 里写"每个事件都过 `legacy/dlp_rules.py`"——和代码对不上（现在是 `signals/`），**这是个信号：README 不可全信，以代码为准。**

然后依次给 Claude Code 这 7 条提示词（按顺序，每条读完回复再发下一条；总共 ≤ 6 分钟）：

1. `Map the architecture of this repo: entry points, the main data flow from raw files to alerts, and the extension points (registries, base classes, config). Cite files and symbols. Do not edit anything.`
2. `README.md and CONTRIBUTING.md: which statements are true for the current code and which are stale? Verify each against the code and list contradictions.`
3. `Explain how a new Signal gets registered and run: what must I touch for it to show up in replay? Same question for a new Connector. Show the exact import/registration lines.`
4. `How are baselines computed and read? What does BaselineStore.get return during cold start, and for an action the user never performed? Which config keys control it?`
5. `Trace one alert end to end: finding -> scoring -> alert row -> notifier. Where are weights, thresholds and severity labels defined? Where do schema changes go?`
6. `Run the test suite and then run: python -m insiderwatch --db /tmp/iw.db replay fixtures/raw --until 2026-09-30 --json, then alerts. Summarize who gets alerts and from which signals. Which modules look deprecated or off limits?`
7. `List the conventions a new contribution must follow (tests location, migrations, logging, time handling, config) and the three places where a generic implementation would most likely diverge from them.`

### 第 10 分钟对面试官说的 60 秒心智模型（英文口播）

> "Here's my mental model. Raw audit logs sit under `fixtures/raw/<source>/` as pages. Each source has a `Connector` — registered with a decorator and imported in the package `__init__` — that parses pages and normalizes records into a single `Event` model with a fixed `Action` enum; anything it doesn't model is counted via `drop()`. The replay pipeline processes events one UTC day at a time: per user, every registered `Signal` returns findings with a 0-to-1 strength, using per-user rolling baselines from SQLite and the HR roster. `scoring` multiplies by a weight from `config.py`, and anything over `alert_threshold` becomes an `Alert` in SQLite and goes to a `Notifier`. Schema changes are numbered migrations. `legacy/dlp_rules.py` is deprecated and the README is stale about it. So the extension points are: signals, connectors, config, migrations, and the CLI command table. Which ticket would you like me to take?"

---

## t1 · departing_exfil

**读 ticket 后的 3 个澄清问题（英文）**

1. "How far back from the last day should we watch, and should that be tunable per customer?"
2. "What counts as taking data: downloads only, or also external sharing and forwarding to personal mail? And is it measured against the person's own baseline or a global threshold?"
3. "What should we do for people with no baseline yet, and for activity after the termination date?"

**显式假设清单（口头说出并写进代码注释/commit message）**

- 离职窗口 = 最后一天前 14 天（`departure_window_days`），最后一天 = `termination_date`；只有辞呈日时按 14 天通知期推算。
- 动作 = 下载 / 外部分享 / 外部转发（/ Slack 导出），全部用已有 `Action`。
- 判断相对**本人**基线（`BaselineStore.get`，超过本人 p95 的一定余量）；重度下载者照常行为不报。
- 冷启动：外部分享/转发无基线也标（本身就是外流），下载不标。
- 离职日之后任何非失败活动 → strength 1.0。
- 不回填、不通知逻辑变更；告警由现有 `scoring` + `alert_threshold` 决定。

**里程碑**

- **M1（≤ 15 min，可演示）**：`@signal("departing_exfil")` 注册；只处理"窗口内外部分享 vs 本人基线"；加权重进 `config`；replay 后 `alerts --user carol...` 有告警，bob 没有。
- **M2**：加入下载/转发/导出，按动作 p95 比较，reasons 写清次数与"距最后一天 N 天"；erin（无辞呈）也命中。
- **M3**：离职日后活动（gina）、冷启动策略、单测（窗口内外、heavy user、冷启动、离职后）、跑全量测试。

**给 Claude 的实现提示词**

```
Add a new detection for departing employees. Follow the existing Signal pattern exactly:
- create insiderwatch/signals/departing_exfil.py with @signal("departing_exfil") (see signals/volume_spike.py and signals/base.py), and register it by importing it in signals/__init__.py
- read termination_date / resignation_submitted from ctx.roster (hr/roster.py); treat resignation + notice as the last day when no termination_date
- compare against the user's OWN baseline with ctx.baselines.get(user, action, ctx.day) (baselines/store.py); handle None as cold start
- use the existing Action enum members FILE_DOWNLOAD, FILE_SHARE_EXTERNAL, EMAIL_FORWARD_EXTERNAL; do not add new ones
- put the window length, notice days and the action list in config.py, and add the weight to Config.signal_weights; do not decide alerting inside the signal, return Findings only
- do not touch legacy/ or pipeline.py
- add tests/test_departing_exfil.py in the style of tests/test_signals.py (use the history()/make_event() helpers from conftest.py)
Then run the tests and replay fixtures/raw --until 2026-09-30 and show alerts for carol.diaz, bob.martin, dave.kim, erin.walsh.
```

**审 AI 输出时看什么（right altitude）**

- 有没有 `if bytes > 500 * 1024 * 1024`（= 照抄 `legacy/dlp_rules.py` 的全局阈值）？有就退回。
- `signals/__init__.py` 里有没有加 import？没有的话测试能过（直接构造类）但 replay 没有任何新告警。
- 阈值/窗口/权重是否在 `config.py`，`signal_weights` 有没有漏（漏了会走 default weight 0.2 并打 warning，分数可能低于 `alert_threshold`）。
- 用 `date` 比较而不是 naive `datetime`；用户不在名册时不崩。
- AI 有没有自己实现一遍均值/标准差（`baselines/stats.py` 已有），或绕过 `BaselineStore` 自己查 SQLite。
- 过度工程信号：新建表、新建 HR 加载器、改 `pipeline.py`。

**验证命令**

```
python3 -m pytest -q
rm -f /tmp/iw.db; python3 -m insiderwatch --db /tmp/iw.db replay fixtures/raw --until 2026-09-30 --json | head -5
for u in carol.diaz bob.martin dave.kim erin.walsh gina.park frank.okafor; do echo $u; python3 -m insiderwatch --db /tmp/iw.db alerts --user $u@acme.example; done
```
（期望：carol、erin、gina 有告警；bob、dave、frank 没有。）

**收尾 known gaps（英文口播）**

> "v1 flags carol, erin and post-termination activity, and stays quiet for bob and dave because it compares against their own baseline. Known gaps: cold-start handling is crude — new hires with external shares get flagged, downloads don't; the 1.25x-p95 margin is a heuristic I'd calibrate on real data; there's no per-customer tuning beyond the config window; and replay is incremental, so changing a termination date doesn't re-evaluate past days."

---

## t2 · alert_cases

**3 个澄清问题（英文）**

1. "What defines one incident — same user within some time gap? How big a gap?"
2. "How severe is a case: the worst alert in it or an aggregate? And when does the Slack/outbox ping fire — per alert, or when the incident starts and gets worse?"
3. "When an analyst closes a case and a new alert comes in for the same person, is that a new case? Does the existing `alerts` command stay as is?"

**假设清单**

- case = 同一用户、相邻告警间隔 ≤ 48h（`case_window_hours`，滚动）；关闭后的 case 永不重开。
- 严重度 = 成员最高分，经 `scoring.severity_label` 映射；通知只在新建/升级时发一次。
- `alerts` 命令与表结构不变；不回填历史；状态仅 open/closed。
- 持久化在 SQLite，走**新迁移**。

**里程碑**

- **M1（≤ 15 min）**：`0005_cases.sql` + `CaseStore.assign()`；pipeline 里每个新 alert 归入 case；`cases --json` 能列出 henry 的 2 个 case。
- **M2**：严重度 = max；通知只在新建/升级时发（`outbox` 从 59 条降到个位数）。
- **M3**：`cases close <id>`；关闭后新告警开新 case；`--user`；单测（窗口、关闭、升级）。

**给 Claude 的实现提示词**

```
Group alerts into cases. Follow existing patterns:
- add a NEW numbered migration insiderwatch/migrations/0005_cases.sql (see db.py:migrate and CONTRIBUTING.md); do not edit 0002_alerts.sql or the alerts table
- add insiderwatch/alerts/cases.py with a CaseStore(conn, config) in the same style as alerts/store.py; severity must come from scoring.severity_label applied to the max alert score
- put the grouping window in config.py (case_window_hours)
- in pipeline.py, after AlertStore.add, assign the alert to a case and only call the existing notifier when the case is created or its severity label rises; do not change notify/
- add `cases [--user U] [--json]` and `cases close <id>` to cli.py using the COMMANDS table; errors must use InsiderWatchError
- JSON per case: id, user, status (open/closed), severity, alerts (list of alert ids)
- add tests/test_cases.py using the conn/config fixtures from tests/conftest.py
Then replay fixtures/raw --until 2026-09-30 --notifier slack and show `cases --user henry.ross@acme.example` and the outbox count.
```

**审 AI 输出时看什么**

- 有没有在 `alerts` 表加列 / 修改 0002（违反迁移约定）；`CREATE TABLE IF NOT EXISTS` 写进 Python 而不是迁移。
- 严重度是不是平均/求和后自造阈值（应复用 `severity_label`）；
- 通知去重是否做在 `notify/slack_webhook.py` 里（错层：notifier 不知道 case）。
- 窗口写死 24h/48h 在代码里；每次 CLI 现算分组（`close` 无处落地）。
- `cases close` 对不存在/已关闭 case 的错误是否走统一错误出口（exit code 2）。
- 过度工程：case 状态机、分配给分析师、评论。

**验证命令**

```
python3 -m pytest -q
rm -f /tmp/iw.db; python3 -m insiderwatch --db /tmp/iw.db replay fixtures/raw --until 2026-09-30 --notifier slack >/dev/null
python3 -m insiderwatch --db /tmp/iw.db cases
python3 -m insiderwatch --db /tmp/iw.db alerts | wc -l; python3 -m insiderwatch --db /tmp/iw.db outbox | wc -l
```
（期望：henry 2 个 case；outbox 行数远小于 alerts 行数。）

**known gaps**

> "Alerts are grouped per user with a 48-hour rolling gap; severity is the worst alert; we notify when a case opens or escalates. Gaps: existing alerts aren't backfilled, no merging or splitting of cases, no cross-user correlation like shared IPs, no assignment or comments, and the window isn't per customer yet."

---

## t3 · gdrive_connector

**3 个澄清问题（英文）**

1. "What should count as an external share — link sharing, public, sharing with someone outside our domains?"
2. "What do we do with events we don't model, like view or rename? Do we need to know how many we skipped?"
3. "Do I add new Action values or map onto the existing ones, and does replay need a flag to include the new source?"

**假设清单**

- 外部分享 = `visibility ∈ {people_with_link, public_on_the_web}` 或 `change_user_access` 的 `target_user` 在 `config.internal_domains` 之外。
- `download` → `FILE_DOWNLOAD`，`bytes = file_size`（`intValue` 是字符串）。
- 其余（view/edit/rename/未知/无 email）全部 `drop(reason)` 并计数；一个 item 里的每个 event 独立。
- 时间一律 `timeutil.parse_ts`；不加新 `Action`；replay 自动发现。

**里程碑**

- **M1（≤ 15 min）**：`GDriveConnector` 注册并 import；只映射 `download`；`replay --json` 里出现 `gdrive`。
- **M2**：分享映射（可见性 + 外部用户）、多 event item、分页（基类已做）。
- **M3**：drop 计数、时区（`--until 2026-09-30` 排除 09-30T20:00-07:00 的事件）、`tests/test_gdrive.py`。

**给 Claude 的实现提示词**

```
Add a Google Drive audit-log connector. Look at connectors/base.py, connectors/m365_audit.py and connectors/okta.py first and follow them:
- new file connectors/gdrive.py: a Connector subclass decorated with @register_connector, source = "gdrive"; implement parse_page (items[].events[] flattened into one record per event, continuation token = nextPageToken) and normalize; do not override fetch/events
- map to EXISTING Action members only: download -> FILE_DOWNLOAD (bytes from the file_size parameter, which is an int64 string); change_document_visibility to people_with_link/public_on_the_web -> FILE_SHARE_EXTERNAL; change_user_access to a target_user outside config.internal_domains (use events.is_external) -> FILE_SHARE_EXTERNAL
- anything else: return self.drop("<reason>") so it is counted
- parse timestamps with timeutil.parse_ts (they carry UTC offsets); skip actors without an email
- register it by importing it in connectors/__init__.py
- add tests/test_gdrive.py using fixtures/raw/gdrive
Then run `python -m insiderwatch --db /tmp/g.db replay fixtures/raw --until 2026-09-30 --json` and show by_source/by_action/dropped.
```

**审 AI 输出时看什么**

- `int(p["intValue"])`：AI 常假设它是 int；
- 只读 `events[0]`，丢掉同一 item 的其他事件；
- 自写分页循环/`json.load` 目录（基类已处理）；
- `datetime.fromisoformat(...)` 直接用（3.11 下对 `Z` 可行，但对 naive/混合偏移的处理与项目约定不一致；应走 `parse_ts`）；
- 忘记 `connectors/__init__.py` import（测试直接构造类能过，replay 却没有 gdrive）；
- 新增 `Action.FILE_VISIBILITY_CHANGE` 之类枚举（下游 signals 不认识）；
- 从 `slack_audit.py` 复制 epoch 时间戳逻辑。

**验证命令**

```
python3 -m pytest -q
python3 -m insiderwatch --db /tmp/g.db replay fixtures/raw --until 2026-10-02 --json | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['by_source'],d['dropped'])"
python3 -m insiderwatch check fixtures/raw
```
（期望：`gdrive` 10 条事件，其中 6 个下载、4 个外部分享；`dropped.gdrive` = 8。）

**known gaps**

> "Drive downloads and external shares are ingested and mapped onto the existing actions; everything else is dropped and counted by reason. Gaps: it reads exported pages rather than calling the Reports API with a persisted cursor, internal-only access changes and shared-drive-level events aren't modelled, and `replay` still loads all events in memory, which won't survive a customer at Drive scale."

---

## 3. 常见翻车（照抄 AI 通用写法为什么不契合）

| 翻车 | 通用 AI 写法 | 为什么不契合本系统 |
|---|---|---|
| t1 全局阈值 | "FILE_DOWNLOAD > 500MB in the last 14 days of employment" | 与 deprecated 的 `legacy/dlp_rules.py` 同款；bob 每天 200MB 被误报；`BaselineStore` 就是为"相对本人"而存在 |
| t1 忘记注册 | 新文件 + 单测直接构造类，测试全绿 | `signals/__init__.py` 没 import，replay 里 signal 根本不存在；不看 `__init__` 就不知道 |
| t1 漏权重 | 在 signal 里 `strength=1.0` 就当完事 | `signal_weights` 没有条目 → 默认 0.2 + warning → 低于 `alert_threshold` → 0 告警 |
| t1 pipeline 分支 | 在 `_process_day` 里 `if emp.termination_date` | 破坏"signal 返回 finding、scoring 决定告警"的分层 |
| t2 改旧迁移 | 在 `0002_alerts.sql` 加 `case_id` 列 | CONTRIBUTING："Never edit an applied migration"；已有库不会重跑 |
| t2 现算分组 | `cases` 命令里读 alerts 再 `itertools.groupby` | 无持久状态，`close` 没地方存；通知时机拿不到 |
| t2 notifier 去重 | 在 `SlackWebhookNotifier` 里按用户去重 | 错层：notifier 不知道 case/升级；console 通知也要变 |
| t2 自造严重度 | 平均分 / 求和 / 自己写 `if score > 0.7` | 已有 `scoring.severity_label` + config 阈值；平均会把一条 high 稀释掉 |
| t3 自写分页 | `for f in sorted(glob)` 读文件 | 基类 `fetch` 已按 token 分页并防环 |
| t3 `intValue` / 多 event | 假设 `intValue` 是 int、只取 `events[0]` | fixtures 里是字符串 + 一条 item 两个 event；不看 fixtures 就会错 |
| t3 新枚举 | 加 `FILE_VISIBILITY_CHANGE` | 所有 signal/配置都按现有 `Action`；下游无人处理 |
| t3 时间 | 直接 `fromisoformat` 或忽略偏移 | `--until` 边界被打破（09-30T20:00-07:00 实为 10-01 UTC）；项目约定统一 `parse_ts` |
