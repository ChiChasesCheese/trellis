# cb03 · 逐场脚本
> 候选人身份欺诈检测服务 `vetting`（ATS 申请 + IdP 登录 → signals → 评分 → reviewer 证据时间线，不做招聘决定）· t1 协同申请者关联（一个操作者多份申请）· t2 接入 Workday 数据源 · t3 用 reviewer 的 cleared 决定降低重复误报 · 练：`python3 loop/ai_screen.py start cb03 <t>` · 面试官视角：`interviewer.md`

## 0. 探索（0–10 min，三个 ticket 通用）
- 先打开：
  - `vetting/pipeline.py:Pipeline.ingest` / `evaluate_all` — 数据流主干；`ingest` 每次重评整个租户，所以"新来的人让旧的人也变"天然成立。
  - `vetting/signals/base.py:register_signal` / `SignalContext` / `Signal.finding` — 检测的扩展点；权重必须在 `config/default.toml [weights]`，否则启动失败。
  - `vetting/sources/base.py:register_source` / `Source.observe` / `Source.bad_record` + `sources/greenhouse.py` — 数据源范本和三条约定（坏记录计数跳过、缺字段只丢该观测、值按提交原样存）。
  - `vetting/settings.py:_SECTIONS` + `config/default.toml` — 新配置段必须在这里注册，否则 `ConfigError`。
  - `vetting/store/repositories.py:ObservationRepository.list_by_kind` / `find`、`ReviewRepository.dispositions` — 取观测与 reviewer 决定；`find` 是原值精确匹配。
  - `tests/conftest.py`（`ingested`、`client`、`make_ctx`）和 `tests/test_signals.py` — 新测试照这个风格放。
- T1 结果应包含：入口 `python -m vetting ingest|review|serve`（`vetting/cli.py:main`）与 `vetting/api/reviews.py:list_reviews/get_review/post_disposition`；数据流 `sources/ → Identity+Observation → store/ → signals/ → scoring.py → timeline.py → api/`；扩展点 `@register_source`、`@register_signal`、`settings._SECTIONS`、`timeline.SOURCE_LABELS`；测试命令 `python -m pytest tests/test_signals.py -q`（单文件）与 `python -m pytest -q`（全量，52 passed）；遗留 `vetting/legacy/blocklist.py`（DEPRECATED，没人 import），README 两处过时（权重不在 `vetting/weights.py` 而在 `config/default.toml`；架构图把 blocklist 画成管线一环）。
- 心智模型（60 s，英文原句）："Data comes in through sources registered with a decorator, Greenhouse for applications and the IdP for sign-ins. Each record becomes an Identity plus Observations, stored as submitted with a raw_ref back to the record, in SQLite where every repository call takes the tenant first. Signals are the extension point: each is registered, reads the observations, and returns a Finding with weighted, cited evidence; weights live in config/default.toml. Scoring sums findings into a tier, timeline renders the citations, and a small WSGI API serves reviews and dispositions. Anything that compares values goes through normalize.py, and ingest re-evaluates the whole tenant. I'll stay away from legacy/blocklist.py, it's deprecated and unwired, and the README's weights.py is stale. The risk is false positives, since the reviewer is a person."

## t1 · coordinated_applicants

### 题
VET-212：一个可疑申请者通常只是一场行动里的一个节点（同一批操作者换名字反复投）；reviewer 打开其中任何一个人，要看到其余的人以及为什么相连。

### 参考答案
- 设计：接缝是 `@register_signal`（已有五个 signal 站在它后面，是真接缝），不是新模块或新表：finding 自带权重、引用、时间线、`GET /reviews/<id>`，且 `ingest` 本来重评全租户，旧申请会自动更新。两个方案：(A) 新 signal，在 `ctx.store.observations.list_by_kind` 取本租户观测、过 `normalize.py` 后比较；(B) 另建 correlator + 关联表。选 A。关联规则：电话块 / IP /24 / 简历指纹 / 邮箱四类标识中，至少两类重合才关联；单个共享值（办公室 NAT、中介电话）不定罪；块位数、最少类数、IP 允许名单进 `[correlation]`。
- 改动：
  - `vetting/signals/coordinated_applicants.py:CoordinatedApplicants` — 新 signal；`_keys` 把观测归一成 family→key（phone / ip / email / resume）；`evaluate` 扫本租户其他 identity，重合 family 数 ≥ `min_overlap_kinds` 才出 finding，摘要点名对方 id，evidence 含双方观测的 `raw_ref`。
  - `vetting/signals/__init__.py` — import 注册（漏了等于没加）。
  - `vetting/normalize.py:phone_prefix` — 取 E.164 前 N 位。
  - `vetting/settings.py:CorrelationSettings` + `_SECTIONS` 加 `correlation` — `phone_prefix_digits=9`、`min_overlap_kinds=2`、`allowlist_cidrs=[]`。
  - `config/default.toml` — `[weights] coordinated_applicants = 40` 与 `[correlation]` 段。
- 关键测试：
  - `tests/test_coordinated.py::test_campaign_members_cite_each_other` — 40111/40112/40113 各自的 finding 引用另外两人，tier 非 NONE。
  - `::test_benign_overlaps_are_not_flagged` — 只共享办公室 NAT 的 40106/40107/40101 没有该 finding。
  - `::test_one_shared_kind_is_not_enough` — 只共享电话块（IP 不同网段）不关联。
  - `::test_phone_formats_and_ip_neighbours_link` — `(206) 555-0101` 与 `+1 206-555-0101 x12`、`198.51.100.40` 与 `.41`（同 /24）仍关联。
  - `::test_other_tenant_is_not_correlated`。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | 用 reviewer 视角复述；T4 定术语 "link"：两份申请在 ≥2 类标识上重合；T2 后问 3 个 | "I read this as: open any applicant in a campaign and see the others with the reason. Let me pin 'linked': two applications overlapping on at least two kinds of identifier." | T4；T2：`Given this ticket and this codebase: list the decisions I must make, ordered so each depends only on earlier ones. Format: Q<n> — question; → the option you'd pick and why. Facts you can look up in the code, look up — don't ask me. No code.` 问面试官：Q1 "Which identifiers count, and at what granularity, phone block or IP /24?" → 电话、IP、邮箱、简历文件（哈希、作者+工具），不要 user agent；块位数你定放配置。默认：9 位 / `/24`。Q2 "Is one shared value enough?" → 不够（办公室 NAT、中介电话）。默认：≥2 类。Q3 "Within one customer or across?" → v1 只本租户，要你讲跨租户怎么做。默认：本租户。其余（要不要改阈值、存哪）说 "I'll assume the new signal uses the existing weights and thresholds; it's config." |
| 13–16 方案 | T3 + T5；定里程碑 | "The seam is the signal registry, five signals already sit behind it, so it's real. Option A is a new signal reading list_by_kind; option B is a separate correlator with its own table. I'll pick A: the finding gives me citations, the weight in config and the timeline for free." | T3：`Here's my list: two kinds of overlap minimum; compare after normalize.py; same tenant only; weight and block size in config; cite the other applicant's raw_ref. What did I miss? Add only what's missing, ranked by user impact. Don't rewrite mine.`（应补：新 section 要进 `settings._SECTIONS`；`find()` 是原值精确匹配不能用）；T5：`I think the seam is vetting/signals/base.py:register_signal (existing adapters: voip_phone, vpn_hosting_ip). Compare a new signal vs a separate correlator module with its own table in 5 lines each: fit with existing code, failure isolation, what a reviewer must do. Recommend one. Don't edit anything.`；T6 写 `CLAUDE.md`。M1 = 电话块 + /24 两类；M2 = 简历 + 邮箱 + `[correlation]`；M3 = 允许名单。 |
| 16–30 M1 | plan mode → 审计划 → 红 → 绿 → 演示 | "Failing test first: the three campaign applicants should each cite the other two." | T7 红：`Write ONE failing test for coordinated_applicants through the HTTP API, in tests/test_coordinated.py, matching tests/test_api.py. Use the client fixture; for greenhouse:40111, 40112 and 40113 assert a finding with signal "coordinated_applicants" whose evidence refs contain the other two ids. Expected ids as literals. Run it and show me it fails. Don't fix anything.`（红的原因：`found` 为 None，不是 import 错）。T7 绿：`Minimal change to make that test pass: a Signal in vetting/signals/ following voip_phone.py, @register_signal, weight in config/default.toml, normalized phone block + ip_prefix24 via list_by_kind, require two kinds. Nothing else. Run that test file.` 最小改动 = 新 signal 文件 + `signals/__init__.py` + `phone_prefix` + 权重一行 + `[correlation]`。 |
| 30–40 M2 | 补简历指纹、邮箱、配置段；再写"共享 NAT 不定罪" | "M2 is the ambiguous part: one shared value must not condemn anyone, so test that with 40106 and 40107." | T7 红：`Write ONE failing test: greenhouse:40106, 40107 and 40101 must have no coordinated_applicants finding (they share only an office NAT). Show it fails/passes honestly.`；若一加简历指纹就多出误报 → T8：`Reproduce this with one command or one failing test that shows the exact symptom. Then give 3 ranked hypotheses, each with the prediction that would confirm it. Don't fix yet.` |
| ~40 审查 | T10 一轮 | "I'd normally run a doubt pass with a fresh reviewer — one round now." | T10 原提示词。典型 v1 的两条：(1) 每个 identity 每次评估都扫整租户（O(N²)），且 `evaluate_all` 重复取数 → 有效但接受，写进 known gaps（几千份量级可用，10x 时存归一化 key 建索引）；(2) 电话用字符串前缀 / 自写 `re.sub`、或 `find(kind, value)` 比对 → 有效且要改，换 `normalize.phone_e164 + phone_prefix`，因为值按提交原样存，格式不同就漏。 |
| 42–45 收尾 | T11 + T12 | "Fresh run: N passed. Here's the real output through the CLI." | T11：`python -m pytest -q`（reference 解下 64 passed）；`python -m vetting --db $DB ingest fixtures --tenant acme`；`python -m vetting --db $DB review greenhouse:40111 --tenant acme` → 输出 `recommendation: RECOMMENDED  score: 40`，并有 `coordinated_applicants: Overlaps with 2 other applicant(s) on multiple kinds of identifier: greenhouse:40112 via email, ip, phone, resume; greenhouse:40113 via ip, phone, resume`；`review greenhouse:40106` → `recommendation: NONE  score: 0`。T12：写 NOTES.md（本租户、≥2 类、块位数在配置、未做传递关联 / 跨租户 / 允许名单演示）。 |
| 45+ 讲解 | 用 `playbook.md` §5.3 模板 | "What I shipped: open any applicant in a campaign and you see the others and which identifiers tie them. It's a registered signal, config in [correlation], it reuses normalize.py and Finding/Citation." | 关键数字：权重 40、`recommended_at=20`、`highly_recommended_at=50`；known gaps 见下。 |

### 追问与答
- "What if there are 10x as many applicants?" 现在每个 identity 扫整租户。10x 时在 ingest 时存一列归一化 key 并建索引，或增量维护一张关联表；signal 只查索引。
- "How would you roll this out?" 先 shadow：权重设 0 只记 finding，看分布后再开权重；按租户开关，配置里已有 `[correlation]`。
- "A recruiting agency submits 200 applicants from one phone line?" 同一类标识上重合人数过多就降权，加上 `allowlist_cidrs`；单类重合本来就不关联，所以电话相同不会单独升级。
- "How would you explain this to the reviewer?" evidence 列出对方 identity 与具体重合的标识类别，措辞是 "overlaps with"，不下 "此人是攻击者" 的结论。
- "What is missing from v1?" 传递关联（A–B、B–C 但 A、C 不直接重合）、跨租户、O(N²)。
- "Privacy across customers?" 只暴露最小信息：归一化值的盐值哈希加 "seen at other organizations"，不给对方数据；需合同与隐私评审。

### 翻车点
- `find(kind, value)` 或手写 `re.sub(r"\D", "")` 比较电话 → 值按提交原样存，`(415) 555-0143` 与 `415.555.0147` 对不上；`normalize.py` 已有 `phone_e164` / `ip_prefix24` / `email_key`。
- 任何共享值就互相标记（含 user agent、办公室 IP） → 40106/40107 只共享 NAT，会被冤枉，reviewer 被误报淹没。
- 新建 `correlation.py` + 新表绕开 `@register_signal` → 权重、证据、时间线、`/reviews` 展示要重做一遍。
- `[correlation]` 不进 `settings._SECTIONS`，或权重不进 `default.toml` → `ConfigError` / 启动即失败。

## t2 · workday_source

### 题
VET-219：新客户用 Workday 不用 Greenhouse，加 Workday 为数据源；样本导出在 `fixtures/workday/`；他们的 reviewer 对这些申请者应看到与 Greenhouse 同样质量的审查。

### 参考答案
- 设计：接缝是 `@register_source`（`greenhouse`、`idp` 两个已在其后，是真接缝）。方案 A：写 `WorkdaySource`，把嵌套字段映射到同一套 `Kind` / `Observation`，所有 signal 不动；方案 B：把 Workday 转成 Greenhouse JSON 再喂旧 source。选 A，B 会丢 `raw_ref` 的来源指向。幂等靠两点：`Identity.make_id("workday", Job_Application_ID)`，以及 `raw_ref` 不含页码，使 `INSERT OR IGNORE` 命中 `UNIQUE (tenant_id, identity_id, kind, value, raw_ref)`。
- 改动：
  - `vetting/sources/workday.py:WorkdaySource.load` — 沿 `Paging.next` 读 `applications.json`、`applications.<cursor>.json`，带环保护；坏 JSON 走 `bad_record`。
  - `WorkdaySource._parse` — 缺 `Job_Application_ID` / 日期 → `bad_record` 跳过整条；其余字段走 `observe()`（缺失只计数）；电话 `+{Country_Code} {Phone_Number}`，`Extension` 不拼入；时间 `parse_ts`（`-07:00` → UTC）。
  - `vetting/sources/__init__.py` — import `workday` 才会注册。
  - `vetting/timeline.py:SOURCE_LABELS` — 加 `"workday": "Workday"`。
- 关键测试：
  - `tests/test_workday.py::test_workday_ingest_follows_pages_and_dedupes` — 四个人（Sam / Pat / Lee / Dana），`sources.workday.bad_record == 1`、`missing.email == 1`。
  - `::test_existing_signals_work_on_workday_data` — Sam 只有 `voip_phone` 且 evidence 只 1 条（重复投递不翻倍），时间线首条 `ts == 2026-09-14T17:22:00+00:00`、`source == "workday"`；Pat 无邮箱仍有 `resume_name_mismatch`。
  - `::test_rerun_is_idempotent` — 再次 ingest `observations == 0`、`identities == 4`。
  - `tests/test_sources.py::test_registry_has_the_sources` — 集合变成 `{"greenhouse", "idp", "workday"}`（starter 里原测试断言两个，会随之变红，要改）。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | 打开 `fixtures/workday/applications.json`、`applications.p2.json` 自己看；T4 定术语 "duplicate" | "Let me pin 'duplicate': the same Job_Application_ID delivered twice. Same person re-applying under a new id is a different application." | T4；T2 原提示词。问面试官：Q1 "By duplicate, do you mean the same application id on two pages?" → 是（`JA-100234` 同时在 p1 和 p2），幂等、同一 identity、证据不翻倍。默认：幂等。Q2 "A record with no email: drop it or keep the rest?" → 别整条丢，缺字段要计数。默认：只丢该观测。Q3 "Own signals or weights for Workday?" → 不要，现有 signal 原样生效。默认：不新增。其余说 "I'll assume UTC and the extension stays out of the phone number; both are easy to change." |
| 13–16 方案 | T3 + T5 | "The seam is the source registry; Greenhouse and the IdP already sit behind it. Option A: a WorkdaySource mapping into the same Kinds. Option B: convert to Greenhouse JSON first. I'll take A, B loses the raw_ref pointing at Workday." | T3：`Here's my list: new Source following greenhouse.py; map to existing Kinds; same-id redelivery is one identity; missing field skips only that observation; UTC via parse_ts. What did I miss? Add only what's missing, ranked by user impact. Don't rewrite mine.`（应补：`sources/__init__.py` import、`SOURCE_LABELS`、phone extension）；T5：`I think the seam is vetting/sources/base.py:register_source (existing adapters: greenhouse, idp). Compare a new WorkdaySource vs converting Workday to Greenhouse JSON in 5 lines each: fit with existing code, failure isolation, what a customer must do. Recommend one. Don't edit anything.`；M1 = 读 `applications.json` 一页 + 映射 + Sam 出 `voip_phone`；M2 = 分页、去重、缺字段、`SOURCE_LABELS`；M3 = 回归（Workday 与 Greenhouse 同目录）。 |
| 16–30 M1 | plan mode → 红 → 绿 | "Failing test first: ingest the Workday fixture and Sam should come out with a VoIP finding, timestamp in UTC." | T7 红：`Write ONE failing test through vetting.cli.main ingest, in tests/test_workday.py, mirroring tests/test_sources.py. Copy fixtures/workday into tmp_path; ingest as tenant acme; GET /reviews/workday:JA-100234 must have findings == ["voip_phone"] and timeline[0].ts == "2026-09-14T17:22:00+00:00". Literals. Show it fails.`（红的原因：`workday:JA-100234` 无 review，不是 import 错）。T7 绿：`Minimal change: WorkdaySource following vetting/sources/greenhouse.py exactly: @register_source, Source.observe(), Source.bad_record(), Identity.make_id('workday', Job_Application_ID), timeutil.parse_ts. Join Country_Code and Phone_Number, no extension. Register it in sources/__init__.py. Do not touch signals/ or pipeline.py. Run that test file.` |
| 30–40 M2 | 分页、重复、缺字段、`SOURCE_LABELS`；starter 的旧测试变红 | "Two things turned red: the registry test expects two sources, and the fixtures directory now has sixteen identities not twelve. Those are expected consequences, I'll update them, not weaken anything." | T8：`Reproduce this with one command or one failing test that shows the exact symptom. Then give 3 ranked hypotheses, each with the prediction that would confirm it. Don't fix yet.`（用于 `tests/test_pipeline.py` 的 `identities=12 → 16`、`len(reviews) == 12 → 16` 与 `test_sources.py` 注册集合）。再补测试：Pat（无邮箱）仍被审、p2 里无 id 的记录计 `bad_record`。 |
| ~40 审查 | T10 一轮 | "One doubt round now, then I decide which to take." | T10 原提示词。典型 v1 的两条：(1) 手写 `datetime.strptime` 或 `raw_ref` 带页码/行号 → 有效且要改：用 `parse_ts`，`raw_ref` 只用 `observe()` 的 `path`，否则重复投递证据翻倍；(2) 读到不存在的 cursor 文件或循环 cursor 会死循环 → 有效，已用 `seen` 集合与 `path.exists()` 守住，接受并写进 known gaps（无页数上限）。若 AI 把分机拼进号码则当场改掉。 |
| 42–45 收尾 | T11 + T12 | "Fresh run: N passed. Here's the real output through the CLI." | T11：`python -m pytest -q`（64 passed）；`mkdir -p /tmp/wd && cp -r fixtures/workday /tmp/wd/ && python -m vetting --db $DB ingest /tmp/wd --tenant acme` → `workday: skipping bad record: KeyError('Job_Application_ID')`、`tenant=acme identities=4 observations_added=44 reviews=4`、`metric sources.workday.bad_record=1`、`metric sources.workday.missing.email=1`；再跑一次同命令 → `observations_added=0`（幂等）；`review workday:JA-100234 --tenant acme` → `recommendation: RECOMMENDED  score: 30`，`[workday] Application received via Workday` 与 `voip_phone ... <workday:JA-100234#Candidate.Phone>`，时间 `2026-09-14T17:22:00+00:00`；`ingest fixtures` → `identities=16`（12 个 Greenhouse + 4 个 Workday），`review greenhouse:40120` 仍 `HIGHLY_RECOMMENDED  score: 75`。T12 写 NOTES.md。 |
| 45+ 讲解 | §5.3 | "Two sources map to the same Observation model, so signals didn't change; a Workday reviewer gets the same review a Greenhouse one does." | 要能复述假设："duplicate = same Job_Application_ID"。 |

### 追问与答
- "What if the export is 100x larger in one file?" `load()` 已是生成器，换成流式 JSON 解析即可；`_parse` 一次只处理一条。
- "How would you onboard a third ATS faster?" 把"嵌套路径 → Kind"抽成映射表，`_parse` 变声明式；`Source.observe` 已统一缺字段计数。
- "What if Workday renames a field?" `sources.workday.missing.<kind>` 计数会突增；需要阈值告警，现在只打印，不静默吞掉也不告警。
- "How do you know Workday reviews are as good as Greenhouse's?" 把同一批人在两个源各灌一遍，对比 findings。Sam 的 `voip_phone` 证据与 Greenhouse 的 `40102` 同类。
- "What did you assume about the duplicate?" 同 `Job_Application_ID` 即同一 identity；用新 id 再投的是另一份申请，合并属于 t1。
- "What is missing?" 增量拉取（API 而非文件）、重试、cursor 页数上限。

### 翻车点
- 把 Workday 转成 Greenhouse JSON 再喂旧 source，或在 signals/pipeline 里写 `if source == "workday"` → 丢掉 `raw_ref` 来源指向；signal 本该对来源无感，`Pipeline` 本来就遍历 `SOURCES`。
- 漏 `sources/__init__.py` 的 import → 注册不发生，`ingest` 零身份、不报错。
- `raw_ref` 带页码，或手写 `strptime` → 重复投递在 `UNIQUE` 约束下不去重、证据翻倍；`-07:00` 偏移未转 UTC。
- 缺邮箱就丢整条记录 → Pat 的 `resume_name_mismatch` 本来还能跑；约定是缺字段只丢该观测。

## t3 · reviewer_feedback

### 题
VET-224：reviewer 经常清除被标记的人（公司 VPN、合法 Google Voice）；用他们的决定，别再重复标记同样的良性模式。决定通过 `POST /reviews/<identity_id>/disposition` 记录。

### 参考答案
- 设计：接缝是评分层（`Pipeline.evaluate` 里 signal 之后、`scoring.score` 之前），数据来自已有的 `dispositions` 历史与 `Finding.subject`（`asn:AS64500`、`phone:+1…` 已填好）。两个方案：(A) 评分前对 finding 降权，保留证据并标注；(B) 改全局权重或在每个 signal 里查 disposition。选 A：具体的值才算"同样的模式"，不关 signal，也不改全局权重。收窄条件防止洗白：只对"唯一一个 finding"、权重 ≤ `weak_signal_max_weight`（30）、subject 在本租户 cleared 集合里且不在 escalated 集合里时，权重乘 `cleared_weight_factor`（0.25）。决定在下次 `ingest` 重评时生效，不改 POST 接口。
- 改动：
  - `vetting/store/repositories.py:ReviewRepository.reviewer_subjects` — 按租户、每个 identity 的最新决定，返回 `{"cleared": {...}, "escalated": {...}}` 的 subject 集合。
  - `vetting/scoring.py:ReviewerHistory` / `apply_reviewer_history` — 上述降权规则，`CLEARED_NOTE = "previously cleared by reviewer"`。
  - `vetting/pipeline.py:Pipeline._reviewer_history` / `evaluate_all` / `evaluate` — 每轮取一次历史，评估后调用降权，再 `scoring.score`。
  - `vetting/models.py:Finding.annotations` — 新增字段并进 `to_dict` / `from_dict`。
  - `vetting/timeline.py` — 注释附在 finding 的时间线行末 `[previously cleared by reviewer]`。
  - `vetting/settings.py:FeedbackSettings` + `_SECTIONS` 加 `feedback`；`config/default.toml [feedback]`。
- 关键测试：
  - `tests/test_feedback.py::test_cleared_vpn_asn_softens_the_next_lone_vpn_candidate` — 同 ASN 的下一个单 VPN 申请者从 `RECOMMENDED` 变 `NONE`，`vpn_hosting_ip` finding 与 evidence 仍在，`annotations` 含 `previously cleared by reviewer`，disposition 历史仍可查。
  - `::test_escalated_value_is_never_softened` — 同值有人 escalated，下一个人仍 `RECOMMENDED`。
  - `::test_strong_combinations_and_other_tenants_are_unaffected` — 多信号的人仍 `HIGHLY_RECOMMENDED`；globex 租户不受 acme 的 cleared 影响。

### 逐阶段
| 分钟 | 做 | 说（英文原句） | 敲（T 编号 + 填好的具体内容） |
|---|---|---|---|
| 10–13 读题+Grill | 看 `api/reviews.py:post_disposition` 与 `dispositions` 表；T4 定术语 "pattern" = 具体的值（subject） | "Let me pin 'the same benign pattern': the specific value, this VPN's ASN or this phone number, not the whole signal." | T4；T2 原提示词。问面试官：Q1 "Should a cleared value hide the finding, or weigh less but stay visible?" → 保留证据、降权、标注。默认：降权不隐藏。Q2 "What if another reviewer escalated the same value?" → 不能被洗白，同值 escalated 就不降权。默认：escalated 优先。Q3 "What about people with several signals?" → 不受影响，只对单一弱信号降权。默认：单弱信号。其余说 "I'll assume tenant-local, takes effect at the next ingest, and the factor is config." |
| 13–16 方案 | T3 + T5 | "The seam is the scoring step in Pipeline.evaluate; dispositions and Finding.subject are already there. Option A: soften a lone weak finding on a cleared value and keep the evidence. Option B: lower the vpn_hosting_ip weight globally. I'll take A, B lets one cleared candidate launder the whole signal." | T3：`Here's my list: soften by Finding.subject, not by signal; keep the finding and annotate it; only a lone weak finding; escalated value never softened; tenant-local; factor in [feedback] config. What did I miss? Add only what's missing, ranked by user impact. Don't rewrite mine.`（应补：取每个 identity 的**最新**决定；`[feedback]` 要进 `_SECTIONS`）；T5：`I think the seam is vetting/scoring.py called from Pipeline.evaluate (existing inputs: Finding.subject, ReviewRepository.dispositions). Compare softening in scoring vs checking dispositions inside each signal in 5 lines each. Recommend one. Don't edit anything.`；M1 = 单 `vpn_hosting_ip` + ASN；M2 = 标注、`[feedback]`、组合与租户测试；M3 = escalated 优先、号码级放行。 |
| 16–30 M1 | plan mode → 红 → 绿 → 演示 | "Failing test first: clear Morgan, re-ingest, and Morgan's lone VPN finding should drop a tier but stay visible." | T7 红：`Write ONE failing test through the API in tests/test_feedback.py: with the client fixture, POST {"decision":"cleared"} to /reviews/greenhouse:40104/disposition (40104 has only a vpn_hosting_ip finding, asn:AS64500), re-run ingest, then GET the review: recommendation == "NONE" and findings still contains signal vpn_hosting_ip. Literals. Show it fails.`（红的原因：recommendation 仍是 `RECOMMENDED`）。T7 绿：`Minimal change: a ReviewRepository method returning cleared subjects per tenant from each identity's latest disposition; in scoring, soften a lone finding whose subject is in that set; call it from Pipeline.evaluate; keep the finding. No global weight changes; leave api/ and legacy/ alone. Run that test file.` |
| 30–40 M2 | 标注、`[feedback]`、escalated、组合、租户 | "M2 is where laundering shows up, so the next tests are escalated, a strong combination, and the other tenant." | T7 红 ×2（一次一个）：`Write ONE failing test: a value cleared by one identity and escalated by another must not soften the next lone applicant on it.`；`... a candidate with voip_phone plus resume_name_mismatch plus the cleared ASN stays HIGHLY_RECOMMENDED; the same ASN in tenant globex is not softened.` 若改了 `ingest` 后别的测试变红 → T8。 |
| ~40 审查 | T10 一轮 | "One doubt round now; I'll take one and reject one." | T10 原提示词。典型 v1 的两条：(1) SQL 取"任一 cleared"而不是每人最新决定，或没带 `tenant_id` → 有效且要改：`reviewer_subjects` 用每个 identity 的 `MAX(id)`、查询带租户，租户隔离是安全产品的硬伤；(2) 建议 "要求 N 次 cleared 才降权 / 加过期" → 有效但接受：v1 一次即可，写进 known gaps，不加范围。 |
| 42–45 收尾 | T11 + T12 | "Fresh run: N passed. Here's the real output through the CLI." | T11：`python -m pytest -q`（64 passed）；`python -m vetting --db $DB ingest fixtures --tenant acme` → `review greenhouse:40104 --tenant acme` 先看到 `recommendation: RECOMMENDED  score: 20`；用 `vetting.api.testing.TestClient(create_app(DB), token="tok-acme-reviewer")` 对 `/reviews/greenhouse:40104/disposition` POST `{"decision":"cleared","note":"corporate VPN"}`（返回 `201`）；再 `ingest fixtures` → `review greenhouse:40104` → `recommendation: NONE  score: 5`，且两行 `vpn_hosting_ip: IP address belongs to a VPN network (ExampleVPN, AS64500) [previously cleared by reviewer]`（证据保留）。T12 写 NOTES.md。 |
| 45+ 讲解 | §5.3 | "Reviewer decisions now teach the system about specific values, but a cleared value never launders a combination or an escalated one." | 要能讲清为什么限定"单弱信号 + escalated 优先"。 |

### 追问与答
- "An attacker gets one fake candidate cleared, then reuses the same VPN?" 只降这一个弱信号的权重，finding 与证据仍在；他再带第二个信号就不降权；同值只要有人 escalated 就一律不降。还可加过期与最少 cleared 次数。
- "How would you roll this out safely?" 先只标注不降权，观察一周对比；再按租户灰度，系数在 `[feedback]`。
- "What if two reviewers disagree?" 每个 identity 取最新决定；跨 identity 同值只要有 escalated 就优先，所以分歧时偏安全。
- "How would a reviewer see why a score changed?" finding 与 evidence 保留，时间线行末有 `[previously cleared by reviewer]`；`GET /reviews/<id>` 的 `annotations` 同样可见。
- "What does 'the same pattern' mean for a Google Voice number?" 现在是号码本身（`phone:+1…`），不是运营商；运营商级放行容易被滥用，所以不做。
- "What is missing?" 过期与最少 cleared 次数、撤销路径（cleared 后又 escalated 的处理只靠最新决定）、按岗位或部门细分。

### 翻车点
- 把 `vpn_hosting_ip` 权重调低或加全局开关 → 违背"具体的值"，一个 cleared 的假候选人洗白整个信号，也动了全局 `[weights]`。
- 任何 cleared 就降权，不看单弱信号、escalated → 强信号组合被压低，被 escalated 的值被洗白。
- 删除 finding 而不是降权标注 → reviewer 失去证据，无法审计。
- 取 cleared 的 SQL 不带 `tenant_id` → globex 的决定影响 acme，破坏租户隔离。
