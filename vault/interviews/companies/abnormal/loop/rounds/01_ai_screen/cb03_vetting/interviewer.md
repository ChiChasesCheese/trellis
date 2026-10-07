# interviewer.md · cb03_vetting（面试官视角；做完练习再看）

> 场景：你是面试官，候选人在 `starter/` 里和 Claude Code 一起做**一张** ticket（≈ 35 min）。这个领域是 Infiltration Prevention（对应 Chi 要进的 Identity Security 团队）：ATS（Greenhouse / Workday）+ IdP + 外部情报 → signals → 评分 → 给安全 reviewer 的证据时间线；**不做任何招聘决定**。
> 评分原话：*Judgment*（evaluate approaches, scope work into milestones, decide what fits the existing system）· *Agency*（make decisions, state assumptions, test your own work, keep momentum）· "The bar is whether the code fits the existing system — its patterns, its conventions, its infrastructure."
> 通用默认答案（候选人没问也按此判）：v1 只做本租户；宁可漏报也不要把正常候选人标成高风险（reviewer 是人，误报要花人力）；不引入新依赖；不改 `legacy/`。

代码库速览（面试官记住即可）：`sources/`（`@register_source`）→ `Identity` + `Observation`（值按提交原样存，`raw_ref = <identity_id>#<路径>`）→ `store/`（sqlite、编号迁移、repository 全部先传 `tenant_id`）→ `signals/`（`@register_signal`，权重只在 `config/default.toml [weights]`）→ `scoring.py` → `timeline.py` → `api/`（`GET /reviews`、`GET /reviews/<id>`、`POST /reviews/<id>/disposition`）。比较值一律走 `normalize.py`。`Pipeline.ingest` 每次**重评整个租户**。README 里有两处过时：写着权重在 `vetting/weights.py`（实际在 `config/default.toml`），架构图把 `legacy/blocklist` 画成管线的一环（实际没人 import）。

---

## t1 · Coordinated applicants（关联同一批操作者的多份申请）

### ① 好 v1 长什么样
一个新的 signal（`signals/coordinated_applicants.py`，`@register_signal`，权重 `coordinated_applicants` 进 `config/default.toml`，新增的 `[correlation]` 小节在 `settings.py` 里有字段和校验）。它用 `ctx.store.observations` 取本租户的 PHONE / IP / EMAIL / 简历指纹观测，**先过 `normalize.py`**（E.164、/24、`email_key`）再比较；两份申请至少在**两类**标识上重合才算关联（单个共享的办公室 NAT、中介电话只是常见值，不能定罪）；`Finding` 的 `evidence` 带 `Citation`（含对方 `raw_ref`，其中就有对方的 identity_id），摘要里点名其它 identity_id；于是 `GET /reviews/<id>` 与时间线什么都不用改就能展示。候选人能说出"哪些是常见值、为什么不单独定罪"，说出 v1 只做本租户，说出 O(N²) 的扩展路径。

### ② 澄清问答（候选人问 → 你答；没问的默认）
| 候选人可能问 | 面试官回答 |
|---|---|
| "关联"指哪些字段？ | 申请里的电话、提交 IP、邮箱、简历文件（哈希、作者+生成工具）。不要用 user agent。 |
| 号码差一两位也算吗？ | 号码块（前 N 位）算，N 你定，放配置。默认我们更在意"同一批号码"。 |
| 只共享一个值够不够？ | 不够。很多正常人共用公司出口 IP；中介会替很多人填同一个电话。**没问的默认：至少两类标识重合。** |
| 跨租户关联可以吗？ | 产品页确实说跨组织关联，但 v1 只做本租户；请你说明跨租户要怎么设计（隐私/合同/脱敏哈希）。 |
| 要不要改评分阈值？ | 不要。新信号走已有权重与阈值，权重进配置。 |
| 关联结果存哪？ | 不新建表也行：它是个 signal 的 finding，已有 review 表存 findings。 |
| 新增一份申请后，旧的申请要更新吗？ | 要——reviewer 打开任何一个人都应看到全部。（`ingest` 本来就重评全租户。） |
| 性能？ | 几千份申请的量级，v1 不用优化，但要能讲 10x 时怎么办。 |
| 允许名单怎么给？ | 配置里一个 CIDR 列表就行；stretch。 |

### ③ 隐藏期望（按 文件:符号）
- `vetting/normalize.py`：`phone_e164`、`ip_prefix24`、`email_key`、`name_key`（新增 `phone_prefix`）——**必须复用，不许另写归一化**。
- `vetting/store/repositories.py`：`ObservationRepository.list_by_kind`（取本租户某类观测）；`find(kind, value)` 是**原值精确匹配**，对 "(415) 555-0143" vs "415.555.0147" 无效——这是陷阱。
- `vetting/signals/base.py`：`@register_signal`、`Signal.finding()`、`SignalContext.store`；权重经 `ctx.settings.weight(name)`。
- `vetting/settings.py`：新 section 必须加进 `_SECTIONS` 与 dataclass，否则 `ConfigError`；`Pipeline.__init__` 的 `require_weights` 会在缺权重时启动失败。
- `vetting/models.py`：`Finding` / `Citation`；`raw_ref` 的 `<identity_id>#...` 约定让证据天然指向另一个人。
- 不该改：`vetting/legacy/blocklist.py`（deprecated 静态黑名单，看起来像"已知坏指标匹配"但已不在管线里）；不要改 `ip_geo_mismatch` 或 `scoring.py` 去承载关联。
- 模糊点（不问就会做错）：常见值/最少重合类数；是否跨租户；N 取多少。

### ④ 追问（4–6 个）
1. "What if there are 10x as many applicants?" —— 现在每个 identity 都扫整个租户；期望：存一列归一化后的 key 并建索引，或 ingest 时增量更新一张关联表。
2. "How would you roll this out?" —— 先 shadow 模式（记 finding 但权重 0）看分布，再开权重；按租户开关。
3. "A recruiting agency submits 200 applicants from one phone line. What happens?" —— 允许名单/ 先验：同一类标识重合的人数过多时降权。
4. "How would you explain this to the reviewer?" —— 证据里列出对方 identity 与具体重合的标识；不出现"此人是攻击者"的结论。
5. "What is missing from your v1?" —— 传递关联（A–B、B–C 但 A–C 不直接重合）、跨租户、允许名单。
6. "What can go wrong with privacy if we correlate across customers?" —— 看他是否想到最小披露（只给"在其他组织出现过"，不给对方数据）。

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 提出"至少两类重合 + 常见值不定罪"，并给出理由（误报成本）；先做 M1 再扩 | 做出关联，但只用一种标识或没讨论常见值 | 把所有共享 UA / 工具 / IP 都当关联；全员互相标记 |
| Agency | 问 2–3 个问题后写下假设（"N=9 放配置，v1 本租户"）直接推进，主动演示 | 问完等你拍板 | 没问也没写假设；做到一半才发现歧义 |
| Fit-the-system | 新 signal 走注册表+配置权重+`normalize.py`+`Finding/Citation`，新测试放 `tests/` | 复用了注册表但自己写了电话清洗 | 新建平行"correlator"模块、硬编码权重、改 `legacy/` |
| Testing | 测试包含：真阳性三人组、共享 NAT 的正常人、跨租户、号码格式变体 | 只有真阳性 | 没跑测试 / 只让 AI 写了 happy path |
| AI-supervision | 提示词点名文件与抽象；能指出 AI 用了 `find(kind,value)` 或自己写正则并改掉 | 接受 AI 方案但读过 diff | 整段粘贴；解释不了为什么这样比较 |
| Communication | 第 10 分钟说得出数据流；收尾给 known gaps（传递关联、跨租户、O(N²)） | 讲了做了什么但没讲取舍 | 念文件名；不说假设 |

---

## t2 · Workday as a source（新增 Workday 数据源）

### ① 好 v1 长什么样
`sources/workday.py`：`@register_source` 的 `WorkdaySource(Source)`，照 `greenhouse.py` 的结构：`load()` 沿 `Paging.next` 读各页，`_parse()` 把嵌套字段映射成同样的 `Identity` + `Observation`（Kind 枚举不变），`Source.observe()` 记录缺字段，`Source.bad_record()` 记录无法识别的整条记录；`Identity.make_id("workday", Job_Application_ID)` 使重复投递落到同一 identity，观测因 `raw_ref` 不含页码而被 `INSERT OR IGNORE` 去重；时间用 `timeutil.parse_ts`；电话 `Country_Code` + `Phone_Number` 拼成一个值，**分机不拼进号码**；`sources/__init__.py` 里 import；`timeline.SOURCE_LABELS` 加 `workday`。**所有 signal 一行不改**。

### ② 澄清问答
| 候选人可能问 | 面试官回答 |
|---|---|
| "重复投递"是什么意思？ | 同一个 `Job_Application_ID` 在两页都出现（翻页重叠）。**默认：幂等，同一 identity，不重复计证据。** 同一个人用新的 application id 再投是另一份申请，不合并（那是 t1 的事）。 |
| 缺邮箱的记录怎么办？ | 别整条丢，其它信号照样跑；缺字段要计数。 |
| 没有 `Application ID` 的记录？ | 无法识别 → 计 bad record、跳过。 |
| 时区？ | 一律 UTC，和现有数据一致。 |
| Workday 的 identity id 长什么样？ | 沿用现有约定：`<source>:<外部 id>`。 |
| 要不要给 Workday 单独的权重/信号？ | 不要，现有信号对 Workday 数据原样生效。 |
| 分页怎么读？ | `Paging.next` 是游标，`p2` 对应 `applications.p2.json`；读到 `null` 为止。 |
| ingest 命令要变吗？ | 不变，所有已注册的 source 都会读。 |
| 要不要把 Workday 数据先转成 Greenhouse 格式？ | 不要，那会丢掉 `raw_ref` 的来源指向。 |

### ③ 隐藏期望
- `vetting/sources/base.py`：`Source`、`@register_source`、`Source.observe()`、`Source.bad_record()`；`vetting/sources/greenhouse.py` 是范本。
- `vetting/sources/__init__.py`：注册要靠 import（漏了就等于没加，ingest 零身份）。
- `vetting/models.py`：`Identity.make_id`、`Kind`；`vetting/timeutil.py`：`parse_ts`（`-07:00` 偏移直接可用）。
- `vetting/timeline.py`：`SOURCE_LABELS`（不加则文案回退成 `workday` 小写，验收看 `source` 字段；加了才有 "Application received via Workday"）。
- `vetting/store/__init__.py` / `repositories.py`：`observations` 的 UNIQUE 约束 + `INSERT OR IGNORE`；`raw_ref` 里不能带页码或行号，否则重复投递会产生双倍证据。
- 不该改：`signals/*`（别为 Workday 写分支）、`legacy/`、`pipeline.py`（它遍历 `SOURCES`）。
- 模糊点：什么叫"重复投递"；缺字段只丢观测而非整条；`Phone.Extension` 不进号码。

### ④ 追问
1. "What if the Workday export is 100x larger and arrives as one file?" —— 流式解析 / 分块；`load()` 已是生成器。
2. "How would you onboard a third ATS faster next time?" —— 抽取"嵌套字段 → Kind"映射表，或给 `Source` 加声明式 mapping。
3. "What should happen when Workday renames a field?" —— 缺字段计数会突增，需要一个告警/阈值；别静默吞掉。
4. "How do you know the Workday reviews are as good as the Greenhouse ones?" —— 用同一批人在两个源里各灌一遍对比 findings。
5. "What did you assume about the duplicate?" —— 看他能否复述"同 application id"这个假设。
6. "What is missing?" —— 增量拉取（API 而非文件）、重试、`Paging` 环检测。

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 明确"不改 signals、不转格式，写一个 Source"；M1 = 读取+映射+一个 VoIP 演示 | 能做出来但先打算转成 Greenhouse 格式 | 在 pipeline / signals 里为 Workday 加分支 |
| Agency | 读完 `greenhouse.py` 就开工；对"重复"写下假设；自己跑 CLI 看结果 | 等你解释字段含义 | 一直在问字段，不看 fixtures |
| Fit-the-system | 注册 + `observe()` + `parse_ts` + `make_id` + `SOURCE_LABELS` 全用上 | 缺 `SOURCE_LABELS` 或手写时间解析 | 手写 `datetime.strptime` 处理偏移；自己拼 identity id |
| Testing | 测试：分页、重复、缺邮箱、缺 id、UTC；并跑一遍 greenhouse 回归 | 只测 happy path | 没测重复/缺字段 |
| AI-supervision | 提示词要求"follow greenhouse.py"；审出 AI 把分机拼进号码或把页码放进 raw_ref | 读 diff 但没发现 | 让 AI 自行设计 schema |
| Communication | 讲清"两个源映射到同一个 Observation 模型，signals 不动" | 讲了结果没讲理由 | 无法解释重复投递如何幂等 |

---

## t3 · Learn from reviewer decisions（reviewer 反馈降低重复误报）

### ① 好 v1 长什么样
读已有的 disposition 历史（`ReviewRepository` 的 `dispositions` 表，按每个 identity 的**最新**决定），把"被 cleared 过的具体值"（finding 的 `subject`：`asn:AS64500`、`phone:+1…`）取出来；在 `scoring` 这一层对**租户内**、**单一且偏弱**的 finding 降权（系数进 `[feedback]` 配置），finding 与证据保留并标注 "previously cleared by reviewer"；被 escalated 的同值不降权；多信号组合不受影响；其它租户不受影响；不关掉任何 signal，不改全局权重。

### ② 澄清问答
| 候选人可能问 | 面试官回答 |
|---|---|
| "同样的模式"指什么？ | 具体的值：某个 VPN 网络（ASN）、某个号码。不是"所有 VPN"。 |
| 降权还是完全隐藏？ | 保留证据、降权、并标注；reviewer 要能审计。**没问的默认：降权不隐藏。** |
| 被 escalated 的值呢？ | 不能被洗白：同一个值有人 escalated，就不降权。 |
| 多个信号同时命中的人？ | 不受影响。降权只针对"只有这一个弱信号"的人。 |
| 要不要跨租户共享 cleared 结果？ | 不要。每个租户的 reviewer 判断只用于本租户。 |
| 决定要立即生效吗？ | 下次评估生效即可（`ingest` 重评时）；不用在 POST 里重算所有人。 |
| 要不要改 disposition 的接口？ | 不用，数据已经在。 |
| 一次 cleared 就够了吗？ | v1 一次即可；说明你会怎么用计数/时效。 |
| 阈值/系数放哪？ | 配置，不要写死。 |

### ③ 隐藏期望
- `vetting/store/repositories.py`：`ReviewRepository.dispositions` / `latest_disposition`（disposition 是追加历史，取最新）；需要一个按租户查"最新决定 → 被决定过的 subject"的方法。
- `vetting/models.py`：`Finding.subject`（`vpn_hosting_ip` 的 `asn:`、`voip_phone` 的 `phone:` 已经填好——正是"具体值"）。
- `vetting/scoring.py`：打分入口；降权在这里或紧挨着它，不在每个 signal 里。
- `vetting/settings.py` + `config/default.toml`：新增 `[feedback]` 要在 `_SECTIONS` 与 dataclass 注册。
- `vetting/pipeline.py`：`evaluate` / `evaluate_all` 是调用点（每次 ingest 重评，决定自然生效）。
- 不该改：`config/default.toml` 里把 `vpn_hosting_ip` 权重调低或关掉（全局解决方案）；`legacy/blocklist.py`；`api/reviews.py` 的 disposition 接口。
- 模糊点：能否被"洗白"（escalated 同值）；是否只对单一弱信号；保留证据 + 标注。

### ④ 追问
1. "An attacker gets one fake candidate cleared, then reuses the same VPN. How does your design hold up?" —— 单弱信号限制、escalated 优先、组合不受影响；还可加时效/需要 N 次 cleared。
2. "How would you roll this out safely?" —— 先只标注不降权，对比一周；灰度到租户。
3. "What if two reviewers disagree?" —— 取最新？还是任何 escalated 优先（我们的默认）。
4. "How would a reviewer see why a score changed?" —— 标注与证据；时间线里写明。
5. "What does 'the same pattern' mean for a Google Voice number?" —— 号码本身还是运营商；运营商级别的放行风险更大。
6. "What is missing?" —— 时效、撤销（cleared 后又 escalated）、按岗位/部门的细分。

### ⑤ 打分信号
| 维度 | strong | ok | weak |
|---|---|---|---|
| Judgment | 先说"降权具体值、不关信号"，列出洗白风险与限定条件；M1 = 单弱信号 + ASN | 做出降权但没想到 escalated / 组合 | 直接把 `vpn_hosting_ip` 权重调低或加全局开关 |
| Agency | 假设写明（降权不隐藏、本租户、单弱信号），做完可演示 | 问了但不敢定默认值 | 等面试官给方案 |
| Fit-the-system | 用 `dispositions` + `Finding.subject` + `scoring` + `[feedback]` 配置；不动 API | 自己再建一张 "cleared_values" 表 | 在每个 signal 里查 disposition；改 `legacy/` |
| Testing | 测试：降权、证据保留、组合不受影响、其它租户、escalated | 只测降权 | 没测边界 |
| AI-supervision | 审出 AI 把整租户的同类信号都关掉、或没做租户过滤 | 读了 diff | 不看 AI 写的 SQL |
| Communication | 清楚讲"为什么不让它被洗白"，说出 known gaps | 讲了机制 | 说不清为什么是单弱信号 |
