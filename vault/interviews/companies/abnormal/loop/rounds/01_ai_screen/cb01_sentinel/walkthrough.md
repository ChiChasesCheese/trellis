# walkthrough.md · cb01_sentinel（参考的 60 分钟）

时间表：0–10 探索 · 10–45 实现一张 ticket · 45–60 walkthrough + 反问。每次模拟 = 探索 + 一张 ticket，都从 `starter/` 开始。
先抄一份：`python3 loop/ai_screen.py start cb01 t1`（或手动 `cp -r starter ~/abnormal-practice/cb01-t1`）。
官方原话（要记住的标准）："AI will produce working code. That's not enough. The bar is whether the code fits the existing system — its patterns, its conventions, its infrastructure. AI doesn't know what's already in the codebase unless you tell it to look."
所以每一条给 Claude 的提示词，都要点名它**先去看**哪些文件。

---

## ① 探索 10 分钟

先自己看 90 秒：`README.md`（注意：它有一处是过时的）、`CONTRIBUTING.md`、`ls sentinel/`。然后按顺序用下面 7 条提示词（每条都要求"引用文件"，防止 AI 瞎编）。

1. `Map the architecture of this repo: entry points, the main data flow from raw event to stored alert, and the extension points. Cite files and symbols. Do not modify anything.`
2. `Read CONTRIBUTING.md and then check which of those conventions are actually followed in the code (migrations, tenant scoping, error handling, metrics). Point to one example of each.`
3. `README.md says some things about enrichment and legacy/. Verify each claim against the code and list every claim that is wrong or stale.`（→ 抓出 "enrichers are pluggable" 与 "legacy still evaluated" 两处过时）
4. `Walk through Pipeline.process for one login event end to end. For each stage name the class, the file, and what it reads and writes (event.enrichment, the db tables).`
5. `Show me the registries in this codebase: how are collectors, rules and enrichers registered or discovered? Which of them have a registry and which don't?`（→ 规则与采集器有 `@register_*`；enrichers 没有）
6. `Which modules look relevant but are deprecated or unused? Prove it with grep.`（→ `sentinel/legacy/`）
7. `Run the test suite and the CLI on fixtures/events for tenant acme (python -m sentinel ingest ... --db /tmp/x.db, then alerts). Summarise what the alerts show.`（→ 13 条告警，其中 dave 的暴力破解一连串）

第 10 分钟对面试官说的 60 秒心智模型（英文口播）：

> "Here's my model. Raw events come in through collectors, one per source, registered with a decorator. Each becomes a `SecurityEvent` with a tenant id. The pipeline enriches it — right now `EnrichmentService` hardcodes geo, history and threat intel, even though there is an `Enricher` base class and a TODO about making it configurable. Then the rule engine runs the registered rules, which read `event.enrichment`; hits are combined into a threat level, scored, and `AlertService.create_from` stores an alert. Everything is tenant-scoped in sqlite, schema changes go through numbered migrations, and the API is a small WSGI framework where handlers register with `@route` and all errors share one JSON shape. Config is TOML with per-tenant overrides, strictly validated. The README is stale in two places, and `legacy/` is dead code. The natural extension points are: the seam between rules and alert creation, the `Enricher` interface plus the config layer, and `AlertService.create_from`. I'm ready to look at the ticket."

---

## ② t1 · rule suppression

**读 ticket 后的 3 个澄清问题（英文）**
1. "When a hit is suppressed, should it be gone, or stored somewhere so we can explain why no alert fired?"
2. "Can customers suppress anything — including `known_bad_ip` or critical hits — and do you want a guard rail?"
3. "For the match conditions: is it event fields plus enrichment fields like `geo.country`, all ANDed? And scope: new events only?"

**显式假设清单（口头说出来）**
- 抑制按租户；只对**新**事件生效；多个条件 AND；`match` 缺省 = 整条规则静音。
- 被抑制的命中不进告警队列，但计数 + 审计表留痕。
- `rule_id` 必须是已注册规则，否则 400（已有错误形状）。
- v1 不做过期、不做 PATCH；对 CRITICAL 先允许，并把"是否需要护栏"列为 known gap。

**里程碑**
- M1（≤15 min，可 demo）：migration + 仓储 + `POST/GET/DELETE /suppressions`，只支持 `rule_id`；`Pipeline.process` 里过滤；demo：创建后 `ingest` 同一批夹具，对应告警消失。
- M2：`match`（事件字段 + `geo.country` 这类 enrichment 路径，值相等/列表/CIDR）；租户隔离测试。
- M3：审计表 + 计数器；`match` 校验；追问里的 shadow 模式作为口头方案。

**给 Claude 的实现提示词**
```
Implement SEN-412 (rule suppression) in this repo. Before writing code, read:
- sentinel/pipeline.py (Pipeline.process), sentinel/rules/base.py (RULES, rule_ids)
- sentinel/api/framework.py and sentinel/api/routes/alerts.py (how routes, ApiContext, errors work), sentinel/api/routes/__init__.py
- sentinel/db/__init__.py (migrate) and sentinel/db/migrations/0001_init.sql, sentinel/alerts/repository.py (repository style)
- CONTRIBUTING.md
Constraints: do not modify any rule; filter hits in Pipeline.process after rule evaluation and before alert creation;
store suppressions in sqlite via a NEW migration (tenant_id on every query); register routes with @route and raise
ApiError subclasses; validate rule_id with rule_ids(); standard library only; add tests in the existing test files.
Start with rule_id-only suppression (milestone 1), then add `match` on event fields and enrichment paths like geo.country.
Show me the plan first and wait.
```

**审 AI 输出时看什么（right altitude）**
- diff 里有没有动 `rules/*.py`、`alerts/service.py`、`0001_init.sql`、`legacy/`？有 → 退回。
- 新增的是不是又一套错误类 / 路由装饰器 / 配置加载？应只出现 1 个新模块 + 1 个路由文件 + 1 个 migration。
- 每条 SQL 都带 `tenant_id`；DELETE 也是 `WHERE tenant_id = ? AND id = ?`。
- `match` 取值函数对"缺失字段"返回不匹配（而不是 KeyError → 500）。
- 引入了第三方依赖（pydantic / flask / sqlalchemy）？一律不要。

**如何验证**
```bash
python3 -m pytest -q                                   # 在你的练习副本里
python3 -m sentinel ingest fixtures/events --tenant acme --db /tmp/t1.db && python3 -m sentinel alerts --tenant acme --db /tmp/t1.db
python3 -m sentinel serve --db /tmp/t1.db &            # 然后用 curl 建一个抑制，重跑 ingest 到新库对比
python3 loop/ai_screen.py check cb01 t1 <练习目录>
```

**收尾说的 known gaps（英文口播）**
> "v1 suppresses by rule id plus AND-ed equality, list and CIDR conditions, per tenant, between rule evaluation and alert creation. Suppressed hits are counted and audited, not queued. What I did not do: expiry, editing, a guard rail for critical rules like `known_bad_ip`, a shadow mode for safe rollout, and caching suppressions per tenant — right now it is one query per event."

---

## ③ t2 · enrichment plugins

**读 ticket 后的 3 个澄清问题**
1. "If a tenant doesn't set `enabled`, do they get today's three built-ins?"
2. "If a plugin requires an enricher that isn't enabled, or throws on an event, what should happen?"
3. "Should plugin output feed into rules, or just be stored on the event? And are plugins trusted code?"

**显式假设清单**
- 默认 = 三个内置全开；插件必须显式启用；`enabled` 的顺序不重要，`requires` 决定执行顺序。
- 缺依赖 / 未知名字 / 循环 / 插件文件 import 失败 = 启动时 `ConfigError`；运行时单个插件抛异常 = 记录 + 计数 + 继续。
- 插件是受信任代码（客户工程师、托管部署），沙箱不在 v1。
- 规则不改；插件结果写入 `event.enrichment[name]`。

**里程碑**
- M1（≤15 min）：内置 enrichers 也走注册表（`@register_enricher`），`EnrichmentService` 按 `[enrichment] enabled` + `requires` 拓扑排序运行；`config.py` 校验新键。demo：租户配置 `enabled = ["geo"]`，`GET /events/<id>` 只剩 geo。
- M2：`plugin_dirs` 目录发现（`importlib`，只取目录里定义的 `Enricher` 子类，跳过 `_` 开头文件）；每租户独立的名字表。
- M3：异常隔离 + 计数；未知名字/缺依赖/重名/import 失败的 `ConfigError`；`Pipeline.ingest_dir` 启动即构造。

**给 Claude 的实现提示词**
```
Implement SEN-437 (configurable enrichment). Before writing code, read:
- sentinel/enrichment/base.py (the existing Enricher interface), sentinel/enrichment/service.py (the hardcoded service and its TODO),
  the three built-in enrichers
- sentinel/rules/base.py (register_rule/RULES) and sentinel/collectors/base.py (register_collector): the registry pattern to mirror
- sentinel/config.py (strict validation, per-tenant SettingsProvider), sentinel/pipeline.py (_runtime builds one service per tenant)
- sentinel/errors.py, sentinel/metrics.py, CONTRIBUTING.md
Constraints: reuse the existing Enricher base class (do not introduce a new plugin interface); built-ins must be registered through
the same mechanism; sort by `requires`; plugins are per tenant, never in a global registry; a plugin exception must be logged and
counted, not raised; bad config (unknown name, missing dependency, cycle, broken plugin file) raises ConfigError at startup; do not touch the rules.
Plan first, then milestone 1 only.
```

**审 AI 输出时看什么**
- 有没有新造 `Plugin`/`PluginManager`/entry-points？应复用 `Enricher`。
- 插件类是否被塞进全局 `ENRICHERS`（会跨租户泄漏）？应只在该租户的 service 里。
- `requires` 是否真的用来排序，而不是"按 enabled 列表顺序跑"？（验收测试故意把依赖写在后面。）
- 模块名冲突：同一路径被两个租户加载，`sys.modules` 里的名字是否唯一/可复用。
- 是否把 README 的"drop a class in sentinel/enrichment/"当成了真的？

**如何验证**
```bash
python3 -m pytest -q
# 手工：写一个 /tmp/plugins/asn_owner.py，acme.toml 里加 [enrichment] plugin_dirs / enabled
python3 -m sentinel ingest fixtures/events --tenant acme --db /tmp/t2.db
python3 loop/ai_screen.py check cb01 t2 <练习目录>
```

**收尾说的 known gaps**
> "Enrichment is now config-driven per tenant: built-ins and plugins register through the same `Enricher` interface, ordered by `requires`, errors isolated and counted, bad config fails at startup. Not done: a sandbox or timeouts for slow plugins, hot reload, a CLI to list discovered plugins or dry-run one, and interface versioning for customer plugins."

---

## ④ t3 · alert dedup

**读 ticket 后的 3 个澄清问题**
1. "What makes two alerts 'the same' — same rule, same user, same source IP? And over what window?"
2. "If an analyst has already acknowledged the alert and more events arrive, do we merge or open a new one?"
3. "What does `event_count` count, and do existing alerts need to keep working?"

**显式假设清单**
- 去重键 = 租户 + 规则集合 + user + src_ip；窗口 = 距上一个事件的滑动窗口，默认 60 分钟，可配置。
- 只有 OPEN 的告警吸收新事件；ACKED/CLOSED 之后开新告警。
- `event_count` = 触发了命中的事件数；合并后威胁等级取最大；旧告警回填 1。

**里程碑**
- M1（≤15 min）：migration（`event_count`、`last_seen`、`dedup_key`）+ `AlertService.create_from` 合并 + `Alert.to_dict()` 输出 `event_count`；demo：`ingest` 夹具，13 → 7 条告警，dave 的告警 `x5`。
- M2：窗口进 `[alerts] dedup_window_minutes`（校验）；ack 语义；`Pipeline.run` 返回去重后的告警。
- M3：`score` 随 `event_count` 增长；`event_ids` 封顶；回填。

**给 Claude 的实现提示词**
```
Implement SEN-451 (alert dedup). Before writing code, read:
- sentinel/alerts/service.py (AlertService.create_from: the only place alerts are created), sentinel/alerts/__init__.py (Alert), sentinel/alerts/repository.py
- sentinel/rules/brute_force.py (why one source produces many hits: leave it alone), sentinel/pipeline.py
- sentinel/db/migrations/0001_init.sql and sentinel/db/__init__.py (migrations), sentinel/config.py (AlertSettings), sentinel/scoring.py, sentinel/api/routes/alerts.py
- CONTRIBUTING.md
Constraints: merge in AlertService.create_from, persisted in sqlite (no in-memory dict); every query scoped by tenant_id; window from config
([alerts] key validated in config.py); a NEW migration adds the columns and backfills existing rows; only OPEN alerts absorb events;
merged alert takes the highest threat level; expose event_count through Alert.to_dict(); do not change rules. Plan first, then milestone 1.
```

**审 AI 输出时看什么**
- 它是否去改了 `BruteForce` 规则让它只命中一次？（治标；其它规则同样会重复。）
- 合并逻辑是否在 service 层，且查询带 `tenant_id`、`status = 'OPEN'`？
- 时间比较：存的是 `iso()` 字符串，查询参数也必须用 `iso()`，别混用 `isoformat()`。
- 现有测试 `test_fixture_run_produces_expected_alerts` 的期望会变——它是否**默默改了断言**而没告诉你？
- migration 是否 `ALTER TABLE ... ADD COLUMN ... DEFAULT`，对旧行有值？

**如何验证**
```bash
python3 -m pytest -q
python3 -m sentinel ingest fixtures/events --tenant acme --db /tmp/t3.db && python3 -m sentinel alerts --tenant acme --db /tmp/t3.db   # 看 x5
python3 loop/ai_screen.py check cb01 t3 <练习目录>
```

**收尾说的 known gaps**
> "Repeats of the same rules for the same user and source address inside an hour fold into one open alert, with a running `event_count`, last seen time and the highest threat level. Acked alerts are not reopened. Not done: concurrency — two workers could both miss the existing alert and insert twice; I'd add a unique key or an upsert. Also: a configurable dedup key, reopening, and splitting a merged alert."

---

## ⑤ 常见翻车（照抄 AI 的通用写法会怎样不契合）

| 翻车 | 为什么不契合 | 对应 |
|---|---|---|
| AI 生成一个 Flask/FastAPI 风格的 `suppressions` 路由，或自带 `pydantic` 模型 | 本仓库只有标准库；有自己的 `@route`、`ApiContext`、`ApiError` | t1 |
| 把抑制放在 JSON 文件 / 模块级 list | 重启丢失、没有租户隔离、违反 CONTRIBUTING（schema 变更 = migration） | t1 |
| 在每条规则里加 `if is_suppressed(...)` | 5 处重复，新增规则会漏；正确的缝在 `Pipeline.process` | t1 |
| 把 `sentinel/legacy/static_rules.py`（"deny if country == RU"）当作抑制机制扩展 | 它已冻结且不在管线里；README 里的架构图过时 | t1 |
| 新造 `PluginBase` / `PluginManager` / setuptools entry points | 已有 `Enricher`；本仓库不是 pip 安装模型 | t2 |
| 全局可变的 `PLUGINS` 字典 | 租户 A 的插件泄漏给租户 B | t2 |
| 按 `enabled` 列表顺序执行 | 忽略 `requires`；用户把 `history` 写在 `geo` 前就坏 | t2 |
| 插件异常直接冒泡 | 一个客户的 bug 让所有租户的检测停摆 | t2 |
| 相信 README "drop a class in sentinel/enrichment/" | 它是过时的；那条路径根本没有被发现机制读取 | t2 |
| 在 `BruteForce` 里改成"首次越线才命中" | 治标；其它规则的洪水还在；改了规则语义 | t3 |
| `Pipeline` 里维护 `dict[(user, ip)] -> alert` | 进程重启丢失；多租户/多进程不安全 | t3 |
| 查询漏了 `tenant_id` 或 `status='OPEN'` | 跨租户合并 / ack 后的告警被复活 | t3 |
| 悄悄修改旧测试的期望值让它变绿 | 面试官会看 diff；应当说明"这个期望本来就应该变" | t3 |
