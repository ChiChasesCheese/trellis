# 真题复刻 · Abnormal AI Screening Round（security-events 代码库）—— 题目、讲解与参考答案

> 来源：LeetCode Discuss #8335187 "Abnormal Ai screening round was a sh*t"（2026-06-15，候选人自述；编排者 2026-10-06 经 `POST leetcode.com/graphql` 重取，逐字核对）。另有 1p3a thread 1181621（2026-06-29，Telegram 镜像摘要）与 PracHub 标题 "Extensible Security-Event Pipeline: Rule Suppression and Plugin-Based Enrichment" 印证同一代码库形态。
> **练法**：`python3 loop/ai_screen.py start cb01 real` —— 拿到的是**接近原话的口述版题目**（不给接口名，和真面试一样模糊）；做完 `check cb01 real <目录>` 跑题②（t2）的隐藏验收（题①另跑 `check cb01 t1`）；`reveal cb01 real` 打印本文件。
> 本库 `starter/` 就是照原帖描述造的代码库：采集 → 富化（geo-ip、history、threat intel，**写死**）→ 规则 → 威胁等级 → 排序 → 告警 → API → DB。

---

## 1. 原帖原文（英文原话 + 中文翻译）

> "They ask you to read a codebase which I skimmed through in like 10 mins and claude (allowed). Then they … again mentioned you still have 3 mins to go through code. I was like - let me understand the question first then I'll deep-dive into specific component … Then he gave me a question after I started acting on it. He said sorry I gave the wrong question and it was still a vague question."

中文：先给你一个代码库读，可以用 Claude，他大概 10 分钟扫完；面试官又说"你还有 3 分钟看代码"；他想先看题再深入；面试官给了题，他开始做之后，面试官说"抱歉给错题了"，换的题依然很模糊。

> "The repo did was - processed all security events like collection/ingestion, ranking, threat levelling based on some rules, created alerts, created apis on top of it and put it to database."

中文：代码库做的是——处理所有安全事件：采集/摄入、排序、基于规则定威胁等级、生成告警、在上面提供 API、存进数据库。

> **题①（面试官说给错了）**："We've to allow users to suppress some rules (it can be complex rules like based on geo-ip (existing in code) and other rules)."

中文：要让用户能**抑制（静音）某些规则**；条件可能很复杂，比如基于 geo-ip（代码里已有）以及其它规则。

> **题②（真正的题）**："The enrichment layer currently hardcodes based on some threats (geo-ip, history, 1 more) clients want more configurability without touching platform code. Implement a plugin based mechanism to ensure no code touching by clients. (On these lines, very vague)"

中文：富化层目前**写死**了几种威胁信息（geo-ip、history，还有一种）；客户想要更多可配置性，而且**不碰平台代码**。实现一个**插件机制**，保证客户不用改我们的代码。（大意如此，非常模糊）

> "After 20 mins of struggling and explaning them how can we add decorator pattern and clients can choose which threats they want to use/avoid etc I resorted to claude to code it completely for me. I'll mostly get a No."

中文：他花了 20 分钟挣扎、口头解释"可以加 decorator 模式、让客户选择用哪些威胁信息"，最后让 Claude 全部代写。自评大概率挂。

### 他哪里做错了（对照官方评分）

| 官方要的 | 他做的 | 应该做的 |
|---|---|---|
| Agency：做决定、说假设、保持推进 | 20 分钟停在口头讨论 | 2–3 个澄清问题后**当场定下假设**，5 分钟内开始写 M1 |
| Judgment：契合现有系统 | 提 decorator 模式（通用答案，没先看代码里有什么） | 先发现代码里**已有一个没被用起来的 `Enricher` 基类**，让它成为插件契约 |
| "AI is a resource you supervise" | 最后让 Claude 全写 | 让 Claude 先找已有模式，再按你定的方案写，你审 diff |
| "ship a working v1" | 没有能跑的东西 | 第 30 分钟前通过 CLI 演示：插件文件丢进目录 → 配置启用 → 事件上出现新字段 |
| 模糊性被评分 | 抱怨题目模糊 | 模糊是考点：把模糊拆成决策点，逐个说"我选 X，因为 Y，可配置/可改" |

另外：题①被收回不代表白做——面试官很可能在后面的扩展讨论里追问它。两题都要会。

---

## 2. 题②（插件化富化）讲解与参考答案

### 2.1 读代码时必须看到的三件事

1. `sentinel/enrichment/service.py`：`EnrichmentService.enrich()` 用 if/else **按固定顺序**调用 geo、history、threat_intel 三个富化器；注释写着 `TODO(platform): this should be driven by config, per tenant`，还说明 **history 依赖 geo 先跑**。
2. `sentinel/enrichment/base.py`：已经有 `Enricher` 抽象基类——`name`（结果存到 `event.enrichment[name]`）、`requires`（依赖哪些富化器）、`enrich(event, ctx) -> dict`。**这个接口存在，但 service 没用它做发现**。这就是题目说的"hardcode"。
3. `sentinel/config.py` + `config/default.toml` + `config/tenants/<tenant>.toml`：已有**按租户覆盖、严格校验**的 TOML 配置。"客户可配置"就应该落在这里，而不是新建一个 JSON 文件。

### 2.2 澄清问题（问 2–3 个，没答案就用括号里的默认）

1. "Who writes the plugins — customers' own engineers, or our solutions team on their behalf? Do we trust that code?"（默认：客户提供的 Python 文件，与平台同进程运行；沙箱化列为 known gap）
2. "Should customers also be able to turn off our built-in enrichers, or only add new ones?"（默认：都可以——启用列表决定跑哪些，内置的也走同一机制）
3. "If a customer plugin throws, should that event fail, or should we skip that enricher and keep going?"（默认：跳过 + 记日志 + 计数；安全管线不能因为一个客户插件停摆）
4. （可选）"Can one enricher depend on another's output, like history depends on geo today?"（默认：可以，用已有的 `requires` 声明，按依赖排序）

### 2.3 方案对比（说出口，然后选）

| 方案 | 优点 | 缺点 | 结论 |
|---|---|---|---|
| A. decorator 注册（`@register_enricher`），客户 import 我们的包 | 简单 | 客户代码要被 import 进平台才能注册——谁来 import？还是要改平台代码 | 只用于**内置**富化器 |
| B. 配置里写模块路径（`"acme_plugins.asn:AsnEnricher"`） | 精确 | 依赖 `sys.path`、打包与部署 | 可行，v2 再考虑 |
| C. **目录发现**：租户配置给出 `plugin_dirs`，加载目录下每个 `.py`，找出 `Enricher` 的具体子类；`enabled = [...]` 按名字启用 | 客户只需"丢文件 + 改配置"，**零平台代码改动**；复用已有基类 | 要处理加载错误、重名、依赖顺序 | **v1 选它** |
| D. entry points / 独立进程 / gRPC 插件 | 隔离好 | 35 分钟做不完 | 作为扩展讨论的答案 |

口播（英文）：
> "There's already an `Enricher` base class with `name` and `requires`, but the service ignores it and hardcodes three calls. I'll make that base class the plugin contract: built-ins register through it, customer plugins are discovered from a directory in their tenant config, and the tenant enables enrichers by name. That way a customer never touches platform code — they drop a file and change config."

中文：代码里已经有带 `name` 和 `requires` 的 `Enricher` 基类，但 service 没用它、写死了三个调用。我把这个基类当作插件契约：内置富化器通过它注册，客户插件从租户配置里的目录被发现，租户按名字启用。这样客户永远不用改平台代码——放一个文件、改一下配置就行。

### 2.4 里程碑

- **M1（≤ 15 min，可演示）**：内置三个富化器改为注册表（`ENRICHERS` + `register_enricher`）；`EnrichmentService` 按租户配置 `enabled` 列表构建，按 `requires` 拓扑排序。行为与原来完全一致（回归测试全绿）。
- **M2**：`plugin_dirs` 目录发现（`importlib` 加载 `.py`，收集 `Enricher` 具体子类）；重名、缺 `name`、导入失败 → 启动时报 `ConfigError`（已有错误类型）；未知名字 → `ConfigError`。
- **M3**：运行时容错：某个富化器抛异常 → 记日志 + `metrics.incr("enrichment.error")` + 跳过；依赖没跑成的富化器 → 跳过并计数。规则读 `event.enrichment[...]` 的方式不变。

### 2.5 参考实现要点（`solution/` 里对应文件）

- `sentinel/enrichment/base.py`：新增 `ENRICHERS: dict[str, type[Enricher]]` 与 `register_enricher`；三个内置类加 `@register_enricher`。
- `sentinel/enrichment/plugins.py`：`discover(plugin_dirs)` —— 遍历目录里每个不以 `_` 开头的 `.py`，用 `importlib.util.spec_from_file_location` 加载（模块名带路径哈希防冲突），收集"定义在该模块里、非抽象、是 `Enricher` 子类"的类；导入失败、缺 `name`、与内置或其它插件重名都抛 `ConfigError`。
- `sentinel/enrichment/service.py`：`resolve_order(names, available)` 做拓扑排序（检测循环依赖、依赖未启用都报 `ConfigError`）；`enrich()` 逐个运行，依赖缺失则跳过并计数，异常则记录并计数，**永不让单个插件拖垮管线**。
- `sentinel/config.py` + `config/default.toml`：`[enrichment]` 段新增 `plugin_dirs`（路径列表）与 `enabled`（名字列表，缺省 = 全部内置），沿用已有的严格校验。
- `sentinel/pipeline.py`：`ingest_dir` 先构建租户 runtime，**配置错误在启动时就暴露**，而不是处理到一半才炸。
- 测试：内置顺序不变（回归）· 插件结果出现在 `event.enrichment` · 未启用不出现 · 插件依赖 geo 时顺序正确 · 插件抛异常其余照常 · 未知名字报错 · 禁用 geo 后 `impossible_travel` 不触发且不崩。

### 2.6 收尾 walkthrough（英文口播 + 中文意思）

> "What I shipped: tenants can choose which enrichers run and add their own by dropping a Python file implementing our existing `Enricher` interface into a configured directory — no platform change. Built-ins go through the same registry. Order is resolved from `requires`, so history still runs after geo. A broken plugin is reported at startup; a plugin that throws at runtime is logged, counted and skipped, so one customer's bug can't stop detection. Known gaps: plugins run in our process with full access — for untrusted code I'd move them out of process or into a sandbox; there's no per-plugin timeout yet; and rules don't declare which enrichers they need, so disabling geo silently disables impossible travel — I'd surface that as a config warning next."

中文：做了什么——租户可以选择跑哪些富化器，并且通过"把实现了已有 `Enricher` 接口的 Python 文件放进配置的目录"来添加自己的，平台不用改。内置的也走同一个注册表。顺序由 `requires` 决定，所以 history 仍在 geo 之后。坏插件在启动时报错；运行时抛异常的插件被记录、计数、跳过，一个客户的 bug 不会让检测停摆。已知缺口：插件在我们进程里、权限完整——对不可信代码应移到进程外或沙箱；还没有单插件超时；规则没有声明自己依赖哪些富化器，所以关掉 geo 会**静默**让 impossible travel 失效——下一步把这种情况做成配置告警。

### 2.7 扩展讨论（面试官追问 → 中文参考答案）

1. **"How would you sandbox customer code?"** → 进程外执行：每个插件一个子进程/容器（或 WASM），通过 stdin/stdout 或 gRPC 传 JSON；超时、内存上限、无网络；或者干脆不让客户写代码，改成声明式（配置 lookup 表、HTTP 富化 webhook）。
2. **"A plugin is slow — 200 ms per event. What happens?"** → 管线吞吐直接被拖垮。加单插件超时 + 熔断（连续失败/超时后暂停该插件）、结果缓存（按 IP/用户）、批量接口；把慢的富化移到异步旁路，规则先用已有字段跑。
3. **"How do rules know an enricher is missing?"** → 规则声明 `requires_enrichment = ("geo",)`；启动时校验"启用的规则所需的富化器都启用了"，否则报错或告警；运行时缺失则规则跳过并计数。
4. **"Versioning — a customer's plugin breaks after we change `SecurityEvent`."** → 插件只依赖稳定的、文档化的接口（只读事件视图 + dict 输出）；接口加版本号；CI 里用客户插件跑契约测试。
5. **"Multi-tenant isolation?"** → 插件只对配置了它的租户加载与运行；模块名带租户/路径前缀防止冲突；结果只写到该事件上。

---

## 3. 题①（规则抑制）讲解与参考答案

### 3.1 关键观察

规则由 `@register_rule` 注册，各自返回 `RuleHit`；`Pipeline.process` 里先 `rules.evaluate` 再 `alerts.create_from`。**抑制是跨规则的策略决策**，应该插在"规则命中之后、建告警之前"这一个点上，而不是改每一条规则。geo 信息在 `event.enrichment["geo"]` 里，条件可以直接引用它。

### 3.2 澄清问题

1. "When a hit is suppressed, should it disappear, or be recorded so we can explain why no alert fired?"（默认：不进告警队列，但写审计表 + 计数——安全产品必须能解释"为什么没报"）
2. "Can customers suppress anything — including known-bad-IP or critical hits?"（默认：v1 允许，把"关键规则需要护栏/审批"列为 known gap；问出来本身就是判断力的证据）
3. "What can a condition match on — event fields plus enrichment like `geo.country`? ANDed? IP ranges?"（默认：点路径 `user`、`src_ip`（支持 CIDR）、`attrs.*`、`<富化器名>.<字段>`；多个条件 AND；列表 = 任一）

### 3.3 参考实现要点（`solution/`）

- 新 migration `0002_suppressions.sql`：`suppressions(id, tenant_id, rule_id, match JSON, created_at)` + 审计表 `suppressed_hits`（**不改已有 migration**）。
- `sentinel/suppressions.py`：`SuppressionRepository`（所有查询带 `tenant_id`）+ `matches()`（点路径解析，进 enrichment；CIDR 用 `ipaddress`）+ `SuppressionService.apply(event, hits)`：过滤命中，被抑制的记审计、计数。
- `sentinel/pipeline.py`：在 `rules.evaluate` 之后加一行 `hits = runtime.suppressions.apply(event, hits)`。
- API `sentinel/api/routes/suppressions.py`：`POST/GET/DELETE /suppressions`，走已有的 `@route`、认证（token → 租户）与统一错误形状；`rule_id` 必须是已注册规则，否则 400。
- 测试：抑制后不产生告警 · 其他租户不受影响 · 条件不匹配的同规则事件仍告警 · 只给 `rule_id` 即整条静音 · 非法 rule_id → 400 · 删除后恢复。

### 3.4 口播（英文 + 中文）

> "Suppression is a policy decision across rules, so I'm putting it in one place — after rules fire and before alerts are created — instead of touching every rule. Conditions are dotted paths into the event, including enrichment like `geo.country`, so the geo-ip case from the ticket is just `{"geo.country": "DE"}`. Suppressed hits are audited, because a security product has to be able to say why it didn't alert."

中文：抑制是跨规则的策略决定，所以放在一个地方——规则命中之后、建告警之前——而不是改每条规则。条件是指向事件的点路径，包括 `geo.country` 这样的富化字段，所以 ticket 里的 geo-ip 场景就是 `{"geo.country": "DE"}`。被抑制的命中要审计，因为安全产品必须能说清楚"为什么没报警"。

### 3.5 扩展追问

1. **"Suppressions that never expire are dangerous."** → 加 `expires_at`；默认 30/90 天；到期前提醒；列表显示"最近 7 天吞掉了多少命中"。
2. **"An attacker who compromises an admin account adds a suppression."** → 抑制本身是高危操作：审计日志、通知其他管理员、关键规则需要双人审批、不能抑制 known-bad-IP。
3. **"10,000 suppressions per tenant."** → 按 `rule_id` 建索引，进程内缓存按租户分组的抑制列表（变更时失效），匹配时只看该规则的抑制。
4. **"Suppress by more complex logic (time of day, combos)."** → v2 引入小型条件 DSL 或复用规则引擎的表达式；先观察客户真实需求再做。

---

## 4. 60 分钟怎么分配（按这道题）

| 分钟 | 做什么 |
|---|---|
| 0–8 | E1–E3 探索提示词；自己看 `enrichment/service.py`、`base.py`、`config.py`、`pipeline.py` |
| 8–10 | 心智模型口播（`walkthrough.md` ① 末尾那段） |
| 10–13 | 面试官可能先给题①再改口给题②：**不慌**，"Got it — so the real ask is configurable enrichment. Can I ask three quick questions?" |
| 13–16 | 方案对比 + 选 C + M1/M2/M3 + 假设 |
| 16–30 | M1 → 跑测试 → CLI 演示行为不变；M2 → 写一个 `asn_owner` 插件演示 |
| 30–42 | M3 容错 + 测试 |
| 42–45 | 全量测试、`git diff --stat` |
| 45–60 | walkthrough（§2.6）+ 扩展讨论（§2.7）+ 题①的设计口头说一遍（§3.4）+ 反问 |
