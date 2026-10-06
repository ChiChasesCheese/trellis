# REPORT · cb01_sentinel

## Summary

`sentinel`：多租户安全事件处理管线（采集 → 补全 → 规则 → 威胁等级 → 告警 → sqlite → HTTP API），照一手报道的面试代码库形态（LeetCode Discuss #8335187）原创。三张 ticket：t1 规则抑制、t2 enrichment 插件化（starter 里 `EnrichmentService` 是硬编码的）、t3 告警去重。`starter/` 是要打开的 repo，`solution/` 实现全部三张，`acceptance/` 是只走已有入口的隐藏验收。

## 代码库地图（`starter/`）

| 模块 | 一句话 |
|---|---|
| `sentinel/cli.py`, `__main__.py` | `ingest` / `alerts` / `rules` / `serve` 四个子命令 |
| `sentinel/app.py` | 组合根：`create_app()` 返回 db + settings + `Pipeline` + WSGI app |
| `sentinel/pipeline.py` | `Pipeline.run/process`：collect → enrich → rules → threat → alert → store；每租户一份 runtime |
| `sentinel/config.py` | `Settings` dataclass、tomllib 加载 + 租户覆盖深度合并、严格校验（未知键 = `ConfigError`）、`SettingsProvider`、仓库路径常量 |
| `sentinel/models.py`, `errors.py`, `metrics.py`, `timeutil.py` | `SecurityEvent`/`RuleHit`/`ThreatLevel`；异常类型；计数器；UTC 时间与 `sliding_window` |
| `sentinel/scoring.py` | `combine()`（hits → ThreatLevel）、`AssetCatalog`、`score()`（严重度 × 资产重要性 × 时间衰减） |
| `sentinel/collectors/` | `Collector` 基类 + `@register_collector` 注册表；`auth_log`、`endpoint`、`saas_audit`；坏记录计数并跳过 |
| `sentinel/enrichment/` | `Enricher` 抽象基类（`name`/`requires`/`enrich`）；`geo_ip`（含 CIDR 库与 haversine）、`history`、`threat_intel`；`service.py` 里的硬编码 `EnrichmentService`（带 `TODO(platform)`） |
| `sentinel/rules/` | `Rule` 基类 + `@register_rule` 注册表 + `rule_ids()`；5 条规则；`RuleEngine`（单条规则异常被计数、不外抛） |
| `sentinel/alerts/` | `Alert`/`AlertStatus`、`AlertRepository`（sqlite）、`AlertService.create_from` |
| `sentinel/db/` | `connect()`、`migrate()`（`migrations/NNNN_*.sql` 按序应用）、`EventRepository`（所有查询带 `tenant_id`）、`0001_init.sql` |
| `sentinel/api/` | `framework.py`（`ApiError` 家族、`Request`/`Response`、`@route` 注册表、`ApiContext`）、`app.py`（Bearer → tenant、统一错误形状）、`testing.py`（`TestClient`）、`routes/`（`GET /alerts`、`/alerts/<id>`、`POST /alerts/<id>/ack`、`GET /events/<id>`） |
| `sentinel/legacy/static_rules.py` | deprecated 的 v1 规则 DSL（"deny if country == RU"），不在管线里 |
| `config/`, `fixtures/` | `default.toml` + `tenants/{acme,globex}.toml`；事件 jsonl（3 个来源、2 个租户、含坏记录）、geoip/bad_ips/assets/tokens |
| `README.md`, `CONTRIBUTING.md` | 架构概览（**两处过时**：声称 enrichers 可插拔；声称 legacy 仍被执行，另有不存在的 `run` 命令）；团队约定 |

## 规模（命令实测）

| 项 | 值 | 命令 |
|---|---|---|
| starter Python 文件数 | 45 | `find starter -name '*.py' -not -path '*/__pycache__/*' \| wc -l` |
| starter Python 行数（含测试） | 2,425 | `... \| xargs wc -l \| tail -1` |
| starter 全部文件数（含 toml/json/sql/md） | 59 | `find starter -type f -not -path '*/__pycache__/*' \| wc -l` |
| starter 测试 | 44 passed，0.31 s | `cd starter && pytest` |
| solution Python 文件数 / 行数 | 48 / 3,002 | 同上 |
| solution 测试 | 59 passed，0.41 s | `cd solution && pytest` |
| 验收 | 32 passed（solution）；`IMPL=starter -m core`：20 failed，12 deselected；`IMPL=starter -m regression`：6 passed | 见下 |

## 埋点清单（位置 · 正确做法 · AI 不看代码时的典型错法）

### t1 规则抑制
| # | 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|---|
| 1 | 必须复用 | `rules/base.py:RULES/rule_ids()` | 用注册表校验 `rule_id`，非法 → `BadRequest` | 硬编码一份规则名单；或不校验 |
| 2 | 必须复用 | `api/framework.py:route/ApiError/ApiContext` + `routes/__init__.py` | 用 `@route` 注册，抛 `ApiError` 子类，在 `routes/__init__.py` import | 自造路由/手写错误 body；忘了注册 → 404 |
| 3 | 必须复用 | `db/__init__.py:migrate` + `migrations/` | 新 `0002_*.sql`，每条查询带 `tenant_id` | JSON 文件/内存 list；改 `0001_init.sql` |
| 4 | 必须复用 | `pipeline.py:Pipeline.process`（规则与建告警之间的缝） | 在此过滤命中，规则一行不改 | 在每条规则里加 `if suppressed` |
| 5 | 看起来像但不该改 | `legacy/static_rules.py`（"deny if ..."）与 README 的 legacy 架构图 | 不碰 | 扩展旧 DSL 当抑制机制 |
| 6 | 模糊点 | 被抑制的命中：丢弃 vs 存成 SUPPRESSED；能否抑制 CRITICAL / `known_bad_ip` | 问；默认不进队列但留审计 | 不问，直接丢弃且无痕 |

### t2 enrichment 插件
| # | 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|---|
| 1 | 必须复用 | `enrichment/base.py:Enricher`（`name`/`requires`/`enrich`） | 插件就是它的子类；内置三个走同一机制 | 新造 `Plugin` 接口 / entry points |
| 2 | 必须复用 | `rules/base.py:register_rule`、`collectors/base.py:register_collector`（注册表范本） | 为 enrichers 加同风格注册表 | 全局可变 `PLUGINS` 字典，租户间泄漏 |
| 3 | 必须复用 | `config.py`（严格校验 + `SettingsProvider` 每租户）、`pipeline.py:_runtime`（每租户一个 service） | 加 `enabled`/`plugin_dirs` 并校验；在 `_runtime` 里构造即得隔离 | 读环境变量/全局配置；漏掉校验 |
| 4 | 必须复用 | `errors.py:ConfigError`、`metrics.incr`、`Rule.enrichment()`（容忍缺失） | 配置问题启动即 `ConfigError`；运行时异常计数继续 | 异常冒泡，一个插件拖垮管线 |
| 5 | 看起来像但不该改 | README"drop a class in `sentinel/enrichment/`"（过时）；各条规则文件 | 不信 README；不改规则 | 按 README 以为已有发现机制；改规则读插件 |
| 6 | 模糊点 | 缺省 `enabled`；依赖未启用；相对路径基准；插件是否受信 | 问；默认内置全开、缺依赖启动报错、相对仓库根 | 不问，按列表顺序执行 |

### t3 告警去重
| # | 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|---|
| 1 | 必须复用 | `alerts/service.py:AlertService.create_from`（唯一创建点）+ `alerts/repository.py` | 在此合并，持久化在 sqlite | `Pipeline` 里的内存 dict |
| 2 | 必须复用 | `db/migrations/` + `db/__init__.py:migrate` | 新 migration `ADD COLUMN` 并回填 | 手改 `0001_init.sql`；旧行为 NULL |
| 3 | 必须复用 | `config.py:AlertSettings` + `default.toml` | 窗口进配置并校验 | 硬编码常量 |
| 4 | 必须复用 | `scoring.py:score/combine`、`Alert.to_dict()` → `routes/alerts.py` | 用 `ThreatLevel` 取最大；`to_dict` 暴露 `event_count`，路由不用改 | 在路由里手拼字段 |
| 5 | 看起来像但不该改 | `rules/brute_force.py`（逐事件命中是洪水的来源） | 不改规则语义 | 让规则"只命中一次" |
| 6 | 模糊点 | 去重键含哪些字段；ack 后新事件；`event_count` 数什么 | 问；本实现：规则集合+user+src_ip，只合并 OPEN，数触发命中的事件 | 不问；合并进已 ACKED 的告警 |

## 验收测试清单（`grep` 实测）

| ticket | core | stretch | regression | 合计 |
|---|---|---|---|---|
| t1 | 6 | 2 | 3 | 11 |
| t2 | 7 | 2 | 1 | 10 |
| t3 | 7 | 2 | 2 | 11 |

四条验收命令的结果：solution 全绿 32 passed；starter `-m core` 20 failed（全部 core 红）；starter `-m regression` 6 passed；starter 自带测试 44 passed；solution 自带测试 59 passed。测试只用已有入口：`create_app()`、`Pipeline.ingest_dir()`、auth_log jsonl 格式、HTTP API（`TestClient`）、租户配置文件；新名字只有 ticket 点名的（`/suppressions`、`[enrichment] plugin_dirs/enabled`、`event_count`）。

## 每张 ticket 的 solution 改动行数（`diff -ruN`，增 + 删，含新增测试）

| ticket | 总行数 | 其中测试 |
|---|---|---|
| t1 | 221 | 46 |
| t2 | 197 | 48 |
| t3 | 169 | 52 |
| 合计（starter → solution） | 587 | — |
