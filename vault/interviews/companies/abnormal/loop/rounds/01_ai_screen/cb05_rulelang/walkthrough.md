# cb05 · 逐场脚本
> Rulelang：多租户检测引擎（事件 jsonl → `Detector` 注册表 → `Signal` → sqlite；`CommGraph` 记录谁给谁发过邮件；WSGI API）· t1 客户自定义规则（RUL-208，小语言：tokenizer + 递归下降）· t2 检测器依赖（RUL-231，拓扑排序）· t3 被盗账号影响面（RUL-244，带时间约束的 BFS）· 练：`python3 loop/ai_screen.py start cb05 <t>` · 面试官视角：`interviewer.md`
> T/X 编号见 `../claude_playbook.md`；英文口播模板见 `../playbook.md` §5。每次模拟 = 探索 + 一张 ticket，都从 `starter/` 开始。本题型的考点：**认出模式**（说出模式名）→ **挂在已有抽象上** → **核对 AI 实现的边界字面量**。

## 0. 探索（0–10 min，三个 ticket 通用）
- 先打开：
  - `CONTRIBUTING.md`：租户隔离、schema = migration、配置优于常量、新检测 = `Detector`、`RulelangError`/`ApiError`、`metrics.incr`、不碰 `legacy/`、测试放进已有文件= 评分的"契合"清单。
  - `rulelang/detectors/base.py:Detector / DETECTORS / register_detector / DetectorContext`：检测器接口（`name`、`kinds`、**`requires`**、`evaluate`）与 `ctx.signals`（同一事件上游检测器的结果）。t1/t2 的缝。
  - `rulelang/detectors/runner.py:DetectorRunner.__init__ / run`：按 `DETECTORS` 注册顺序实例化并逐个运行；**不读 `requires`**。t1（追加规则实例）与 t2（排序/跳过）都改这里。
  - `rulelang/graph/comm_graph.py:CommGraph.neighbors / first_contact / record` + `Edge`：有向边，带 `first_ts`/`last_ts`/`count`。t3 的全部输入。
  - `rulelang/config.py:_ALLOWED / build_settings`：未知 section/key = `ConfigError`；租户在 `config/tenants/<t>.toml` 覆盖。t1 的 `[rules]` 与 t3 的 `[blast_radius]` 都要先在这里登记。
- T1 结果应包含：
  - 入口：`python -m rulelang {run,signals,detectors,serve}`（`rulelang/cli.py:main`，`--db / --config-dir / --fixtures-dir`）；`rulelang/app.py:create_app` 是组合根；API 用 `@route`（`api/framework.py`）注册，handler 放 `api/routes/`，在 `routes/__init__.py` import 才生效。
  - 数据流：`events/loader.py:load_events`（坏行计数后跳过）→ `Pipeline.process`：`runner.run(event)`（检测）→ `events.add` + `graph.record`（检测**之后**才入库/入图，所以"首次联系"只看更早的事件）→ `signals.add_many` → `GET /signals`。
  - 扩展点：`@register_detector`；`ctx.intel`（`IntelStore`：`bad_hosts`/`domain_age_days`/`vendors`）；`[detectors] disabled` 租户开关；`@route`；`config.py`；`store/migrations/NNNN_*.sql`。
  - 过时/噪音：README 称 "detectors run in dependency order"（假：`DetectorRunner` 不读 `requires`，`vendor_lookalike` 靠 `detectors/__init__.py` 的字母序 import 碰巧正确）；`rulelang/legacy/yaml_rules.py` 是冻结的 v0 规则格式（半个 parser，没人 import）。
  - 测试：`uv run --with pytest python -m pytest -q`（starter 39 个，约 0.1 s）；单文件 `python -m pytest -q tests/test_detectors.py`。CLI 基线：`python3 -m rulelang run fixtures/events --tenant acme --db /tmp/r.db` → `processed 23 events, 10 signals (3 bad records skipped)`。
- 心智模型（60 s，英文原句）："Events — email, login, mailbox rule — are loaded per tenant and each one goes through a runner that instantiates every registered `Detector` and calls `evaluate`. A detector can read `ctx.intel`, the communication graph, and the signals other detectors already raised for the same event. Signals go to sqlite and out through `GET /signals`. The `Detector` base class already has a `requires` field, but the runner never reads it — the README says detectors run in dependency order, and they don't; `vendor_lookalike` works because of import order. Config is strictly validated TOML with per-tenant overrides, errors are `RulelangError` subclasses and the CLI exits 2 on them, anything skipped is counted with `metrics.incr`. `legacy/` is a dead rule format. The natural seams are: the runner's detector list, the config loader, and `CommGraph.neighbors`."

---

## t1 · custom rules（RUL-208）

### 题
客户想自己写检测规则，例：`sender.domain_age_days < 7 and any(link.host in intel.bad_hosts)`。规则写在租户配置 `[rules]` 下（`<name> = "<expression>"`），命中时要和别的检测一样出现在该事件的 signals 里。

### 参考答案
- 设计：这是一门小语言：tokenizer + 递归下降 parser（优先级 `or` < `and` < `not` < 比较 < 原子）+ 树遍历求值，不用 `eval`（X5，T5）。规则不是新系统，是"另一种 detector"：选项 A：新建规则引擎 + 新配置文件/新结果通道（YAML/JSON）；选项 B：每条规则编译成 `CustomRuleDetector`，runner 把它们追加进检测器列表，`Signal` 同形，存储/API/CLI 零改动。选 B。规则在 `build_settings` 里编译，所以语法错、未知字段、类型错在**租户配置加载时**就以 `ConfigError`（带规则名与行列号）报出，CLI 退出码 2。字段表 `FIELDS` 是白名单，`any(...)` 的迭代变量（`link`/`recipient`）在加载期确定；未知值（域名年龄查不到）一律不匹配。
- 改动：
  - `rulelang/rules/parser.py:tokenize / _Parser / RuleSyntaxError`：词法（`<=` 在 `<` 之前匹配）、文法（`or_ → and_ → not_ → compare → atom`）、1-based 行列号。
  - `rulelang/rules/fields.py:FIELDS / Scope / LOOP_ITEMS`：字段 → 类型 + 取值函数（`sender.domain_age_days` 走 `IntelStore.domain_age_days`，`link.host` 走 `addresses.host_of`，`intel.bad_hosts` 走 `IntelStore.bad_hosts`）。
  - `rulelang/rules/compiler.py:compile_rule / _check / _eval`：加载期类型检查（未知字段、`<` 只比数字、`any` 恰好一个迭代变量、整条规则必须是布尔），求值时 `None` 不匹配。
  - `rulelang/rules/detector.py:CustomRuleDetector`：`Detector` 子类，`kinds = ("email",)`，命中产出 MEDIUM `Signal`，`evidence["expression"]` 留原文。
  - `rulelang/config.py:build_settings / Settings.rules`：`[rules]` 登记并编译；规则名 `^[a-z][a-z0-9_]*$`。
  - `rulelang/detectors/runner.py:DetectorRunner.__init__`：追加 `CustomRuleDetector`；与内置同名 → `ConfigError`。
- 关键测试：
  - `tests/test_rules.py::test_ticket_rule_matches_young_sender_with_bad_link`：ticket 示例规则对（年轻域名 + 坏链接）命中，老域名/干净链接不命中。
  - `tests/test_rules.py::test_load_time_errors_carry_rule_name_and_position`：9 种错误各带规则名与列号（如 `sender.domain == == "x"` → 第 18 列）。
  - `tests/test_rules.py::test_custom_rule_signal_has_the_builtin_shape`：自定义 signal 的键集合与内置一致。
  - `tests/test_cli.py::test_syntax_error_in_a_tenant_rule_exits_2`：退出码 2、stderr 含规则名与 `column 12`。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | 复述 ticket，T4 定义 "rule"；T2 后只问 3 个 | "So a customer rule is a boolean expression over an email event that produces a signal like any detector. Three questions. When a rule is malformed, do we fail at config load or skip it at runtime? What does an unknown domain age mean for `< 7`? Which events do rules apply to?" 面试官答："I don't want a customer's typo to silently disable a detection."；"Unknown is not young."；"Email events." 默认：加载期失败；未知不匹配；只 email；严重度固定 medium | T2：`Given RUL-208 and this repo: list the decisions I must make, ordered so each depends only on earlier ones. Format: Q<n> — question; → the option you'd pick and why. Look up facts in the code. No code.` |
| 13–16 方案 | 说模式、缝、两方案、里程碑 | **模式**："This is a small language: tokenizer, recursive-descent parser, tree-walking evaluator — and not `eval`, because these strings come from customers." **缝**：`DetectorRunner.__init__` 的检测器列表 + `config.py:build_settings`。选项 A 新引擎/新文件格式，B 规则 = `Detector` 实例；选 B。**核对 AI 的实现**：`a or b and c` 的字面结果、`<=` 是否被切成 `<` 和 `=`、`any(...)` 里 `link` 在括号外是否报错、`None` 比较、列号 1-based、字符串里的转义引号。M1 = 示例规则端到端命中；M2 = 优先级/`not`/括号、位置信息、未知字段 | T3：`Here's my list: grammar = or/and/not/compare/any/in with number and string literals; field whitelist resolved at load; rule = Detector instance appended in DetectorRunner; [rules] registered in config._ALLOWED; errors = ConfigError with line/column; unknown value never matches. What did I miss? Add only what's missing, ranked by user impact.` T5：`I think the seam is DetectorRunner.__init__ plus config.build_settings (existing adapters: six registered Detector classes). Compare a separate rule engine with its own result path vs rules as Detector instances in 5 lines each: fit with existing code, failure isolation, what a customer must do. Recommend one. Don't edit.` T6：五条规则写进 `CLAUDE.md`，加一条 `Do not touch rulelang/legacy; no eval/exec/ast.literal_eval.` |
| 16–30 M1 | plan mode → 审计划 → 红 → 绿 → 真实入口 | "First failing test: the ticket's own rule flags a young sender with a bad link. Then the smallest grammar that passes." | T7 红：`Write ONE failing test in tests/test_rules.py: a tenant config with [rules] young_bad_link = "sender.domain_age_days < 7 and any(link.host in intel.bad_hosts)"; process an email from bob@fresh-supplier.example linking https://login-secure.evil-payments.example/pay through app.pipeline.process and assert "young_bad_link" is among the signal detector names. Literals only. Run it and show me it fails. Don't fix.`（失败原因应是 `ConfigError: unknown config sections: rules`，不是 import 错误）T7 绿：`Minimal change to make that test pass: tokenizer + recursive-descent parser for comparison, 'and', any(...) and 'in'; a field table over Event and IntelStore; register [rules] in config.py; CustomRuleDetector appended in DetectorRunner. No eval. Nothing else. Run that test file.` |
| 30–40 M2 | `or`/`not`/括号 + 加载期报错；红了走 T8 | "M2 is what a customer actually hits: a typo. Errors must name the rule and the column at config load, and `a or b and c` must bind the way people expect." | T7 红：`Write ONE failing test: sender.domain == "fresh-supplier.example" or sender.domain == "oldcorp.example" and subject == "Invoice" matches an oldcorp email with subject "Hello"? -> no; a fresh-supplier email with subject "Hello" -> yes. Literals only.` 再一个：`rule 'broken' with source 'sender.domain == == "x"' raises ConfigError whose message contains 'broken' and 'column 18'.` 绿：`Implement precedence or < and < not < comparison; check field names and operand types when the rule is compiled; carry 1-based line/column in RuleSyntaxError(ConfigError).` |
| ~40 审查 | T10 一轮，收一条拒一条 | "I'd normally run a doubt pass with a fresh reviewer — one round now. I'll take the precedence finding and reject the severity knob, and here is why." | T10：`Adversarial review of the current diff against RUL-208. Assume the author is overconfident. Look for unstated assumptions, unhandled edge cases, broken conventions, failure modes under bad input. Do NOT validate or summarize. Max 5 issues, ranked.` 典型发现：① `a or b and c` 被当成左结合同级（或 `None < 7` 抛 `TypeError`，被 runner 吞成 `detector.error`，规则静默失效）→ **收**：加字面量测试、`None` 不匹配；② 给每条规则加 `severity` 配置键 → **拒**：v1 固定 medium，写进 known gaps |
| 42–45 收尾 | 自己跑证据；写 NOTES.md | "Fresh run: 69 passed. Here's the real output through the CLI." | T11：`uv run --with pytest python -m pytest -q`；在租户配置加规则后 `python3 -m rulelang run fixtures/events --tenant acme --db /tmp/t1.db` → `processed 23 events, 11 signals (3 bad records skipped)`（比基线多 1 个）；`python3 -m rulelang signals a-010 --tenant acme --db /tmp/t1.db` → `low      new_sender …` / `high     suspicious_link …` / `medium   young_bad_link             custom rule young_bad_link matched`；删掉右括号后 `run` → `error: rule 'young_bad_link': expected ')', found end of rule (line 1, column 64)`，退出码 2；写错字段 → `error: rule 'young_bad_link': unknown field 'sender.domain_age' (line 1, column 1)`。T12：`NOTES.md`：assumptions + known gaps + v2 |
| 45+ 讲解 | 3–5 min，`playbook.md` §5.3 | "v1 is a small expression language — comparisons, and/or/not, parentheses, `in`, `any` — compiled when the tenant config loads and run as ordinary detectors, so signals, storage and the API are unchanged. Errors name the rule and the column and exit 2. Not done: per-rule severity, non-email events, rules depending on other detectors, a dry-run against recent mail." | — |

### 追问与答（来自 interviewer.md 的追问）
1. "500 rules, 10x volume?" → 规则在加载期编译一次，求值是树遍历，intel 读取已缓存；瓶颈是每事件 500 次求值。按事件字段预过滤（先求值便宜的子表达式）、常量折叠，或按 `kind` 分桶。
2. "Roll out safely?" → shadow 模式：规则命中只计数不产出 signal；按租户开关；先给内部租户；对最近 N 天事件 dry-run 预览命中率。
3. "A rule fires on 40% of mail?" → 命中率监控 + 告警，单规则命中上限，超限自动转 shadow 并通知客户。
4. "How do you know it can't run code?" → 只有自己的 AST 求值器：没有属性访问、调用、名字查找（字段只能走 `FIELDS` 白名单）；测试里放 `__import__("os")...`，加载期报错且无副作用。
5. "What's missing?" → 严重度、其它事件类型、规则间依赖（接 t2 的 `requires`）、行内注释、规则版本与审计、正则。
6. "`sender.domain_age_days < "7"`?" → 加载期类型检查报 `'<' compares numbers`；没做的话运行时 `TypeError` 被 runner 吞成 `detector.error`——规则静默失效，这就是要在加载期校验的原因。

### 翻车点
- `eval()`/`ast.literal_eval` 拼表达式 → 客户可执行代码；`sender.domain_age_days` 这种点路径也不是 Python 名字。
- 新建 `rules.yaml`/JSON 规则文件与独立加载器，或扩展 `legacy/yaml_rules.py:parse_rule` → 绕开租户配置与 `_ALLOWED`，且那是冻结的 v0 格式（只支持单个比较）。
- 规则单独走一条结果通道/自造 `Signal` 子类 → `GET /signals`、存储、CLI 都要再改；`Detector.signal(...)` 已经给了同形。
- 只在求值时报错 → 客户的拼写错误在第一个事件才暴露，还被 runner 的 try/except 吞掉；`ConfigError` + 加载期校验才符合"静默丢弃都是 bug"。

---

## t2 · detector dependencies（RUL-231）

### 题
检测器开始互相依赖对方的结果，已经出现过"依赖的那个还没跑"导致的错误结论。让它安全。

### 参考答案
- 设计：这是依赖排序——拓扑排序（Kahn），不是调整 import 顺序（X5，T5）。`Detector.requires` 已存在、`vendor_lookalike` 已声明、`ctx.signals` 已是传递通道，缺的只是 runner 读它。选项 A：给每个检测器加数字 `priority`；选项 B：按 `requires` 排序。选 B：同层保持注册顺序（无依赖的租户行为不变）；环与未知依赖在 runner 构造（= 每租户启动）时 `ConfigError`，环点名成员；运行时上游**被租户禁用**或**抛异常**则下游跳过、`metrics.incr("detector.skipped", detector=…, missing=…)`，并级联；上游**没触发**不是失败，下游照常运行。
- 改动：
  - `rulelang/detectors/runner.py:order_detectors`：Kahn + 堆（按注册序取就绪项）；未知名 → `ConfigError`；剩余节点里找出一个具体环（`_find_cycle`）→ `detector dependency cycle: a -> b -> c -> a`。
  - `rulelang/detectors/runner.py:DetectorRunner.__init__`：对**全部**检测器（含被禁用的）排序，环不因租户配置而时有时无；保存 `self.disabled`。
  - `rulelang/detectors/runner.py:DetectorRunner.run`：`unavailable = set(self.disabled)`；任一 `requires` 在其中 → 计数、把自己也加入 `unavailable`（级联）；`evaluate` 抛异常 → `detector.error` 计数并加入 `unavailable`。
- 关键测试：
  - `tests/test_detectors.py::test_registration_order_does_not_change_results`：注册表倒序后 `billing@acme-vend0r.example` 仍得 `["new_sender", "vendor_lookalike"]`。
  - `tests/test_detectors.py::test_cycle_is_reported_at_startup_with_its_members`：`cycle: cyc_a -> cyc_b -> cyc_c -> cyc_a`。
  - `tests/test_detectors.py::test_downstream_is_skipped_and_counted_when_upstream_crashes`：`detector.skipped{detector=down,missing=up}` 与级联的 `down2` 各计 1。
  - `tests/test_detectors.py::test_upstream_not_firing_is_not_a_failure`：上游返回 `None` 时下游照常运行，无跳过计数。
  - `tests/test_detectors.py::test_tenant_disabling_an_upstream_skips_its_dependants`：租户禁用 `new_sender` → `vendor_lookalike` 被跳过并计数。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | 复述 ticket，T4 定义 "depends on"；T2 后问 3 个 | "So dependency means: detector B reads detector A's signal for the same event, so A must have run first. Three questions. What should happen when A is disabled for the tenant or throws? Is 'A did not fire' a failure? What about a cycle?" 面试官答："Don't judge on missing data. Skip it, and I want to see that it was skipped."；"No. 'Didn't fire' is a normal answer."；"I want to know at startup, and which detectors are in the loop." 默认：禁用/崩溃 → 跳过并计数；没触发 → 照常；环 → 启动报错点名 | T2：`Given RUL-231 and this repo: list the decisions I must make, ordered so each depends only on earlier ones. Format: Q<n> — question; → the option you'd pick and why. Look up facts in the code. No code.` T4：`Pin the terms: requires, upstream, downstream, skipped vs not fired.` |
| 13–16 方案 | 说模式、缝、两方案、里程碑 | **模式**："This is dependency ordering — a topological sort. `Detector.requires` already exists and nothing reads it; the README claims it's honoured and it isn't." **缝**：`DetectorRunner.__init__`（排序）与 `run`（跳过）。选项 A：`priority` 数字或调整 `detectors/__init__.py` 的 import 顺序；选项 B：按 `requires` 做 Kahn；选 B。**核对 AI 的实现**：环报错是否点名成员、同层顺序是否稳定（默认结果不变）、`requires` 指向未注册名是否被静默当成新节点（`graphlib` 会）、被禁用的检测器是否仍在入度表里、跳过是否级联。M1 = 排序 + 环；M2 = 跳过 + 计数 | T3：`Here's my list: Kahn over Detector.requires at DetectorRunner construction; stable tie-break by registration order; cycle and unknown name = ConfigError naming members; upstream disabled or crashed = skip downstream + metrics.incr; upstream returned None = run normally. What did I miss? Add only what's missing, ranked by user impact.` T5：`I think the seam is DetectorRunner.__init__ and run (existing adapters: six registered detectors, one with requires). Compare priority numbers vs sorting by requires in 5 lines each: fit with existing code, failure isolation, what a detector author must do. Recommend one. Don't edit.` T6：五条规则 |
| 16–30 M1 | plan mode → 审计划 → 红 → 绿 → 真实入口 | "First failing test: reverse the registry and the verdicts must not change." | T7 红：`Write ONE failing test in tests/test_detectors.py: build the app once in the default order and process an email from billing@acme-vend0r.example; then reverse DETECTORS (clear + update from a reversed copy), build a fresh app, process the same email, and assert both give ["new_sender", "vendor_lookalike"]. Restore the registry in a fixture. Run it and show me it fails. Don't fix.`（失败原因：倒序下只得 `["new_sender"]`——`vendor_lookalike` 先于 `new_sender` 运行，看不到它）T7 绿：`Minimal change: in DetectorRunner.__init__ order the detector instances topologically by requires with registration order as tie-break; unknown names and cycles raise ConfigError naming the detectors. Nothing else. Run that test file.` |
| 30–40 M2 | 跳过 + 计数；红了走 T8 | "M2 is the runtime half: if the thing I depend on is switched off or crashed, I don't judge on missing data — I skip and count." | T7 红：`Write ONE failing test: register up (raises) and down (requires up); process one event; assert down produced no signal and metrics.get("detector.skipped", detector="down", missing="up") == 1 while an unrelated detector still fired.` 绿：`Track unavailable detectors per event (disabled + crashed + skipped); skip any detector whose requires intersect it; count with metrics.incr. Return None from a detector is NOT unavailable.` |
| ~40 审查 | T10 一轮，收一条拒一条 | "One doubt round. I'll take the cascade finding and reject the parallel-execution one." | T10：`Adversarial review of the current diff against RUL-231. Assume the author is overconfident. Look for unstated assumptions, unhandled edge cases, broken conventions, failure modes under bad input. Do NOT validate or summarize. Max 5 issues, ranked.` 典型发现：① 上游被跳过后，下游的下游仍然运行（未级联）→ **收**：把被跳过的也放进 `unavailable`；② 建议引入线程池并行跑无依赖的检测器 → **拒**：`Pipeline` 同步、sqlite 连接非并发，写进 known gaps |
| 42–45 收尾 | 自己跑证据；写 NOTES.md | "Fresh run: 69 passed. Here's the real output through the CLI." | T11：`uv run --with pytest python -m pytest -q`；`python3 -m rulelang detectors` → `vendor_lookalike           email (requires new_sender)`；租户配置加 `[detectors] disabled = ["new_sender"]` 后 `python3 -m rulelang run fixtures/events --tenant acme --db /tmp/t2.db` → `processed 23 events, 5 signals (3 bad records skipped)`（基线 10 个），`python3 -m rulelang signals a-011 --tenant acme --db /tmp/t2.db` 无输出（`vendor_lookalike` 被跳过）；计数用 `python -m pytest -q tests/test_detectors.py -k disabling_an_upstream`（断言 `detector.skipped{detector=vendor_lookalike,missing=new_sender} == 1`）。T12：`NOTES.md` |
| 45+ 讲解 | 3–5 min | "v1 orders detectors by their declared `requires` when the runner is built — registration order is only the tie-break, so nothing changes for tenants that don't use it. A cycle or an unknown dependency stops startup and names the detectors. At runtime, if an upstream is disabled or crashed, its dependants are skipped and counted, cascading; an upstream that simply didn't fire is not a failure. Not done: skips are only a counter, no analyst-visible trace; no 'requires any of'; custom rules can't declare dependencies yet." | — |

### 追问与答（来自 interviewer.md 的追问）
1. "No dependency between two detectors — does order matter?" → 不影响结果；Kahn 用堆按注册序取就绪项，同层输出顺序稳定，所以默认租户输出不变。
2. "Surface skips to an analyst?" → 现在只是计数器 + 日志；v2 把 `skipped` 作为事件级元信息写进 `GET /signals` 或 `signals` CLI 末尾。
3. "A cycle from a customer rule?" → 规则声明的依赖来自配置，在同一个构造点校验，报错同样点名；不会进入运行期。
4. "10x the detectors?" → 排序只在 runner 构造时做一次，O(V+E)；`run` 里是集合查找，开销不变。
5. "Why not a priority number?" → 数字要人手维护，不表达"为什么"，也检测不出写错；`requires` 已经存在且被 `vendor_lookalike` 用了。
6. "What's missing?" → 条件依赖、并行、跳过的可观测性、自定义规则的依赖声明。

### 翻车点
- 把 `detectors/__init__.py` 的 import 改成"new_sender 排前面" → 治标：字母序本来就碰巧对，新检测器仍会踩；错误排列在启动时依然检测不出。
- 在 `VendorLookalike.evaluate` 里加 `if "new_sender" not in ctx.signals: …` 之类补丁，或新增 `priority`/`depends_on` 字段 → 另起一套表达依赖的方式，`requires` 继续被忽略。
- 上游被禁用/崩溃时让下游照跑 → 就是 ticket 里"wrong verdicts"：`ctx.signals` 里缺的不是"没触发"，是"不知道"。
- 环只报 "cycle detected" 不点名，或抛 `graphlib.CycleError` 原样冒泡 → CLI 变成 traceback、退出码 1，而不是 `error: ...` 退出码 2（不符合 `RulelangError` 约定）。

---

## t3 · blast radius（RUL-244）

### 题
确认账号被盗后，SOC 要知道还有谁有风险：该账号在被盗时间之后发过邮件的人，以及这些人又转发给了谁。要有 `GET /blast-radius?account=&since=`、CLI `blast-radius <addr> --since <ts>`，跳数上限是租户配置 `[blast_radius] max_hops`（默认 2）。

### 参考答案
- 设计：这是图上的带时间约束的 BFS：起点 = 被盗账号（0 跳），只沿"在 `since` 之后发生过联系"的出边走，按层截断到 `max_hops`，`seen` 防环，外部域名进名单但不展开（X5，T5）。选项 A：每一跳回头对 `events` 表写 SQL 扫邮件；选项 B：只用 `CommGraph.neighbors`（边上已有 `first_ts`/`last_ts`）。选 B。边条件：`edge.last_ts >= arrival`（`last_ts` 是最近联系，所以满足即"之后至少有一次"）；到达时间 `arrival` 从 `since` 起，沿路用 `max(arrival, edge.first_ts)` 作下界，所以第二跳的联系不会早于风险到达那个人之前。路径随队列携带。
- 改动：
  - `rulelang/graph/blast_radius.py:blast_radius / Exposure`：BFS（`deque`，`seen`，`hops == max_hops` 时不展开，外部 `is_internal` 为假时不入队），结果按 `(hops, address)` 排序，`Exposure.to_dict` 给 `address/hops/path`。
  - `rulelang/config.py:BlastRadiusSettings / _ALLOWED["blast_radius"] / build_settings`：`max_hops` 整数 1–10；`config/default.toml` 加 `[blast_radius] max_hops = 2`。
  - `rulelang/api/routes/blast_radius.py:get_blast_radius`：`@route("GET", "/blast-radius")`，缺参数或 `since` 非 ISO → `BadRequest`，图用 `CommGraph(ctx.conn, req.tenant)`；`routes/__init__.py` 注册。
  - `rulelang/cli.py:main`：`blast-radius` 子命令（`--since`、`--tenant`、`--max-hops` 可覆盖配置；非法 `--since` → `ConfigError` → 退出码 2）。
  - `rulelang/graph/__init__.py`：导出 `blast_radius`、`Exposure`。
- 关键测试：
  - `tests/test_graph.py::test_blast_radius_follows_time_respecting_edges`：`since` 之前的联系、早于到达的联系、外部之后的人都不进名单；路径与跳数正确。
  - `tests/test_graph.py::test_blast_radius_hop_limit`：`max_hops=1` 只有 b 与外部；`3` 才出现 d。
  - `tests/test_api.py::test_blast_radius_endpoint`：夹具里 `dana@acme.example` 在 `2026-09-10T09:00:00Z` → 5 人，`frank` 的 path 为 `dana → erin → frank`，globex 令牌查到 0 人。
  - `tests/test_cli.py::test_blast_radius_command`：默认 2 跳无 `hank`，`--max-hops 3` 才有；`--since tuesday` 退出码 2。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | 复述 ticket，T4 定义 "at risk"/"hop"；T2 后问 3 个 | "So at risk means: emailed by the compromised account at or after the compromise time, then emailed by those people, up to a hop limit. Three questions. Is `since` inclusive, and do we only follow outgoing mail? Do external addresses get listed, and expanded? Does a forward have to happen after the mail it forwards?" 面试官答："At or after."；"List them… but don't go past them."；"A forward can't happen before the mail it forwards."（未问则默认只做 `last_ts >= since`，时间传递是 stretch） | T2：`Given RUL-244 and this repo: list the decisions I must make, ordered so each depends only on earlier ones. Format: Q<n> — question; → the option you'd pick and why. Look up facts in the code. No code.` T4：`Pin the terms: compromise time, hop (account = 0), at risk, external.` |
| 13–16 方案 | 说模式、缝、两方案、里程碑 | **模式**："This is a time-constrained BFS over the communication graph: level by level so hop counts are shortest, a seen set against cycles, edges filtered by time, external addresses as leaves." **缝**：`CommGraph.neighbors` + `Edge.first_ts/last_ts`。选项 A：每跳扫 `events` 表；选项 B：只用 `neighbors`；选 B。**核对 AI 的实现**：`since` 当刻是否包含（`>=`）、`seen` 在入队时标记还是出队时（出队会重复入队）、`hops == max_hops` 的截断位置（先加入名单再不展开）、路径元组是否被分支共享修改、外部地址是否被展开、`since` 无时区、入边是否被误算。M1 = 默认跳数 + CLI；M2 = 路径、外部叶子、配置、API | T3：`Here's my list: BFS from the account over CommGraph.neighbors; edge counts if last_ts >= since; max_hops from [blast_radius] in config (default 2); external = not in org.internal_domains, listed but not expanded; each result carries its path; route via @route with req.tenant; CLI subcommand. What did I miss? Add only what's missing, ranked by user impact.` T5：`I think the seam is CommGraph.neighbors (existing adapters: new_sender uses first_contact). Compare querying the events table per hop vs walking CommGraph edges in 5 lines each: fit with existing code, tenant isolation, cost per hop. Recommend one. Don't edit.` T6：五条规则 |
| 16–30 M1 | plan mode → 审计划 → 红 → 绿 → 真实入口 | "First failing test: the two-hop scenario on paper — erin and frank are in the list, hank at three hops is not." | T7 红：`Write ONE failing test in tests/test_graph.py: record emails a->b at T+10m, b->c at T+30m, c->d at T+40m and a->old at T-60m; blast radius of a since T with max_hops 2 must be exactly {b, c}. Expected values as literals. Run it and show me it fails. Don't fix.` T7 绿：`Minimal change: a function blast_radius(graph, account, since, max_hops, internal_domains) doing BFS over graph.neighbors with a seen set, edges kept when last_ts >= since, paths carried in the queue; plus the CLI subcommand. Nothing else. Run that test file.` |
| 30–40 M2 | 外部叶子、配置、API、租户；红了走 T8 | "M2 is the SOC-facing part: the path for each person, external addresses as leaves, and the hop limit as a tenant setting." | T7 红：`Write ONE failing test in tests/test_api.py: GET /blast-radius?account=dana@acme.example&since=2026-09-10T09:00:00Z through the acme client lists erin, pat, vendor@acme-vendor.example, frank, gus, frank's path is dana->erin->frank, and the globex client gets zero items.` 绿：`Add [blast_radius] max_hops to config._ALLOWED/build_settings/default.toml; a route file registered in routes/__init__.py using req.tenant, BadRequest for missing or non-ISO params; stop expanding addresses outside internal_domains.` |
| ~40 审查 | T10 一轮，收一条拒一条 | "One doubt round. I'll take the arrival-time finding and reject the pagination one." | T10：`Adversarial review of the current diff against RUL-244. Assume the author is overconfident. Look for unstated assumptions, unhandled edge cases, broken conventions, failure modes under bad input. Do NOT validate or summarize. Max 5 issues, ranked.` 典型发现：① 第二跳的联系可以早于风险到达该人（erin 在 dana 来信之前发给 jon 也被列入）→ **收**：到达时间下界 `max(arrival, first_ts)`，写 stretch 测试；② 结果无分页/上限，hub 节点会炸 → **拒**：v1 有 `max_hops`，列为 known gap |
| 42–45 收尾 | 自己跑证据；写 NOTES.md | "Fresh run: 69 passed. Here's the real output through the CLI and the API." | T11：`uv run --with pytest python -m pytest -q`；`python3 -m rulelang blast-radius dana@acme.example --since 2026-09-10T09:00:00Z --tenant acme --db /tmp/t3.db`（先 `run fixtures/events`）→ 5 行：`erin@acme.example                  hops=1  dana@acme.example -> erin@acme.example`、`pat@…`、`vendor@acme-vendor.example …`、`frank@acme.example                 hops=2  dana@acme.example -> erin@acme.example -> frank@acme.example`、`gus@…`；加 `--max-hops 3` 多出 `hank@acme.example                  hops=3  dana@acme.example -> erin@acme.example -> frank@acme.example -> hank@acme.example`；API（`TestClient`）→ `{'account': 'dana@acme.example', 'max_hops': 2, 'since': '2026-09-10T09:00:00+00:00', 'total': 5}`，globex 令牌 → `'items': [], 'total': 0`。T12：`NOTES.md` |
| 45+ 讲解 | 3–5 min | "v1 is a breadth-first walk of the tenant's communication graph from the compromised account: only edges with contact at or after the compromise time, each hop no earlier than when the risk reached the sender, capped by `[blast_radius] max_hops`. Every person comes with the path that put them there; external addresses are listed as leaves. Not done: exact arrival times — the graph only keeps first and last contact, so it's a lower bound; paging for hub addresses; telling forwards from ordinary mail." | — |

### 追问与答（来自 interviewer.md 的追问）
1. "100M edges, one hub emailed everyone?" → `neighbors` 是单次索引查询，`max_hops` 限制深度，但 hub 的出度会让一层爆炸：加结果上限/分页，对超大出度的节点只列不展开，或在图里按时间范围建索引。
2. "Why BFS and not DFS?" → 要最短跳数的路径并按层截断；DFS 先走深路径，配合 `seen` 得到的路径不是最短的。
3. "Same person reached at different times?" → v1 的 `seen` 固定第一次到达的时间，严格解法是最早到达搜索（Dijkstra 式）；而且只有 `first_ts/last_ts`，精确需要逐封邮件时间戳（新表）。
4. "Roll out / who uses it?" → 只读且按租户，先给 SOC；每次查询落审计；`since` 必填避免无限回溯。
5. "What does the SOC do with the list?" → 隔离、重置凭据、通知外部伙伴；v2 带上联系次数、最近联系时间、是否点击链接。
6. "What's missing?" → 精确到达时间、分页、区分转发与普通邮件、`since` 缺时区时的默认（现在按 UTC）、导出。

### 翻车点
- 每一跳回头对 `events` 表 `SELECT … WHERE actor = ?` → 绕开 `CommGraph`（`CommGraph.record` 已经维护了出边），N+1 查询，且容易漏掉租户条件。
- 用 `first_contact` 做时间过滤 → 它只返回"首次"，对"之前联系过、之后又联系"的人（`pat`）会漏或误判；要用边的 `last_ts`。
- 外部地址继续展开 → 把合作方的邮件往来当成我方图；本系统的"内部"由 `[tenant] internal_domains` 定义，用 `is_internal`。
- 递归 DFS + 无 `seen` → 互发邮件的两人（a↔b）无限递归；路径也不是最短的。
- 在 `config.py` 之外读 `max_hops`（常量或 `os.environ`）→ 违反"配置优于常量"，且 `[blast_radius]` 不登记 `_ALLOWED` 租户文件根本加载不了。
