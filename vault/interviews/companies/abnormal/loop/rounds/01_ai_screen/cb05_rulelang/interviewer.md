# interviewer.md · cb05_rulelang（面试官视角）

> 本文件包含答案：只在做完某张 ticket 之后再看那一节（`python3 loop/ai_screen.py reveal cb05 tN`）。
> 面试官开场原话（英文）："This is Rulelang, our detection engine. Pick up this ticket. You can use Claude Code. I'll answer questions, but I won't tell you how to build it."
> 评分原话（官方）：Judgment — "evaluate approaches, scope work into milestones, and decide what fits the existing system"；Agency — "make decisions, state assumptions, test your own work, keep momentum"。
> 本题型是算法型扩展：三张 ticket 各藏一个经典模式（t1 递归下降解析、t2 拓扑排序、t3 带时间约束的 BFS）。AI 写算法本身没有难度；被评的是**认出模式**、**挂在已有抽象上**、**验证 AI 的实现踩没踩边界**。

通用的"契合本系统"清单（三张 ticket 都适用）：

| 约定（`CONTRIBUTING.md`） | 对应落点 |
|---|---|
| 一切按租户隔离 | repository / `CommGraph(conn, tenant_id)` 都带租户；API handler 只用 `req.tenant` |
| 改 schema = 新 migration | `rulelang/store/migrations/NNNN_*.sql`（三张 ticket 的参考解都不需要新表） |
| 配置优于常量 | `config/default.toml` + `rulelang/config.py:_ALLOWED / build_settings`：未知 section/key = `ConfigError`；租户在 `config/tenants/<t>.toml` 覆盖 |
| 新检测 = `Detector` 子类 | `detectors/base.py:Detector / register_detector / DETECTORS`，用 `self.signal(...)` 造 `Signal`，经 `ctx.intel` / `ctx.graph` 读数据 |
| 错误形状统一 | `RulelangError` 子类（`ConfigError`），CLI 打印 `error: ...` 退出码 2；API 抛 `ApiError` 子类 |
| 跳过/吞掉的都要计数+日志 | `rulelang.metrics.incr(...)` |
| 不碰 `rulelang/legacy/` | v0 规则格式（`yaml_rules.py`），半成品，没有人 import |
| 新模块有测试 | 放进匹配的 `tests/test_*.py`；API 经 `TestClient` |

README 只有一处过时：`rulelang/detectors/` 一行写着"detectors run in dependency order (see `Detector.requires`)"——**并没有**。`requires` 字段存在，`vendor_lookalike` 也声明了 `requires = ("new_sender",)`，但 `DetectorRunner` 从不读它；目前的正确性靠 `detectors/__init__.py` 里按字母序 import（`new_sender` 恰好排在 `vendor_lookalike` 前面）。

---

## t1 · custom rules（RUL-208）

### ① 好的 v1 长什么样
候选人读完 `DetectorRunner`、`Detector`、`config.py`，认出这是一个**小型表达式语言**（字段访问、比较、`and/or/not`、括号、`any(...)`、字符串/数字字面量）：tokenizer + 递归下降 parser + evaluator，**不用 `eval`**。规则不是新系统，而是"另一种 detector"：每条 `[rules]` 里的规则在 runner 构造时变成一个 `Detector` 实例，产出与内置检测器同形的 `Signal`，所以 `GET /signals`、`signals` CLI、存储都不用改。字段表（`sender.domain_age_days`、`link.host`、`intel.bad_hosts` …）直接取 `IntelStore` / `Event`；**规则在加载租户配置时就解析并校验**（未知字段、语法错、类型错），错误带规则名和行列号，走 `ConfigError`→CLI 退出码 2，而不是等第一个事件到来时在运行时崩。35 分钟内 M1 = 解析 + 求值 + 接入 runner + 示例规则命中；M2 = 位置信息、未知字段/类型的加载期校验、租户隔离。收尾说得出 known gaps：严重度固定为 medium、只作用于 email、规则之间不能互相依赖、没有规则预览/dry-run。

### ② 澄清问答
| 候选人可能问 | 面试官答（English line） |
|---|---|
| 规则存哪儿？ | "In their tenant config, under `[rules]`, name equals expression. Same files we already have." |
| 规则出错怎么办——运行时跳过还是启动失败？ | "I don't want a customer's typo to silently disable a detection. Tell them when the config loads."（→ 加载期失败，带位置；未问：默认加载期失败） |
| `any(...)` 是什么意思？ | "Any link, or any recipient, satisfying the condition. The example reads: some link points at a bad host."（→ 隐式迭代变量 `link` / `recipient`） |
| 域名年龄未知（intel 里没有）时 `< 7` 算真还是假？ | "Unknown is not young. Don't flag what you can't tell." （→ 未知值不匹配） |
| 规则作用于哪些事件？ | "Email events. Logins and mailbox rules are out of scope for now." |
| 严重度怎么定？ | "Medium for everything in v1. We'll add a knob later." |
| 能不能引用别的检测器的结果？ | "Not in v1." |
| 要不要支持正则、函数、算术？ | "No. Comparisons, boolean logic, `in`, and `any`. Keep the language small." |
| 规则是租户独立的吗？ | "Yes. One customer's rules never run on another customer's events." |
| 能用 Python 的 `eval` 吗？ | "These strings come from customers." （→ 否） |

### ③ 隐藏期望（文件:符号）
- `rulelang/detectors/runner.py:DetectorRunner`：规则变成 `Detector` 实例追加到 runner 的列表；`detectors/base.py:Detector.signal` 造 `Signal`（同形）。
- `rulelang/config.py:_ALLOWED / build_settings / _section`：`[rules]` 是**新 section**，未知 section 是 `ConfigError`——不扩展它，租户文件根本加载不了；规则在这里编译。
- `rulelang/errors.py:ConfigError`：语法错继承它，`cli.py:main` 就会给出 `error: ...` + 退出码 2。
- `rulelang/intel.py:IntelStore`（`ctx.intel`）：`bad_hosts`、`domain_age_days`；`rulelang/addresses.py:host_of / domain_of / is_internal`：字段求值复用，不自己 `urlparse`/`split("@")`。
- `rulelang/metrics.py:incr`（规则求值抛异常时由 runner 已有的 try/except 计数）。
- 不该碰：`rulelang/legacy/yaml_rules.py`（有个现成的 `parse_rule`，看起来像"已经有半个解析器"，但它是 v0 格式、只支持一个比较、没人 import）；README 里 `requires` 那句是 t2 的坑，与本题无关。

### ④ 追问
1. "What if a customer writes 500 rules and we process 10x the event volume?"（→ 规则在加载时编译一次，求值是树遍历；`intel` 读取已缓存；瓶颈是每事件 500 次求值——按事件 kind/字段做预过滤，或把常量子表达式折叠）
2. "How would you roll this out safely?"（→ shadow 模式：规则只记录命中、不产生 signal；按租户开关；先给内部租户）
3. "A customer's rule fires on 40% of mail. How do we protect them?"（→ 命中率监控 + 告警；规则预览：对最近 N 天事件 dry-run；上限）
4. "How do you know the evaluator can't run arbitrary code?"（→ 只有 AST 求值，没有属性访问/调用/`eval`；字段白名单；测试里放 `__import__("os")` 看加载期报错）
5. "What's missing from your v1?"（→ 严重度、其它事件类型、规则间依赖（接 t2 的 `requires`）、字符串转义、行内注释、规则版本/审计）
6. "Someone writes `sender.domain_age_days < \"7\"`. What happens?"（→ 加载期类型检查；若没做就是运行时 `TypeError` 被 runner 吞成 `detector.error`——静默失效）

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 一眼说出"这是 tokenizer + 递归下降 + 求值，不是 `eval`、不是正则"；把规则做成 detector；错误在加载期 | 做出解析器但规则走独立的通道/新配置文件 | 用 `eval`/`ast.literal_eval` 拼，或用 split/regex 硬切 |
| Agency | 先说假设（未知年龄不匹配、email only、固定 medium），M1 先让 ticket 示例规则命中 | 做了但假设没说出口 | 一次性让 AI 生成整套语言，自己读不懂 |
| Fit-the-system | `[rules]` 进 `_ALLOWED`；`ConfigError`；复用 `IntelStore`/`host_of`；`Signal` 同形 | 复用部分，另造了错误类型 | 新 YAML/JSON 规则格式，或扩展 `legacy/yaml_rules.py` |
| Testing | 先写红的示例规则测试；语法/未知字段/类型错各一个；优先级（`and` 比 `or` 紧）有字面量用例 | 只测 happy path | 测试里复述实现（tautological） |
| AI-supervision | 审出 AI 的实现：优先级写反、`any` 里变量泄漏到外层、`None` 比较抛 `TypeError`、字符串字面量转义、位置信息是 0-based 还是 1-based | 发现一两处 | "tests pass" 就收 |
| Communication | 先说再做；收尾列 known gaps 并写 NOTES.md | 讲得清但没写下来 | 沉默 / 讲实现细节不讲用户 |

---

## t2 · detector dependencies（RUL-231）

### ① 好的 v1 长什么样
候选人读 `DetectorRunner` 与 `Detector`，发现 `requires` 字段**已经存在却没人用**，`vendor_lookalike` 靠 `detectors/__init__.py` 的 import 顺序碰巧正确——认出这是**依赖排序问题 = 拓扑排序（Kahn）**，不是"调整 import 顺序"也不是"给每个检测器加优先级数字"。在 `DetectorRunner` 构造时按 `requires` 排序（相同层保持注册顺序，行为不回退）；环和未知依赖是**启动时**的 `ConfigError` 并点名环上的检测器；运行时若上游被租户关闭（`[detectors] disabled`）或抛了异常，下游**跳过并 `metrics.incr` 计数**，而不是拿着缺失的数据去判断；"上游没触发"不是失败，下游照常运行。M1 = 排序 + 环报错；M2 = 跳过与计数、级联跳过。收尾说得出 known gaps：跳过计数没有出现在 CLI 输出里、没有 `detectors --graph`、自定义规则（t1）的依赖声明。

### ② 澄清问答
| 候选人可能问 | 面试官答（English line） |
|---|---|
| "wrong verdicts" 具体指什么？ | "A detector reads another one's signal, and the other one hadn't run yet, so it decided as if nothing had fired." |
| 排序要同时管内置和客户自定义的检测器吗？ | "Anything registered as a detector." |
| 有环怎么办？ | "That's a bug in whoever registered them. I want to know at startup, and which detectors are in the loop." |
| 上游被租户关掉了，下游怎么办？ | "Don't judge on missing data. Skip it, and I want to see that it was skipped."（→ 跳过 + 计数） |
| 上游运行了但没触发，算失败吗？ | "No. 'Didn't fire' is a normal answer."（未问：默认不算失败） |
| 上游抛异常呢？ | "Same as disabled for that event. The other detectors keep going." |
| 依赖了一个不存在的名字？ | "Also a startup error."（未问：默认启动报错，stretch） |
| 要不要保持现有输出顺序/结果不变？ | "Yes. Nothing should change for tenants that don't use `requires`." |
| 要不要做成并行？ | "No." |

### ③ 隐藏期望（文件:符号）
- `rulelang/detectors/base.py:Detector.requires`（已有字段）+ `DETECTORS`（注册表，字典保持注册顺序）：直接读它，不新增 `priority`/`order`/`depends_on`。
- `rulelang/detectors/runner.py:DetectorRunner.__init__ / run`：排序在构造时做（`Pipeline._runtime` 每租户构造一次 → "启动时"）；跳过逻辑在 `run` 里；`ctx.signals`（`DetectorContext`）本来就是下游读上游的通道。
- `rulelang/errors.py:ConfigError`：环、未知依赖。`rulelang/metrics.py:incr`：`detector.skipped`。
- `rulelang/config.py:DetectorSettings.disabled`（已有租户开关）：禁用上游 → 下游跳过。
- 不该碰：`detectors/__init__.py` 的 import 顺序（"把 `new_sender` 排前面"是治标）；`legacy/`；README 那句"already in dependency order"是假的，别信。

### ④ 追问
1. "What if two detectors have no dependency between them — does their order matter?"（→ 稳定排序：同层保持注册顺序，输出不变）
2. "How would you surface skipped detectors to an analyst, not just a counter?"（→ 给事件记一条 `skipped` 痕迹/`GET /signals` 的元信息；或 `signals` CLI 末尾打印）
3. "Where would you catch a cycle introduced by a customer rule?"（→ 同一个地方：runner 构造；规则声明的 `requires` 来自配置，加载期校验）
4. "10x the detectors?"（→ 排序只在构造时做一次；`run` 的开销不变；`missing` 检查是集合查找）
5. "Why not just sort by a priority number?"（→ 数字要人手维护，且不表达"为什么"；`requires` 让错误排列在启动时可检测）
6. "What's missing from your v1?"（→ 条件依赖（"requires one of"）、并行执行、跳过的可观测性、自定义规则的依赖声明）

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 一句话认出"这是依赖图 → 拓扑排序"，并指出 `requires` 已存在；区分"禁用/崩溃（跳过）"与"没触发（照常）" | 做了排序，没有区分三种上游状态 | 改 import 顺序 / 加 priority 数字 / 在下游里 `if "new_sender" not in ctx.signals` 打补丁 |
| Agency | 假设写出口（环=启动错、跳过要计数）；先写"注册顺序倒过来结果不变"的红测试 | 假设没说出口 | 一次性重写 runner |
| Fit-the-system | 复用 `requires`、`DETECTORS`、`ConfigError`、`metrics.incr`、租户 `disabled` | 复用大部分，新增了排序配置 | 新建 `DependencyResolver` 类 + 新配置段 |
| Testing | 倒序注册、三层链、环（断言消息里有每个成员）、禁用上游 + 计数；默认顺序输出回归 | 只测倒序 | 没测环，或测试复述算法 |
| AI-supervision | 审出：环检测只报"有环"不点名；Kahn 里不稳定的同层顺序；被跳过的检测器没有向下级联；入度表漏掉 `disabled` 的检测器 | 发现一处 | 收下 AI 的 `networkx` 依赖或 `graphlib` 之外的重造轮子而不自觉 |
| Communication | 讲清"三种上游状态各怎么处理" | 讲清排序 | 只讲算法 |

> `graphlib.TopologicalSorter` 是标准库，直接可用，也会抛 `CycleError`（带环成员）；接受它，但要核对：同层顺序是否稳定、错误是否被转成 `ConfigError`、"未知依赖"是否被它静默当成新节点。

---

## t3 · blast radius（RUL-244）

### ① 好的 v1 长什么样
候选人读到 `CommGraph`（`neighbors(addr)` 返回出边，边上有 `first_ts`/`last_ts`/`count`）后认出：这是图上的**带时间约束的 BFS**——从被盗账号出发，只沿"在 `since` 之后发生过的联系"走，跳数上限来自租户配置（默认 2），结果要带路径。BFS 而不是 DFS，因为要最短跳数和按层截断；要有 `seen` 集合避免环；**外部域名**（不在 `settings.org.internal_domains`）进名单但不展开。时间约束在两层：边的 `last_ts >= since`（`last_ts` 是最近一次联系，所以满足就说明 `since` 之后至少有一次）；第二跳起要求联系发生在风险到达该人**之后**（用上一条边的 `first_ts` 作到达时间的下界；v1 可以先只做第一层，stretch 才要求时间传递）。入口：`GET /blast-radius`（`@route` + `req.tenant`，参数缺失/时间非法 → `BadRequest`）与 `blast-radius` CLI 子命令；`[blast_radius] max_hops` 进 `config.py:_ALLOWED`。M1 = 默认跳数的 BFS + CLI；M2 = 路径、外部叶子、配置、API。

### ② 澄清问答
| 候选人可能问 | 面试官答（English line） |
|---|---|
| "after the compromise time"含不含 `since` 当刻？ | "At or after."（→ `>=`） |
| 只算被盗账号发出的邮件，还是也算收到的？ | "Who it emailed. People who wrote *to* it aren't at risk because of it." （→ 只走出边） |
| 第二跳要不要求"转发"发生在第一跳收到之后？ | "A forward can't happen before the mail it forwards."（未问：默认只做 `last_ts >= since`；问了就做时间传递，stretch） |
| 外部地址要不要列出来？ | "List them — the SOC needs to call the partner. But we can't see inside their org, so don't go past them." |
| 跳数怎么数？被盗账号本身算几跳？ | "The account is hop zero; people it emailed directly are hop one." |
| 默认 2 跳够吗/能改吗？ | "Default two, per tenant." |
| 同一个人多条路径，列哪条？ | "The shortest is fine." |
| 结果里要不要被盗账号自己？ | "No." |
| 其它租户的账号查得到吗？ | "Never." |

### ③ 隐藏期望（文件:符号）
- `rulelang/graph/comm_graph.py:CommGraph.neighbors / Edge`：整个遍历只用它；**不要**回头扫 `events` 表，也不要另建邻接表。`CommGraph(conn, tenant_id)` 构造时带租户，租户隔离随之而来。
- `rulelang/config.py:_ALLOWED / build_settings`：新增 `[blast_radius] max_hops`（未知 section 默认是 `ConfigError`）；校验范围；`default.toml` 给默认 2。
- `rulelang/config.py:OrgSettings.internal_domains` + `rulelang/addresses.py:is_internal / normalize_address`：判断"外部"和归一化输入地址。
- `rulelang/api/framework.py:route / BadRequest / Request.arg`、`rulelang/api/routes/signals.py`（照着它写 `routes/blast_radius.py` 并在 `routes/__init__.py` import）；`rulelang/timeutil.py:parse_ts`：`since` 解析。
- `rulelang/cli.py:main` 的子命令结构与 `--db / --config-dir`。
- 不该碰/不该照抄：`CommGraph.first_contact`（只有"首次"，看起来像时间过滤的现成工具，其实不是）；`store/events.py:count_emails_from`（窗口计数，不是遍历）；`legacy/`。

### ④ 追问
1. "What if the graph has 100M edges and one hub address emailed everyone?"（→ `neighbors` 是单次索引查询，`max_hops` 限制深度，但 hub 会爆炸：设结果上限/分页；对 hub 节点要不要展开）
2. "Why BFS and not DFS?"（→ 要最短跳数的路径和按层截断；DFS 会先走深路径，`seen` 集合下得到的路径不是最短的）
3. "Two paths reach the same person at different times. Does yours get the right arrival time?"（→ v1 的 `seen` 在第一次访问时固定到达时间；严格解法是按到达时间做最早到达搜索（Dijkstra 式）；只有 `first_ts/last_ts`，精确需要逐封邮件的时间戳）
4. "How would you roll this out / who uses it?"（→ 只读、按租户；先给 SOC 内部；结果落审计）
5. "What does the SOC do with this list?"（→ 隔离/重置凭据/通知；要不要带上联系次数、最近联系时间、是否点击了链接——v2）
6. "What's missing from your v1?"（→ 精确到达时间、结果分页/上限、把转发（`Fwd:`）与普通邮件区分开、`since` 的时区默认、导出）

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 一句话认出"时间约束的 BFS，外部为叶子，`seen` 防环"；说出 `last_ts >= since` 为什么够用、哪里不够 | 做了 BFS，时间约束只在第一层 | 递归 DFS；或每跳都重扫 `events` 表 |
| Agency | 先问"含不含当刻/只走出边/外部要不要列"，假设写下来；M1 先出 CLI 结果 | 假设没说出口 | 在等面试官确认每一个细节 |
| Fit-the-system | `CommGraph.neighbors`、`is_internal`、`@route`/`BadRequest`、`_ALLOWED`、租户构造的图 | 复用了图但自写了外部判断/配置读取 | 新建图/新表/新配置文件，或直接写 SQL |
| Testing | 夹具图画在纸上/注释里；用字面量期望集合；before-since、hop 上限、外部叶子、跨租户各一例 | 只测整体名单 | 期望值由被测代码算出 |
| AI-supervision | 审出：`seen` 放在入队前还是出队后（会重复/漏路径）；`hops == max_hops` 的截断位置；`since` 无时区；路径元组被后续分支共享修改；外部地址被展开 | 发现一两处 | 名单"看着对"就收 |
| Communication | 讲清到达时间的近似与它的局限 | 讲清算法 | 只说"BFS" |

---

## 出题备注（面试官用）

- 三张 ticket 的"模式词"：t1 = "write rules without waiting on us" → 小语言；t2 = "wrong verdicts when one runs before the thing it depends on" → 依赖/拓扑；t3 = "who else is at risk … after the compromise time … who they forwarded it to" → 时间约束图遍历。候选人若说不出模式名，追问 "What kind of problem is this?"。
- 用于判断 AI 实现的"字面量清单"（口头抽查）：t1 `a or b and c` 的结果、`1.5`/`'x'`/`"x"` 字面量、`any(...)` 里变量作用域、`None` 比较、列号从 1 开始；t2 环上的每个名字、同层稳定顺序、"上游没触发"≠"上游失败"；t3 `since` 当刻、`max_hops` 边界（`hops == max_hops` 时不再展开）、外部叶子、入边不算、跨租户。
