# cb01 · 逐场脚本
> Sentinel：多租户安全事件管线（采集 → 富化 → 规则 → 威胁等级/排序 → 告警 → sqlite → WSGI API）· t1 规则抑制（SEN-412）· t2 富化插件化（SEN-437）· t3 告警去重（SEN-451）· 练：`python3 loop/ai_screen.py start cb01 <t>` · 面试官视角：`interviewer.md`
> T/X 编号见 `../claude_playbook.md`；英文口播模板见 `../playbook.md` §5。每次模拟 = 探索 + 一张 ticket，都从 `starter/` 开始。

## 0. 探索（0–10 min，三个 ticket 通用）
- 先打开：
  - `CONTRIBUTING.md`：七条约定（租户隔离、schema = migration、配置优于常量、`ApiError`、`metrics.incr`、不碰 `legacy/`、测试放进已有文件）= 评分的"契合"清单。
  - `sentinel/pipeline.py:Pipeline.process`：enrich → `rules.evaluate` → `events.add` → `alerts.create_from`；`_runtime` 每租户一份 service。t1/t3 的缝都在这里或它调用的地方。
  - `sentinel/enrichment/base.py:Enricher` + `enrichment/service.py:EnrichmentService`：基类（`name`/`requires`/`enrich`）已存在，service 手工 new 三个并带 `TODO(platform)`。t2 的全部内容。
  - `sentinel/config.py:_ALLOWED` / `build_settings`：未知键 = `ConfigError`，租户在 `config/tenants/<t>.toml` 覆盖。
  - `sentinel/alerts/service.py:AlertService.create_from`：告警唯一创建点（t3）；`sentinel/rules/base.py:RULES`、`register_rule`：注册表范本（t2）。
- T1 结果应包含：
  - 入口：`python -m sentinel {ingest,alerts,rules,serve}`（`sentinel/cli.py:main`）；`sentinel/app.py:create_app` 是组合根；API 用 `@route`（`api/framework.py`）注册，handler 放 `api/routes/`，在 `routes/__init__.py` import 才生效。
  - 数据流：`collect_all` → `SecurityEvent` → `EnrichmentService.enrich`（写 `event.enrichment[name]`）→ `RuleEngine.evaluate`（规则经 `Rule.enrichment(event, name)` 读，缺失返回 `{}`）→ `AlertService.create_from` → `AlertRepository`。
  - 扩展点：`@register_rule` / `@register_collector` 有注册表，enrichers 没有；`routes/__init__.py`；`config.py`；`db/migrations/NNNN_*.sql`。
  - 过时：README 称 enrichers "drop a class into this package and it is picked up"（假，没有发现机制）、`legacy/` "still evaluated"（假，不在管线里）；`sentinel/legacy/` 冻结。
  - 测试：`uv run --with pytest python -m pytest -q`（starter 44 个，solution 59 个，约 0.1 s）；单文件 `python -m pytest -q tests/test_ingest.py`。CLI 基线：`python3 -m sentinel ingest fixtures/events --tenant acme --db /tmp/s.db` → `ingested 24 events, 13 alerts (3 bad records skipped)`，其中 203.0.113.140（dave）占 8 条。
- 心智模型（60 s，英文原句）："Raw events come in through collectors, one per source, registered with a decorator. Each becomes a `SecurityEvent` with a tenant id. The pipeline enriches it — right now `EnrichmentService` hardcodes geo, history and threat intel, even though there is an `Enricher` base class and a TODO about making it configurable. Then registered rules read `event.enrichment`, hits become a threat level and a score, and `AlertService.create_from` stores the alert. Everything is tenant-scoped in sqlite, schema changes are numbered migrations, API handlers register with `@route`, config is strictly validated TOML with per-tenant overrides. README is stale in two places and `legacy/` is dead code. The natural seams are: between rule evaluation and alert creation, the `Enricher` interface plus config, and `AlertService.create_from`."

---

## t1 · rule suppression（SEN-412）

### 题
客户要静音某条检测，例：公司 VPN 出口在国外，员工的 impossible_travel 不该报。通过 `POST /suppressions`（`rule_id` + 可选 `match`，如 `{"geo.country": "DE"}`）、`GET /suppressions`、`DELETE /suppressions/<id>` 管理。

### 参考答案
- 设计：抑制是跨规则的策略，缝在 `Pipeline.process` 的 `evaluate` 与 `create_from` 之间（X5，T5）。选项 A：每条规则里加 `if suppressed`（5 处重复，新规则会漏）；选项 B：管线里一个 `SuppressionService.apply(event, hits)`。选 B。存储用 sqlite + 新 migration，所有 SQL 带 `tenant_id`；`match` 是点路径 → 值（AND，列表 = any-of，`src_ip` 含 `/` = CIDR），路径可解析事件字段和 `enrichment`（`geo.country`）。被抑制的命中不进队列，但写审计表并计数。
- 改动：
  - `sentinel/db/migrations/0002_suppressions.sql`：`suppressions` + `suppressed_hits` 两张表，索引以 `tenant_id` 开头；不动 `0001_init.sql`。
  - `sentinel/suppressions.py:SuppressionRepository / matches / SuppressionService.apply`：查询、点路径匹配、过滤并 `record_hit` + `metrics.incr("suppression.applied")`。
  - `sentinel/pipeline.py:Pipeline.process`：`hits = runtime.suppressions.apply(event, hits)`；`_TenantRuntime` 加字段。
  - `sentinel/api/routes/suppressions.py`：三个 `@route`；`rule_id not in rule_ids()` → `BadRequest`；`routes/__init__.py` import 它。
- 关键测试：
  - `tests/test_api.py::test_suppression_crud_and_validation`：201/200/204；另一租户 GET 为空、DELETE 他人 id → 404；非法 `rule_id` → 400 `bad_request`。
  - `tests/test_api.py::test_suppressed_rule_raises_no_alert`：抑制 `impossible_travel` + `geo.country=SG` 后，只剩 `[["new_country_login"]]`。
  - `tests/test_detection.py::test_match_paths_cover_event_fields_and_enrichment`、`::test_apply_drops_and_audits`：路径/列表/CIDR 匹配，缺失 enrichment 不匹配，审计与计数，跨租户不受影响。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | 复述 ticket，T4 定义 suppress；T2 后只问 3 个 | "So suppress means: the rule still runs, but the hit does not become an alert — and we can still say why. Three questions. When a hit is suppressed, gone or recorded? Can they suppress `known_bad_ip` or critical hits? Is `match` event plus enrichment fields, ANDed, new events only?" 面试官答："I don't want analysts to see them in the queue, but we need to answer 'why didn't this alert fire?'"；"Allow it, but I'd want the customer to know what they're doing."（或 "Never for critical"，随意）；"AND. If they want OR they create two suppressions." 默认：丢弃 + 审计 + 计数；CRITICAL 先允许并列 known gap；AND；只对新事件 | T2：`Given SEN-412 and this repo: list the decisions I must make, ordered so each depends only on earlier ones. Format: Q<n> — question; → the option you'd pick and why. Look up facts in the code. No code.` |
| 13–16 方案 | 说缝，两方案，选一个，定 M1–M3，立规矩 | "The seam is between `rules.evaluate` and `alerts.create_from` in `Pipeline.process`. Option A is a check inside each rule; option B is one `SuppressionService` after evaluation. B keeps rules unaware and new rules get it for free. M1 is rule-id-only mute end to end by minute thirty." | T3：`Here's my list: seam after evaluate; sqlite via a new migration with tenant_id; routes via @route; validate rule_id with rule_ids(); audit + counter. What did I miss? Add only what's missing, ranked by user impact.` T5：`I think the seam is Pipeline.process between rules.evaluate and alerts.create_from (existing adapters: none yet, rules are the producers). Compare per-rule check vs one service after evaluation in 5 lines each: fit with existing code, failure isolation, what a customer must do. Recommend one. Don't edit.` T6：写 CLAUDE.md 五条规则 |
| 16–30 M1 | plan mode → 审计划 → 红 → 绿 → 真实入口 | "First failing test: mute one rule and see no alert. Then the minimal change." | T7 红：`Write ONE failing test in tests/test_api.py: POST /suppressions {"rule_id": "impossible_travel"} through the acme TestClient, run app.pipeline.run on a US->SG pair, and assert GET /alerts has no impossible_travel alert. Expected values as literals. Run it and show me it fails. Don't fix.`（失败原因应是 `/suppressions` 404，不是 import 错误）T7 绿：`Minimal change to make that test pass: migration 0002, SuppressionRepository, route file registered in routes/__init__.py, and the one-line apply call in Pipeline.process. Nothing else. Run tests/test_api.py.` |
| 30–40 M2 | `match` 点路径 + 租户隔离测试；红了走 T8 | "M2 is the geo-ip case from the ticket: `match` as dotted paths, so `geo.country` reads the enrichment the rules read." | T7 红：`Write ONE failing test: suppression {"rule_id": "impossible_travel", "match": {"geo.country": "SG"}} drops the SG travel hit but a DE travel event still alerts. Literals only.` 绿：`Add dotted-path lookup over user, src_ip, kind, source, attrs.* and enrichment names; AND across conditions; a missing path never matches.` |
| ~40 审查 | T10 一轮，收一条拒一条 | "I'd normally run a doubt pass with a fresh reviewer — one round now. I'll take the first finding and reject the second, and here is why." | T10：`Adversarial review of the current diff against SEN-412. Assume the author is overconfident. Look for unstated assumptions, unhandled edge cases, broken conventions, failure modes under bad input. Do NOT validate or summarize. Max 5 issues, ranked.` 典型发现：① `match` 路径缺失/类型错 → 要么 KeyError 500，要么静默不匹配（收：缺失即不匹配，`POST` 时校验 `match` 形状 → 400）；② 每个事件 `repo.list(tenant)` 查一次表（拒：v1 成本可接受，写进 known gaps：按租户缓存 + 写时失效） |
| 42–45 收尾 | 自己跑证据；写 NOTES.md | "Fresh run: 59 passed. Here's the real output through the API and the CLI." | T11：`uv run --with pytest python -m pytest -q`；`python3 -m sentinel serve --db /tmp/t1.db --port 8791` 后 `curl -XPOST -H 'Authorization: Bearer tok-acme-analyst' -d '{"rule_id":"impossible_travel","match":{"geo.country":"SG"}}' localhost:8791/suppressions` → `{"created_at": ..., "id": "sup_...", "match": {"geo.country": "SG"}, "rule_id": "impossible_travel"}`；用 globex token `GET /suppressions` → `{"items": [], "total": 0}`；错 id → `{"error": {"code": "bad_request", ... "unknown or missing rule_id"}}`；停服务后 `python3 -m sentinel ingest fixtures/events --tenant acme --db /tmp/t1.db` → `ingested 24 events, 7 alerts`，`python3 -m sentinel alerts --tenant acme --db /tmp/t1.db` 不再有 `moved 15822 km`（换成 `alice@acme.test logged in from SG for the first time`，另一条规则）；`sqlite3 /tmp/t1.db "select rule_id,event_id from suppressed_hits"` → `impossible_travel|a-003`。T12：`NOTES.md`：assumptions + known gaps + v2 |
| 45+ 讲解 | 3–5 min，`playbook.md` §5.3 | "v1 suppresses by rule id plus AND-ed equality, list and CIDR conditions, per tenant, between rule evaluation and alert creation. Suppressed hits are counted and audited, not queued. Not done: expiry, editing, a guard rail for critical rules like `known_bad_ip`, a shadow mode for safe rollout, and caching suppressions per tenant — right now it is one query per event." | — |

### 追问与答（来自 interviewer.md）
1. "10,000 suppressions per tenant, 10x volume?" → 每个事件查一次表是 O(n)。按 `rule_id` 建索引（已有 `(tenant_id, rule_id)`），进程内按租户缓存、写时失效，匹配时只看该规则的抑制。
2. "Roll out safely?" → shadow 模式：只记录"本来会被抑制"，不真丢；按租户 feature flag 开启，对比 shadow 命中数再切真。
3. "Suppress `known_bad_ip` with no conditions — OK?" → 策略题：无条件静音关键规则要警告、禁止或双人审批；审计留痕；被盗管理员账号加抑制是攻击路径，需通知其他管理员。
4. "How does an analyst learn an alert was suppressed?" → `suppressed_hits` 审计表 + 计数器 `suppression.applied`；v2 加只读端点和"近 7 天吞掉多少命中"。
5. "What's missing?" → 过期（`expires_at`，默认 30/90 天）、PATCH、分页、`match` 路径从不存在时的提示。
6. "A `match` path never exists — how to catch it?" → 创建时对已知字段前缀（`user`、`src_ip`、`kind`、`source`、`attrs.*`、已启用 enricher 名）校验；或统计该抑制 N 天内命中为 0 并提示。

### 翻车点
- 在每条规则里加 `if is_suppressed(...)` → 5 处重复，新规则会漏；缝在 `Pipeline.process`。
- 抑制放 JSON 文件或模块级 list → 重启丢失、无租户隔离，违反"schema 变更 = migration"。
- 扩展 `legacy/static_rules.py`（"deny if country == RU"）→ 已冻结且不在管线里，README 的"still evaluated"是过时的。
- 自带 Flask/pydantic 风格路由 → 仓库只有标准库，已有 `@route`/`ApiContext`/`ApiError`。

---

## t2 · enrichment plugins（SEN-437）

> 这张就是 `REAL_QUESTION.md` 的真题（LeetCode Discuss #8335187）：面试官先说 t1（"suppress some rules … based on geo-ip"），一分钟后改口 "Sorry, I gave you the wrong question"，换成 "enrichment layer hardcodes geo-ip, history and one more … plugin-based mechanism so clients never have to change our code"。改口时说："Got it — so the real ask is configurable enrichment. Can I ask three quick questions?" t1 被收回不代表白做，扩展环节可能追问，两题都要会（见上一节）。
> 口述版练习的口播题：`python3 loop/ai_screen.py start cb01 real`；做完 `check cb01 real <目录>` 跑 t2 的隐藏验收。

### 题
富化层写死 geo / history / threat intel。客户要选择自己跑哪些 enricher，并加自己的：实现了现有 `Enricher` 接口的 Python 文件放进租户配置 `[enrichment] plugin_dirs` 列出的目录，用 `[enrichment] enabled = [...]` 按名字启用，平台代码不动。

### 参考答案
- 设计：`Enricher` 基类已有（`name`/`requires`/`enrich`），service 却手工 new 三个——这就是 "hardcode"。把基类当插件契约（X5）：内置三个通过与 `@register_rule` 同风格的 `@register_enricher` 注册；租户配置的 `plugin_dirs` 经 `importlib` 发现目录里的 `Enricher` 子类，只进该租户 service 的名字表，不进全局 `ENRICHERS`（租户隔离）；`enabled` 缺省 = 三个内置；执行顺序由 `requires` 拓扑排序决定，不由 `enabled` 列表顺序。配置错误（未知名、缺依赖、循环、重名、插件 import 失败）在构造 service 时 `ConfigError`，`ingest_dir` 提前构造所以启动即报；运行时单个插件抛异常只记录并计数。规则代码一行不改：它们经 `Rule.enrichment()` 读，缺失本就返回 `{}`，所以禁用 geo 后 `impossible_travel` 不崩，只是静默不触发。
- 改动：
  - `sentinel/enrichment/base.py:ENRICHERS / register_enricher`：注册表；重名抛 `ValueError`。`geo_ip.py`/`history.py`/`threat_intel.py` 三个内置类加 `@register_enricher`；`enrichment/__init__.py` import 三个模块触发注册。
  - `sentinel/enrichment/plugins.py:discover`：遍历每个不以 `_` 开头的 `*.py`，模块名带路径哈希（`sentinel_plugin_<hash>_<stem>`）防冲突；只收定义在该模块内、非抽象的 `Enricher` 子类；缺 `name`、与内置或其它插件重名、import 失败、目录不存在都抛 `ConfigError`。
  - `sentinel/enrichment/service.py:resolve_order / EnrichmentService`：`resolve_order` 拓扑排序（未知名、依赖未启用、循环 → `ConfigError`）；`enrich()` 依赖没产出则 `metrics.incr("enrichment.skipped")` 跳过，异常 → `log.exception` + `metrics.incr("enrichment.error", enricher=...)`。
  - `sentinel/config.py:EnrichmentSettings / _ALLOWED["enrichment"] / build_settings`：新增 `enabled`、`plugin_dirs`，类型校验（字符串列表）；相对路径相对仓库根（`config_dir.parent`），不依赖 CWD。
  - `sentinel/pipeline.py:Pipeline.ingest_dir`：`self._runtime(tenant_id)` 取代 `settings.for_tenant`，启动即暴露配置错误。
- 关键测试：
  - `tests/test_ingest.py::test_plugin_runs_after_its_dependency`：`svc._enrichers` 顺序 `["geo", "asn_owner"]`，`event.enrichment["asn_owner"] == {"owner": "AS64500"}`。
  - `tests/test_ingest.py::test_failing_plugin_is_counted_and_others_continue`：`exploding` 不在 enrichment 里、`geo` 在，`metrics.get("enrichment.error", enricher="exploding") == 1`。
  - `acceptance/test_t2.py::test_requires_decides_order_not_the_enabled_list`：`enabled` 把 `geo` 写在最后，`asn_owner` 仍读到 geo。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | 复述；T4 定义 enricher / enrichment；问 3 个 | "An enricher adds facts about one event under `event.enrichment[name]`, and rules read that. Three questions. If a tenant sets no `enabled`, do they get today's three? If a plugin requires an enricher that is not enabled, or throws, what should happen? Who writes the plugins, and do we trust that code?" 面试官答："Same as today: the three built-ins."；"Fail loudly at startup." 与 "One customer's bug must not take down detection for anyone."；"They're our customers' engineers on a managed deployment … mention it as a risk, but don't build a sandbox today." 默认：缺省全开内置；插件须显式启用；启动期配置错误 `ConfigError`，运行期异常记录 + 计数 + 继续；也可关内置（`enabled` 决定跑哪些）；`requires` 决定顺序；插件是受信任代码 | T2：`Given SEN-437 and this repo: list the decisions I must make, ordered so each depends only on earlier ones. Format: Q<n> — question; → the option you'd pick and why. Look up facts in the code. No code.` |
| 13–16 方案 | 说缝（`EnrichmentService` + `Enricher` + `config.py`），四选一，选 C | "There's already an `Enricher` base class with `name` and `requires`, but the service ignores it and hardcodes three calls. I'll make that base class the plugin contract: built-ins register through it, customer plugins are discovered from a directory in their tenant config, and the tenant enables enrichers by name. A decorator alone means the customer's code has to be imported by us, which is a platform change. Dotted module paths in config depend on `sys.path` and packaging — v2. Entry points or out-of-process plugins don't fit in thirty-five minutes — that's the extension discussion. M1 is built-ins through a registry and `enabled`; M2 is directory discovery; M3 is error isolation." | T3：`Here's my list: reuse Enricher as the contract; registry like register_rule for built-ins; plugin_dirs discovery per tenant, not in the global registry; enabled by name, requires sorts order; ConfigError at startup, count and skip at runtime. What did I miss?` T5：`I think the seam is EnrichmentService.__init__ (existing adapters: GeoIpEnricher, HistoryEnricher, ThreatIntelEnricher behind Enricher). Compare decorator-only registration vs plugin_dirs directory discovery in 5 lines each: fit with existing code, failure isolation, what a customer must do. Recommend one. Don't edit anything.`（方案表：A decorator 注册只用于内置；B 配置写模块路径 v2；C 目录发现 v1；D entry points / 独立进程 / gRPC 作扩展答案）T6：CLAUDE.md 五条规则 |
| 16–30 M1 | 内置走注册表，service 按 `enabled` + `requires` 构建；回归全绿；CLI 演示 `enabled = ["geo"]` | "M1 must keep behaviour identical by default, so the first test is the regression, then one that restricts `enabled`." | T7 红：`Write ONE failing test in tests/test_ingest.py: with settings enabled=["geo"] (via build_settings), EnrichmentService.enrich leaves only "geo" in event.enrichment. Literals only. Run it and show me it fails; don't fix.`（失败原因应是 `build_settings` 不认 `enabled`，不是 import 错误）T7 绿：`Minimal change: ENRICHERS + register_enricher in enrichment/base.py, decorate the three built-ins, add enabled/plugin_dirs to _ALLOWED and EnrichmentSettings, make EnrichmentService build from enabled sorted by requires. Run tests/test_ingest.py.` |
| 30–40 M2、M3 | M2 目录发现；M3 异常隔离与启动期 `ConfigError`；红了走 T8 | "M2 is the actual ask: drop a file, change config, no platform change. M3 is that one bad plugin cannot stop detection." | T7 红：`Write ONE failing test: a tmp_path plugin dir with AsnOwner (name="asn_owner", requires=("geo",)), enabled=["asn_owner","history","threat_intel","geo"]; assert event.enrichment["asn_owner"] == {"owner": "AS64500"} — geo listed last must still run first.` 绿：`Add enrichment/plugins.py discover(plugin_dirs) with importlib.util.spec_from_file_location, skip files starting with _, collect concrete Enricher subclasses defined in that module; raise ConfigError on import failure, missing name or duplicate name.` M3 红/绿：`failing plugin raises RuntimeError; assert "exploding" not in enrichment, "geo" in enrichment, metrics.get("enrichment.error", enricher="exploding") == 1` → `wrap enrich in try/except Exception with log.exception and metrics.incr; skip an enricher whose requires did not run.` |
| ~40 审查 | T10 一轮；收一条拒一条 | "I'd normally run a doubt pass with a fresh reviewer — one round now." | T10 同 claude_playbook。典型发现：① 插件类进了全局 `ENRICHERS`（收：跨租户泄漏，只进该租户 service 的字典）；② 同一路径被两个租户加载时 `sys.modules` 名字冲突（收：模块名带路径哈希）；③ 慢插件无超时（拒：v1 做不完，写进 known gaps）。另盯 T9：它顺手把 `Enricher` 改成 Protocol / 新造 `PluginManager`，当场点名拒绝 |
| 42–45 收尾 | 自己跑证据；写 NOTES.md | "Fresh run: 59 passed. Here's a real plugin through the CLI." | T11：`uv run --with pytest python -m pytest -q`。演示：`/tmp/plugins/asn_owner.py`（`AsnOwner`，`requires = ("geo",)`）+ `config/tenants/acme.toml` 追加 `[enrichment]` `plugin_dirs = ["/tmp/plugins"]` `enabled = ["asn_owner", "history", "threat_intel", "geo"]`；`python3 -m sentinel ingest fixtures/events --tenant acme --db /tmp/t2.db` → `ingested 24 events, 7 alerts`；`GET /events/a-003` 的 enrichment 含 `"asn_owner": {"owner": "AS64504-corp"}` 与 geo/history/threat_intel。`enabled = ["geo"]` → `ingested 24 events, 3 alerts`（只剩 role.grant、mfa.disable、brute-force，impossible_travel/known_bad_ip 静默不触发，不崩）。`enabled = ["geoo", ...]` → `error: unknown enrichers: geoo (available: geo, history, threat_intel)`，退出码 2；`enabled = ["history"]` → `error: enricher 'history' requires 'geo', which is not enabled`。T12 写 NOTES.md |
| 45+ 讲解 | 3–5 min | "Tenants can choose which enrichers run and add their own by dropping a Python file implementing our existing `Enricher` interface into a configured directory — no platform change. Built-ins go through the same registry. Order is resolved from `requires`, so history still runs after geo. A broken plugin is reported at startup; a plugin that throws at runtime is logged, counted and skipped. Known gaps: plugins run in our process with full access, so untrusted code would need a sandbox; no per-plugin timeout; rules don't declare which enrichers they need, so disabling geo silently disables impossible travel — I'd surface that as a config warning next." | — |

### 追问与答（来自 interviewer.md 与真题）
1. "A plugin is slow — 2 s (真题：200 ms) per event?" → 管线吞吐被拖垮。先加单插件耗时指标，再加超时 + 熔断（连续失败/超时后暂停该插件）、按 IP/用户缓存结果、批量接口；慢的移到异步旁路，规则先用已有字段跑。v1 没做，要说明。
2. "Tenant A's plugin loaded into tenant B's state?" → 插件只进启用它的租户 service 的字典，不进全局 `ENRICHERS`；模块名带路径哈希，同路径被多租户加载不冲突；结果只写到该事件上；没启用的租户看不到输出。
3. "A plugin imports a library we don't ship?" → import 失败 = `ConfigError`，带文件名，启动即报，不拖到处理中途。
4. "How can customers test a plugin first?" → 干跑：对样本目录 `sentinel ingest --tenant x`；v2 加 `enrichers` 子命令列出已发现的插件。
5. "Evolve `Enricher` without breaking plugins?" → 只加不改；接口加版本号属性；插件只依赖稳定的、文档化的接口（事件只读视图 + dict 输出）；CI 里用客户插件跑契约测试。
6. "How would you sandbox customer code?" → 进程外：每个插件一个子进程/容器（或 WASM），stdin/stdout 或 gRPC 传 JSON，超时、内存上限、无网络；或不让客户写代码，改成声明式（配置 lookup 表、HTTP 富化 webhook）。
7. "How do rules know an enricher is missing?" → 规则声明 `requires_enrichment = ("geo",)`；启动时校验已启用规则所需的 enricher 都启用，否则报错或告警；运行时缺失则规则跳过并计数。
8. "What's missing?" → 沙箱、超时、热加载（"No. Restart is fine."）、列出/干跑 CLI、接口版本。

- **"Customers can't wait for a restart — can config changes take effect at runtime?"**（PracHub 版题面的 "without requiring redeployment"，见 `REAL_QUESTION.md` 末节）→ 按租户缓存已构建的 `EnrichmentService`，缓存键 = 租户配置文件的 mtime 或内容哈希；每批事件前比对一次（或提供 `POST /admin/reload` / SIGHUP），变了就在旁边构建新实例，**构建成功才原子替换引用**，失败保留旧实例并计数 `enrichment.reload_error`；插件模块按文件内容哈希命名导入，避免 `sys.modules` 里的旧版本被复用。说清代价：正在处理的批次用旧插件集，下一批才生效；多进程部署时每个 worker 各自检测。

### 翻车点
- 提 decorator 模式却不看代码（真题原帖那位）→ 代码里已有未被使用的 `Enricher` 基类；decorator 只能注册我们自己 import 的类，客户代码要进来仍要改平台。
- 新造 `PluginBase` / `PluginManager` / setuptools entry points → 已有 `Enricher`；本仓库不是 pip 安装模型。
- 全局可变 `PLUGINS` 字典 → 租户 A 的插件泄漏给租户 B；已有 `Pipeline._runtime` 每租户一份就是隔离点。
- 按 `enabled` 列表顺序执行 → 忽略 `requires`；客户把 `history` 写在 `geo` 前就坏（验收故意这样写）。
- 信 README "drop a class into the package" → 过时，没有任何发现机制读那个目录。

---

## t3 · alert dedup（SEN-451）

### 题
分析师抱怨队列被重复告警淹没：一个暴力破解源一小时几十条。让队列可用，并让告警显示覆盖了多少事件（`event_count`）。

### 参考答案
- 设计：洪水的根是 `BruteForce` 对每个越线的失败登录都命中一次——这是规则语义，不改（改了治标，其它规则同样会重复）。合并放在 `AlertService.create_from`（唯一创建点，X5）：去重键 = 规则集合 + user + src_ip（租户在查询里），在窗口内找同键的 OPEN 告警，找到就更新 `event_count / last_seen / event_ids / threat_level / score`，否则新建。选项 A：`Pipeline` 里内存 dict（重启丢失、不隔离租户）；选项 B：service 层 + sqlite。选 B。ACKED/CLOSED 不再吸收新事件。窗口来自 `[alerts] dedup_window_minutes`（默认 60，0 = 关闭），`event_ids` 封顶 100，`event_count` 数触发了命中的事件。
- 改动：
  - `sentinel/db/migrations/0003_alert_dedup.sql`：`ALTER TABLE alerts ADD COLUMN event_count/last_seen/dedup_key`，`UPDATE alerts SET last_seen = created_at` 回填，索引 `idx_alerts_dedup (tenant_id, dedup_key, status, last_seen)`。
  - `sentinel/alerts/__init__.py:Alert`：加 `event_count`、`last_seen`、`dedup_key`；`to_dict()` 输出 `event_count`、`last_seen`。
  - `sentinel/alerts/repository.py:AlertRepository.find_open / update_activity`：均带 `tenant_id`，`status = 'OPEN'`，时间用 `iso()`。
  - `sentinel/alerts/service.py:AlertService.create_from / _merge / _open / dedup_key`：合并逻辑；`max(alert.threat_level, level)` 取最高严重度。
  - `sentinel/config.py:AlertSettings.dedup_window_minutes` + `_ALLOWED["alerts"]` + 校验；`config/default.toml` 加 `dedup_window_minutes = 60`。
  - `sentinel/scoring.py:score`：`event_count` 参与（每翻倍 +25%）；`sentinel/pipeline.py:Pipeline.run`：返回创建或更新的告警（每个一次）；`sentinel/cli.py`：`alerts` 输出 `x<count>`。
- 关键测试：
  - `tests/test_detection.py::test_repeats_inside_the_window_merge`：三次（间隔 50 分钟）合并成同一个 id，`event_count == 3`，`threat_level is HIGH`，`repo.count("acme") == 1`。
  - `tests/test_detection.py::test_acked_alert_is_not_reopened_by_new_events`：ack 后新事件开新告警，旧告警 `event_count == 1`。
  - `tests/test_ingest.py::test_fixture_run_produces_expected_alerts`（改过的既有测试）：`(flood,) = by_rule["brute_force"]`，`flood.event_count == 5`——这是该测试的期望本来就该变的地方，要明说。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | 先复现：CLI 跑夹具看洪水；T4 定义 same alert；问 3 个 | "Let me reproduce first: thirteen alerts, eight of them from one IP. So 'same' means what? Three questions. What makes two alerts the same, and over what window? If an analyst already acked it and more events arrive, merge or open new? What does `event_count` count, and do old alerts keep working?" 面试官答："Same customer, same detection, same actor. Use your judgement for what 'actor' is." 与 "An hour is fine. Make it configurable."；"That's new information. They should see it."；"How many events the alert covers." 与 "Don't lose them." 默认：键 = 规则集合 + user + src_ip，滑动窗口 60 分钟；ack 后开新告警；`event_count` = 触发命中的事件数（说出口径）；旧告警回填 1 | T1 复现：`python3 -m sentinel ingest fixtures/events --tenant acme --db /tmp/s.db` → `ingested 24 events, 13 alerts`；T2：`Given SEN-451 and this repo: list the decisions I must make ... No code.` |
| 13–16 方案 | 说缝：`AlertService.create_from`；两方案；选 B | "The flood comes from `BruteForce` hitting on every attempt past the threshold — that's the rule's semantics, other rules repeat too, so I won't change it. `create_from` is the only place alerts are created, so the merge goes there, persisted in sqlite and tenant-scoped; an in-memory dict in the pipeline would vanish on restart. M1 is same key, same window merges and exposes `event_count`." | T3：`Here's my list: merge in AlertService.create_from; key = rules + user + src_ip; sqlite columns via a new migration with backfill; window in [alerts] config; ack stops absorbing. What did I miss?` T5：`I think the seam is AlertService.create_from (existing producers: Pipeline.process only). Compare merging in create_from vs changing BruteForce to fire once, in 5 lines each... Recommend one. Don't edit.` |
| 16–30 M1 | 红 → 绿 → CLI 演示 | "First failing test: three repeats inside the window become one alert with count three." | T7 红：`Write ONE failing test in tests/test_detection.py: AlertService.create_from three times for the same user and src_ip, 50 minutes apart, assert the three results share one id, stored.event_count == 3 and repo.count("acme") == 1. Literals only. Show it fails; don't fix.` 绿：`Minimal change: migration 0003 (event_count, last_seen, dedup_key, backfill), Alert fields, AlertRepository.find_open/update_activity scoped by tenant_id and status='OPEN', merge in AlertService.create_from, Alert.to_dict exposes event_count. Run tests/test_detection.py.` |
| 30–40 M2 | 窗口进配置、ack 语义；既有 fixture 测试期望变红 → T8 | "The existing fixture test now goes red: it expects five brute-force alerts. That expectation is exactly what this ticket changes, so I'm updating it deliberately and telling you." | T7 红：`Write ONE failing test: an ACKED alert is not reopened; the next event opens a new alert and the old one keeps event_count == 1.` 绿：`find_open filters status = 'OPEN'; window from settings.alerts.dedup_window_minutes validated in config.py.` T8（`test_fixture_run_produces_expected_alerts` 变红）：`Reproduce this with one test run showing the exact symptom, then 3 ranked hypotheses with predictions. Don't fix yet.` |
| ~40 审查 | T10 一轮；收一条拒一条 | "One round of doubt, and I'll take one finding and reject one." | T10 同 claude_playbook。典型发现：① 时间字符串格式不一致（`isoformat()` vs `iso()`）导致 sqlite 字典序比较错（收：统一 `iso()`）；② 两个 worker 同时 ingest 同一用户 → 读-改-写竞态，可能重复插入（拒：v1 单进程，写进 known gaps：唯一键或 upsert）。同时检查 AI 有没有悄悄改既有测试的期望而不告诉你 |
| 42–45 收尾 | 自己跑证据；写 NOTES.md | "Fresh run: 59 passed, and the same fixtures through the CLI went from thirteen alerts to seven." | T11：`uv run --with pytest python -m pytest -q`；`python3 -m sentinel ingest fixtures/events --tenant acme --db /tmp/t3.db` → `ingested 24 events, 7 alerts`；`python3 -m sentinel alerts --tenant acme --db /tmp/t3.db` → `HIGH 0.006206 OPEN x5 203.0.113.140 is listed on tor-exit (confidence 0.60)` 与 `x3` 一条（规则集合不同，键不同），其余 `x1`。T12 写 NOTES.md |
| 45+ 讲解 | 3–5 min | "Repeats of the same rules for the same user and source address inside an hour fold into one open alert, with a running `event_count`, last seen time and the highest threat level. Acked alerts are not reopened. Not done: concurrency — two workers could both miss the existing alert and insert twice; I'd add a unique key or an upsert. Also a configurable dedup key, reopening, and splitting a merged alert." | — |

### 追问与答（来自 interviewer.md）
1. "Two workers ingest the same user at once?" → 读-改-写竞态，两边都没找到就都插入。用唯一约束 + `INSERT ... ON CONFLICT` 或 `UPDATE ... WHERE` 在事务内合并。
2. "Events arrive out of order?" → `last_seen = max(last_seen, ts)`；窗口要看事件时间两侧，当前 `find_open` 只往前看。
3. "Roll out without hiding real incidents?" → 按租户 flag，窗口默认保守，先只对 brute-force 开；`dedup_window_minutes = 0` 即关闭。
4. "10x volume: hot query and index?" → `find_open`，由 `idx_alerts_dedup (tenant_id, dedup_key, status, last_seen)` 服务。
5. "Analyst wants the events behind a merged alert?" → `event_ids` + `GET /events/<id>`；`event_ids` 封顶 100，计数照常。
6. "What's missing?" → 重新打开、手动拆分、对 CLOSED 的策略、可配置的去重键。

### 翻车点
- 改 `BruteForce` 只在首次越线命中 → 治标，其它规则的洪水还在，且破坏依赖逐事件命中的下游。
- `Pipeline` 里维护 `dict[(user, ip)] -> alert` → 重启丢失，不隔离租户，多进程不安全。
- 查询漏了 `tenant_id` 或 `status = 'OPEN'` → 跨租户合并 / 被 ack 的告警被复活。
- 悄悄改旧测试期望让它变绿 → 面试官会看 diff；应说明这个期望本来就该变。
