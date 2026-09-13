# Stripe 官方侧原始资料 —— 招聘流程、面试指南、API 设计原则、工程博客（面试相关）

> 范围：Stripe OA 之后的轮次（technical phone screen → onsite：bug squash / integration / coding / system design → HM/behavioral）在 **Stripe 官方渠道**（stripe.com、docs.stripe.com、Stripe 工程博客、Stripe 官方 GitHub 组织）能找到的一手资料：招聘/面试流程页、API 设计原则文档、与面试题直接对应的工程博客、开源项目、官方术语表。
> 采集日期：2026-09-01。方法：WebFetch 直读 stripe.com/docs.stripe.com/stripe.com/blog；被 Cloudflare/反爬拦截时尝试 `https://r.jina.ai/` 前缀重试；WebSearch 定位具体文章/页面 URL。
> 可信度分级：**[官方]** = stripe.com/docs.stripe.com/Stripe 官方博客一手内容；**[官方转载]** = 第三方站点转载/引用官方原文；**[二手]** = 培训站/博主转述；**[推断]** = 本文综合判断，如"面试怎么考"的关联。
> 体例：每条事实后附 `[来源 / URL / 日期]`。题名、API、代码、repo 名保留英文，其余中文。

---
## 0. 速览

1. Stripe 官方招聘页反复强调两组关键词：**"Speed and Craft"**（速度与匠心的张力）+ **"First-Principles Thinking"**（第一性原理），以及候选人画像"generalists"（通才，能空降任何领域快速学习并落地）——面试评分隐含标准之一。[stripe.com/jobs/culture, 2026-09-01]
2. 官方 `stripe-interview` GitHub org（详见文件 1 第 1.1 节）里 Python 分支预装依赖只有 `requests`/`six`/`urllib3`，**官方亲口印证 Integration 轮 Python 候选人默认用 `requests` 库**。[github.com/stripe-interview/python-interview-prep, 2026-09-01]
3. `docs.stripe.com` 的 **Idempotent requests**、**Errors**、**Pagination**、**Webhooks**、**Rate limits** 五篇文档是 Integration/System Design 轮被反复追问的官方一手依据，本文件第 3 节逐条摘录原文。
4. Stripe 工程博客《Online migrations at scale》《Rate limiters》《Ledger: Stripe's system for tracking and validating money movement》与面经里的 Ledger/Rate Limiter System Design 题**直接对应**，是目前找到的最具"官方标准答案"性质的素材。
5. `stripe/stripe-mock` 是唯一可用来**本地零依赖跑 Stripe API 假环境**的官方开源项目，非常适合搭 Integration 轮练习环境；`stripe/smokescreen` 对应 webhook SSRF 追问的官方生产实现。

## 1. 官方招聘/面试页面

- **`stripe.com/jobs`**——招聘首页明确写"Most processes include a recruiter screen, a technical or skills-based assessment, and a series of interviews with the team you'd be joining."（大多数流程包含：招聘经理电话、技术/技能评估、与目标团队的一系列面试）；并声明"try to work quickly and give clear feedback at every stage"（尽快推进、每阶段给清晰反馈）。工程文化两大原则：**"Speed and Craft"**（速度与匠心）+ **"First-Principles Thinking"**（不接受约定俗成的做法，从第一性原理重新思考金融服务该怎么做）。成功员工画像：使命认同、超越个人专长的 ownership、偏好挑战性问题而非舒适区、遇到"对不上"的地方保持好奇并愿意基于证据改变立场。[官方 / https://stripe.com/jobs / 访问 2026-09-01]
- **`stripe.com/jobs/culture`**——工程文化更细的表述：**"Users First"**（"Our users trust us to provide an essential service, and it's a heavy responsibility that we take very seriously."）、**"Collaborate egolessly"**（"no fiefdoms, no hoarding information, no 'not my problem'"）、**"Create with craft and beauty"**（"anything can be made surprisingly great"）、**"Move with urgency and focus"**（目标"become the world's fastest company"）、**"Stay curious"**（"an applied exercise in learning about how businesses tick"）。理想候选人是**"rigorous thinkers who appreciate that things worth doing are rarely simple"**，偏好**通才（generalists）**能"parachute anywhere into our operations, learn a new field quickly, and execute competently"。招聘哲学原话：**"Not everyone finds success at Stripe."**（明确表示高标准、非人人适合）。[官方 / https://stripe.com/jobs/culture / 访问 2026-09-01]
- **`stripe.com/jobs/compatibility`**（"Culture Fit Assessment"页）——补充细节：**"generous with credit and stingy with blame"**（功劳归他人、责任揽自己）；候选人自问"Does enabling entrepreneurship and helping to unlock the internet economy's full potential seem like a compelling use of my time?"；**"comfortable taking on problems outside my domain or experience"**；重要警示原话：**"People who thrive in high-conflict work environments often do not enjoy the experience here"**（爱冲突环境的人在 Stripe 未必舒服，暗示协作/沟通类行为题的评分权重）。[官方 / https://stripe.com/jobs/compatibility / 访问 2026-09-01]
- **`stripe.com/careers/listing/software-engineer-new-grad/...`**（New Grad SWE 职位描述，以 2026 London 版本为例）——技术期望原文："We work mostly in Java, Ruby, JavaScript, Scala, and Go" 但认为"new programming languages can be learned if the fundamentals and general knowledge are present"；明确要求 **"Ability to leverage AI tools to accelerate development while applying rigorous critical thinking and professional judgement"**（2026 年新增的 AI 工具使用能力要求，早期职位描述里没有——说明 Stripe 近期把 AI 辅助编程能力写进了新毕业生 JD，面试/coding 轮可能允许甚至鼓励用 AI 工具，但需要保持批判性判断）。该页**没有**提供面试流程/环节的具体描述。[官方 / https://stripe.com/careers/listing/software-engineer-new-grad/8130930 / 访问 2026-09-01]
- **官方 "interview process" 独立页面 / candidate FAQ**——**未找到**。多次 WebSearch（`site:stripe.com interview process`、`site:stripe.com candidate FAQ`）均未返回专门的面试流程说明页或候选人 FAQ 页；`stripe.com/jobs/emerging-talent` 路径返回 **404**（页面已下线或路径变更，实际路径疑似 `stripe.com/careers/emerging-talent` 或按地区分流的 `stripe.com/en-ch/careers/emerging-talent`）。**结论：Stripe 官方目前没有公开的、独立的"面试流程详解"页面**，候选人对具体环节（bug squash/integration/programming exercise 等专有名词）的了解**全部来自口口相传和第三方培训站的转述，不是 Stripe 官方术语**（见第 2 节）。[官方检索结果为空 / 访问 2026-09-01]
- **University recruiting / emerging talent 页面**——`stripe.com/careers/emerging-talent`（新版路径，见 WebSearch 结果标题"Stripe Careers | Stripe Internship and Early Career Opportunities"）是校招/实习入口，具体流程文案与本节其他招聘页类似（未见独立于本节已摘录内容的新信息）。[官方 / https://stripe.com/en-ch/careers/emerging-talent（区域变体）/ 访问 2026-09-01]

## 2. Stripe 公开的面试形式说明

- **官方侧没有"bug squash"/"integration round"/"programming exercise"这些专有名词的原始出处**——这些名字全部是候选人/培训站约定俗成的叫法，Stripe 官方招聘页/职位描述里**未使用**这些术语（多次 WebSearch 定向查询均未命中 stripe.com 域名下的原始定义）。这本身是一个值得记录的发现：**面试环节的名字是"民间共识"，不是 Stripe 官方命名**，如果候选人在电话里被 recruiter 提到某个环节名称，应以 recruiter 口头说法为准，而不要预设它和网上流传的名字完全对应同一套评分标准。
- **Patrick Collison（联合创始人兼 CEO）公开谈及工程招聘的只言片语**（The Knowledge Project 播客等二手转述整理，非 Stripe 官方博客）：**"Stripe's engineering interviews largely involve writing code on your laptop"**（工程面试主要是在自己笔记本上写代码，这与英文面经反复提到的"bring your own laptop / IDE"高度吻合）；"every engineer who joined would ship something on every other team before joining their own team"（早期 Stripe 的做法，新工程师入职前会先在其他团队"实战"一次再定组——这是历史上的入职文化而非现行面试环节，不要误解为现在的面试流程）。[二手转述 / 综合自 growth.eladgil.com、medium.com 对 The Knowledge Project 播客的转述 / 访问 2026-09-01，原始播客未直接核实]
- **第三方培训站对面试哲学的转述**（非官方原文，谨慎使用）：Exponent《Get a Job at Stripe》一文将大多数流程结论**明确归因于"recent Stripe candidates and interviewers"（近期候选人与面试官），而非 Stripe 官方通信**，文中坦承"No direct quotes from Stripe official communications are included regarding the interview process structure itself"。候选人原话转述："felt less like LeetCode and more like real work"（不像刷题，更像真实工作）；integration 轮"felt more like design than coding"（更像做设计而不是写代码）。[二手 / https://www.tryexponent.com/blog/stripe-interview-process / 访问 2026-09-01]
- **Stripe 官方 Atlas 指南《Scaling engineering organizations》**——虽非面试流程页，但内容提到 Stripe 招聘工程师的演变："提供书面指南帮助候选人理解公司文化并准备面试"、"给工程师选择编程语言和自己开发环境的自由"（与 `stripe-interview` org 的语言矩阵吻合）、"面试后无论是否录用都会和候选人聊一次"、"发匿名后续调查收集候选人体验反馈"，以及从"只招通才工程师"演变为"为前端等专项角色设计专门的候选人体验"。这是**目前找到的最接近官方"我们怎么招聘工程师"的一手内容**，虽然是从组织规模化视角写的，不是专门的面试指南。[官方 / https://stripe.com/guides/atlas/scaling-eng / 访问 2026-09-01]

## 3. Stripe API 设计原则（面试 integration/system design 直接考）

### 3.1 Idempotent requests（幂等请求）

原文摘录（`docs.stripe.com/api/idempotent_requests`）：
- "The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key."
- "Stripe's idempotency works by saving the resulting status code and body of the first request made for any given idempotency key, regardless of whether it succeeds or fails. Subsequent requests with the same key return the same result, **including `500` errors**."（连 500 错误也会被完整重放，这是常被面试追问的细节）
- Key 生成建议：**V4 UUID** 或其他有足够熵的随机字符串；**Key 最长 255 字符**；**不要用邮箱等敏感信息做 key**。
- **保留时长**："You can remove keys from the system automatically after they're at least **24 hours old**. We generate a new request if a key is reused after the original is pruned."
- **参数不一致处理**："The idempotency layer compares incoming parameters to those of the original request and **errors if they're not the same** to prevent accidental misuse."——对应 `idempotency_error` 错误类型（见 3.2）。
- **何时不会保存幂等结果**："We save results only after the execution of an endpoint begins. If incoming parameters fail validation, or the request conflicts with another request that's executing concurrently, we don't save the idempotent result"——即**参数校验失败**或**并发冲突**（对应 `409 Conflict`）时不落幂等记录，这两种情况可以直接重试。
- **适用范围**：所有 `POST` 请求都接受 idempotency key；`GET`/`DELETE` 请求**不需要**（它们天然幂等）。
- **面试怎么考**：Bug squash/Integration 轮如果涉及"重试逻辑"，考察点常是——① 网络错误重试要不要带上次的 Idempotency-Key（要）；② 用户主动改参数重试是不是该用新 key（是，否则触发 `idempotency_error`）；③ 幂等窗口 24h 之后重试等价于全新请求这个边界。[官方 / https://docs.stripe.com/api/idempotent_requests / 访问 2026-09-01]

### 3.2 错误模型（type / code / decline_code，HTTP 状态映射）

**HTTP 状态码总表**（`docs.stripe.com/api/errors`）：

| 状态码 | 含义 | 说明原文 |
|---|---|---|
| 200 | OK | Everything worked as expected. |
| 400 | Bad Request | 常见于缺少必填参数。 |
| 401 | Unauthorized | 没有有效 API key。 |
| 402 | Request Failed | 参数合法但请求本身失败（如卡被拒）。 |
| 403 | Forbidden | API key 没权限执行该请求。 |
| 404 | Not Found | 资源不存在。 |
| 409 | Conflict | 与另一个请求冲突（例如复用了同一个 idempotent key）。 |
| 424 | External Dependency Failed | 因 Stripe 外部依赖失败导致请求无法完成。 |
| 429 | Too Many Requests | 建议指数退避重试。 |
| 500/502/503/504 | Server Errors | Stripe 服务端问题，罕见。 |

**四种 `type`**：
- `api_error`——"cover any other type of problem (e.g., a temporary problem with Stripe's servers), and are extremely uncommon."
- `card_error`——"the most common type of error you should expect to handle. They result when the user enters a card that can't be charged for some reason."
- `idempotency_error`——"occur when an `Idempotency-Key` is re-used on a request that does not match the first request's API endpoint and parameters."
- `invalid_request_error`——"arise when your request has invalid parameters."

**关键字段**：`code`（可编程处理的短字符串错误码）、`decline_code`（发卡行拒绝原因）、`advice_code`/`network_advice_code`（对商户"接下来怎么办"的建议，2 位数字码）、`network_decline_code`（网络层拒绝的字母数字码）、`doc_url`（错误码文档链接）、`param`（定位到具体哪个参数出错，便于前端定位表单字段）、`request_log_url`（Dashboard 请求日志链接）。
**面试怎么考**：Integration 轮写"调用 API 并处理响应"的代码时，面试官常追问"如果卡被拒你怎么给用户展示错误"——标准答案是读 `error.type == 'card_error'` 时把 `error.message` 直接展示给用户（官方明确说这类消息"can be shown to your users"），其他类型的错误不应该把 `message` 原样暴露给终端用户。[官方 / https://docs.stripe.com/api/errors / 访问 2026-09-01]

### 3.3 Pagination（游标分页）

原文摘录（`docs.stripe.com/api/pagination`）：
- "Stripe's list API methods use **cursor-based pagination** through the `starting_after` and `ending_before` parameters."
- "Both parameters accept an existing object ID value... and return objects in **reverse chronological order**."
- `ending_before`——返回该对象**之前**列出的对象；`starting_after`——返回该对象**之后**列出的对象；**两者互斥，不能同时使用**。
- `limit`：默认 10，范围 1–100。
- List 响应结构固定为 `{object: "list", url, has_more, data: [...]}`；`has_more` 为 `false` 表示已到列表末尾。
- 官方客户端库提供 **auto-pagination helpers** 自动翻页遍历全部数据。
- **v2 API（`/v2` 命名空间）用的是不同的分页接口**，与 v1 的 `starting_after`/`ending_before` 不通用——这是版本迁移类系统设计题常考的细节。
- **面试怎么考**：System design 轮如果让你设计一个"列表 API"，游标分页（而非 offset 分页）是标准答案，理由是 offset 分页在数据频繁插入删除时会跳过或重复记录，游标分页天然稳定；Integration 轮如果要"拉取全部数据"，标准写法是循环判断 `has_more` 并把最后一个对象 id 传给下次请求的 `starting_after`。[官方 / https://docs.stripe.com/api/pagination / 访问 2026-09-01]

### 3.4 Webhooks（签名验证、重试、事件顺序、幂等处理）

原文摘录（`docs.stripe.com/webhooks`）：
- **签名 header**：`Stripe-Signature`，格式为 `t=<timestamp>,v1=<signature>[,v0=<fake signature for testing>]`，用 **HMAC-SHA256** 生成；`v1` 是当前唯一合法 scheme，**必须忽略非 `v1` 的 scheme 以防降级攻击**。
- **验证步骤**（手动实现四步）：① 按 `,`/`=` 拆出 `t` 和 `v1`；② 拼接 `signed_payload = timestamp + "." + raw_body`；③ 用 endpoint secret 作 key 对 `signed_payload` 算 HMAC-SHA256；④ **用常数时间比较（constant-time comparison）** 防时序攻击，且要检查时间戳新鲜度。
- **时间戳容忍度**："Our libraries have a default tolerance of **5 minutes** between the timestamp and the current time." 并明确警告：**"Don't use a tolerance value of `0`. Using a tolerance value of `0` disables the recency check entirely."**
- **必须用原始请求体验证**："Stripe requires the raw body of the request to perform signature verification... Any manipulation to the raw body of the request causes the verification to fail."（框架的 body-parser 中间件常会篡改原始 body，是候选人写 webhook handler 时最常见的坑）。
- **重试策略**："Stripe attempts to deliver events to your destination for **up to three days with an exponential back off** in live mode."（sandbox 环境是"三小时内重试 3 次"，与生产环境不同）。
- **事件顺序**："Stripe **doesn't guarantee** the delivery of events in the order that they're generated."，并举例："creating a subscription might generate `customer.subscription.created` → `invoice.created` → `invoice.paid` → `charge.created`"，但顺序不保证。明确建议：**"Don't use `created` to determine event order or whether you've already processed an event. Track event IDs to identify duplicate deliveries instead."**
- **幂等处理**（重复事件）："Webhook endpoints might occasionally receive the same event more than once."——标准做法是记录已处理过的 `event.id`，跳过重复；**极端情况下同一个业务动作可能对应两个不同的 Event 对象**，此时要用 `data.object` 的对象 ID + `event.type` 联合去重。
- **必须快速返回 2xx**："Your endpoint must quickly return a successful status code (`2xx`) before any complex logic that could cause a timeout."——推荐把耗时逻辑放异步队列处理。
- **安全实践**：IP allowlist（Stripe 从固定 IP 段发 webhook）+ 签名验证双重防护；定期"roll"（轮换）签名密钥，轮换时新旧密钥可并存最多 24 小时。
- **面试怎么考**：这是 Bug squash（React async race 描述之外，Webhook handler 常见 bug 是"body 被中间件改过导致验证失败"）+ System Design（"设计一个幂等、顺序不敏感的 webhook 消费系统"）两个轮次的共同素材，几乎是"必考重灾区"。[官方 / https://docs.stripe.com/webhooks / 访问 2026-09-01]

### 3.5 Rate limits（限流）

原文摘录（`docs.stripe.com/rate-limits`）：
- **全局限流**：Live mode **100 requests/秒**；Sandbox（测试环境）**25 requests/秒**。（原描述用词是 "Sandbox" 而非旧文档里的 "test mode"，是 Stripe 近期的产品改名，System Design 轮若提到"test mode"要留意面试官可能已经改口叫 "sandbox"）
- 单个 API 端点默认限流 **25 requests/秒**（除非另有说明）；部分资源有专属限流（如 PaymentIntents：每个对象每小时最多 1000 次 update；Subscriptions：每分钟 10 张新发票/每天 20 张/每小时 200 次数量变更；Payouts：15 创建请求/秒 + 30 并发请求/商户）。
- **429 响应**带 `Stripe-Rate-Limited-Reason` header，五种取值：`global-rate`、`endpoint-rate`、`global-concurrency`、`endpoint-concurrency`、`resource-specific`——**这是比"泛泛而谈 429"更细的官方分类，回答"如何处理限流"时可以按这五种原因分别讨论应对策略**。
- **并发限制（Concurrency limits）**与速率限制是两回事：速率限制通常"每秒重置"，并发限制"统计同一时刻有多少请求在处理中"，常见诱因是 list 请求或带 `expand` 的请求（更耗资源、耗时更长）。
- **处理建议**：**指数退避 + 加随机抖动（jitter）**防雷鸣群效应（thundering herd）；更高阶方案是客户端实现 **token bucket 限流算法**做全局流量控制。
- **Object lock timeouts**（也是 429，但 `code: lock_timeout`，与限流是不同机制）：同一对象被并发访问时可能抢锁超时，官方建议**同一对象的并发写请求应该串行化排队而不是并发发**；Stripe 官方 SDK 的自动重试机制**会自动重试**因锁超时导致的 429（但不会自动重试普通限流 429，需要业务代码自己实现退避重试）——这是一个容易被面试官用来"钓鱼"的细节：不是所有 429 都该无脑退避重试，要先判断是限流还是锁超时。
- **读请求配额**（与限流不同的另一套机制）：账户读请求（GET）平均不能超过**每笔交易 500 次**（30 天滚动窗口），且每个账户不论交易量都有**每月最低 10,000 次读请求**保底；写请求（POST 类）无此配额限制。
- **面试怎么考**：System Design 轮"设计一个 Stripe 风格的 rate limiter"几乎是标准题（对应文件 2 第 4 节 Paul Tarjan 的官方博客），官方文档的"限流原因分类 + token bucket + 指数退避 + 锁超时区分"这套完整答案可以直接当模板用。[官方 / https://docs.stripe.com/rate-limits / 访问 2026-09-01]

### 3.6 Expand（展开关联对象）

原文摘录（`docs.stripe.com/expand`）：
- 原理：把关联对象的 ID 替换成完整对象，一次请求代替多次请求。用法：`expand[]=customer`；多个属性可以并列展开；**深层嵌套**用点号语法 `expand[]=payment_intent.payment_method`。
- **展开深度上限**："Expansions have a maximum depth of **four levels**. Meaning that an `expand` string can contain no more than four properties: `property1.property2.property3.property4`."
- **列表里展开**：用 `data` 关键字把展开游标移进列表，如 `expand[]=data.payment_method` 能一次性展开列表里每个对象的关联属性，避免 N+1 请求。
- **不是所有属性都能展开**：API 文档里用 "Expandable" 标签标出哪些属性支持展开；有些属性（如 Checkout Session 的 `line_items`）**默认不返回，必须靠 `expand` 主动请求**才能拿到（"includable" 而非纯粹"expandable"的属性）。
- **Webhook 里不能自动展开**："You can't receive webhook events with properties auto-expanded. Objects sent in events are always in their minimal form."——必须在 webhook handler 里单独发请求取展开数据。
- **性能提示**：官方明确警告"Expanding responses has performance implications. To keep requests fast, try to limit many nested expansions on list requests."——这也解释了第 3.5 节里"并发限制常因 list + expand 请求触发"的原因。
- **面试怎么考**：Integration 轮如果要"减少 API 调用次数"，`expand` 是标准答案；同时官方文档本身就点出了"expand 会拖慢请求、且不能用于 webhook"两个陷阱，可以在追问"有什么权衡"时直接引用。[官方 / https://docs.stripe.com/expand / 访问 2026-09-01]

### 3.7 Versioning（API 版本、向后兼容承诺）

原文摘录（`docs.stripe.com/api/versioning` + `docs.stripe.com/upgrades`）：
- **版本命名**：主版本用**植物名代号**（如 `Basil`、`Acacia`），当前版本号形如 `2026-08-26.dahlia`（日期 + 代号）。**每月小版本**只含向后兼容变更、复用上一个大版本的名字；**大版本**（不定期发布）才含 breaking change。
- **`Stripe-Version` header**：curl/CLI 请求默认用账户在 Workbench 里设置的默认版本，可用该 header 覆盖；webhook 事件默认用账户默认版本，除非在**创建 endpoint 时**显式指定了版本（且一旦指定，该 endpoint 之后**始终**用这个版本，不随账户默认版本变化）。
- **官方语言 SDK 的版本锁定行为**（各语言不同，容易在面试被问"这个坑你知道吗"）：`stripe-ruby v9+`/`stripe-python v6+`/`stripe-php v11+`/`stripe-node v12+` 都改成了"SDK 发布时锁定的 API 版本"，而不是账户默认版本；`stripe-java`/`stripe-go`/`stripe-dotnet` 因为是强类型语言，**版本直接跟 SDK 版本绑定**，要用新/老 API 版本必须升级/降级 SDK 版本。
- **向后兼容变更的官方权威定义**（`docs.stripe.com/upgrades` 原文列表，**逐条引用价值极高**）：
  - 新增 API 资源（resource）。
  - 给已有 API 方法新增**可选**请求参数。
  - 给已有响应新增属性。
  - **改变已有响应里属性的顺序**（说明字段顺序从不被视为契约的一部分）。
  - **改变不透明字符串（opaque string）的长度或格式**——包括 object ID、错误消息等人类可读字符串；**明确包括"给 ID 加/去掉固定前缀"（如 `ch_`）**，并提醒"要确保你的系统能处理最长 255 字符的 Stripe 生成 ID"（举例 MySQL 要用 `VARCHAR(255) COLLATE utf8_bin`）。
  - 新增**事件类型**——要求 webhook listener 能"优雅处理不认识的事件类型"（即 switch/case 必须有默认分支，不能因未知 `event.type` 而崩溃）。
- **回滚窗口**："For **72 hours** after you've upgraded your API version, you can safely roll back to the version you were upgrading from in Workbench."——回滚后，升级期间失败的 webhook 会用旧版本结构重新投递。
- **Connect 场景的特殊规则**：平台代表连接账户发请求且未指定版本时，**始终使用平台自己的 API 版本**，不管连接账户本身是什么版本。
- **面试怎么考**：System design 轮如果问"如何设计一个不 breaking 现有客户端的 API 演进策略"，上面这份"向后兼容变更清单"就是官方标准答案模板；Integration/Bug squash 轮如果 mock 服务器返回了未知字段/未知事件类型，考察点正是"你的解析代码是不是对未知字段/类型健壮"（对应向后兼容原则第 3、5 条）。[官方 / https://docs.stripe.com/api/versioning + https://docs.stripe.com/upgrades / 访问 2026-09-01]

### 3.8 Request IDs

原文摘录（`docs.stripe.com/api/request_ids`）：每个 API 请求都有一个关联的 **`Request-Id`** 响应头，也能在 Dashboard 请求日志的 URL 里找到；联系 Stripe 支持时提供这个 ID 能加快排查。**面试怎么考**：Bug squash/Integration 轮如果要求"给调用加可观测性/方便排查"，把 `Request-Id` 记录进日志是标准答案之一（对应文件 2 第 4 节 canonical log lines 那篇博客的实践）。[官方 / https://docs.stripe.com/api/request_ids / 访问 2026-09-01]

### 3.9 Metadata / Description（附加数据）

原文摘录（`docs.stripe.com/api/metadata`）：
- 支持 `metadata` 的对象包括 `Account`、`Charge`、`Customer`、`PaymentIntent`、`Refund`、`Subscription`、`Transfer` 等。
- **容量限制**：最多 **50 个 key**，key 名最长 **40 字符**，value 最长 **500 字符**；key/value 都是字符串，**key 里不能包含方括号 `[` `]`**。
- **Stripe 不使用 metadata 做任何业务判断**："Stripe doesn't use metadata—for example, we don't use it to authorize or decline a charge and it won't be seen by your users unless you choose to show it to them."——纯粹是给接入方自己存业务关联数据用的（如自己系统的订单号）。
- 区别于 `description`（单个字符串，**用户可能会看到**，比如出现在 Stripe 代发的邮件收据里）。
- **明确警告**："Don't store any sensitive information (bank account numbers, card details, and so on) as metadata or in the `description` parameter."
- **典型用例**：关联自己系统的 ID（订单号/用户 ID）、退款留痕（记录退款原因和操作人）、客户备注。**面试怎么考**：Integration 轮如果让你"把外部系统的某个 ID 存到 Stripe 对象上"，`metadata` 是标准做法；如果候选人把敏感信息塞进 `metadata`，是一个常见的隐性扣分点。[官方 / https://docs.stripe.com/api/metadata / 访问 2026-09-01]

### 3.10 金额用最小单位整数（Zero-decimal currencies）

原文摘录（`docs.stripe.com/currencies`）：
- **所有 API 请求的 `amount` 都用该货币的"最小单位"整数表示，不带小数点**："The Stripe API expects currency values using the given denomination's smallest unit represented without decimals."——`1000` 表示 10.00 USD（两位小数货币），`10` 表示 10 JPY（零小数货币）。
- **Zero-decimal 货币**（如 JPY）charge 金额和 amount 数值直接相等，不需要乘 100。
- **特殊例外货币**（面试容易挖坑的细节）：
  - **ISK（冰岛克朗）/UGX（乌干达先令）**：官方规则上已变成零小数货币，但**为了向后兼容仍要求按两位小数格式传参**，小数位固定为 `00`（如 charge 5 ISK 要传 `500`），且**不能收零头**。
  - **HUF（匈牙利福林）/TWD（新台币）**：charge 时按两位小数处理，但**手动 payout 时必须传能被 100 整除的整数金额**（因为 payout 侧被当作零小数货币处理）——官方举例："if you have an available balance of HUF 10.45, you can pay out HUF 10 by submitting `1000`... You can't submit a payout for the full balance."
- **最小/最大充值金额**：因为 Stripe 手续费不能超过充值金额，所有货币都有最低充值额（如 0.50 USD、50 JPY、0.30 GBP）；最大金额受"允许的数字位数"限制，多数卡组织交易上限是 **12 位数字（999,999,999,999 最小单位）**，**American Express 是 9 位数字**（多数币种），日本境内处理 JCB/Diners/Discover 卡上限是 **8 位数字（99,999,999 JPY）**。
- **面试怎么考**：这是 System Design/Integration 轮"设计一个货币金额字段"的标准依据——**永远用整数存最小单位，不要用浮点数**，且要专门处理"零小数货币"和"HUF/TWD/ISK/UGX 这类特例货币"的边界（这几个特例本身就很适合改编成一道"货币金额格式化"的 bug squash/coding 题）。[官方 / https://docs.stripe.com/currencies / 访问 2026-09-01]

### 3.11 PaymentIntent 状态机

原文摘录（`docs.stripe.com/payments/paymentintents/lifecycle`，Stripe 现推荐用 Checkout Sessions + Payment Element 代替直接用 PaymentIntent API，但状态机本身仍是文档现役内容）：

| 状态 | 触发条件（原文） |
|---|---|
| `requires_payment_method` | 创建 PaymentIntent 后的初始状态，直到附加了 payment method。**旧版 API（2019-02-11 之前）叫 `requires_source`**（版本迁移类问题的经典细节）。 |
| `requires_confirmation` | 客户提供了支付信息后进入此状态，"ready to confirm"；**"Most integrations skip this state"**（大多数集成方式会跳过这个状态，因为提交支付方式信息和确认支付通常在同一步完成）。 |
| `requires_action` | 需要额外操作（如 3D Secure 认证）时进入。**旧版 API 叫 `requires_source_action`**。 |
| `processing` | 完成必需操作之后、且使用**异步支付方式**（如银行代扣，可能需要几天处理）时进入；**如果是手动 capture 模式，会先进入 `requires_capture`**，之后尝试 capture 才转到 `processing` 或 `succeeded`（取决于支付方式）。 |
| `requires_capture` | 文档正文以行内方式提及（手动"先 authorize 后 capture"场景），未在状态表格中单列一行——**这是容易被面试官追问"为什么表格没有专门列出来"的细节**：官方把它描述为"`processing` 的一个变体路径"而非并列的独立大状态。 |
| `succeeded` | "means that the corresponding payment flow is complete. The funds are now in your account and you can confidently fulfill the order."；**如果支付尝试失败（如被拒），状态会退回 `requires_payment_method` 以便重试**——这是常被面试追问的"失败路径"细节。 |
| `canceled` | 可以在进入 `processing`/`succeeded` 之前取消；对 **ACH/ACSS/AU BECS/BACS/NZ BECS/SEPA** 这几种支付方式，即使在 `processing` 状态也能取消（但有时间窗口限制，可能失败）；**PaymentIntent 被确认（confirm）次数过多也会被系统自动转为 `canceled`**（防止暴力重试攻击的官方机制）。 |

**面试怎么考**：System Design 轮如果要求"设计一个支付状态机"，上表就是权威模板，尤其"失败退回 `requires_payment_method`"、"`requires_capture` 不是独立大状态而是 `processing` 的分支路径"、"确认次数过多自动取消"这三个细节是官方文档里才有、候选人容易漏掉的坑。[官方 / https://docs.stripe.com/payments/paymentintents/lifecycle / 访问 2026-09-01]

### 3.12 Connect charge 类型（direct / destination / separate charges and transfers）

原文摘录（`docs.stripe.com/connect/charges`）：Connect 用两大类三种 charge：

| 类型 | 谁收款（platform 还是 connected account） | 适用场景（官方原文举例） | 谁承担 Stripe 手续费 | 谁承担退款/拒付 |
|---|---|---|---|---|
| **Direct charges** | 直接打到 **connected account**，platform 通过 `application fee` 参数抽成 | 独立卖家电商平台、SaaS（如"账单支付"类应用），"customers who are often unaware of your platform's existence" | 可以选择由 connected account 或 platform 承担 | connected account 承担 |
| **Destination charges** | 打到 **platform**，随后自动把一部分转给 connected account | Marketplace，如"品牌化的服务+独立承包商"（举例：打车 app）、服务撮合市场 | platform 承担 | platform 承担（platform 可以反向 reverse transfer 找 connected account 追回） |
| **Separate charges and transfers** | 打到 **platform**，转账（transfer）与 charge **解耦**，可以延后/拆分给多个 connected account | 一笔交易涉及多个 connected account（如 DoorDash 式外卖平台）、下单时还不知道具体分给谁、需要先转账后收款 | platform 承担 | platform 承担 |

- **`on_behalf_of` 参数**（间接 charge 的补充机制）：把 connected account 设为"business of record"，Stripe 会自动：按该账户所在国家结算（减少拒付、避免货币转换）、用该国家的费率、用该账户的对客户账单描述符（statement descriptor）、（跨国时）在客户账单上用该账户的地址/电话而非平台的。
- **面试怎么考**：System Design 轮如果给一个"多方分账"的场景（外卖平台/打车/多商户市场），**先问清楚"一笔交易是否涉及多个收款方、下单时是否已知具体分给谁"，这两个问题直接决定该用哪种 charge 类型**，是这道题的破题关键，官方表格给的三个"适用场景"例子（SaaS/打车/DoorDash）可以直接套用。[官方 / https://docs.stripe.com/connect/charges / 访问 2026-09-01]

### 3.13 Balance / Payout 概念

原文摘录（`docs.stripe.com/connect/account-balances`）：
- 每个 Stripe 账户（含 platform 和每个 connected account）的余额分两种状态：**`pending`**（资金尚不可提现）和 **`available`**（可提现）。非 Connect 账户里，charge 成功后金额（扣除 Stripe 费用）先进 `pending`，**按 2 天滚动窗口**转为 `available`（因国家/账户而异）。
- Payout（提现）会相应扣减账户余额。
- Connect 场景下，platform 账户还有第三种余额状态：**`connect_reserved`**，用于覆盖 connected account 的负余额。
- **跨账户转账不会自动重试**："if you attempt to transfer funds from your platform's balance to a connected account's balance, but your platform has insufficient available funds, that transfer attempt fails... You must explicitly attempt the transfer again."——这是设计"平台内部转账系统"时必须处理的失败重试逻辑。
- **负余额处理**：退款/拒付会先在 charge 所在的账户产生负交易，Stripe 优先自动用未来收入抵消负余额；如果 connected account 持续负余额，platform 可能要承担（取决于 `losses_collector` 配置是 `stripe` 还是 `application`）；负余额超过 **180 天**，Stripe 会自动发起 **`connect_collection_transfer`** 把 platform 的 reserve 转去清零 connected account 余额。
- **合规性资金冻结期**（按国家）：泰国 10 天、美国 **2 年（!）**、其他国家 90 天——这是官方文档里一个非常反直觉但极重要的细节（"美国 2 年"常被面试官用来考察候选人是否真的读过文档还是靠常识猜）。
- **面试怎么考**：System Design 轮如果问"如何设计账本/余额系统"，`pending`/`available`/（Connect 场景下的）`connect_reserved` 三态模型 + "转账失败不自动重试，需要显式重试" + "负余额优先用未来收入抵消，超期后平台兜底"这套逻辑就是官方标准答案骨架，可以直接对应文件 2 第 4 节 Ledger 工程博客一起回答。[官方 / https://docs.stripe.com/connect/account-balances / 访问 2026-09-01]

## 4. Stripe 工程博客中与面试题对应的文章

### 4.1《Ledger: Stripe's system for tracking and validating money movement》（2024-02，stripe.dev/blog）

- **规模**："Ledger sees **five billion events** [per day] and **99.99%** of our dollar volume is fully ingested and verified within **four days**"；进一步"**99.999%** is monitored, categorized, and triaged through rich investigative tooling"；系统整体达到"**over 99.9999%** explainability of money movement, even as Stripe's data volume has grown **10x**"。
- **架构**：Ledger 是**不可变（immutable）交易日志**，把内部各系统建模为**状态机**，用"逻辑资金流（logical fund flows）在账户间移动"来表示money movement；基于**复式记账（double-entry bookkeeping）**原理，为分布式支付处理系统提供数学上可证明的正确性。
- **不可变性**原文："Transactions previously published into Ledger cannot be deleted or modified, and we can always reconstruct past state by processing all events."（不可删除/修改，任何历史状态都能通过重放事件重建——这是"事件溯源 Event Sourcing"模式的教科书式描述）。
- **数据质量三指标**：clearing（正确完成）、timeliness（及时到达）、completeness（数据完整）。
- **面试对应**：System Design 轮的 **Ledger** 题（`joeytor/StripeInterview` README、多篇面经均有提及）如果要"设计得像 Stripe 真实系统"，这篇文章给的模板是**不可变事件日志 + 复式记账 + 状态机建模 + 三维数据质量监控**，比"随便用消息队列+聚合"的朴素答案高出一个维度。[官方 / https://stripe.dev/blog/ledger-stripe-system-for-tracking-and-validating-money-movement / 2024-02]

### 4.2《Designing robust and predictable APIs with idempotency》（2017-02，stripe.com/blog）

- **三原则**：① **Handle failures consistently**——"Have clients retry operations against remote services. Not doing so could leave data in an inconsistent state that will lead to problems down the line."；② **Handle failures safely**——用 idempotency key 让客户端安全重试；③ **Handle failures responsibly**——用**指数退避 + 随机抖动**，"Be considerate of servers that may be stuck in a degraded state."
- **幂等 key 工作原理**：客户端为每次操作生成唯一 ID，通过 `Idempotency-Key` header 发送，"the server receives the ID and correlates it with the state of the request on its end."；连接失败但服务端其实已成功执行时，"the server simply replies with a cached result of the successful operation."
- **退避公式**：等待时间正比于 **2^n**（n 为已发生的失败次数）。
- **面试对应**：与文件本身第 3.1 节官方文档互相印证，是 Integration/System Design 轮"如何设计可靠重试机制"的经典参考答案来源，比文档本身多了"为什么"的设计动机。[官方 / https://stripe.com/blog/idempotency / 2017-02]

### 4.3《Online migrations at scale》（2017-02，stripe.com/blog）

- **场景**：迁移"hundreds of millions of Subscriptions objects"，如果串行处理、每个对象耗时 1 秒，"sequential processing would take over **three years**"。
- **标准 4 步 dual-write 模式**（面试 System Design/"如何做零停机数据迁移"的标准模板）：
  1. **Dual Writing**——新写入同时写旧表和新表，历史数据靠 lazy update + backfill 逐步补齐。
  2. **Changing Read Paths**——读路径切到新表，用 GitHub 的 **Scientist** 库跑"影子对比实验"验证新旧路径结果一致后再正式切换。
  3. **Changing Write Paths**——写路径反过来先写新表、旧表降级为归档，涉及"跨多个服务重构上千行代码"。
  4. **Removing Old Data**——确认没有代码依赖旧模型后，用后台任务懒删除旧表数据。
- **离线处理**：用 Hadoop MapReduce 做离线数据处理，避免直接对生产数据库跑昂贵查询，从而在不影响可用性的前提下并行处理海量数据。
- **面试对应**：这套"dual write → 切读 → 切写 → 清理"四步法几乎是所有大厂"零停机迁移"题的标准答案骨架，Stripe 官方博客提供了权威版本可以直接引用。[官方 / https://stripe.com/blog/online-migrations / 2017-02]

### 4.4《Scaling your API with rate limiters》（Paul Tarjan，stripe.com/blog）

- **四层限流/降载机制**（由轻到重）：
  1. **Request Rate Limiter**——按用户限制"每秒 N 次请求"，"has rejected millions of requests this month alone, especially for test mode requests."
  2. **Concurrent Requests Limiter**——限制同时进行中的请求数（如最多 20 个），针对"资源密集型端点被用户疯狂重试"的场景，触发频率远低于第一层（"12,000 requests this month"）。
  3. **Fleet Usage Load Shedder**——按"关键方法"（如创建 charge）vs"非关键方法"（如 list charges）预留独立的基础设施容量配额。
  4. **Worker Utilization Load Shedder**——最后一道防线，重大故障时才触发；流量按"关键方法 / POST / GET / test mode 流量"分级，**test mode 流量最先被丢弃**。
- **实现**：**token bucket 算法** + **Redis** 做集中式限流；强调渐进式降载以避免"flapping"（在过载和恢复之间来回震荡）。
- **面试对应**：这是"设计 Stripe 风格 rate limiter"System Design 题的**官方标准答案**，比自己发明的单一 token bucket 方案更完整——面试官很可能就是照着这篇文章的四层模型来打分的。[官方 / https://stripe.com/blog/rate-limiters / 作者 Paul Tarjan]

### 4.5《APIs as infrastructure: future-proofing Stripe with versioning》（Brandur Leach，2017-08-05，stripe.com/blog）

- Stripe 用 **`Stripe-Version` HTTP header**（形如 `2017-02-14`）做版本控制，而不是 URL 路径版本（如 `/v2/...`）；网关层跑一个**翻译层（translation layer）**，把旧版本的请求/响应结构转换成当前内部模型，**内部代码只需维护一套最新逻辑**，无需为每个历史版本都留一份实现。
- 每次发生不兼容变更就引入一个新版本，版本名用日期命名。
- **面试对应**：与本文件第 3.7 节官方文档互相印证，"版本翻译层"这个实现细节是文档本身没有的、只有工程博客才讲的架构决策，回答"如何设计向后兼容的 API 版本系统"时可以直接引用这个思路（每次请求先转换到内部规范形态，再统一处理，输出时再转换回客户端指定的版本）。[官方 / https://stripe.com/blog/api-versioning / 2017-08-05]

### 4.6《Fast and flexible observability with canonical log lines》（2019-07，stripe.com/blog）

- **核心思想**：每个请求结束时输出**一行"胖"结构化日志**，包含这次请求所有重要遥测信息，而不是分散成几十条零散日志。
- **实现**：请求生命周期中，各个模块往一个共享的 environment 对象上"装饰"字段；canonical logger 挂在 middleware 链**最末端**，统一把所有字段汇总成一行日志；用 Ruby 的 **`ensure` 块**包裹日志输出，保证**即使请求中途抛异常也一定会输出**这行日志——"guaranteeing you always have observability, especially during incidents."
- **存储与分析**：**Kafka** 把 canonical line 序列化成 **Protocol Buffers** 异步推送到 topic（不阻塞请求主路径），下游用 **Splunk**（近实时查询）+ **Redshift**（离线分析）两条腿走路。
- **定位**：canonical log lines **不是要替代 metrics 或分布式 tracing**，而是"调试时的第一站"——查询快、聚合成本低。
- **面试对应**：Bug squash/Integration 轮如果被问"你会怎么给这段代码加日志/可观测性"，"每个请求末尾输出一条结构化 canonical log line 而不是到处散落 print"是 Stripe 官方实践，直接引用能加分；也对应本文件第 3.8 节 `Request-Id` 的用法（canonical log line 里应该带上 Request-Id）。[官方 / https://stripe.com/blog/canonical-log-lines / 2019-07]

### 4.7《How we built it: Stripe Radar》（Ryan Drapeau，2023-03-29，stripe.com/blog）

- Radar 评估一笔交易的**超过 1,000 个特征**，在**小于 100 毫秒**内做出欺诈判定，**误伤合法支付的比例只有 0.1%**。
- 核心挑战三角：**准确 + 快 + 每笔交易运行成本要低**；欺诈本身是**稀有事件**（约每 1000 笔支付才有 1 笔欺诈），这对机器学习的样本不均衡处理提出更高要求。
- 三条改进路径：依托 Stripe 网络的广度做联合特征、持续迭代机器学习架构本身、优化"如何把拒绝原因解释清楚"给商户看。
- **面试对应**：`cn_forums.md` 已收录多道 Fraud Detection / Radar Rules 相关的 coding 题（如 femisowems repo 的"Catch Me If You Can: Fraud Detection"），这篇文章提供了"真实 Radar 是怎么做的"背景知识，System Design 轮如果被问"设计一个反欺诈系统"，"1000+ 特征 + 100ms 延迟预算 + 类别极度不均衡"这三个约束条件可以直接借用。[官方 / https://stripe.com/blog/how-we-built-it-stripe-radar / 2023-03-29]

### 4.8《Sorbet: Stripe's type checker for Ruby》/《Open-sourcing Sorbet》（stripe.com/blog）

- 背景：2017 年前后 Stripe 已有数百工程师、**1500 万行 Ruby 代码**，"Ruby 开始在接缝处散架"——新人难上手、老人不敢大改。
- Sorbet 静态分析代码库、建立各部分之间关系的理解，暴露为**类型错误、自动补全、悬浮文档、跳转定义/引用**；支持**渐进式引入类型标注**，不需要一次性重写。
- **面试对应**：与题目关系不大（属于"为什么 Stripe 大量用 Ruby 却也很重视类型安全"的背景知识），更适合 HM/behavioral 轮聊"Stripe 工程文化""为什么选 Ruby"这类话题时引用。[官方 / https://stripe.com/blog/sorbet / 访问 2026-09-01]

### 4.9《Stripe's payments APIs: the first 10 years》（Michelle Bu，stripe.com/blog）

- 回顾 Stripe 支付 API 十年演化：从最初只支持美国信用卡支付，到统一的 **PaymentIntents API**（对应本文件 3.11 节状态机）；提到 **Stripe CLI**、Dashboard 重设计等提升开发者体验的举措。
- **面试对应**：这篇文章是理解"为什么现在的 PaymentIntents 状态机长这样"的历史背景（早期 API 更简单粗暴，后来因为 SCA/3DS 等强监管认证需求才演化出 `requires_action` 等中间状态），HM/behavioral 轮如果被问"你对 Stripe 产品的理解"可以引用其中的演化脉络。[官方 / https://stripe.com/blog/stripes-payments-apis-the-first-ten-years / 访问 2026-09-01]

## 5. Stripe 开源项目

| repo | 用途 | 与面试的关系 |
|---|---|---|
| `stripe/stripe-python` | 官方 Python SDK（2040 星，持续维护，最后更新 2026-09-02） | Integration 轮如果用 Python 调 Stripe API，直接看这个库的实现能学到官方推荐的重试/错误处理写法；bug squash 轮如果拿 Stripe SDK 本身练手（虽然本次未在面经里见到），这里能找到真实历史 issue。 |
| `stripe/stripe-node` | 官方 Node.js/TypeScript SDK（4499 星） | 同上，JS/TS 候选人的参考实现；`stripe-interview/javascript-interview-prep` 用的 `node-fetch` 是原始 HTTP 层，与官方 SDK 的封装层可以对比着看。 |
| `stripe/stripe-java` | 官方 Java SDK（1002 星） | 同上，Java 候选人参考；`stripe-interview/java-interview-prep` 的 `pom.xml` 依赖（`guava`+`junit`）风格上和这个 SDK 的工程实践一脉相承。 |
| **`stripe/stripe-mock`** | **官方 mock HTTP server**，用 OpenAPI 规范生成假响应，"responds like the real Stripe API"（1641 星，Go 语言，持续维护） | **这是唯一一个官方出品、专门用来在没有真实网络/API key 的情况下跑 Stripe API 集成测试的工具**——非常适合拿来搭 Integration 轮/System Design 轮的本地练习环境（比文件 1 第 3.3 节列的第三方 mock 方案更贴近 Stripe 真实响应格式）。 |
| `stripe/stripe-cli` | 官方命令行工具（2169 星） | 本文件多处官方文档提到用 `stripe listen`/`stripe trigger`/`stripe sandbox create` 本地测试 webhook 和 API，是练习 Webhook/Integration 题时最值得装的官方工具；`docs.stripe.com` 现在甚至建议"用 CLI 在终端里读文档"（`stripe docs` 命令），说明 Stripe 近期在强推 CLI 作为一手信息源。 |
| `sorbet/sorbet`（原 `stripe/sorbet`，现独立组织） | Stripe 开源的 Ruby 静态类型检查器 | 与具体面试题关系不大，属于 Stripe 工程文化背景知识（见文件 2 第 4.8 节），HM/behavioral 轮可以用来展示"了解 Stripe 工程实践"。 |
| `stripe/veneur` | "A distributed, fault-tolerant pipeline for observability data"，实现 DogStatsD 协议/SSF 做 metrics 聚合，转发到多种下游存储 | System Design 轮如果考"设计一个 metrics 采集系统"（`cn_forums.md` 已收录"Metric Counter Library"一题），Veneur 是 Stripe 真实生产实现，可以直接引用其"分布式、容错管道"的设计思路。 |
| **`stripe/smokescreen`** | "A simple HTTP proxy that fogs over naughty URLs"——Stripe 生产环境用来代理"从 Stripe 发往外部的流量"（如 webhook 出站请求），用预配置的 **hostname allowlist（ACL）**只放行指定域名，防止恶意代码访问非预期的内部/外部服务 | **直接对应 Webhook/SSRF 追问**：面试官如果在 Webhook 系统设计题里追问"如果客户端配置的 webhook URL 指向了你内网的服务怎么办"（经典 SSRF 攻击面），Smokescreen 就是 Stripe 真实的解法——**出站请求必须经过 allowlist 代理**，这是标准答案。 |
| `stripe-archive/rainier` | Scala 贝叶斯推断库，"Stan, but on the JVM" | 与 SWE 面试关系较远，更偏 Data/ML 岗背景，附带说明其"已归档（archive）"——Stripe 近年把部分历史开源项目移到了 `stripe-archive` 组织下，不代表项目不重要，只代表不再积极维护。 |
| `stripe-archive/pd2pg` | 把 PagerDuty 数据导入 Postgres 做分析的小工具 | 同上，已归档，价值主要是"Stripe 工程团队怎么做内部数据分析"的旁证，非面试直接素材。 |

**面试怎么用这批开源项目**：Integration 轮练习时，**用 `stripe-mock` 起一个本地假 Stripe 服务器**（不需要真实 API key），配合 `stripe-python`/`stripe-node`/`stripe-java` 官方 SDK 写集成代码，是目前找到的**最接近 Stripe 官方出题环境**的本地练习组合；Webhook/System Design 追问"SSRF 怎么防"时直接点名 `smokescreen` 会显得对 Stripe 工程实践有真实了解。[官方 GitHub / https://github.com/stripe / 2026-09-01（部分描述经 WebSearch 交叉确认，GitHub API 请求本轮触发限速，未能逐个访问 API 核实最新 star 数/更新时间，`veneur`/`smokescreen`/`rainier`/`pd2pg` 的描述来自 WebSearch 摘要而非直接 API 调用，标注为 **[未直接验证具体数字，描述内容可信]**）]

## 6. 官方术语表

> 每条给出一句话官方定义（多数来自 docs.stripe.com 页面内嵌的术语解释气泡，本文抓取时这些站点内嵌定义会随相关词汇出现在正文中，如第 3 节引用的 "Connect is Stripe's solution for multi-party businesses..." 等）+ 关联到本文件/文件 1 里出现过的面试题。

| 术语 | 定义（官方口径） | 关联面试题 |
|---|---|---|
| **PaymentIntent** | 追踪一次收款尝试从创建到完成全生命周期的对象，驱动客户完成认证、driving a customer through the steps required to collect a payment | 本文件 3.11 节状态机；Coding/Integration 轮涉及"处理一次支付"的题基本都围绕它。 |
| **SetupIntent** | 用于**收集并保存**支付方式信息以备将来使用、**不产生实际扣款**的对象 | 与 PaymentIntent 共享同一套状态机（3.11 节），常在"先绑卡后续订阅扣款"场景里被提及。 |
| **Charge** | 早期 API 里代表一次实际扣款的对象，现被 PaymentIntent 取代但仍在历史版本 API/部分场景里出现 | `femisowems` 题 6（卡片校验）、`joeytor` README 的 Money Transfer 等题的底层概念。 |
| **Customer** | 代表一个终端用户/买家的对象，可挂载多个 payment method、订阅、发票 | 本文件 3.3 节 pagination 示例、3.9 节 metadata 示例都用 Customer 对象举例。 |
| **Invoice** | "statements of amounts owed by a customer... track the status of payments from draft through paid or otherwise finalized. Subscriptions automatically generate invoices, or you can manually create a one-off invoice."（官方术语气泡原文） | `cn_forums.md` 的 PaymentLedger/Subscription 相关题；`joeytor` README 的 Invoicer 题。 |
| **Subscription** | 代表客户对某个 Price/Product 的周期性订阅关系，驱动自动生成 Invoice | femisowems 题 5（Subscription Notification Scheduler）、多篇面经提到的订阅通知/邮件调度题。 |
| **Price / Product** | Product 描述"卖的是什么"，Price 描述"怎么定价"（一次性/周期性、金额、货币） | 与 Subscription 题配套出现的基础对象。 |
| **Connect** | "Stripe's solution for multi-party businesses, such as marketplace or software platforms, to route payments between sellers, customers, and other recipients"（官方术语气泡原文） | 本文件 3.12/3.13 节；System Design 轮的多方分账/marketplace 题。 |
| **Radar** | Stripe 的机器学习欺诈检测系统，见文件 2 第 4.7 节 | 文件 1 的 Fraud Detection/Radar Rules 系列题。 |
| **Atlas** | Stripe 帮创业者远程注册美国公司的产品 | femisowems 题 1（Atlas Company Name Check）直接点名。 |
| **Capital** | Stripe 面向平台商户的商业融资产品（预付款/贷款） | `joeytor`/`sahaia1` repo 提到的 Stripe Capital 相关题。 |
| **Issuing** | Stripe 让平台方发行实体卡/虚拟卡的产品 | 与 3.10 节金额格式化、卡号校验类题有背景关联，本次未见直接对应面试题。 |
| **Treasury** | Stripe 提供的"银行即服务"基础设施（存款账户、资金流转） | 未见直接对应面试题，属背景知识。 |
| **Terminal** | Stripe 的线下读卡器/POS 硬件+SDK 产品 | 未见直接对应面试题。 |
| **Sigma** | Stripe 提供的用 SQL 查询自己 Stripe 数据的分析产品（3.5 节提到用它替代高频只读 API 调用） | 与 rate limit 那道题的"减少 API 读请求"追问有关。 |
| **Link** | Stripe 的一键支付/记住支付信息的用户身份产品 | 未见直接对应面试题。 |
| **Checkout / Payment Element** | Stripe 官方推荐的托管收银台 / 可嵌入支付组件（3.11 节提到"现在官方推荐用 Checkout Sessions + Payment Element 而非直接用 PaymentIntent API"） | 影响 Integration 轮"如果面试官问你怎么收集支付信息"的最新推荐答案。 |
| **balance transaction** | 记录每一笔影响 Stripe 账户余额变动的底层账目条目（含手续费、退款、转账等） | 与 3.13 节 balance/reserve 概念、Ledger 题相关。 |
| **payout** | "the transfer of funds to an external account, usually a bank account, in the form of a deposit"（官方术语气泡原文） | 3.10/3.13 节；Ledger/账本类 System Design 题。 |
| **dispute / chargeback** | 持卡人向发卡行发起的拒付争议，会从对应账户扣减余额（3.12 节已展开各 charge 类型下的处理差异） | Connect 分账 System Design 题的追问重灾区。 |
| **refund** | 商户主动退款给客户，减少对应账户余额（区别于 dispute 是持卡人发起的争议） | 同上。 |
| **reversal** | 撤销一笔 transfer（如 platform 向 connected account 追回错误转账），常见于 destination charge 的退款场景（3.12 节） | Connect 多方分账题。 |
| **MCC**（Merchant Category Code，商户类别码） | 银行卡行业标准，标识商户所属行业类别 | femisowems 题 3（Fraud Detection）直接使用这个术语。 |
| **BIN**（Bank Identification Number） | 卡号前 6 位，标识发卡行/卡组织 | femisowems 题 2（Card Range Obfuscation）核心概念。 |
| **3DS / SCA**（3D Secure / Strong Customer Authentication） | 信用卡交易的额外认证层，欧盟 PSD2 监管要求的强客户认证；对应 PaymentIntent 的 `requires_action` 状态（3.11 节） | System Design/PaymentIntent 状态机题的高频追问点。 |
| **KYC**（Know Your Customer） | 平台/金融机构对客户身份的合规核实流程 | `cn_forums.md` 收录的"KYC Data Validation"一题（Team Screen，归属存疑）。 |
| **PCI**（PCI DSS，Payment Card Industry Data Security Standard） | 支付卡行业数据安全标准，规范如何存储/传输卡信息 | 呼应 3.9 节"不要把卡信息存进 metadata"的官方警告；System Design 轮问"怎么存卡信息"的合规背景。 |

## 附：来源清单 + 未能访问

**已成功访问/验证的来源：**
- WebFetch 直读 `docs.stripe.com`：`api/idempotent_requests`、`api/errors`、`error-handling`、`api/pagination`、`webhooks`、`rate-limits`、`expand`、`api/versioning`、`upgrades`、`api/request_ids`、`api/metadata`、`currencies`、`payments/paymentintents/lifecycle`、`connect/charges`、`connect/account-balances` —— 共 15 篇官方文档全文成功抓取，均未被拦截，**无需使用 `r.jina.ai` 前缀重试**（docs.stripe.com 本身对 WebFetch 友好）。
- WebFetch 直读 `stripe.com/jobs`、`stripe.com/jobs/culture`、`stripe.com/jobs/compatibility`、`stripe.com/careers/listing/software-engineer-new-grad/...`、`stripe.dev/blog/ledger-...`、`stripe.com/blog/idempotency`、`stripe.com/blog/rate-limiters`、`stripe.com/blog/online-migrations`。
- WebSearch 约 20 次，覆盖招聘流程、面试形式、工程博客定位、开源项目描述。
- GitHub REST API（`api.github.com/repos/stripe/...`）成功获取 `stripe-python`/`stripe-node`/`stripe-java`/`stripe-mock`/`stripe-cli` 五个仓库的 star/更新时间数据；`sorbet/sorbet`、`stripe/veneur`、`stripe/smokescreen`、`stripe-archive/rainier`、`stripe-archive/pd2pg` 因**本次会话与文件 1 共用同一 GitHub API 限额，检索后期触发 60 次/小时限速**，改用 WebSearch 摘要替代，已在第 5 节标注。

**未能访问 / 检索为空：**
- `stripe.com/jobs/emerging-talent` 直接路径返回 **404**（实际路径已变为 `stripe.com/careers/emerging-talent` 或按地区分流路径，未逐一核实每个地区变体）。
- Stripe 官方**独立的"面试流程详解"页面/candidate FAQ**——多次定向 WebSearch（`site:stripe.com interview process`、`site:stripe.com candidate FAQ`）均未命中，判定为**当前不存在**这样的公开页面（详见第 2 节讨论）。
- Patrick Collison / Stripe Sessions / Increment 杂志里关于"工程招聘具体怎么做"的一手原始文本——本次只拿到经二手转述整理的只言片语（growth.eladgil.com 对访谈的转述明确说"不含工程招聘具体细节"），未直接核实播客/杂志原始逐字稿。
- 官方术语表里部分产品（Issuing、Treasury、Terminal、Link）**未找到与之直接对应的公开面试题**，术语定义本身来自 docs.stripe.com 页面内嵌气泡，但未逐一去对应产品文档首页做交叉验证，标注为背景知识而非面试实锤。

