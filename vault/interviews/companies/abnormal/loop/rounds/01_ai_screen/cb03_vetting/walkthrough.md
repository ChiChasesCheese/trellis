# walkthrough.md · cb03_vetting 的参考 60 分钟

> 一次模拟 = 探索（~10 min）+ 一张 ticket（~35 min）+ walkthrough（~8 min）+ 反问。在练习副本里跑：`python3 loop/ai_screen.py start cb03 t1`。
> 下面的命令都在练习副本根目录执行；`DB=/tmp/vetting-practice.db`。
> 口播英文，解释中文。口播是"模板"，用你自己的话说，关键是**每一句都是结论**，不是念文件名。

---

## ① 探索 10 分钟

### 1.1 先自己看（终端 2，与 Claude 并行，约 2 分钟）
```
python -m pytest -q                                         # 绿，~1 s
python -m vetting --db /tmp/vetting-practice.db ingest fixtures --tenant acme
python -m vetting --db /tmp/vetting-practice.db review greenhouse:40120 --tenant acme
```
注意 CLI 会打印 `metric ...` 计数和 `skipping bad record` 警告：这说明坏记录是**计数后跳过**，是后面要学的约定。

### 1.2 给 Claude Code 的提示词（顺序执行；每条都要求引用文件）
1. **E1 地图**："Map the architecture of this repo: entry points (CLI and HTTP), the main data flow from raw files to a reviewer-facing review, the core domain models, and the extension points (registries, base classes). Cite files and symbols. Keep it under 25 lines."
2. **E2 约定**："What conventions does this codebase follow for configuration, persistence and migrations, tenancy, error handling, logging and metrics, time handling, and tests? Give one canonical example file for each. Read CONTRIBUTING.md and tell me where README.md disagrees with the code."
3. **E3 过时/遗留**："Which parts of this repo are deprecated, dead or misleading? I want to know what I must not extend. Show evidence (imports, comments, tests)."
4. **E4 一条数据的旅程**："Trace one application, greenhouse:40120, from fixtures/ to what GET /reviews/<id> returns, function by function. Where are values normalized, and where are they stored as submitted?"
5. **E5 扩展点**："List every registry or base class a new feature could hang on (sources, signals, lookups, settings sections) and what a new member must provide: name, weight, config, tests, imports."
6. **E6 租户**："How is tenant isolation enforced in storage, config, and the API? Show the exact lines. Is there any query that is not tenant-scoped?"
7. **E7 测试约定**："How are tests organised and what helpers exist in tests/conftest.py? Show me the closest existing test I should mirror for a new signal and for a new source."
8. （拿到 ticket 后）**E8 定位**："Given this ticket: <paste>. Which existing modules and abstractions would a change like this touch, and is there an existing feature that is the closest precedent? Do not write code yet."

> 官方："Candidates who only use AI to write code leave signal on the table"。探索也用 AI，但结论要你自己说出口。

### 1.3 第 10 分钟的 60 秒心智模型（口播）
"Here is my mental model. Data comes in through **sources**, registered with a decorator: Greenhouse for applications and the identity provider for pre-boarding sign-ins. Each record becomes an **Identity** plus **Observations**, stored as submitted with a `raw_ref` back to the record, in SQLite with numbered migrations; every repository call is tenant-scoped. **Signals** are the extension point for detection: each is a registered class that gets a context of observations, lookups and settings, and returns a Finding with weighted, cited evidence. Weights and thresholds are per-tenant config. **Scoring** sums findings into a recommendation tier, **timeline** renders the cited evidence, and a small WSGI API exposes reviews and reviewer dispositions. Anything that compares values goes through `normalize.py`. `Pipeline.ingest` re-evaluates the whole tenant each run. Two things I'll avoid: `legacy/blocklist.py` is deprecated and unwired, and the README's mention of a weights module is stale: weights live in `config/default.toml`. The risk I see is false positives: a reviewer is a person, so I'll keep defaults conservative."

---

## ② 三张 ticket

### t1 · Coordinated applicants

**读完 ticket 后的 3 个澄清问题**（口播）
1. "Which identifiers should count as a connection: phone, IP, email, resume file? And at what granularity, say the phone block or the IP /24?"
2. "A shared value like an office NAT or a recruiter's phone is common. Should one shared value alone ever raise someone, or do I need two kinds of overlap?"
3. "Is this within one customer only, or across customers? I'll assume within the tenant for v1 and write down how cross-tenant would work."

**显式假设**（写进 NOTES.md 并说出来）
- 范围：只在本租户内；v1 不做传递关联。
- 关联 = 至少两类标识重合（电话号码块、IP /24、简历指纹、归一化邮箱）；单个共享值不定罪。
- 号码块位数、最少重合类数、允许名单都在配置里，所以容易改。
- 输出是一个新的 signal，它的 finding 引用对方 identity，reviewer 在现有接口里直接看到。

**里程碑**
- M1（≤ 15 min，可演示）：`coordinated_applicants` signal + `normalize.phone_prefix`，用 `list_by_kind` 取本租户观测，电话块 + /24 两类重合就出 finding；配置里加权重。演示：`ingest fixtures --tenant acme`，`review greenhouse:40111`，看到指向 40112/40113 的证据。
- M2：补简历指纹（sha256、作者+工具）与邮箱；`[correlation]` 配置段（块位数、最少类数）；测试"共享办公室 IP 的两个正常人不被提升"。
- M3：允许名单（CIDR）、时间线检查、跨租户设计说明。

**给 Claude 的实现提示词（plan mode）**
"Plan the smallest change that raises applicants who look like nodes of one campaign. Constraints: add a new Signal in vetting/signals/ following voip_phone.py (use @register_signal, build the Finding with Signal.finding() and Citations); read other applicants through ctx.store.observations.list_by_kind, not find(), because stored values are as-submitted; compare only after vetting/normalize.py (phone_e164, ip_prefix24, email_key) and add phone_prefix there; weight goes in config/default.toml and any new config section must be added to vetting/settings.py; do not touch vetting/legacy; tests go in tests/ in the style of tests/test_signals.py. Require at least two kinds of identifier to overlap. List the files you will change and the test cases first."

**审 AI 输出时看什么（right altitude）**
- 方法：挂在 `@register_signal` 上吗？还是新建了一个"correlator"类/模块、一张关联表？
- 集成：用了 `normalize.py` 吗？有没有自己写 `re.sub(r"\D", ...)`？权重在 `default.toml` 吗？`[correlation]` 加进 `settings.py` 了吗？
- 覆盖：共享办公室 IP 的正常人？跨租户？号码格式变体？最后一个人入库后前面的人也更新了吗？
- AI 常见误用：`ObservationRepository.find(kind, value)` 做精确匹配；把 user agent / 常见简历工具当关联；用字符串包含判断。

**如何验证**
```
python -m pytest -q
python -m vetting --db $DB ingest fixtures --tenant acme
python -m vetting --db $DB review greenhouse:40111 --tenant acme   # 应看到 40112 / 40113 的证据行
python -m vetting --db $DB review greenhouse:40106 --tenant acme   # 共享办公室 IP 的人，不应有 coordinated_applicants
```

**收尾说的 known gaps（口播）**
"Known gaps: it's a scan over the tenant's observations per applicant, fine for thousands but I'd store a normalized key and index it at 10x. It doesn't follow chains where A matches B and B matches C but A doesn't match C. Cross-tenant correlation is deliberately out: it needs a privacy and contract decision, and I'd expose only 'seen at other organizations' as a hashed indicator. The allowlist for known agency numbers is config-only today."

---

### t2 · Workday as a source

**3 个澄清问题**
1. "By 'duplicate application' do you mean the same application id delivered twice, for example across pages?"
2. "When a record lacks a field like email, should I drop the whole record or just that observation and still analyze the rest?"
3. "Should Workday get its own signals or weights, or should the existing signals just work on it?"

**显式假设**
- 重复 = 同一个 `Job_Application_ID`：同一个 identity、证据不翻倍。
- 缺字段：只跳过那条观测并计数；无法识别 id/时间的整条记录才算 bad record。
- 不新增信号、不改权重：映射到现有 `Kind`，已有 signals 自然生效。
- 时间统一 UTC；分机不进号码。

**里程碑**
- M1（≤ 15 min）：`sources/workday.py`，读 `applications.json`，映射姓名/邮箱/电话/IP/简历元数据，`@register_source` + import；演示：ingest 只含 `workday/` 的目录，`GET /reviews`（或 CLI `review workday:JA-100234`）里 Sam 有 `voip_phone`。
- M2：沿 `Paging.next` 读完所有页；重复幂等；缺字段/缺 id 计数；`SOURCE_LABELS` 加 Workday。
- M3：greenhouse 回归（两个源同目录）；更新测试里的身份数。

**给 Claude 的实现提示词**
"Plan a new Source for Workday. Follow vetting/sources/greenhouse.py exactly in structure: subclass Source, @register_source, yield Ingested(identity, observations) built with Source.observe(), and use Source.bad_record() for records we cannot identify. Use Identity.make_id('workday', Job_Application_ID), timeutil.parse_ts for the offset timestamps, and keep raw_ref free of page numbers so redelivered applications dedupe on insert. Join Country_Code and Phone_Number into one phone value and do not append the extension. Follow Paging.next across files. Do not touch signals/, pipeline.py or legacy/. Register it in sources/__init__.py and add the label to timeline.SOURCE_LABELS. Add tests in tests/ mirroring tests/test_sources.py."

**审 AI 输出时看什么**
- 方法：它是不是把 Workday 转成 Greenhouse JSON 再喂旧 source？是不是在 pipeline/signals 里加了 `if source == "workday"`？
- 集成：`@register_source` + `__init__` import；`observe()` / `bad_record()`；`parse_ts`；`make_id`；`SOURCE_LABELS`。
- 覆盖：重复、缺邮箱、无 id 的记录、第二页、偏移时区。
- 误用：`datetime.strptime(...)` 手写偏移；`raw_ref` 里放页码；把 `Extension` 拼进号码。

**如何验证**
```
python -m pytest -q
mkdir -p /tmp/wd && cp -r fixtures/workday /tmp/wd/
python -m vetting --db $DB ingest /tmp/wd --tenant acme
python -m vetting --db $DB review workday:JA-100234 --tenant acme   # voip_phone，来源 workday，17:22 UTC
python -m vetting --db $DB ingest fixtures --tenant acme            # greenhouse 的人不变
```

**known gaps**
"Gaps: it reads exported files, not the Workday API, so there's no incremental sync or retry. If Workday renames a field we'd see the missing-field counters jump but nothing alerts on it yet. The `next` cursor is followed with a loop guard but there's no pagination limit. And a person who re-applies under a new application id is a separate identity by design; linking them is the correlation feature."

---

### t3 · Learn from reviewer decisions

**3 个澄清问题**
1. "By 'the same benign patterns', do you mean the specific value, such as this VPN network or this number, rather than the whole signal?"
2. "Should a cleared pattern hide the finding, or keep it visible but weigh less so a reviewer can still audit it?"
3. "What if another reviewer escalated the same value? I don't want a cleared decision to launder an attacker."

**显式假设**
- 按具体值（`Finding.subject`）降权，不关闭信号、不动全局权重。
- 保留 finding 与证据，标注 "previously cleared by reviewer"；只在本租户内生效。
- 只对**单一的弱信号**降权；多信号组合不受影响；同值被 escalated 过则不降权。
- 系数与"弱"的上限放配置。

**里程碑**
- M1（≤ 15 min）：从 dispositions 取"最新决定为 cleared"的 subject 集合；单一 `vpn_hosting_ip` finding 的 ASN 在其中则降权；演示：A 被 cleared 后 ingest B，B 从 RECOMMENDED 变为 NONE，finding 仍在。
- M2：标注、`[feedback]` 配置、组合与租户测试。
- M3：escalated 优先、号码级放行的测试。

**给 Claude 的实现提示词**
"Plan a reviewer-feedback adjustment at the scoring layer. Constraints: reviewer decisions are in the dispositions table via ReviewRepository (append-only; use the latest decision per identity); the specific value a finding fired on is Finding.subject; add a repository method that returns, for one tenant, the subjects of cleared and of escalated identities; apply the adjustment in or next to scoring.score, called from Pipeline.evaluate, not inside signals; only soften a finding when it is the only finding, is weak (config), and its subject was cleared and never escalated; keep the finding and its evidence and add an annotation 'previously cleared by reviewer'; new config goes in a [feedback] section registered in settings.py; no global weight changes; leave api/ and legacy/ alone; tests mirror tests/test_pipeline.py. List the files and test cases first."

**审 AI 输出时看什么**
- 方法：它是不是把 `vpn_hosting_ip` 权重调成 0 或加"跳过信号"的开关？是不是在 `signals/*` 里查 disposition？
- 集成：租户过滤？取"最新"决定还是任一？配置还是魔法数？
- 覆盖：组合不受影响、escalated 优先、证据保留、其它租户、重复 ingest 结果稳定。
- 误用：SQL 没带 `tenant_id`；把 `note` 文本当匹配条件；POST 里重算全部人。

**如何验证**
```
python -m pytest -q
python -m vetting --db $DB ingest fixtures --tenant acme
# 40104 是唯一一个只有 vpn_hosting_ip 的人：先 cleared，再 ingest 同 ASN 的新申请，看推荐档位变化
python -m vetting --db $DB review greenhouse:40104 --tenant acme
```
（HTTP 决定用 `vetting.api.testing.TestClient` 或 `python -m vetting serve` + curl 带 `Authorization: Bearer tok-acme-reviewer`。）

**known gaps**
"Gaps: one cleared decision is enough in v1; I'd add expiry and a minimum count. There's no revoke path beyond a later escalate. A cleared Google Voice number only helps that exact number, not the carrier, on purpose, since carrier-level clearing is easy to abuse. And the adjustment is recomputed at ingest, so a decision applies from the next evaluation, not instantly."

---

## ③ 常见翻车（照抄 AI 通用写法会怎样不契合）

| 翻车 | 为什么不契合 |
|---|---|
| t1：`find(kind, value)` 精确匹配或手写 `re.sub(r"\D","")` 比较电话 | 值按提交原样存，格式不同就漏；`normalize.py` 已有 `phone_e164` / `ip_prefix24` / `email_key` |
| t1：任何共享值都互相标记（含 UA、简历工具、办公室 IP） | 误报会淹没 reviewer；产品语言是"signals 的组合"，不是单点命中 |
| t1：新建 `correlation.py` + 新表，绕开 `@register_signal` | 权重/阈值/证据/时间线全靠 Finding+Citation 免费得到；平行系统要重做一遍 |
| t1：权重写死在代码里，`[correlation]` 不进 `settings.py` | `ConfigError` 或违背 CONTRIBUTING；租户无法覆盖 |
| t1：改 `legacy/blocklist.py` | 已 deprecated 且不在管线里 |
| t2：把 Workday 转成 Greenhouse JSON 再喂旧 source；或在 signals 里加 `if source == "workday"` | 丢掉来源引用；signals 本该对来源无感 |
| t2：漏掉 `sources/__init__.py` 的 import | ingest 悄悄零身份，没有报错 |
| t2：手写 `strptime`、`raw_ref` 带页码、分机拼进号码 | 时区错、重复投递翻倍证据、号码不匹配 VoIP 库 |
| t2：缺邮箱就丢整条 | 其它信号（简历姓名不符）本来还能工作 |
| t3：把 `vpn_hosting_ip` 权重调低 / 加全局开关 | 违背"按具体值"，攻击者可借一个 cleared 洗白整个信号 |
| t3：任何 cleared 就降权，不看单弱信号、不看 escalated | 强信号组合也被压低；被 escalated 的值被洗白 |
| t3：SQL 没带 `tenant_id`；把其它租户的 cleared 带进来 | 租户隔离被破坏，是安全产品的硬伤 |
| t3：隐藏 finding 而不是降权标注 | reviewer 无法审计，也不满足"证据保留" |
