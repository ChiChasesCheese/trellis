# interviewer.md · cb01_sentinel（面试官视角）

> 本文件包含答案：只在做完某张 ticket 之后再看那一节（`python3 loop/ai_screen.py reveal cb01 tN`）。
> 面试官开场原话（英文）："This is Sentinel, our security-event pipeline. Pick up this ticket. You can use Claude Code. I'll answer questions, but I won't tell you how to build it."
> 评分原话（官方）：Judgment — "evaluate approaches, scope work into milestones, and decide what fits the existing system"；Agency — "make decisions, state assumptions, test your own work, keep momentum"。

通用的"契合本系统"清单（三张 ticket 都适用）：

| 约定（`CONTRIBUTING.md`） | 对应落点 |
|---|---|
| 一切按租户隔离 | repository 方法都带 `tenant_id`；API handler 只用 `request.tenant`，不信 body 里的租户 |
| 改 schema = 新 migration | `sentinel/db/migrations/NNNN_*.sql`，不改 `0001_init.sql`；表带 `tenant_id` 索引 |
| 配置优于常量 | `config/default.toml` + `sentinel/config.py` 校验（未知键 = `ConfigError`）；租户在 `config/tenants/<t>.toml` 覆盖 |
| 错误形状统一 | 抛 `ApiError` 子类（`sentinel/api/framework.py`），不手写错误 body |
| 跳过/吞掉的都要计数+日志 | `sentinel.metrics.incr(...)` |
| 新模块有测试 | 放进 `tests/test_ingest.py` / `test_detection.py` / `test_api.py` |
| 不碰 `sentinel/legacy/` | 冻结的旧 DSL |

---

## t1 · rule suppression（SEN-412）

### ① 好的 v1 长什么样
候选人读完 `Pipeline.process`，意识到"规则命中 → 告警"之间有一个天然的缝：`hits = runtime.rules.evaluate(...)` 之后、`runtime.alerts.create_from(...)` 之前。他在这里插一个 `SuppressionService.apply(event, hits)`，只丢被抑制的命中，不碰任何一条规则，也不碰 `AlertService`。抑制存在 sqlite（新 migration `0002_*`），所有查询带 `tenant_id`；三个端点用 `@route` 注册并在 `routes/__init__.py` 里 import；`rule_id` 用 `rules.rule_ids()` 校验，非法 → `BadRequest`（走已有错误形状）；`match` 是 `{字段路径: 值}`，路径能解析事件字段（`user`、`src_ip`）和 enrichment（`geo.country`）。被抑制的命中留痕（计数器 + 审计表）。收尾时他说得出 known gaps：过期时间、对 CRITICAL 的策略、10 倍量下每个事件都查一次 suppressions 表。35 分钟内能把 M1（只按 `rule_id` 静音，端到端能 demo）做完，M2 才做 `match`。

### ② 澄清问答
| 候选人可能问 | 面试官答（English line） |
|---|---|
| 抑制是按租户的吗？ | "Yes, per customer. One customer's mute must never affect another." |
| 被抑制的命中是丢掉，还是存成一个 SUPPRESSED 告警？ | "I don't want analysts to see them in the queue. But we do need to be able to answer 'why didn't this alert fire?'"（→ 不进告警队列，但留审计痕迹；默认：丢弃 + 计数） |
| `match` 能匹配哪些字段？ | "Event fields and enrichment fields, like the geo country in the example. Keep the shape simple." |
| 多个条件是 AND 还是 OR？ | "AND. If they want OR they create two suppressions."（未问：默认 AND） |
| 能抑制 `known_bad_ip` / CRITICAL 吗？ | "Allow it, but I'd want the customer to know what they're doing." 或者 "Never for critical." —— 面试官随意取一个；**验收不依赖**，重点是候选人是否主动提出这个问题并给出一个有理由的默认 |
| 需要过期时间吗？ | "Nice to have. Not for v1." |
| 要不要对已有告警回溯？ | "No. Only new events." |
| API 返回什么？ | "Whatever fits the other endpoints." |
| 规则 id 写错了怎么办？ | "The API should tell them." |

### ③ 隐藏期望（文件:符号）
- `sentinel/pipeline.py:Pipeline.process`：在 `evaluate` 与 `create_from` 之间过滤（**不要**改每条规则、不要改 `AlertService`）。
- `sentinel/rules/base.py:RULES / rule_ids()`：校验 `rule_id`。
- `sentinel/api/framework.py:route / BadRequest / NotFound / Response.no_content`，`routes/__init__.py` 里注册新模块；handler 里用 `req.tenant`、`req.json()`。
- `sentinel/db/__init__.py:migrate` + 新 migration 文件（不改 `0001_init.sql`）。
- `SecurityEvent.enrichment["geo"]["country"]`（规则读取 enrichment 的同一个入口）作为 `geo.country` 的语义来源。
- `sentinel/metrics.py:incr` 给被抑制的命中计数；日志。
- 不该碰：`sentinel/legacy/static_rules.py`（"deny if country == RU" 看起来就是抑制，但已冻结且不在管线里）；README 里"legacy still evaluated"是过时的。

### ④ 追问
1. "What if one customer has 10,000 suppressions and we process 10x the event volume?"（→ 每个事件查表的代价；按租户缓存 + 写时失效；先按 `rule_id` 索引过滤）
2. "How would you roll this out safely?"（→ 先 shadow 模式：只记录"本来会被抑制"，不真正丢；feature flag / 按租户开启）
3. "A customer suppresses `known_bad_ip` with no conditions. Is that OK?"（→ 策略题：警告 / 禁止 / 要审批；审计留痕）
4. "How does an analyst find out an alert was suppressed?"（→ `suppressed_hits` 审计表 + 一个只读端点；计数器）
5. "What's missing from your v1?"（→ 过期、编辑（PATCH）、CIDR/列表匹配的校验、对 enrichment 键不存在的处理、分页）
6. "Someone creates a suppression whose `match` path never exists. How would you catch that?"

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 提出过滤点在命中之后、建告警之前，并说出为什么不改规则；先问丢弃/存留与 CRITICAL 策略，给出默认并说明 | 想到过滤点，但没讨论策略 | 在每条规则里加 `if suppressed`；或在 `AlertService` 之后再删告警 |
| Agency | 10 分钟内说出 3 条假设；M1 先交 `rule_id` 级静音；主动说"我先不做过期" | 做了但假设没说出口 | 一直在等面试官告诉他怎么做 / 一次性重写 |
| Fit-the-system | 新 migration、`@route`、`ApiError` 子类、`tenant_id` 全部到位；`rule_ids()` 校验 | 大部分到位，漏一两个（如没注册到 `routes/__init__.py` 靠测试发现） | 内存里放个列表；JSON 文件；自造路由/错误体；改了 `0001_init.sql` |
| Testing | 在 `tests/` 里为 service 和 API 各加测试，还跑了 CLI `ingest` 手工验证；覆盖租户隔离 | 只有 happy path 测试 | 没测试或只手测 |
| AI-supervision | 让 Claude 先读 `pipeline.py`、`framework.py`、`CONTRIBUTING.md` 再动手；审 diff 时指出"它又加了个新的错误类" | 接受了大部分输出，事后清理 | 整段粘贴 AI 的通用 Flask 风格实现，引入新依赖/新抽象 |
| Communication | walkthrough 讲清取舍和 known gaps（一句话一个） | 讲了做了什么，没讲没做什么 | 只念代码 |

---

## t2 · enrichment plugins（SEN-437）

### ① 好的 v1 长什么样
候选人在探索阶段就注意到：`enrichment/base.py` 已经有 `Enricher` 抽象基类（`name`、`requires`、`enrich`），但 `EnrichmentService` 把三个内置实现手工 new 出来，还带着 `TODO(platform): make enrichment configurable per tenant`；README 说"enrichers are pluggable"是**过时**的。好的 v1：给 `Enricher` 加一个与 `@register_rule` 同风格的注册表（内置三个用同一机制注册）；新增 `plugins.discover(plugin_dirs)` 用 `importlib` 加载目录里的 `*.py` 并取 `Enricher` 子类；`EnrichmentService` 改为按租户配置 `[enrichment] enabled` 取出类、按 `requires` 做拓扑排序后逐个运行；一个插件抛异常只记录并计数（`metrics.incr`），不拖垮管线；未知名字/缺依赖/循环依赖在构造 service 时抛 `ConfigError`（`Pipeline.ingest_dir` 里提前构造，所以启动即报）；`config.py` 里加两个键并校验类型。插件不进全局注册表（租户隔离）。规则代码一行不改（它们读 `event.enrichment[...]`，且已容忍缺失）。

### ② 澄清问答
| 候选人可能问 | 面试官答 |
|---|---|
| 没写 `enabled` 时跑哪些？ | "Same as today: the three built-ins." （默认：全部内置，插件需显式启用） |
| 插件依赖一个没启用的 enricher 怎么办？ | "Fail loudly at startup. I'd rather they fix the config than debug silently missing data."（也接受"自动启用依赖"，但要说明取舍） |
| 插件抛异常呢？ | "One customer's bug must not take down detection for anyone." |
| 插件是 Python 代码——信任问题？ | "They're our customers' engineers on a managed deployment, not arbitrary tenants. Mention it as a risk, but don't build a sandbox today." |
| `plugin_dirs` 相对路径相对谁？ | "Pick something sensible and tell me."（本实现：相对仓库根，不是 CWD） |
| 不同租户能共享同一个插件目录吗？ | "Sure, but tenants who don't enable it must not see its output." |
| 要热加载吗？ | "No. Restart is fine."（PracHub 版题面强调 "without requiring redeployment"：若面试官改口要运行时生效，答法见 `walkthrough.md` §t2 追问） |
| 禁用 `geo` 后 `impossible_travel` 怎么办？ | "It shouldn't crash. Quietly not firing is fine." |
| 插件的 `name` 和内置重名？ | "Reject it."（`ConfigError`） |

### ③ 隐藏期望
- `sentinel/enrichment/base.py:Enricher`（`name`/`requires`/`enrich`）——**必须复用**，不是另造 `Plugin` 接口。
- 注册表模式照抄 `sentinel/rules/base.py:register_rule` / `collectors/base.py:register_collector`。
- `sentinel/enrichment/service.py:EnrichmentService`：删掉手工 if/else，改成配置驱动；`# TODO(platform)` 就是这张 ticket。
- `sentinel/config.py`：`_ALLOWED["enrichment"]`（严格校验，未知键即错）、`build_settings`、`SettingsProvider` 已按租户缓存；路径解析不依赖 CWD。
- `sentinel/pipeline.py:Pipeline._runtime`：每租户一份 runtime，在这里构造 service 即得到租户隔离。
- `sentinel/errors.py:ConfigError`；`sentinel/metrics.py:incr`。
- `Rule.enrichment(event, name)`：规则读取 enrichment 的唯一入口，已容忍缺失——所以"禁用 geo 不崩"几乎是免费的。
- 不该碰：规则文件；`sentinel/legacy/`；README 那句"drop a class into the package and it is picked up"。

### ④ 追问
1. "What if a plugin is slow — 2 seconds per event?"（→ 超时/线程池/批处理；至少先计时指标；说明 v1 没做）
2. "How do you keep tenant A's plugin from being loaded into tenant B's process state?"（→ 每租户独立模块名与类字典；注意同路径模块名冲突）
3. "A plugin imports a library we don't ship. What happens?"（→ import 失败 = `ConfigError` 启动即报，带文件名）
4. "How would you let customers test a plugin before enabling it?"（→ 干跑 CLI：`sentinel ingest --tenant x` 对样本目录；或 `enrichers` 子命令列出已发现的插件）
5. "How do you evolve the `Enricher` interface without breaking customer plugins?"（→ 版本号属性 / 只加不改 / 适配层）
6. "What's missing?"

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 一开始就问"没配置时默认什么、依赖缺失怎么办"；说出"插件不进全局注册表"的理由 | 做出来了，决策是隐含的 | 先做一个很大的插件框架（生命周期、沙箱、事件总线） |
| Agency | 10 分钟定位到 `EnrichmentService` 与 TODO；先 M1：用配置选择内置 enrichers；再 M2：目录发现；再 M3：错误隔离 | 顺序做完但没分里程碑 | 一头扎进 `importlib` 细节，35 分钟末还没有端到端 |
| Fit-the-system | 复用 `Enricher`、注册表模式、`ConfigError`、`metrics`、`Pipeline._runtime`；`config.py` 校验同步更新 | 复用了 `Enricher`，但在 service 里写死发现逻辑、没走校验 | 新造 `Plugin`/`PluginManager` 基类；改规则去读插件；全局可变注册表 |
| Testing | tmp 目录写插件文件做测试；覆盖排序、异常隔离、未知名字 | 只测发现 | 手测 |
| AI-supervision | 先让 Claude 读 `enrichment/`、`rules/base.py`（找注册表范本）、`config.py`；审出它"顺手把 `Enricher` 改成 Protocol" | 接受输出后再修 | 采用 AI 生成的 setuptools entry-points 方案（本代码库不是包安装模型） |
| Communication | 明确说出"插件是受信任代码，沙箱不在 v1" | 提到安全但没说边界 | 没提 |

---

## t3 · alert dedup（SEN-451）

### ① 好的 v1 长什么样
候选人先复现问题：跑 `python -m sentinel ingest fixtures/events --tenant acme` 看到 dave 的暴力破解一连串告警；追到 `BruteForce` 规则"每个超过阈值的失败登录都命中一次"——这是**规则的语义**，不改它。合并发生在 `AlertService.create_from`（所有告警的唯一创建点）：算一个去重键（租户 + 规则集合 + 用户 + 源 IP），在窗口内找同键的 OPEN 告警，找到就更新 `event_count / last_seen / event_ids / threat_level / score`，找不到才新建。窗口来自 `[alerts] dedup_window_minutes`（`config.py` 校验），新 migration 增列（`event_count`、`last_seen`、`dedup_key`，并给已有行回填），`Alert.to_dict()` 暴露 `event_count`，`AlertRepository` 加查询/更新。ACKED/CLOSED 的告警不再吸收新事件（分析师已处理，新事件开新告警）。

### ② 澄清问答
| 候选人可能问 | 面试官答 |
|---|---|
| "同一个"告警怎么算？ | "Same customer, same detection, same actor. Use your judgement for what 'actor' is." （本实现：规则集合 + user + src_ip） |
| 窗口多长？固定窗口还是滑动？ | "An hour is fine. Make it configurable."（本实现：自上一个事件起的滑动窗口） |
| 分析师 ack 之后又来了事件？ | "That's new information. They should see it."（→ 开新告警） |
| 合并后严重度？ | "Show the worst one." |
| `event_count` 数什么？ | "How many events the alert covers."（本实现：触发了命中的事件数——不含未触发的失败登录；把整串失败登录都算上（12 而非 9）同样说得通，验收两者都接受，关键是**说出你选的口径**） |
| 已存在的旧告警怎么办？ | "Don't lose them."（→ migration 回填 `event_count=1`） |
| 要不要去重所有规则，还是只 brute-force？ | "The queue is the problem, not one rule."（→ 在 `AlertService` 通用实现） |
| 排序要变吗？ | "If it falls out naturally."（stretch：score 随 `event_count` 增长） |
| 事件很多，`event_ids` 会不会爆？ | "Good question."（→ 本实现封顶 100 条，计数照常） |

### ③ 隐藏期望
- `sentinel/alerts/service.py:AlertService.create_from`：唯一创建点，去重在这里，**不要**放进 `Pipeline` 的内存 dict（重启丢失、不隔离租户）。
- `sentinel/alerts/repository.py:AlertRepository`：新增按 `(tenant_id, dedup_key, status, last_seen)` 的查询（带 `tenant_id`！）+ 更新方法。
- 新 migration（`ALTER TABLE ... ADD COLUMN`，回填 `last_seen`）；不改 `0001_init.sql`。
- `sentinel/config.py:AlertSettings` + `_ALLOWED["alerts"]` + 校验；`config/default.toml` 加默认值。
- `sentinel/scoring.py:score`（stretch：`event_count` 参与排序）；`scoring.combine` 复用，取最大严重度用 `ThreatLevel` 的 IntEnum 比较。
- `sentinel/api/routes/alerts.py` 不用改（它直接序列化 `Alert.to_dict()`）——这就是"复用"的信号。
- `sentinel/timeutil.py` 的 UTC aware 时间；时间字符串用 `iso()` 保持同一格式后才能在 sqlite 里字典序比较。
- 不该碰：`sentinel/rules/brute_force.py`（改成"只在第一次越线时命中"会破坏其它依赖逐事件命中的下游，且治标不治本）；`legacy/`。
- 注意 `Pipeline.run` 的返回：现在是"创建或更新的告警（每个一次）"。

### ④ 追问
1. "Two workers ingest events for the same user at the same time. What breaks?"（→ 读-改-写竞态；唯一约束/`UPDATE ... WHERE`、事务、或 `INSERT ... ON CONFLICT`）
2. "What if events arrive out of order — an event older than the alert's `last_seen`?"（→ `max(last_seen, ts)`；窗口两侧）
3. "How would you roll this out without hiding real incidents?"（→ 按租户 flag、窗口默认保守、先只对 brute-force 开）
4. "10x volume: what's the hot query and what index serves it?"（→ `find_open` 与 `idx_alerts_dedup`）
5. "An analyst wants to see the individual events behind a merged alert."（→ `event_ids` + `GET /events/<id>`；封顶问题）
6. "What's missing?"（→ 重新打开、手动拆分、对 `CLOSED` 的策略、可配置的去重键）

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 先复现 + 找到洪水的根（规则逐事件命中）→ 选择在创建点合并而不是改规则；主动问 ack 后怎么办 | 在创建点合并，但没讨论 ack/窗口语义 | 改 `BruteForce` 让它只命中一次；或在 API 层 `GROUP BY` 掩盖 |
| Agency | M1 = 同键同窗口合并并返回 `event_count`；M2 = ack 语义 + 配置；M3 = 排序；每步用 CLI/测试验证 | 一次做完没有里程碑 | 做了过度设计（去重策略插件、规则可配置的键） |
| Fit-the-system | migration、`AlertRepository`、config 校验、`Alert.to_dict()` 一路改全；窗口读 `settings.alerts` | 键和窗口硬编码成常量，"TODO 以后进 config" | 内存 dict；不带 `tenant_id` 的查询；字符串时间戳格式不一致 |
| Testing | 加了窗口边界、不同用户、ack、租户隔离测试；CLI 前后对比 13 → 少数告警 | 只测合并 | 无 |
| AI-supervision | 指出 AI 的实现忘了 `tenant_id` / 没写 migration / 改了现有测试的期望而不告诉他 | 事后发现 | 直接接受 |
| Communication | 讲清"actor"的定义和 ack 的决定，以及未做的竞态 | 只讲实现 | — |
