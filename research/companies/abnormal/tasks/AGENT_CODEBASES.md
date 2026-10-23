# 子代理指令 · Abnormal AI Technical Screen 练习代码库（`loop/rounds/01_ai_screen/cbNN_*`）

> 你是 `sonnet`（或 `opus`）子代理，**不得再派生代理**。你只拥有分配给你的那一个 `cbNN_*` 目录，不碰别的文件。
> 读者 Chi：1.5 年后端（PayPal Braintree：Python/Kotlin、Snowflake/SQL），自建 66K 行 Python 研究平台。岗位 **Abnormal AI · SWE II – Insider Risk**。
> 目标轮次：**AI Technical Screen，60 min**：浏览器 VS Code + Claude Code 预装，在一个**已有 Python 代码库**里：~10 min 探索建立心智模型 → ~35 min 实现一个**故意说不清楚的 feature**（怎么处理模糊性本身被评）→ walkthrough + 反问。
> 官方评分原话：*Judgment* — "evaluate approaches, scope work into milestones, and decide what fits the existing system"；*Agency* — "make decisions, state assumptions, test your own work, keep momentum"；"Strong candidates ship a working v1 that fits the system… notice existing abstractions and patterns and let those inform their approach. They think about the user, not just the code." "AI will produce working code. That's not enough. The bar is whether the code fits the existing system — its patterns, its conventions, its infrastructure. AI doesn't know what's already in the codebase unless you tell it to look."
> **所以你造的代码库的价值 = 让"照抄 AI 的通用写法"和"契合本系统的写法"拉开差距**：正确做法必须依赖代码库里已有的抽象，而 AI 不看就会重造一个。

## 0. 先读

- `../CONVENTIONS.md`（目录形状、验收口径、marker）——**严格照做**。
- `acceptance_conftest.py`（本目录）：原样复制到你的 `acceptance/conftest.py`，只改 `PACKAGE`。

## 1. 恢复规则

开工先 `find <你的目录> -type f | head -100`。已存在且自带测试为绿的部分不重写，只补缺。

## 2. 硬规则（违反即退回）

1. **只用标准库 + pytest**（`sqlite3`、`dataclasses`、`json`、`logging`、`argparse`、`wsgiref`、`http`、`datetime`、`zoneinfo`…）。Python 3.11+ 语法。不联网、不读环境里的真实凭据。
2. **规模**：starter 2,000–3,500 行（`find starter -name '*.py' | xargs wc -l` 实测），25–45 个文件；`starter/tests` 全绿且 `< 5 s`。代码要像一个真实的小团队写的：一致的命名、类型注解、docstring 适量、模块边界清楚、有 `README.md`（架构概览，**故意有一处已过时**）、`CONTRIBUTING.md`（约定）、`fixtures/`（JSON 样本数据）、一个 `python -m <pkg>` CLI、**自己的 `pytest.ini`**（`testpaths = tests`，使代码库在任何父目录下都自成 rootdir）。
3. **埋设计**（写进 `REPORT.md` 的"埋点清单"，每条一行：位置 · 正确做法 · AI 不看代码时的典型错法）：每张 ticket 至少 2 个"必须复用的已有抽象"、1 个"看起来像但不该改的地方"（deprecated 模块、旧 API）、1 个"不问就会做错的模糊点"（answer 在 `interviewer.md`）。
4. **ticket**（`tickets/tN_<slug>.md`）：英文，2–8 行，像真实工单——说用户问题与期望结果，**不说怎么做**；可点名必要的对外接口（命令名 / 端点 / 配置键），这是验收测试唯一允许依赖的新名字。末尾不写提示。
5. **solution/**：= starter 复制后实现全部 ticket，**最小且地道**：复用已有抽象、遵守 CONTRIBUTING、为每张 ticket 新增测试（放在约定位置）。`solution/tests` 全绿。用 `diff -ru starter solution | wc -l` 报每张 ticket 的改动行数（可分步做：先 t1 后 t2…）。
6. **acceptance/**：`conftest.py`（照抄改 PACKAGE）+ `test_t1.py`…；每个测试恰一个 `t1/t2/t3` marker + 恰一个 `core/stretch/regression`。每张 ticket ≥ 5 个 `core`、≥ 1 个 `stretch`、≥ 1 个 `regression`。只经由已有入口与 ticket 点名的接口测试；**不要测内部函数名**，否则合理的不同设计会被误判。starter 上 `core` 必须全红，solution 全绿：
   ```
   cd /home/user/trellis/vault/interviews/companies/abnormal
   uv run --project /home/user/trellis --with pytest python -m pytest loop/rounds/01_ai_screen/<dir>/acceptance -q -p no:cacheprovider
   IMPL=starter uv run --project /home/user/trellis --with pytest python -m pytest loop/rounds/01_ai_screen/<dir>/acceptance -q -p no:cacheprovider -m core
   (cd loop/rounds/01_ai_screen/<dir>/starter && uv run --project /home/user/trellis --with pytest python -m pytest -q -p no:cacheprovider)
   (cd loop/rounds/01_ai_screen/<dir>/solution && uv run --project /home/user/trellis --with pytest python -m pytest -q -p no:cacheprovider)
   ```
7. **interviewer.md**（中文说明 + 英文原句）：每张 ticket 一节：① 面试官心里的"好 v1"长什么样（一段）② 澄清问答表（候选人可能问的 6–10 个问题 → 面试官回答；没问时的默认）③ 隐藏期望（复用哪些抽象，按文件:符号）④ 追问 4–6 个（"what if 10x volume"、"how would you roll this out"、"what's missing"…）⑤ 打分信号表：Judgment / Agency / Fit-the-system / Testing / AI-supervision / Communication 各给 strong · ok · weak 的具体可观察行为。
8. **walkthrough.md**（中文 + 英文口播）：① 探索 10 分钟：按顺序给 5–8 条**真的能用的 Claude Code 提示词**（如 "Map the architecture of this repo: entry points, the main data flow, the extension points. Cite files."），以及第 10 分钟该对面试官说的 60 秒心智模型（英文）② 每张 ticket：读 ticket 后的 3 个澄清问题 → 显式假设清单 → 里程碑 M1/M2/M3（M1 ≤ 15 min 可演示）→ 给 Claude 的实现提示词（点名要复用的文件/抽象）→ 审 AI 输出时看什么（"right altitude"）→ 如何验证（命令）→ 收尾时说的 known gaps。③ 常见翻车（照抄 AI 的写法会怎样不契合）。
9. **REPORT.md**（中文）：Summary · 代码库地图（模块一行一句）· 规模（命令实测：文件数、行数、starter/solution 测试数与耗时）· 埋点清单 · 验收测试清单（每 ticket 各 marker 数，`grep` 实测）· 每 ticket solution 改动行数。
10. 所有数字来自你跑过的命令。不写过程话。完成后回复：目录树（`find -maxdepth 2`）、四条 pytest 命令的最后一行、规模数字、你认为最弱的两处。

## 3. 分配（编排者填）

### cb01_sentinel —— 安全事件处理管线（**一手报道的面试代码库形态，最高优先级**）

一手原文（LeetCode Discuss #8335187，2026-06-15，Abnormal AI screening round）："The repo … processed all security events like collection/ingestion, ranking, threat levelling based on some rules, created alerts, created apis on top of it and put it to database." 报道的两个 feature："allow users to suppress some rules (it can be complex rules like based on geo-ip (existing in code) and other rules)"；"The enrichment layer currently hardcodes based on some threats (geo-ip, history, 1 more) clients want more configurability without touching platform code. Implement a plugin based mechanism"。**照这个形态造，但代码全部原创。**

包名 `sentinel`。多租户（每个事件带 `tenant_id`）。数据流：
- `collectors/`：`Collector` 基类 + 注册表；已有 `auth_log`（登录事件：user, src_ip, user_agent, result）、`endpoint`（进程/文件事件）、`saas_audit`（SaaS 管理操作）；各读 `fixtures/events/<source>/*.jsonl`，`normalize()` → `SecurityEvent` dataclass（id, tenant_id, ts UTC aware, source, kind, user, src_ip, attrs）。坏记录计数并跳过（`metrics.py` 计数器）。
- `enrichment/`：`base.py` 定义 `Enricher` 抽象基类（`name: str`、`requires: tuple[str, ...] = ()`、`enrich(event, ctx) -> dict`，结果并进 `event.enrichment[name]`）；已有 `GeoIpEnricher`（读 `fixtures/intel/geoip.json`：CIDR → country/city/lat/lon/asn）、`HistoryEnricher`（查 db：该用户过去见过的国家/IP/设备，first_seen）、`ThreatIntelEnricher`（`fixtures/intel/bad_ips.json` 等）。**但 `service.py` 的 `EnrichmentService.enrich()` 是硬编码的**：按固定顺序 if/else 调三个，history 依赖 geo 的结果，注释 `# TODO(platform): make enrichment configurable per tenant`。基类存在但没有被用于发现/注册——这是 t2 的"已有抽象"。
- `rules/`：`Rule` 基类 + `@register_rule` 注册表；已有 `impossible_travel`（用 geo + history，速度 > 阈值 km/h）、`new_country_login`、`known_bad_ip`、`brute_force`（窗口内失败次数，用 `timeutil.sliding_window`）、`rare_admin_action`。每条返回 `RuleHit(rule_id, severity, reason, evidence)`。规则阈值来自 config。
- `threat.py`：把 hits 合成 `ThreatLevel`（LOW/MEDIUM/HIGH/CRITICAL）。`ranking.py`：告警排序分 = 严重度权重 × 资产重要性（`fixtures/assets.json`：用户/主机 criticality）× 时间衰减。
- `alerts/`：`Alert` dataclass（id, tenant_id, rule_ids, threat_level, score, status OPEN/ACKED/CLOSED, created_at, event_ids）；`AlertService.create_from(event, hits)`；`AlertRepository`（sqlite）。
- `db/`：sqlite 连接、`migrations/0001_init.sql…` + 迁移器（启动时按序应用）、repositories（所有查询带 tenant_id）。
- `api/`：标准库 WSGI 迷你框架（`router.py` 的 `@route`、`request/response`、`errors.py` 统一 JSON 错误形状、Bearer token → tenant 的中间件，token 在 `fixtures/tokens.json`）、`testing.py` 的 `TestClient`；已有 `GET /alerts`（分页、按 score 排序）、`GET /alerts/<id>`、`POST /alerts/<id>/ack`、`GET /events/<id>`。
- `config/`：`tomllib` 读 `config/default.toml` + `config/tenants/<tenant>.toml` 覆盖，`Settings` dataclass + 校验。
- `pipeline.py`：`Pipeline.run(events) -> list[Alert]`（collect → enrich → rules → threat → alert → store）。CLI：`python -m sentinel ingest fixtures/events --tenant acme`、`python -m sentinel alerts --tenant acme`、`python -m sentinel serve`。
- 噪音：`legacy/static_rules.py`（deprecated 的旧规则 DSL，README 架构图还画着它）；README 里一处过时（如说"enrichment is pluggable" 但实际硬编码，或命令名过时）。

ticket：
- **t1_rule_suppression**："Customers keep asking us to mute specific detections — e.g. impossible-travel alerts for staff who work through a corporate VPN egress in another country. Let customers suppress rules." 点名接口：`POST /suppressions`（JSON：`rule_id` 必填，可选匹配条件，如 `{"rule_id": "impossible_travel", "match": {"geo.country": "DE"}}`；字段路径语义是候选人的设计，但 ticket 给出这一个例子，验收只用例子里的形状 + `rule_id` 单独一项）、`GET /suppressions`、`DELETE /suppressions/<id>`。隐藏期望：存 db（新 migration），租户隔离，在规则命中之后、建告警之前过滤（不改每条规则），匹配能用 enrichment 字段（geo）与事件字段（user、src_ip CIDR）；被抑制的命中留痕（审计/计数，模糊点：丢弃还是存为 SUPPRESSED）；可选过期时间（stretch）；判断力：CRITICAL / known_bad_ip 是否允许抑制（问了才知道：面试官答"allow but warn"或"never"——写在 interviewer.md，验收不依赖）。验收：抑制后对应事件不产生 OPEN 告警；其他租户不受影响；不匹配条件的同规则事件仍告警；只给 `rule_id` 时整条规则静音；非法 rule_id → 400 走已有错误形状；DELETE 后恢复告警。
- **t2_enrichment_plugins**："Enrichment is hardcoded to geo-ip, history and threat intel. Customers want to choose which enrichers run for them and plug in their own, without us touching platform code. A customer enricher is a Python file implementing our existing `Enricher` interface, dropped into a directory listed in their tenant config under `[enrichment] plugin_dirs`; they enable enrichers by name with `[enrichment] enabled = [...]`." 隐藏期望：用已有 `Enricher` 基类做发现（扫描 plugin_dirs 中的子类 / 注册表），内置三个也走同一机制；按 `requires` 拓扑排序（history 依赖 geo）；某个插件抛异常不拖垮管线（记录 + 计数，继续）；未知名字启动时报配置错误；租户间插件隔离；规则读 `event.enrichment[<name>]` 不变。验收：tmp 目录写一个 `Enricher` 子类插件（如 `asn_owner`），租户配置启用后事件上出现其结果；未启用则不出现；禁用 `geo_ip` 后 `impossible_travel` 不再触发（或优雅跳过）不崩；插件抛异常时其余告警照常；`requires` 顺序正确（插件依赖 geo 的输出）。
- **t3_alert_dedup**："Analysts say the alert queue is flooded with repeats — one brute-force source produces dozens of alerts an hour. Make the queue usable. An alert should show how many events it covers (`event_count`)." 隐藏期望：在 `AlertService` 里按去重键（tenant + rule set + user/src_ip，模糊点）在时间窗内合并（窗口来自 config），更新 `event_count`、`last_seen`、`event_ids`，威胁等级取最大；ACKED/CLOSED 之后的新事件开新告警（模糊点）；ranking 考虑 event_count（stretch）；`GET /alerts` 返回 `event_count`。验收：同源 brute-force 夹具在窗口内只产生 1 个 OPEN 告警且 `event_count` 正确；不同用户不合并；窗口外开新告警；ack 后新事件开新告警；API 列表含 `event_count`。

### cb02_insiderwatch —— Insider Risk 平台（通用 insider-risk 领域：数据外泄 · 基线 · 告警归并 · 新数据源）

包名 `insiderwatch`。数据流：`connectors/`（基类 `Connector`：`fetch(since) -> Iterable[RawRecord]`（分页游标）+ `normalize(raw) -> Event | None`；已有 `m365_audit`（Microsoft 365 统一审计日志样式）、`okta`（登录）、`slack_audit`，各自读 `fixtures/raw/<source>/*.json`）→ `events.Event` dataclass（user, ts(UTC aware), action 枚举：`FILE_DOWNLOAD/FILE_SHARE_EXTERNAL/EMAIL_FORWARD_EXTERNAL/LOGIN/…`, bytes, target, source, attrs）→ `baselines/`（每用户每动作的滚动日统计：均值/标准差/分位，存在 sqlite，`BaselineStore` 有 `update(events)` 与 `get(user, action)`；冷启动规则）→ `signals/`（基类 + `@signal` 注册表；已有：`unusual_login_location`、`volume_spike`（对 baseline 的 z-score）、`off_hours_activity`）→ `scoring.py`（signal → 风险分，带权重与时间衰减，权重在 `config.py`）→ `alerts/`（`Alert`、`AlertStore`）→ `notify/`（`Notifier` 协议：`ConsoleNotifier`、`SlackWebhookNotifier`（stub，写到 outbox 表））。`hr/`：HR 名册（`fixtures/hr/roster.json`：员工、经理、部门、`termination_date` 可空、`resignation_submitted` 日期）。`timeutil.py`：时区、窗口、business hours。`legacy/dlp_rules.py`（deprecated）。CLI：`python -m insiderwatch replay fixtures/raw --until 2026-09-30`、`python -m insiderwatch alerts --user ...`。
- **t1_departing_exfil**："Most data theft happens in the weeks before someone leaves. Flag employees who are taking data on their way out." 隐藏期望：HR 名册（`resignation_submitted`/`termination_date`）+ 既有 baseline（相对本人基线而不是全局阈值）+ signal 注册表 + 已有动作枚举（下载、外部分享、转发到个人邮箱）+ scoring 权重在 config。模糊点：窗口多长（离职前 N 天，N 在 config）、"带走数据"包括哪些动作、没有基线的新人、已离职后仍有活动（应更严重）。
- **t2_alert_cases**："Analysts are drowning — one bad actor generates 40 alerts a day. Group them so an analyst sees one thing per incident." 点名接口：CLI `python -m insiderwatch cases [--user U]`。隐藏期望：新 `Case` 用 store 的 sqlite 与迁移约定；按用户 + 时间窗合并（窗口在 config）；case 严重度 = 成员最大（或分数和，模糊点）；case 关闭后的新 alert 开新 case；通知只在 case 新建/升级时发（复用 Notifier，不要每个 alert 都发）。
- **t3_gdrive_connector**："We're onboarding a customer on Google Workspace. Add Google Drive audit logs as a source." 给出 `fixtures/raw/gdrive/*.json`（starter 里就有，Google Admin Reports API 样式：`items[].id.time` RFC3339、`events[].name` 如 `download`/`change_user_access`/`change_document_visibility`、`parameters[]` 键值列表、`nextPageToken` 分页）。隐藏期望：照 `Connector` 基类与已有 connector 的结构写；映射到已有 `Action` 枚举（外部分享 = visibility 变为 `people_with_link`/`public_on_the_web` 或 target 是外部域）；未知事件丢弃并计数（照已有 connector 的日志/指标做法）；在 connector 注册处登记、CLI replay 自动包含；分页；时区。

### cb03_vetting —— 候选人身份欺诈检测（Chi 要进的团队的真实产品：Infiltration Prevention）

官方产品页原文（`catalog/raw/official.md` O-1/O-4）："detect synthetic personas and nation-state actors using signals from Workday or Greenhouse, identity providers, and email"；信号示例 `voip_phone`（"Phone number resolves to a VoIP line"）、"Name in resume differs from application name"、"IP geolocation mismatches"、"shared phone prefixes, overlapping IP ranges, and identical infrastructure patterns"；"For every flagged identity, Abnormal builds an evidence timeline … each signal cited with its source"；UI 分档 "Highly Recommended / Recommended / None"，disposition "Security review recommended — Routed for human security review"；"It does not make any decisions in hiring"。JD："correlation engines that match candidate details (IPs, phone numbers, email history, resume metadata) against known indicators"。

包名 `vetting`。多租户（每个客户组织）。数据流：
- `sources/`：`Source` 基类 + 注册表；已有 `greenhouse`（`fixtures/greenhouse/applications/*.json`：application id、candidate 姓名、email、phone、地址/国家、提交时 IP、user agent、resume 附件元数据：文件名、作者、创建工具、页数、提取出的姓名/邮箱/电话、`sha256`）、`idp`（`fixtures/idp/*.jsonl`：入职前账户的登录：ip、device、geo）。规范化成 `Identity` + `Observation`（identity_id, kind, value, source, ts, raw_ref）。
- `lookups/`：可注入的外部查询（假实现读 `fixtures/intel/*.json`）：`phone.py`（号码类型 MOBILE/LANDLINE/VOIP、运营商、国家）、`ip.py`（geo、asn、是否 VPN/hosting）、`email.py`（域名年龄、是否一次性邮箱、是否见于泄露）。带简单缓存（`cache.py`，TTL）。
- `normalize.py`：电话 E.164、邮箱（大小写、Gmail 点号/加号）、姓名（大小写、空白、变音符）、IP → /24 前缀。**t1 必须复用**。
- `signals/`：`Signal` 基类 + `@register_signal`；已有 `voip_phone`、`ip_geo_mismatch`（申请国家 vs 提交 IP / idp 登录国家）、`resume_name_mismatch`、`disposable_email`、`vpn_hosting_ip`。每个返回 `Finding(signal, weight, summary, evidence=[Citation(source, ref, ts)])`。权重在 config。
- `scoring.py`：findings → 分数 → `Recommendation`（HIGHLY_RECOMMENDED / RECOMMENDED / NONE，阈值在租户 config）。
- `timeline.py`：按时间把 application 事件 + findings 渲染成证据时间线（每条带 source 引用）。
- `store/`：sqlite + migrations + repositories（`IdentityRepository`、`ObservationRepository` 有按 (kind, value) 的索引查询、`ReviewRepository`）。
- `api/`：标准库 WSGI 迷你框架（同 cb01 风格但独立实现：router、errors、Bearer token → tenant、`TestClient`）；已有 `GET /reviews`（列表，分档过滤）、`GET /reviews/<identity_id>`（含 timeline）、`POST /reviews/<identity_id>/disposition`（安全团队标记 cleared / escalated）。
- `config/`：`tomllib`，default + tenant 覆盖。CLI：`python -m vetting ingest fixtures --tenant acme`、`python -m vetting review <identity_id>`、`python -m vetting serve`。
- 噪音：`legacy/blocklist.py`（deprecated 的静态黑名单），README 一处过时。

ticket：
- **t1_coordinated_applicants**："What looks like one suspicious applicant is usually one node in a campaign — the same operators apply many times under different names. Surface those connections to the security reviewer." 隐藏期望：用 `normalize.py` 归一后在 `ObservationRepository` 上做关联（同 E.164 号码、同号码前缀（如前 N 位，N 在 config）、同 /24 IP、同 resume sha256 / 同作者+工具指纹、同归一化邮箱）；作为新 signal 注册（权重进 config），证据带引用；**判断力**：共享常见值（大公司 NAT IP、大学网段、同一个招聘代理商的电话）不能单独定罪——需要两类以上重合或排除 allowlist（模糊点）；跨租户关联（官方说 "correlated across organizations"）是否允许——隐私/合同问题，面试官默认"v1 只做本租户，说明跨租户的设计"。验收（只走已有入口）：夹具里一组 3 个不同姓名、共享号码段 + /24 + resume 指纹的申请，ingest 后每个人的 `GET /reviews/<id>` 推荐等级提升且 timeline/findings 里能看到指向另外两人的证据（检查其它 identity_id 出现在 findings 的 evidence 里）；只共享一个常见公司 IP 的两个正常候选人不被提升；其他租户的同号码不关联（v1 默认）。
- **t2_workday_source**："We're onboarding a customer that uses Workday instead of Greenhouse. Add Workday as a source." 给出 `fixtures/workday/*.json`（starter 里就有：不同字段名、嵌套结构、`Phone_Number` 带分机/国家码分离、时间是 `2026-09-14T10:22:00.000-07:00`、简历元数据在 `Attachments[]`、分页 `next` 游标、一条缺邮箱、一条重复投递）。隐藏期望：照 `Source` 基类与 greenhouse 的结构写并注册；产出同样的 `Identity`/`Observation`，使所有已有 signals 不改代码就生效；复用 `normalize.py`；重复投递幂等；缺字段不崩（计数 + 跳过该观测，不是整条丢弃）；时区转 UTC。验收：ingest Workday 夹具后，其中一个 VoIP 号候选人得到 `voip_phone` finding；时间线的 source 标为 workday；重复投递不产生两个 identity；缺邮箱的记录仍有其它 findings；greenhouse 行为不变（regression）。
- **t3_reviewer_feedback**："Security reviewers clear a lot of candidates we flag — mostly people on a corporate VPN or using Google Voice legitimately. Use their decisions so we stop re-flagging the same benign patterns." 隐藏期望：用已有 `POST /reviews/<id>/disposition` 的数据（`ReviewRepository`）；在 scoring 层按租户对"被 cleared 过的具体值"（某 VPN ASN、某号码）降权或抑制，而不是全局关掉 signal；保留证据但标"previously cleared by reviewer"（透明，可审计）；**判断力**：别让攻击者"洗白"——被 escalated 的同值不降权，降权只对单一弱信号，强信号组合不受影响（模糊点，stretch）。验收：某 ASN 的 VPN 候选人被 cleared 后，新的、同 ASN、仅此一个弱信号的候选人推荐等级下降；同时有 VoIP + 姓名不符的候选人不受影响；其他租户不受影响；disposition 历史仍可查（regression）。

### cb04_quarantine —— 钓鱼邮件隔离服务：修埋好的 bug + 推到生产可用（题型：fix-the-codebase，HI Schedulr/Transcribe 同类）

> 题型说明：开放式面试最常见的一类是"这个服务带着埋好的 bug，找到并修好，然后按你的判断推向 production-ready"。这一题专练：先建反馈回路再修（Prove-It）、bug 清单分级、加固时的取舍、收口（点名的要么做完要么写进 known gaps）。

包名 `quarantine`。多租户。数据流：
- `intake/`：用户在邮件客户端点"Report phishing"→ `POST /reports`（message_id、reporter、headers、links、attachments 元数据）；`Report` dataclass；去重键 = (tenant, message_id)。
- `analyzers/`：`Analyzer` 基类 + `@register_analyzer`；已有 `sender_reputation`、`link_reputation`（查 `lookups/url.py` 假实现读 `fixtures/intel/urls.json`）、`attachment_type`、`display_name_spoof`。每个返回 `Verdict(analyzer, score 0–100, reasons)`。
- `decision.py`：verdict 聚合 → `Disposition`（QUARANTINE / RELEASE / NEEDS_REVIEW，阈值在租户 config）。
- `actions/`：`Mailbox` 接口 + `FakeMailbox`（内存，记录调用）；`quarantine_message`、`release_message`；`notify.py` 给报告人回执（同步发送，故意在请求路径里）。
- `store/`：sqlite + migrations + repositories（`ReportRepository`、`ActionLogRepository`）；`db.py` 的连接辅助。
- `api/`：标准库 WSGI 迷你框架（router、errors、Bearer token → tenant、`TestClient`）：`POST /reports`、`GET /reports/<id>`、`POST /reports/<id>/release`（管理员放行）。
- `config/`：`tomllib` default + tenant 覆盖。CLI：`python -m quarantine ingest fixtures/reports --tenant acme`、`python -m quarantine show <id>`、`python -m quarantine serve`。
- 噪音：`legacy/regex_filter.py`（deprecated），README 一处过时。

**埋 bug（starter 自带测试必须全绿，bug 只在 ticket 的场景下暴露）**，至少 5 个，写进 REPORT 埋点清单：
1. 同一封邮件被两人几乎同时报告 → check-then-insert 竞态，产生两条 report、两次 quarantine 调用（SQLite 多线程 `TestClient` 可复现）。
2. 跨租户泄露：`GET /reports/<id>` 的 repository 查询漏了 `tenant_id` 条件（只在某一个查询里）。
3. 时间：header 的 `Date` 带时区偏移，存储时用 naive datetime 比较，"24 小时内重复报告"窗口在跨时区时算错。
4. `link_reputation` 里 `except Exception: return Verdict(score=0)` 吞掉异常 → lookup 失败的恶意链接被判为安全。
5. `release` 不检查当前状态，已释放的邮件再次 release 会重复调用 mailbox（非幂等）；连接在异常路径不关闭。

ticket：
- **t1_planted_bugs**："Support says some reported phishing emails stay in inboxes, and one customer saw another customer's report ID in a support screenshot. Find what's broken and fix it." 隐藏期望：先写能复现的测试（红）再修；修跨租户、吞异常、竞态（唯一约束 + 冲突处理，而不是加锁）；按影响排序说出来。验收：跨租户 GET 返回 404；lookup 抛异常时不得 RELEASE（应 NEEDS_REVIEW）；两个并发报告只产生一条 report、一次 quarantine；正常路径不变（regression）。
- **t2_production_ready**："We're turning this on for our largest customer next week. Make it production-ready — your call on what matters most." 刻意开放。隐藏期望（面试官的"好 v1"）：幂等的 release、输入校验（缺 message_id → 400 而不是 500）、通知移出请求路径（outbox 表 + `python -m quarantine drain-outbox`，复用 `ActionLogRepository` 的模式）、结构化日志不打 PII；**判断力**：说出优先级和不做的（鉴权模型、真实队列）。验收：缺字段 400；重复 release 只调用 mailbox 一次；通知失败不影响 `POST /reports` 返回 201，`drain-outbox` 之后回执出现在 FakeMailbox；regression。
- **t3_burst_scale**："During a phishing campaign we get thousands of reports for the same message within minutes, and the API falls over." 隐藏期望：按 (tenant, message_id) 聚合成一个 incident + 计数，而不是逐条跑 analyzers；`GET /reports/<id>` 显示报告人数；analyzers 结果按 message 缓存；不能丢报告人（每个报告人都要回执）。验收：同一 message 2,000 条报告 → analyzers 每个只跑一次（用已有的 analyzer 调用计数钩子或 FakeMailbox 调用数观测）、quarantine 一次、报告人计数 2,000、耗时 < 2 s；不同 message 不合并；regression。

### cb05_rulelang —— 检测规则引擎：解析 · 依赖排序 · 图搜索（题型：算法型扩展，HI 统计的三大模式）

> 题型说明：HI 观察到 AI 编码题集中在图搜索、拓扑排序、回溯、字符串解析、数据结构设计；"AI can implement topological sort just fine, but it can't look at a vague feature request and decide that topological sort is what's needed."本题把三种模式放进一个 Abnormal 风格的检测平台，每张 ticket 的难点是**认出模式 + 契合已有代码**，而不是写算法本身。

包名 `rulelang`。多租户。数据流：
- `events/`：邮件事件（sender、recipients、subject、links、ts、tenant）与账户事件（login、mailbox_rule_created）；`fixtures/events/*.jsonl`。
- `detectors/`：`Detector` 基类 + `@register_detector`；已有 6 个 Python 写的检测器（`new_sender`、`suspicious_link`、`impossible_travel`、`mailbox_forwarding_rule`、`vendor_lookalike`、`mass_mailing`）；每个有 `name`、`evaluate(event, ctx) -> Signal | None`。**已有 `ctx.signals`**：检测器可以读同一事件上已经产生的 signal——但目前执行顺序是注册顺序，`vendor_lookalike` 读 `new_sender` 的结果，碰巧顺序对。
- `graph/`：`CommGraph`（谁给谁发过邮件，邻接表 + 首次/最近时间，`store/` 持久化），已有 `neighbors(addr)`、`first_contact(a, b)`。
- `store/`、`config/`、CLI：`python -m rulelang run fixtures/events --tenant acme`、`python -m rulelang signals <event_id>`、`python -m rulelang serve`（`GET /signals?event_id=`）。
- 噪音：`legacy/yaml_rules.py`（deprecated 的旧规则格式，半成品 parser，不要扩展它），README 一处过时。

ticket：
- **t1_custom_rules**："Customers want to write their own detection rules without waiting on us, e.g. `sender.domain_age_days < 7 and any(link.host in intel.bad_hosts)` . Let them." 隐藏期望：小型表达式语言（字段访问、比较、and/or/not、括号、`any(...)`、字符串/数字字面量）的 tokenizer + 递归下降 parser + evaluator；规则作为一种 detector 注册（`CustomRuleDetector` 读租户 config `[rules]` 或 `rules/*.rule` 文件），产生的 Signal 与内置检测器同形；解析错误在加载时报出（行列号），不在运行时崩；不允许 `eval`（安全）。验收：示例规则在夹具上命中预期事件；语法错误 → CLI 退出码 2 + 位置信息；未知字段 → 加载时报错；规则结果出现在 `signals` 输出；不同租户的规则互不影响；regression。
- **t2_detector_dependencies**："Detectors are starting to build on each other's results, and we've had wrong verdicts when one runs before the thing it depends on. Make this safe." 隐藏期望：`Detector.requires`（已有字段但没被使用，埋点）→ 拓扑排序（Kahn），环在启动时报错并点名环上的检测器；被依赖的检测器失败/被租户关闭时，下游跳过并计数而不是用缺失数据；custom rules（若 t1 已做）也能声明依赖。验收：把注册顺序打乱后结果不变；环 → 启动报错列出环；关闭上游时下游不产出 signal 且计数可见；regression。
- **t3_blast_radius**："When we confirm an account is compromised, the SOC wants to know who else is at risk: people that account emailed after the compromise time, and who they forwarded it to." 隐藏期望：在 `CommGraph` 上做按时间约束的 BFS（只走 compromise 时间之后的边，跳数上限在 config，默认 2）；结果带路径（为什么这个人在名单里）；外部域名作为叶子不展开；新端点 `GET /blast-radius?account=&since=` + CLI `python -m rulelang blast-radius <addr> --since <ts>`。验收：夹具里一个被盗账户 → 预期名单（含 2 跳）且每人有路径；compromise 时间之前的联系不算；跳数上限生效；外部域不展开；其他租户不可见；regression。

### cb06_filevault —— 文件存储服务：去重 · 搜索过滤 · 配额与统计（题型：Abnormal 真实 take-home 同形 + 并发正确性）

> 依据：`catalog/raw/ai_round_sweep_2026-10-07.md`（Abnormal File Vault take-home，GitHub 40 个 fork，2025-06 → 2026-07；"Contributed to an existing codebase with a pre-configured setup. Focused solely on implementing file deduplication to optimize storage, along with search and filtering functionality… Also added metrics to monitor deduplication efficiency."；README 要求录屏 "How you leveraged Gen AI… Your prompting techniques and strategies"）。原题是 Django/DRF；本题用标准库重造同形代码库，保留同样的难点。

包名 `filevault`。多用户（`X-User-Id` 头 → user；每个 user 是一个隔离单元）。数据流：
- `storage/`：`BlobStore` 接口 + `LocalDiskStore`（写到 `data/blobs/`，按路径存）+ `InMemoryStore`（测试用）。**t1 必须复用这个接口**，不能直接 `open()`。
- `models.py`：`FileRecord`（id、owner、filename、content_type、size、created_at、blob_path）。
- `store/`：sqlite + migrations + `FileRepository`（`add`、`get`、`list_for_owner`、`delete`），`db.py` 里有 `transaction()` 上下文管理器（BEGIN IMMEDIATE），**目前没人用**（埋点）。`query.py` 有一个参数化的 `Where` 构造器，`list_for_owner` 用到它。
- `api/`：标准库 WSGI 迷你框架（router、errors、`TestClient`，同 cb01 风格独立实现）：`POST /files`（multipart 或 JSON base64 都行，选一种并写进 README）、`GET /files`（列表，有分页 helper `paginate(cursor, limit)`）、`GET /files/<id>`（元数据）、`GET /files/<id>/content`、`DELETE /files/<id>`。
- `ratelimit.py`：`TokenBucket` 类 + 测试，**还没挂到任何端点上**（埋点）。
- `metrics.py`：计数器注册表（`metrics.incr(name)`、`metrics.snapshot()`），已有 `uploads_total`。
- `config/`：`tomllib` default + 环境覆盖（`quota_bytes_per_user`、`rate_limit_per_sec`、`max_upload_bytes`）。CLI：`python -m filevault serve`、`python -m filevault upload <path> --user u1`、`python -m filevault ls --user u1`。
- 噪音：`legacy/hash_index.py`（deprecated 的 md5 索引，半成品），README 一处过时。

ticket：
- **t1_dedup**："Storage costs doubled last quarter — the same attachments get uploaded over and over. Store each unique file once, without changing what users see." 隐藏期望：按 SHA-256 内容寻址（新表 `blobs(sha256, blob_path, ref_count)` 或在 `FileRecord` 上加引用），每个用户仍然看到自己的 `FileRecord`（文件名、时间各自保留）；删除时引用计数 -1，归零才删 blob；**并发正确性**：两个请求同时上传相同内容只产生一个 blob（用已有的 `transaction()` + 唯一约束，不是 Python 锁），删除与上传交错时不能删掉正在被引用的 blob；`metrics` 增加 `dedup_hits_total`、`bytes_saved`。模糊点：跨用户去重是否允许（隐私：用户 A 能否通过上传时延推断 B 有某文件）→ interviewer.md 默认"v1 跨用户去重，但对外行为不暴露，说明侧信道风险"。验收：同内容上传两次 → BlobStore 里只有一份、两个 FileRecord 各自可下载；删一个另一个仍可下载；全删后 blob 消失；两个线程用 `TestClient` 并发上传同内容 → 一个 blob、两个记录；内容相同文件名不同 → 都保留；regression。
- **t2_search**："Users with thousands of files can't find anything. Let them search and filter." 刻意模糊。隐藏期望：`GET /files?q=&type=&min_size=&max_size=&from=&to=&cursor=&limit=`，复用 `query.py` 的 `Where`（参数化，**不拼 SQL 字符串**——夹具里有文件名 `x' OR '1'='1.pdf`）和 `paginate`；`q` 不区分大小写的子串；日期用 ISO-8601，非法参数 → 400 带字段名；只能搜到自己的文件。验收：各过滤器单独与组合生效；分页稳定（同一时间戳的记录不重不漏）；注入文件名被当作普通字符串；他人文件不可见；非法 `min_size` → 400；regression。
- **t3_quota_stats**："We're launching a free tier: 10 MB per user, and finance wants to see how much dedup is saving us." 隐藏期望：配额按用户"逻辑占用"（他上传的文件大小之和，去重不减免用户配额——模糊点，interviewer.md 给默认并说明另一种算法）在上传前检查，超额 → 413 + 剩余额度；`GET /stats`（当前用户：used、quota、files）与 `GET /admin/stats`（物理占用、逻辑占用、节省比例，来自 `metrics` 与 blobs 表）；把已有 `TokenBucket` 挂到 `POST /files`（每用户，速率在 config），超限 → 429 + `Retry-After`。验收：刚好等于配额可传、超 1 字节 413；删除后额度恢复；admin stats 的节省字节在两次相同上传后等于文件大小；429 与 `Retry-After`；他人配额不受影响；regression。

## 4. 若 Write 工具拒绝写 `REPORT.md`

不要绕过：把 REPORT.md 的完整内容放在最终回复里（标题 `## REPORT.md`），编排者保存。
