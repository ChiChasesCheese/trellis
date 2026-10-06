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

### cb01_mailguard —— 入站邮件威胁检测管线（Abnormal 核心产品形态）

包名 `mailguard`。数据流：`fixtures/messages/*.json`（多租户入站邮件：headers、from display name/address、reply-to、subject、body text、urls、attachments 元数据、recipient）→ `ingest`（解析为 `Message` dataclass）→ **enrichers**（sender 域名信誉/域名年龄来自 `fixtures/intel/*.json` 的假查询服务、组织目录 `fixtures/tenants/<tenant>/directory.json`（员工、VIP 标记、title）、历史通信关系 `contact_graph`：谁给谁发过信，存在 sqlite）→ **detectors**（基类 + `@register_detector` 注册表；已有 4–5 个：可疑链接、恶意附件哈希、新发件域、外部回复链伪造…；每个返回 `Signal(name, score, reasons)`）→ **policy**（按租户 settings 的阈值把 signals 合成 `Verdict(action=DELIVER|BANNER|QUARANTINE, score, reasons)`）→ **remediation**（`actions/` 里 Action 基类：quarantine、add_banner、notify_admin，记录到 `store` 的审计表）。`tenants/settings.py`：每租户 settings（JSON 加载 + 默认值 + 校验）。`utils/`：`normalize_display_name`、`registrable_domain`（简单后缀规则）、`levenshtein`/相似度、时间窗口。`legacy/rules_v1.py`（deprecated 的正则规则引擎，README 还提到它）。CLI：`python -m mailguard scan fixtures/messages --tenant acme`、`python -m mailguard report …`。
- **t1_vip_impersonation**："Our CEO keeps getting impersonated — attackers use her name from a Gmail account and ask finance for gift cards. We're missing these. Catch them." 隐藏期望：用目录 enricher 的 VIP 列表 + `normalize_display_name` + 相似度工具 + detector 注册表 + 租户阈值；不误伤 VIP 自己从公司域发信、也不误伤与收件人已有通信关系的外部同名者（contact_graph）。模糊点：只管 VIP 还是全员？display name 近似（"Jane  Doe"、"Jane D0e"）？free-mail vs lookalike 域名？
- **t2_vendor_allowlist**："Customers say we quarantine legit invoices from their vendors. Let tenant admins allowlist senders." 点名接口：CLI `python -m mailguard allowlist add <tenant> <sender-or-domain>` / `list` / `remove`。隐藏期望：存在 store（不是新 JSON 文件），按租户隔离，域名匹配用 `registrable_domain`，进 policy 层而不是在每个 detector 里判断；**模糊点（stretch）：allowlist 不应压过恶意附件/已知恶意 URL**（安全产品的判断力）；审计记录。
- **t3_campaign_remediation**："When several employees report the same phishing email, we should pull every copy of it from everyone's inbox automatically." 点名接口：CLI `python -m mailguard report-phish <tenant> <message_id> --reporter <email>`。隐藏期望：复用 store 里的消息索引 + 已有 quarantine Action + 审计；"同一封"= 同发件人 + 归一化主题 / 相同 URL 集合（模糊点）；阈值（几个人报告）来自租户 settings；幂等（重复报告不重复处置）；不跨租户。

### cb02_insiderwatch —— Insider Risk 平台（Chi 申请的团队）

包名 `insiderwatch`。数据流：`connectors/`（基类 `Connector`：`fetch(since) -> Iterable[RawRecord]`（分页游标）+ `normalize(raw) -> Event | None`；已有 `m365_audit`（Microsoft 365 统一审计日志样式）、`okta`（登录）、`slack_audit`，各自读 `fixtures/raw/<source>/*.json`）→ `events.Event` dataclass（user, ts(UTC aware), action 枚举：`FILE_DOWNLOAD/FILE_SHARE_EXTERNAL/EMAIL_FORWARD_EXTERNAL/LOGIN/…`, bytes, target, source, attrs）→ `baselines/`（每用户每动作的滚动日统计：均值/标准差/分位，存在 sqlite，`BaselineStore` 有 `update(events)` 与 `get(user, action)`；冷启动规则）→ `signals/`（基类 + `@signal` 注册表；已有：`unusual_login_location`、`volume_spike`（对 baseline 的 z-score）、`off_hours_activity`）→ `scoring.py`（signal → 风险分，带权重与时间衰减，权重在 `config.py`）→ `alerts/`（`Alert`、`AlertStore`）→ `notify/`（`Notifier` 协议：`ConsoleNotifier`、`SlackWebhookNotifier`（stub，写到 outbox 表））。`hr/`：HR 名册（`fixtures/hr/roster.json`：员工、经理、部门、`termination_date` 可空、`resignation_submitted` 日期）。`timeutil.py`：时区、窗口、business hours。`legacy/dlp_rules.py`（deprecated）。CLI：`python -m insiderwatch replay fixtures/raw --until 2026-09-30`、`python -m insiderwatch alerts --user ...`。
- **t1_departing_exfil**："Most data theft happens in the weeks before someone leaves. Flag employees who are taking data on their way out." 隐藏期望：HR 名册（`resignation_submitted`/`termination_date`）+ 既有 baseline（相对本人基线而不是全局阈值）+ signal 注册表 + 已有动作枚举（下载、外部分享、转发到个人邮箱）+ scoring 权重在 config。模糊点：窗口多长（离职前 N 天，N 在 config）、"带走数据"包括哪些动作、没有基线的新人、已离职后仍有活动（应更严重）。
- **t2_alert_cases**："Analysts are drowning — one bad actor generates 40 alerts a day. Group them so an analyst sees one thing per incident." 点名接口：CLI `python -m insiderwatch cases [--user U]`。隐藏期望：新 `Case` 用 store 的 sqlite 与迁移约定；按用户 + 时间窗合并（窗口在 config）；case 严重度 = 成员最大（或分数和，模糊点）；case 关闭后的新 alert 开新 case；通知只在 case 新建/升级时发（复用 Notifier，不要每个 alert 都发）。
- **t3_gdrive_connector**："We're onboarding a customer on Google Workspace. Add Google Drive audit logs as a source." 给出 `fixtures/raw/gdrive/*.json`（starter 里就有，Google Admin Reports API 样式：`items[].id.time` RFC3339、`events[].name` 如 `download`/`change_user_access`/`change_document_visibility`、`parameters[]` 键值列表、`nextPageToken` 分页）。隐藏期望：照 `Connector` 基类与已有 connector 的结构写；映射到已有 `Action` 枚举（外部分享 = visibility 变为 `people_with_link`/`public_on_the_web` 或 target 是外部域）；未知事件丢弃并计数（照已有 connector 的日志/指标做法）；在 connector 注册处登记、CLI replay 自动包含；分页；时区。

### cb03_casedesk —— 分析师用的案件 API（多租户 Web 服务）

包名 `casedesk`。**标准库 WSGI**（`wsgiref`）+ 自研迷你框架：`web/router.py`（`@route("GET", "/cases/<id>")`）、`web/request.py`/`response.py`、`web/middleware.py`（认证：`Authorization: Bearer <token>` → `fixtures/tokens.json` 里的 `Principal(user, tenant, roles)`；租户隔离；错误 → JSON）、`web/pagination.py`（cursor 分页工具，`paginate(query, cursor, limit)`）、`web/testing.py`（`TestClient`，测试与验收都用它发请求）。`db/`：sqlite 连接、`migrations/0001_*.sql…` + 简单迁移器、`repositories/`（`CaseRepository`、`CommentRepository`、`AuditRepository`，所有查询都带 `tenant_id`）、`db/query.py`（小的 where-builder）。`domain/`：`Case`（status OPEN/IN_PROGRESS/RESOLVED/CLOSED，状态机 `transition()` 校验合法迁移）、`Severity`、`Comment`。`services/case_service.py`（业务逻辑 + 写审计）。`events.py`：进程内事件总线（`publish("case.updated", …)`，订阅者在 `subscribers/` 注册）。`jobs/`：基于 sqlite 的后台任务队列（`enqueue(kind, payload)`、`worker.run_once()`、重试与退避），已有一个 `send_email` job（stub 写到 outbox 表）。`authz.py`：`require_role("analyst")` 装饰器。旧 `api_v0/`（deprecated，路由仍挂着）。CLI：`python -m casedesk serve`、`python -m casedesk seed fixtures/seed.json`、`python -m casedesk worker --once`。
- **t1_case_search**："Analysts can't find anything — the case list is just everything, newest first. Let them filter." 点名接口：`GET /cases` 的 query 参数（ticket 只列需求：by status, severity, assignee, and created date range; keep pagination working）。隐藏期望：用 `db/query.py` 与 `pagination.py`，参数校验错误走已有的错误 JSON 形状（400），租户隔离不破（跨租户查询返回空而不是 404 泄露），多值 status（模糊点：`status=OPEN&status=IN_PROGRESS` 还是逗号分隔，二选一并在文档写明；验收两种都别依赖，只测单值 + 日期范围 + 组合 + 分页 cursor 在过滤下仍正确）。
- **t2_bulk_close**："Triage leads want to close a pile of false-positive cases at once instead of one by one." 点名接口：`POST /cases/bulk-close`，body `{"case_ids": [...], "reason": "..."}`。隐藏期望：`require_role("lead")`（已有角色）；走 `CaseService` 的状态机（非法迁移的 case 不关）、每个 case 写审计、发 `case.updated` 事件；部分成功的返回形状（模糊点：207 风格的逐条结果 vs 全有全无事务；验收只测"合法的都关了、非法的报告出来、其他租户的 id 不可见且不被关"）；上限（如 ≤ 100，超出 400）。
- **t3_resolution_webhook**："Customers want their SOAR to be notified when we resolve a case." 点名接口：`POST /webhooks`（注册 URL + secret，按租户）与投递效果（outbox 表或注入的 HTTP sender）。隐藏期望：订阅 `case.updated` 事件 → **入队 job**（不在请求线程里同步发 HTTP）→ worker 投递、HMAC 签名（`hmac` + secret）、失败重试复用 jobs 的退避；只在迁移到 RESOLVED 时发；租户隔离。验收：注册 webhook → 解决一个 case → `worker run_once` → 注入的 sender 收到一次带正确签名的 payload；重复处理不重复投递（stretch）。
