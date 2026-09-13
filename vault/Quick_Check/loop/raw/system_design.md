# Stripe 系统设计轮（System Design）原始资料汇编

> 采集日期：2026-09-01。方法：WebSearch + WebFetch（约 65 次抓取/检索）。来源覆盖 Blind（11 帖）、LeetCode Discuss（2 帖）、Glassdoor（仅检索摘要，详情页被 Cloudflare 拦截）、Medium（3 篇一手面经/分析）、Exponent（3 页）、Hello Interview（4 页）、interviewing.io、ByteByteGo/Alex Xu（4 页）、DesignGurus（3 页）、Stripe 官方工程博客（4 篇）、Stripe 官方文档（6 页）、以及十余个二手汇总站（Educative、systemdesignhandbook、techinterview.org、linkjob、prepfully、codinginterview、ophyai、techprep、interviewkickstart、getsdeready、vervecopilot、nodeflair、svix、systemdesignschool、systemdr）。
> 一亩三分地相关帖（`stripe-software-engineer-556482`、`thread-1095724`、`thread-1145788`）全部被反爬墙拦截，仅能引用搜索摘要；标注为「未能直接阅读」。
> 每条事实后附 URL + 日期（帖子/文章日期；无日期者标「访问 2026-09-01」）。
> 可信度分级：**[一手]** = 面试者本人叙述；**[官方]** = Stripe 官方博客/文档；**[二手]** = 培训站/汇总站转述；**[推断]** = 本文综合判断。

---

## 1. Stripe SD 轮形式与是否考应届

### 1.1 结论速览（[推断]，综合下列证据）

| 问题 | 结论 | 置信度 |
|---|---|---|
| 应届（New Grad / L1）是否有独立 SD 轮？ | **通常没有。** 应届 onsite = Coding + Integration + Bug Squash（+ HM/行为），设计能力在 Integration 轮和 coding 追问里考。 | 高（4 个独立来源一致，含 2026-02 一手面经） |
| 有工作经验（L2/mid 及以上）是否有 SD 轮？ | **有，1 轮**（少数 2021 年帖子称 2 轮），45 min（部分来源 45–60 min）。 | 高 |
| 时长实际可用时间 | 45 min 含开场自我介绍与结尾提问，**真正设计约 30–35 min**。 | 高（Blind 2021-03 一手 + Exponent） |
| 工具 | Whimsical（在线画图），不是白板。 | 高（Exponent + Blind） |
| 题目风格 | 「实用、贴近 Stripe 日常」，题干常给一大段业务描述让你自己抽取需求；不考「设计 Instagram」类泛题（偶尔出现但少）。 | 高 |
| 侧重 | 正确性/幂等/失败模式/API 契约 > 海量 QPS 估算。 | 高 |

### 1.2 证据清单

**应届不设独立 SD 轮：**

- Exponent《Stripe SWE Interview Guide》：*"New grad and entry-level loops are often leaner, typically coding, integration, and debugging without a full system design round."* 系统设计轮 *"Who takes it: Mid-level and above candidates; typically excluded from new grad/entry-level interviews"*。— https://www.tryexponent.com/guides/stripe-swe-interview （更新于 2026-08 下旬，页面标「9 days ago」）[二手]
- Exponent《Stripe System Design Interview (2026 Guide)》等级表：**New Grad/L3：No standalone system design round; design appears within practical integration round**；Mid-level & above：dedicated core onsite round；Senior：可能多一轮 architecture 或单独 API design round；EM：1–2 轮设计。— https://www.tryexponent.com/blog/stripe-system-design-interview （2026，「last updated 3 months ago」≈2026-06）[二手]
- linkjob《How I Nailed Stripe Integration Round in 2025》：*"Stripe's New Grad virtual onsite has three rounds: coding, integration, and bug squash, taking about three and a half hours total"*，每轮 1 h、中间 15 min 休息，Zoom + 在线 coding pad。— https://www.linkjob.ai/interview-questions/stripe-integration-round/ （2025）[二手/半一手]
- LeetCode Discuss《Stripe New Grad Interview Experience 2026》（Abhishek Kumawat，Java，被拒）：OA（1 题）→ Phone screen 60 min（多 part 题 45 min + 15 min 聊 Stripe）→ Virtual onsite：**Advanced Programming 45 min**（多 part，追问 edge cases）+ **Bug Squash**（大代码库调试，最难）→ **Managerial** 轮（teamwork/ownership）。**全程无 SD 轮。** — https://leetcode.com/discuss/post/7566910/ （2026-02-09）[一手]
- Medium《My Stripe Interview Experience (2025–2026)》（班加罗尔 SWE Intern）：HackerRank OA 60 min（1 题 3 个递进 sub-task）→ Tech screen 60 min → Onsite：Programming Exercise（数据解析/预处理）+ **Integration Round**（私有 GitHub repo + API docs + 可上网；sub-task A 文件操作/数据抽取，sub-task B 调外部 API 并处理响应）→ Managerial。无 SD 轮。— https://medium.com/@diyaag2020/my-stripe-interview-experience-2025-2026-a-journey-to-the-final-round-19990fa6876a （2025-09 至 2025-11）[一手]
- Blind「stripe new grad」相关帖（检索摘要）：*"New grad interviews at Stripe feature non-LeetCode type coding... be prepared for a 'bug squash' round"*；*"new grads may encounter design and bug squash rounds, not just LC-type coding"*（此处「design」在上下文里指 coding 题中的接口设计，非独立轮）。— https://www.teamblind.com/company/Stripe/posts/stripe-interview?page=13 （访问 2026-09-01）[二手摘要]
- 一亩三分地《Stripe Graduate SDE》帖（仅摘要可见）：OA 为 HackerRank 信用卡号段识别（Visa/Mastercard）题；未提及 SD 轮。— https://www.1point3acres.com/bbs/thread-1095724-1-1.html （未能直接阅读，日期不详）[二手摘要]

**应届「设计」考法在哪里：**

- Exponent：*"design shows up inside the integration round instead... you build a feature against a real repo and have to decide how to wire services together."* — https://www.tryexponent.com/blog/stripe-system-design-interview （2026）
- linkjob：Integration 轮考「Payment Intents API、Customers API、Webhooks」的接入、错误处理、可维护代码；示例任务「BikeMap」读 JSON→转 dict→来回 ETL。— https://www.linkjob.ai/interview-questions/stripe-integration-round/ （2025）
- LeetCode Discuss（Stripe SDE OA + 面经，检索摘要）：coding 轮之一是「实现一个去重系统：追踪重复请求、把重复请求合并成一个只处理一次」——这本质是 **幂等键** 的编码版。— https://leetcode.com/discuss/post/6896919/ （访问 2026-09-01）[一手摘要]
- techinterview.org：Stripe 在 coding/API 轮就会追问 *"What happens when a request arrives twice, so the customer is not charged twice"*。— https://www.techinterview.org/post/3233476020/stripe-bug-bash-api-design-interview/ （更新 2026-07-02）[二手]

**有经验者 SD 轮的形式：**

- Blind（5 YOE，senior，2021-03-11）：*"45-minute on-site interview (approximately 30 minutes of actual discussion after introductions and Q&A time)"*，候选人担心 30 min 讲不完分区/扩展/瓶颈。评论区 Salesforce 员工：30 min 讲不完说明不够 senior；Amazon 员工反驳。— https://www.teamblind.com/post/stripe-system-design-interview-tshyvotg （2021-03-11）[一手]
- Blind「Design 1 interview」（Toronto，Money as a Service 团队，2025-03-18 发帖，04-01 更新）：45 min；面试官给「**一大段系统描述**」而非传统 prompt，候选人认为「写得不清楚、面试官也没讲清楚，浪费了很多时间」，被拒。— https://www.teamblind.com/post/stripe-onsite-design-1-interview-ps7pgzwy （2025-03/04）[一手]
- Blind（6.5 YOE，L2/L3，2021-06-19）：5 轮 = Programming Exercise / Manager / **System Design** / System Integration（解析 JSON + HTTP 调 API + 业务逻辑，用 OkHttp+Gson）/ Bug Squash。SD 轮候选人「覆盖了 API、数据建模、组件图、数据库选择、潜在问题，对每个关键决策讲了多种方案的利弊，面试官说 you did very well」；最终因 Bug Squash 超时被拒。— https://www.teamblind.com/post/onsite-experience-at-stripe-umo0fobx （2021-06-19）[一手]
- Blind（2 YOE，2021-04-27）微软员工评论：*"one round of live debugging using your own IDE... One round of coding..2 system design rounds...2 adaptability rounds"*，SD 「related to stripe architecture so you can check out their engineering blog」。— https://www.teamblind.com/post/stripe-interview-4ayknryk （2021-04-27）[二手]
- Blind（L2，Seattle，2025-04-07）：发帖人问 L2 SD 轮考 HLD 还是 LLD，投票「in depth low level Design」vs「High Level only」，无人给出答案。— https://www.teamblind.com/post/stripe-system-design-interview-hq5h6ewo （2025-04-07）[一手提问]
- Blind（~2 YOE，2024-10-06）：Stripe 现任面试官表示可 DM/付费 mock，公开帖无细节。— https://www.teamblind.com/post/stripe-system-design-interview-expectation-kak4gqwj （2024-10-06）
- Blind（M1/senior，2024-04-03）：问「是否会考 payment gateway/wallet 这种支付相关题，还是像 design Instagram 一样宽泛」，无有效回答。— https://www.teamblind.com/post/stripe-on-site-system-design-interview-fhqnsnny （2024-04-03）
- Blind（L3，9 YOE，印度，2025-08-30）：问 SD + HM 轮面经；评论「very easy, use ChatGPT」；另一评论建议去 r/leetcode 看。— https://www.teamblind.com/post/stripe-system-design-and-hm-interview-i8a2p1m5 （2025-08-30）
- interviewing.io《Stripe Interview Process & Questions》：Onsite 5 h：Coding 1 h / **System Design 1 h**（"large-scale systems with scalability and reliability concerns"）/ Bug Bash 1 h / Integrations 1 h（Staff 以下）/ Presentation 1 h（Staff+）/ Behavioral 1 h；AI 使用严格禁止。— https://interviewing.io/stripe-interview-questions （访问 2026-09-01）[二手]
- nodeflair（273 份面经汇总，检索摘要）：*"Stripe onsite interviews include 1 design round... designing an entire service with scalability, reliability, and usability concerns"*；*"It is perfectly fine for applicants to Google for solutions during the interviews"*；备考推荐 DDIA + Alex Xu。— https://nodeflair.com/blog/stripe-software-engineer-interview-questions-and-process （访问 2026-09-01，详情页 403）[二手摘要]
- Glassdoor（检索摘要）：*"System design felt very grounded—instead of drawing huge scalable architecture, candidates basically just talked through failure modes and backward compatibility."* *"surprisingly technical, requiring actual understanding of idempotency and API design rather than just drawing high-level boxes."* 部分岗位有 take-home：*"designing a payment retry service with exponential backoff"*，要求测试+文档。— https://www.glassdoor.com/Interview/Stripe-Interview-Questions-E671932.htm （访问 2026-09-01，详情被拦截）[二手摘要]
- ophyai（2026-07）：把 Stripe loop 描述为 Coding×2 + **API design round** + System design round + Behavioral，称 API design 是 Stripe 的「signature differentiator」。— https://ophyai.com/blog/company-guides/stripe-interview-guide （2026-07）[二手]

### 1.3 「实用、少谈规模、多谈正确性」的证据

- Emily（Senior Backend，2026-05-20）：*"A senior system design interview is not really about the boxes and arrows you draw in the first 10 minutes... entirely about the 40 minutes that follow."* 面试官 10 min 看完架构后 45 min 全部在压 failure modes。— https://medium.com/@emilyhustlenyc/every-question-i-was-asked-in-stripes-system-design-interview-f6f19c2e62d6 （2026-05-20）[一手]
- Exponent：*"Stripe's system design round focuses less on standard design patterns and more on 'a problem about Stripe' where the real test is how you extract the problem from all the context provided."* 与 FAANG 差异：「像和资深同事做 design review，而非 trivia」。— https://www.tryexponent.com/blog/stripe-system-design-interview （2026）
- systemdesignhandbook：*"designing a standard web application makes a lost packet... an annoyance. Financial infrastructure treats this as a catastrophe."* — https://www.systemdesignhandbook.com/guides/stripe-system-design-interview/ （2026）
- Medium h7w：*"Idempotency and atomicity are not aspirational best practices at Stripe but the minimum bar for production readiness"*；*"building something that is boringly correct when everything else is on fire"*。— https://medium.com/h7w/the-stripe-system-design-question-that-separates-senior-from-staff-engineers-ecb9a98af1fd （2026-04-03）
- Alex Xu Vol.2 支付章（Pragmatic Engineer 转载）：题设 100 万笔/天≈10 TPS，*"Focus on correctness over throughput: At 10 TPS, reliability and consistency matter more than raw performance."* — https://newsletter.pragmaticengineer.com/p/designing-a-payment-system （2022-03-17）

---

## 2. Stripe 报道过的题目总表

「来源数」= 独立来源数（一手 + 二手）。「追问」栏合并了各来源记录的面试官追问。

| # | 题目 | 面试官追问（合并） | 来源数 | URLs（日期） |
|---|---|---|---|---|
| 1 | **设计 Webhook 投递系统**（"Stripe needs to notify merchants when an event happens... receives an internal event, finds the merchant's configured webhook URLs, delivers HTTP POST"；约束 10k events/s 全球、接受即必须尝试投递） | ① 商户端点持续 500 怎么办（→ 指数退避 1min/5min/…最长 3 天）② **噪声邻居**：商户 B hang 30 s 且事件量巨大，怎么隔离商户 C（2 s 超时不够→租户隔离、熔断、per-tenant 队列）③ **SSRF/DNS rebinding**：校验时解析为公网 IP、真正请求时 TTL 过期解析到内网怎么办（→ 校验后直连已验证 IP，Host 头带原域名）④ 商户要求 exactly-once 怎么办（→ 不可能，payload 带 event_id 由接收方去重）⑤ 签名校验、重放攻击 ⑥ 顺序保证 ⑦ 重试后是否要重新签名 | 8 | Emily Medium 2026-05-20 https://medium.com/@emilyhustlenyc/every-question-i-was-asked-in-stripes-system-design-interview-f6f19c2e62d6 ；Blind staff 2022-06-15 https://www.teamblind.com/post/stripe-staff-design-interview-iw4qxp2i ；Glassdoor QTN_4393528「Architecture challenge, design a system for delivering webhooks to customers」；Glassdoor QTN_7723981「For systems design I got a webhook design question」（均仅标题可见，访问 2026-09-01）；interviewkickstart 2025-12-18 https://www.interviewkickstart.com/interview-questions/stripe-interview-questions ；prepfully 2026-08-13 https://prepfully.com/interview-guides/stripe-software-engineer ；techprep 2026 https://www.techprep.app/blog/stripe-interview-process ；Exponent 2026 |
| 2 | **设计 Ledger / Bookkeeping 服务**（Exponent 称「signature Stripe prompt」；Hello Interview/Exponent 题库「Design a Bookkeeping Service」；变体「multi-currency ledger」） | 双记账、不可变、余额如何算（实时 vs 物化）、多币种、如何证明 debit=credit、清算账户（clearing）非零怎么查、读写路径、分片热点账户、与外部对账 | 6 | Exponent 2026 https://www.tryexponent.com/blog/stripe-system-design-interview ；Exponent 题库（1 年前）https://www.tryexponent.com/questions?company=stripe&type=system-design ；Blind staff 2022-06-15；Educative 2026-03-10 https://www.educative.io/blog/stripe-system-design-interview-questions ；systemdesignhandbook 2026；techprep 2026「Distributed Ledger design」 |
| 3 | **设计幂等的支付/Charge API**（"Design the core of our payments API. A merchant wants to charge a card. Walk me through it." / "a system that processes payments and never double-charges on a retry" / "card payment authorization flow"） | ① 重试打到另一实例、第一个请求还没写幂等记录——如何 exactly once（→ DB 唯一约束 INSERT…ON CONFLICT 先「claim」再调卡网络；Redis 只是 fast path）② 调用卡网络后崩溃怎么办（recovery point / 状态机）③ 参数不同但 key 相同（→ 422）④ 超时的支付到底成没成功（→ 查询/对账/saga）⑤ 银行重复回调 ⑥ 区域分区 ⑦ 版本兼容 | 7 | Medium h7w 2026-04-03；techinterview.org 2026-07-02 https://www.techinterview.org/post/3233476020/stripe-bug-bash-api-design-interview/ ；techinterview.org 2026-04-16 https://www.techinterview.org/post/3233460268/stripe-interview-guide-2026-process-bug-bash-round-and-payment-systems/ ；Educative 2026-03-10；systemdr 2026-06-02 https://systemdr.systemdrd.com/p/design-stripe-payments-the-senior ；Hello Interview payment-system；ophyai 2026-07「Design duplicate payment prevention」 |
| 4 | **设计 Rate Limiter**（分布式；interviewing.io 记为「Design a rate limiter in any programming language」——coding 版也出现） | token bucket vs sliding window、Redis 原子性、多实例共享状态、多区域一致性、fail-open/fail-closed、优先级/负载削减、429 响应头 | 6 | Exponent 2026 + 题库（13 answers，15 days ago）；interviewing.io；TechPrep YouTube《Rate Limiter: System Design Interview (Stripe & Amazon Offers)》https://www.youtube.com/watch?v=dpEOhfEEoyw ；vervecopilot 2026-05-01 https://www.vervecopilot.com/hot-blogs/top-30-stripe-interview-questions ；techinterview.org 2026-04-16「distributed rate limiter for the Stripe API」；getsdeready 2024-12-17 |
| 5 | **设计 Transactions + Transaction Log 的 API**（Exponent：「narrower, API-first cut of the same domain, common in product-team loops」） | 分页、过滤、幂等 POST、版本、错误结构、expand | 1 | Exponent 2026 |
| 6 | **设计 Metrics 服务 / APM / Monitoring & Alerting 系统** | 时序存储、写入速度 vs 聚合、告警去抖 | 4 | Exponent 2026 + 题库（Metrics 4 年前；APM 2 年前）；Blind staff 2022-06-15「monitoring and alerting」；prepfully「logging system」 |
| 7 | **重设计内部授权（Authorization）系统 / IAM**（"fleet-wide rollout across fixed service count with target RPS"；interviewing.io：「build a simple version of Identity Access Management」） | 策略管理（慢路径）与执行（快路径）分离、灰度、缓存策略、RPS | 3 | Exponent 2026；interviewing.io；vervecopilot「authorization system for Stripe APIs」 |
| 8 | **分布式 LRU Cache** | 驱逐、一致性、热点 | 2 | Exponent 题库（10 answers，3 months ago）；Exponent 博客 |
| 9 | **Login System / 全站统一登录** | 会话、MFA、token | 2 | Exponent 题库（「User Login System」3 months ago；「Login System for All of Stripe's Client-Facing Sites」2 months ago） |
| 10 | **Subscription billing / proration / 发票** | 计费周期、按比例、发票状态机、dunning 重试 | 4 | vervecopilot 2026；ophyai 2026-07「subscription billing API」；getsdeready 2024-12-17；techinterview.org 检索摘要 |
| 11 | **Notification / 支付事件通知系统（大流量）** | Kafka、重试、DLQ、幂等 | 3 | vervecopilot；interviewkickstart 2025-12-18；prepfully |
| 12 | **Fraud detection / Radar 实时评分** | 规则引擎 + ML 实时打分、延迟约束、chargeback 反馈闭环、模型降级时流程怎么走 | 4 | techinterview.org 2026-04-16；vervecopilot；ophyai；Educative 追问「How does fraud model degradation affect the flow?」 |
| 13 | **Refunds API / Disputes & Chargebacks** | 部分退款、状态机、证据提交、与 ledger 联动 | 3 | ophyai；vervecopilot；getsdeready |
| 14 | **Marketplace 分账 / Connect payouts** | 平台 charge → transfer → payout；余额 pending/available；负余额 | 1 | ophyai 2026-07「marketplace payment split system」 |
| 15 | **Reconciliation engine（对账引擎）** | 结算文件解析、mismatch 分类、cut-off 时间 | 1 | codinginterview.com https://www.codinginterview.com/guide/stripe-interview/ （访问 2026-09-01） |
| 16 | **Feature flag 服务；KV store；缓存查询结果；实时支付分析数据管线；负载均衡器；排查线上 API 故障** | — | 1 | vervecopilot 2026（该站为 AI 生成汇总，可信度低） |
| 17 | **Design TurboTax / DocuSign / Twilio** | — | 1 | Exponent 题库（均「16 days ago」，疑为平台批量补充，非一手） |
| 18 | 泛题：Instagram、Ticketmaster、URL shortener | Exponent 称「appear but less distinctive」 | 1 | Exponent 2026 |
| 19 | Product catalog 数据库设计；「大公司大系统的 HLD 怎么画」 | — | 2 | prepfully；interviewkickstart |

**一手 vs 二手权重说明（[推断]）**：一手面经明确出现过的题只有 **Webhook 投递**（Emily 2026 + Glassdoor 两条 + Blind staff 转述）、**Ledger**（Blind staff 转述）、**Monitoring/Alerting**（Blind staff 转述）、以及「一大段业务描述让你自己抽需求」的 Money-as-a-Service 题（Blind 2025）。Rate limiter、Metrics、Auth、LRU、Login 来自 Exponent「verified candidate or interviewer reports」；其余（订阅、欺诈、退款、Connect 分账）主要来自培训站，应视为「可能出、值得准备」而非「有人被问过」。

---

## 3. 评分维度

### 3.1 Exponent 的五维 rubric（最具体的一份）

来源：https://www.tryexponent.com/blog/stripe-system-design-interview （2026）[二手，自称基于候选人/面试官报告]

1. **Problem framing**：把模糊 prompt 变成清晰问题陈述；先抽需求再设计（建议「两句话复述题目」）。
2. **API and data-model design**：接口「易用、难误用」；能为版本化、部分失败辩护。**Stripe 权重最高的一维。**
3. **Failure-mode and scale reasoning**：找热点、全球复制/regionality、缓存放哪。
4. **Separation of concerns**：慢的策略管理路径 vs 快的执行路径分开；组件边界干净。
5. **Delivery beyond the diagram**：rollout、测试、监控、跨团队对齐（staff 级预期；缺了会「cap below staff」）。

常见失分：不先框需求就画；当成泛白板题不聚焦接口；**单 region 单库**（「reads as inexperience」）；把多个关注点塞进一个组件；漏掉 rollout/测试/监控。

### 3.2 其他来源的评分描述

- Exponent SWE guide：*"Stripe weighs API design heavily"*；考察 requirement clarification、clean decomposition、expressive API design、trade-off reasoning、约束变化时的适应性沟通。— https://www.tryexponent.com/guides/stripe-swe-interview （2026-08）
- techinterview.org（API design 轮）：面试官听的是 **edge cases 而非 happy path**：字段命名让开发者「猜得对」、错误响应可操作、幂等防重复扣款、版本/向后兼容、网络失败与重试。强候选人「treat the API as a product whose users are developers」；弱候选人「produce endpoints that technically function」。— https://www.techinterview.org/post/3233476020/stripe-bug-bash-api-design-interview/ （2026-07-02）
- ophyai：Clear thinking & communication / Developer empathy（用户是工程师）/ Rigor without over-engineering / Intellectual honesty & humility / Impact-oriented prioritization；API 轮考 resource modeling + HTTP 语义、结构化错误、幂等与重试安全、版本、分页、鉴权，并点名 **expand pattern**。— https://ophyai.com/blog/company-guides/stripe-interview-guide （2026-07）
- interviewing.io：*"Stripe emphasizes proactivity and independent thinking"*；评估决策依据、技术论证、集成问题。— https://interviewing.io/stripe-interview-questions
- engineeringenablement substack：把 Stripe 当「暴露支付为可编程 API 的基础设施公司」；强候选人体现「developer-facing reliability」、内部正确性与外部可预测性的平衡、trade-off 推理、API 设计与分布式系统思维融合；可观测性的目的是「building trust with developers」。— https://engineeringenablement.substack.com/p/how-i-would-approach-the-stripe-system （2026-07-21）
- systemdesignhandbook：核心不变量「ledger value must be conserved through explicit, balanced entries」「history must remain immutable」；每次状态变化要有审计轨迹；「designs that remain correct during infrastructure failures」。— https://www.systemdesignhandbook.com/guides/stripe-system-design-interview/ （2026）
- Educative 追问模式：「How do you handle duplicate webhook events?」「What happens during a regional partition?」「How does fraud model degradation affect the flow?」「How do you reconcile against external bank reports?」— https://www.educative.io/blog/stripe-system-design-interview-questions （2026-03-10）
- Medium h7w（senior vs staff 分水岭）：senior 答「网关查 Redis 幂等键→处理→缓存结果」在**并发 cache miss、外部授权后部分失败、webhook 失败触发重复扣款**三种情况下崩；staff 答把支付当**持久状态机**：DB 幂等表 upsert 先 claim → 外部调用 → 双记账 ledger → outbox 发事件 + DLQ → 每日对账 → saga 补偿。— https://medium.com/h7w/the-stripe-system-design-question-that-separates-senior-from-staff-engineers-ecb9a98af1fd （2026-04-03）
- Emily 一手反馈原话：*"My initial architecture was sound, but my ability to reason about failure domains and system abuse was not at the level they needed."* — 2026-05-20
- Stripe 运营原则被多站引用为评价参照：「users first」「move with urgency」「think rigorously」。— interviewing.io 检索摘要

### 3.3 综合后的「Stripe SD 评分主线」（[推断]）

```
需求抽取（2 句话复述 + 不变量：钱不能丢/不能双扣/账要平）
  → API 契约（资源建模、幂等键、错误码、版本、分页、expand）
  → 数据模型（业务对象 可变 vs Ledger 条目 不可变；金额整数最小单位）
  → 一致性/幂等（DB 唯一约束是真相源，Redis 只是加速；状态机）
  → 失败处理（重试+退避+抖动、DLQ、outbox、saga 补偿、熔断、租户隔离）
  → 对账/审计（每日 vs PSP/银行结算文件；clearing 账户归零）
  → 可观测性 + rollout（四黄金指标、request id、dark launch、feature flag）
```
「Stripe cares about correctness of money」不是原话出处可考的引语，但同义表述遍布：Better Engineers *"Money is the one domain where 'eventually consistent' is not a strategy — it's a liability"*（https://betterengineers.substack.com/p/how-to-design-a-payment-service ，2026-07-23）；Stripe Ledger 博客「>99.9999% explainability of money movement」（2024-02-16）。

---

## 4. 六大题的中文模型答案

选题依据：一手出现频率 + 培训站覆盖度。顺序：① Webhook 投递 ② 幂等支付/Charge API ③ Ledger ④ 分布式 Rate Limiter ⑤ 订阅计费与发票 ⑥ 账户间转账 / Connect 分账与 Payout。
每题按「需求 → API → 数据模型 → 状态机 → 幂等/投递语义 → 失败处理 → 对账/审计 → 规模 → 监控 → 追问预案」组织，并标注取材来源。

### 4.1 设计 Webhook 投递系统

**取材**：Emily 一手面经（2026-05-20）；Stripe 官方 webhooks 文档（https://docs.stripe.com/webhooks ，访问 2026-09-01）；systemdesignhandbook《Design a Webhook System》（2026）；Svix Stripe webhooks review（2026-08-26）；systemdesignschool webhook solution；codelit/hookray 检索摘要。

**1) 需求澄清（2 min）**
- 功能：内部事件（`payment_intent.succeeded` 等）→ 查找商户订阅的 endpoint → HTTPS POST；商户可注册/更新/禁用 endpoint 与事件类型过滤；可查看投递日志、手动重发。
- 非功能：**至少一次**投递（接受即保证尝试）；10k events/s（Emily 题设）；p99 首次尝试延迟 < 1 s；商户端点不可信（任意 URL、可能慢/挂/恶意）；租户隔离；可审计。
- 明确不做：exactly-once（网络不可能）；严格全局顺序（Stripe 官方文档明说不保证顺序）。

**2) API**
```
POST   /v1/webhook_endpoints        {url, enabled_events[], description}  → {id, secret: "whsec_..."}
GET    /v1/webhook_endpoints/:id
POST   /v1/webhook_endpoints/:id    {enabled_events, disabled?}
DELETE /v1/webhook_endpoints/:id
GET    /v1/events?type=&created[gte]=   （商户可拉取补漏）
POST   /v1/events/:id/resend?endpoint=  （手动重发；Stripe 支持事件创建后 15 天内 Dashboard 重发、CLI 30 天）
```
出站请求：`POST {url}`，头 `Stripe-Signature: t=<ts>,v1=<HMAC-SHA256(secret, ts + "." + body)>`；body 为 Event 对象 `{id: "evt_...", type, created, data:{object}, api_version, livemode}`。事实：Stripe 限每账户 16 个 endpoint；仅 TLS ≥1.2；3xx 视为失败；要求 endpoint「快速返回 2xx 再做复杂逻辑」。

**3) 数据模型**
- `webhook_endpoints(id, account_id, url, enabled_events[], secret_current, secret_previous, secret_previous_expires_at, status[active|disabled], api_version, created_at)` — 密钥轮换期双密钥并存 ≤24 h（Stripe 官方行为）。
- `events(id, account_id, type, payload jsonb, api_version, created_at)` — **不可变**；按账户当时 pinned 的 API 版本生成一次，之后不改。
- `deliveries(id, event_id, endpoint_id, status[pending|succeeded|failed|dead], attempt_count, next_attempt_at, last_response_code, created_at)`，索引 `(status, next_attempt_at)`。
- `delivery_attempts(id, delivery_id, attempted_at, response_code, response_snippet, duration_ms, error)` — 每次 HTTP 尝试一行（Dashboard「Event deliveries」页面即此表）。
- `dead_letters(delivery_id, all_attempts jsonb, created_at)`。

**4) 流程 / 状态机**
```
业务服务 —(同一事务写 events + outbox)→ Outbox relay → Kafka topic `events`（partition key = account_id 或 object_id）
  → Dispatcher（查 endpoints 缓存 Redis `endpoints:{account}:{type}`）→ 为每个匹配 endpoint 建 deliveries(pending)
  → Delivery queue（按 endpoint/tenant 分片）→ Worker：签名 → POST（连接池、2–5 s 超时）
      2xx → succeeded
      非 2xx/超时 → attempt+1, next_attempt = backoff(attempt) → pending
      attempt > N 或超过 3 天 → dead（DLQ）+ 通知商户 + 可自动禁用 endpoint（Stripe：3 天后禁用并通知）
```
delivery 状态机：`pending → (attempting) → succeeded | pending(retry) | dead`。

**5) 投递语义与幂等**
- 至少一次 + 接收方去重：payload 带不可变 `event.id`，商户记录已处理的 event id（Stripe 文档：*"Track event IDs to identify duplicate deliveries"*；有时会生成两个不同 Event 对象，可用 `data.object.id + event.type` 二次去重）。Emily 的回答（被接受）正是这个。
- 重试时重新生成时间戳和签名（Stripe 官方行为），接收方按 5 min 容差拒绝过旧时间戳防重放。
- 顺序：不保证；商户应「收到事件后按需 GET 最新对象」而不是信任事件顺序。若面试官坚持 per-object 顺序：Kafka partition key = object_id + 单 endpoint 串行 worker，代价是吞吐与 head-of-line blocking。

**6) 重试 / 退避 / 抖动 / DLQ**
- 官方事实：live mode 指数退避最长 **3 天**；test/sandbox 仅重试 3 次、几小时内。
- 公式：`delay = base × 2^attempt × (1 + rand(0, 0.3))`，上限 1 h（systemdesignhandbook）；示例序列 1 min → 5 min → 30 min → 2 h → 8 h → 24 h（Emily 答案 + hookray 摘要）。
- 抖动目的：防 thundering herd（Stripe idempotency 博客与 rate-limits 文档均要求 jitter）。
- 延迟队列实现：Redis ZSET（score=next_attempt_at）或 DB 轮询 `(status,next_attempt_at)` 索引，或 Kafka 多级延迟 topic。

**7) 失败域隔离（Emily 失分点，必讲）**
- **噪声邻居**：per-endpoint 并发上限（如 ≤ 20 in-flight）+ per-tenant 队列/令牌桶；连接池按租户分池；慢端点不占满全局 worker。
- **熔断**：endpoint 连续失败 N 次/失败率 > X → open 状态，事件直接进延迟队列不占 worker，半开探测恢复。
- **超时**：连接 2 s / 读 5 s；超时视为失败（Stripe 文档「Timed out」）。
- **SSRF / DNS rebinding**（Emily 失分点）：注册时解析域名→拒绝私网/保留段/云 metadata IP；**投递时以校验通过的 IP 直连，Host 头带原域名**，禁止跟随重定向（Stripe 把 3xx 当失败）；出口走独立 egress 网段。
- 背压：Kafka 消费 lag 触发 worker 扩容；队列深度阈值告警。

**8) 对账 / 补漏**
- 商户侧：`GET /v1/events` 拉取近 30 天事件补漏；Stripe 提供「process undelivered events」流程。
- 平台侧：每日 job 对比 `events × endpoints` 应生成的 deliveries 与实际 succeeded，差集报警。

**9) 规模估算**
- 10k events/s × 平均 2 endpoints = 20k POST/s；平均 200 ms → 4k 并发连接；events 每条 2 KB → 20 MB/s，30 天保留 ≈ 50 TB（冷热分层）。
- Worker 无状态水平扩展；Kafka 按 account_id 分区；deliveries 表按 created_at 分区 + 按 endpoint_id 分片。

**10) 监控**
- 全局投递成功率（>5% 失败持续 10 min 告警）、p99 首次尝试延迟（>5 s）、队列深度（>10k）、DLQ 增长率（>100/h）、每 endpoint 健康分（systemdesignhandbook 阈值）。
- 商户可见：Dashboard 每次尝试的状态码/耗时/下次重试时间（Stripe 官方页面就有）。

**11) 追问预案**
- 「exactly-once？」→ 不可能，讲 at-least-once + 接收方幂等；主动提 Stripe 自己就是这么做的。
- 「密钥泄露？」→ 轮换，24 h 双密钥并存，每个 secret 各签一个 v1 签名。
- 「商户要求按顺序？」→ 讲 partition key 与代价；或推荐 thin events + 拉取最新状态。
- 「API 版本？」→ Event 结构由账户 pinned 版本决定，创建后不变（Stripe 官方）。

### 4.2 设计幂等的支付 / Charge API（"merchant wants to charge a card"）

**取材**：Stripe《Designing robust and predictable APIs with idempotency》（2017-02-22，https://stripe.com/blog/idempotency ）；Stripe 文档 Idempotent requests（访问 2026-09-01，https://docs.stripe.com/api/idempotent_requests ）；brandur《Implementing Stripe-like Idempotency Keys in Postgres》（2017-10-27，https://brandur.org/idempotency-keys ）；Stripe PaymentIntent lifecycle 文档；Medium h7w（2026-04-03）；systemdr（2026-06-02）；Hello Interview payment-system；ByteByteGo how-to-avoid-double-payment；Alex Xu Vol.2。

**1) 需求**
- 功能：商户创建一笔对卡的收款；查询状态；退款（可选）；商户收到状态变化（webhook）。
- 非功能：**绝不双扣**；**不丢单**（接受的请求最终有确定结果）；p99 < 500 ms 同步授权（systemdr）；PCI：卡号不进我们的应用层（tokenize）；审计 7 年；峰值 10k TPS（Hello Interview/systemdr 题设；Alex Xu 题设 10 TPS——先问清）。
- 不变量：一个 idempotency key ↔ 至多一次外部扣款；ledger 借贷恒等。

**2) API**
```
POST /v1/payment_intents
  Headers: Idempotency-Key: <uuid v4, ≤255 chars>, Stripe-Version: 2026-08-26
  Body: amount (integer, 最小货币单位), currency, payment_method (tok_/pm_), customer?, capture_method[automatic|manual], metadata{}
  → 200 {id: "pi_...", status, amount, currency, client_secret, last_payment_error?}
POST /v1/payment_intents/:id/confirm      （幂等）
POST /v1/payment_intents/:id/capture      （manual capture）
POST /v1/payment_intents/:id/cancel
GET  /v1/payment_intents/:id
POST /v1/refunds  {payment_intent, amount?}  + Idempotency-Key
```
契约细则（面试官爱追问）：
- 金额用整数最小单位，禁止 float（systemdr：*"Integer cents is the only correct answer"*）；Alex Xu 用 string。
- 幂等层保存**首个请求的状态码 + body（包括 500）**，同 key 重放返回同结果；key ≥24 h 后可清理；**同 key 不同参数 → 报错**；**同 key 并发在途 → 409/不保存结果，可重试**；只对 POST 生效（Stripe 官方文档）。
- 错误结构：`{error:{type: card_error|invalid_request_error|idempotency_error|rate_limit_error, code, decline_code, message, param, request_id}}`；可重试与否由 type 决定。
- 版本：日期版本 + 账户 pinned + `Stripe-Version` 覆盖；只加字段不删字段（Stripe API versioning 博客 2017-08-05）。

**3) 数据模型**
- `idempotency_keys(user_id, key, request_method, request_path, request_params_hash, locked_at, recovery_point, response_code, response_body, created_at)`，唯一 `(user_id, key)`（brandur 表结构）。
- `payment_intents(id, account_id, amount, currency, status, payment_method_id, capture_method, latest_charge_id, last_error jsonb, created_at, updated_at, version)`。
- `charges(id, payment_intent_id, network_auth_code, network_txn_id, amount_captured, status, outcome jsonb, created_at)`。
- `ledger_entries`（见 4.3）。
- `outbox(id, aggregate_id, event_type, payload, published_at)`。
- 分片键：account_id（商户），保证同商户的 PI 与幂等键同分片，唯一约束可在单分片内成立。

**4) 状态机（Stripe 官方 PaymentIntent）**
```
requires_payment_method → requires_confirmation → requires_action(3DS) → processing → succeeded
                                                                     ↘ requires_capture → succeeded
失败（decline）→ 回到 requires_payment_method（可换卡重试）
任一非终态 → canceled（释放 hold；confirm 次数过多自动 canceled）
```
终态：`succeeded`、`canceled`。退款是另一个对象 `refund(pending→succeeded|failed)`。

**5) 幂等实现（核心，用 brandur/h7w 的「先 claim 再外呼」）**
```
T1: INSERT idempotency_keys(...) ON CONFLICT DO NOTHING
    - 插入成功 → 我方拥有该请求，recovery_point=started
    - 冲突且 finished → 直接返回缓存的 code/body
    - 冲突且 locked_at 新鲜 → 409 "request in flight"（Stripe 行为：不保存结果，客户端可重试）
    - 冲突且参数 hash 不同 → 400 idempotency_error
T2: 原子阶段：创建 payment_intent(status=processing) → recovery_point=pi_created（同一 DB 事务）
外呼：调卡网络授权（foreign state mutation，不在事务内；带 network 级幂等 = 我方 charge_id 作为 PSP 的 idempotency key）
T3: 原子阶段：写 charges + ledger_entries + outbox；pi.status=succeeded；recovery_point=finished；写回 response
```
- 崩溃恢复：任何阶段崩溃，重试请求（或后台 **completer**）从 `recovery_point` 续跑；若在「外呼后、T3 前」崩溃，先向 PSP 查询该 charge_id 是否已授权，再决定续写还是补偿（**这是 h7w 文中 senior 答不出的点**）。
- Redis 仅作 fast path 缓存已完成的 key；**DB 唯一约束才是真相源**。
- **reaper** 每 72 h 删除过期 key（brandur）；Stripe 文档：≥24 h。

**6) 投递语义**
- 对客户端：at-least-once 重试（SDK 自动重试 + 指数退避 + 抖动，Stripe 2017 博客） + 幂等键 = 有效 exactly-once。
- 对 PSP/卡网络：我方 charge_id 作为其幂等键；超时后**先查询再重试**，而非盲重试。
- 事件外发：outbox + relay → Kafka → webhook（4.1），至少一次。

**7) 失败处理**
- 卡网络超时（~200 ms 常态，systemdr）：查询 → 若已授权则记账；若未知则标记 `processing` 并交给 reconciliation；不要立即告诉商户「失败」。
- 部分失败：授权成功但记账失败 → recovery point 续写；绝不「先记账再授权」。
- 区域分区：每个商户的写入固定 home region（单写者），跨区只读副本；切换 region 需先 fence 旧 leader（防双写）。
- 并发同 PI 操作：Stripe 用对象锁，冲突返回 429 `lock_timeout`，SDK 自动重试（rate-limits 文档）。
- Saga：多步骤（风控 → 授权 → 记账 → 通知）用编排器 + 补偿（void authorization）。

**8) 对账**
- 每日 PSP/卡组织结算文件 vs `charges` vs ledger；mismatch 分三类：可自动修复、需人工、无法分类（Alex Xu）；cut-off 时间差异先标为 temporary break 次日再核（ByteByteGo）。
- 监控 `processing` 超过阈值（如 15 min）的 PI 报警（Alex Xu 的 monitoring job）。

**9) 规模**
- 10k TPS，每条 2 KB → 20 MB/s；7 年 ≈ 500 TB（systemdr）；OLTP 保 90 天热数据，其余冷归档。
- 瓶颈：幂等键查找（DB 唯一索引 + Redis 前置）、ledger 写吞吐（按账户分片、批量追加）、webhook 扇出。

**10) 监控**
- 授权成功率/decline 率、p99 延迟、幂等冲突率、`processing` 滞留数、对账差异数、PSP 错误率、request_id 全链路日志。

**11) 追问预案**
- 「retry hits a different instance while first still processing」→ DB 唯一约束 + locked_at，第二个拿到 409 或等待；绝不各自外呼。
- 「同 key 不同金额」→ 拒绝（Stripe 官方行为）。
- 「key 多久有效」→ ≥24 h（官方）；72 h reaper（brandur）；讨论存储成本。
- 「3DS 怎么办」→ requires_action 状态 + client_secret 前端完成 + 再 confirm。

### 4.3 设计 Ledger / Bookkeeping 服务（含多币种）

**取材**：Stripe《Ledger: Stripe's system for tracking and validating money movement》（2024-02-16，https://stripe.dev/blog/ledger-stripe-system-for-tracking-and-validating-money-movement ）；Alex Xu Vol.2 支付章；ByteByteGo reconciliation guide；betterengineers（2026-07-23）；Medium h7w；Hello Interview。

**1) 需求**
- 功能：记录每一次资金移动（charge、fee、refund、payout、transfer、FX）；查询任意账户任意时点余额；按维度（商户/币种/产品）汇总；证明「所有钱都有去向」；供对账与审计。
- 非功能：**不可变（append-only）**、**借贷恒等**、强一致写入、每日 50 亿事件（Stripe 真实数字）、99.99% 金额在 4 天内完成摄取校验（Stripe）、保留 7 年。
- 不变量：Σdebit = Σcredit（每笔 transaction 内）；clearing 账户最终归零；每个生产者对象都有对应 ledger 事件（completeness）。

**2) API（内部 + 少量对外）**
```
POST /ledger/transactions   Idempotency-Key
  {external_id, event_type, occurred_at, entries:[{account_id, direction: debit|credit, amount, currency}], metadata}
  校验：entries 按币种分组后 Σdebit == Σcredit，否则 422
GET  /ledger/accounts/:id/balance?at=<ts>&currency=
GET  /ledger/accounts/:id/entries?cursor=&limit=
GET  /ledger/transactions/:id
对外：GET /v1/balance, GET /v1/balance_transactions（Stripe 真实接口）
```

**3) 数据模型**
- `accounts(id, owner_type, owner_id, type[asset|liability|revenue|expense|clearing], subtype e.g. charge_unsubmitted/merchant_available/merchant_pending/stripe_fee, currency, created_at)` — Stripe 原文：accounts 是「buckets of money distinguished by their type and properties」。
- `transactions(id, external_id UNIQUE, event_type, occurred_at, posted_at, producer, metadata jsonb)` — 每笔业务事件一条。
- `entries(id, transaction_id, account_id, direction, amount BIGINT, currency, seq)` — 不可变；**同 transaction 内借贷相等**由写入时校验 + DB CHECK/触发器。
- `balances(account_id, currency, balance, as_of_seq, updated_at)` — 物化余额，可由 entries 重建；或按日快照 `balance_snapshots(account_id, date, balance)` + 增量。
- 修正：**不 UPDATE/DELETE**，只追加反向 transaction（reversal，引用原 transaction_id）。
- 金额：整数最小单位 + 币种；多币种时**每个币种独立平衡**，FX 通过 `fx_clearing` 账户（USD 借 / EUR 贷各自平衡 + 汇率损益账户）。

**4) 典型分录（面试口述用）**
- 客户付款 $100，手续费 $3：`debit charge_unsubmitted(asset) 100 / credit merchant_pending 97 / credit stripe_fee_revenue 3`。
- 资金结算到账：`debit bank_settlement 100 / credit charge_unsubmitted 100`（clearing 归零）。
- pending → available（T+n）：`debit merchant_pending 97 / credit merchant_available 97`。
- 退款：反向分录，不改原分录。
- Payout：`debit merchant_available / credit bank_outgoing_clearing`；银行确认后再清 clearing。

**5) 写路径与一致性**
- 生产者（支付系统）通过 **outbox** 发事件 → Ledger 摄取（Stripe：Ledger 是「immutable log of events」，生产者「publish」进来）。
- 写入幂等：`external_id` 唯一约束；重复事件直接 ACK。
- 热点账户（Stripe 自己的 fee 账户、大商户）：不要在写路径上 UPDATE 单行余额 → **只追加 entries**，余额异步聚合；需要实时余额校验（如防负余额）时对该账户加乐观锁 version（ByteByteGo wallet 表 `version` 字段）或按账户分片串行化。
- 分片：按 `account_id` 的 owner（商户）分片；一笔 transaction 跨商户（平台→连接账户）时用 saga 或把 clearing 账户放在两边各记一笔。

**6) 读路径**
- 当前余额：物化表；历史余额：最近快照 + 之后 entries 求和；对账/报表走 OLAP 副本（Kafka → 数据仓库）。
- Stripe 官方指标「Timeliness / Completeness / Clearing」三项校验：数据到达窗口硬阈值；生产者 DB 每个 ID 都有对应事件；clearing 账户非零即报警。

**7) 对账 / 数据质量**
- 内部：ledger vs 生产者 DB（completeness）；clearing 账户非零 → 定位「missing, late, or incorrect transaction」（Stripe 原文）。
- 外部：vs 银行/卡组织结算文件（Alex Xu），差异分类处理；Stripe 目标 DQ score 99.99%、>99.9999% 可解释。

**8) 规模**
- Stripe：5B events/day ≈ 58k/s 平均、峰值数倍；「10x」增长仍成立。
- 存储：每 entry ~100 B，5B/天 × 2 entries → 1 TB/天级别 → 分区（按月）+ 冷归档；余额物化表小得多。

**9) 监控**
- 摄取延迟 p99、clearing 非零账户数、completeness 缺失率、写入失败/幂等冲突率、余额重建与物化差异。

**10) 追问预案**
- 「为什么不直接 UPDATE 余额」→ 审计、可重建、并发热点、不可变。
- 「多币种怎么平」→ 每币种独立平衡 + FX clearing。
- 「历史余额怎么快」→ 快照 + 增量。
- 「错误分录怎么改」→ reversal 追加，永不改写。
- 「读写分离一致性」→ 写单主，读副本给报表；对「可用余额」这类强一致读走主库。

### 4.4 设计分布式 Rate Limiter（Stripe API 网关）

**取材**：Stripe《Scaling your API with rate limiters》（2017-03-30，https://stripe.com/blog/rate-limiters ）；Stripe 文档 Rate limits（访问 2026-09-01，https://docs.stripe.com/rate-limits ）；TechPrep YouTube《Rate Limiter (Stripe & Amazon Offers)》；Exponent 题库（Rate Limiter 13 answers）；Hello Interview（页面 404，未取到）。

**1) 需求**
- 功能：按账户（API key）限速；按 endpoint 限速；并发限制；超限返回 429 + 原因头；可热更新限额；测试模式与 live 分开。
- 非功能：判定延迟 < 1–2 ms；网关多实例共享计数；限流器自身故障不能拖垮 API（**fail-open**）；限流只是保护层，不是计费。
- Stripe 真实数字（讲出来加分）：live 全局 100 req/s/账户，sandbox 25；单 endpoint 25 rps；PaymentIntent 每对象每小时 1000 次 update；Payouts 15 create/s、30 并发；Connect 账户创建 30/s；Files 20 r/w；429 带 `Stripe-Rate-Limited-Reason: global-rate|endpoint-rate|global-concurrency|endpoint-concurrency|resource-specific`；另有对象锁 `lock_timeout` 也返回 429。

**2) 四层限流（Stripe 博客原设计，面试主线）**
1. **Request rate limiter**：每用户 N rps，token bucket；处理绝大多数情况。
2. **Concurrent requests limiter**：每用户同时在途 ≤ 20；针对 CPU 密集端点，防止「重试风暴打爆慢端点」。
3. **Fleet usage load shedder**：为关键请求（如创建 charge）保留一部分容量，非关键（list charges）先被削。
4. **Worker utilization load shedder**：重大事故时按优先级 critical methods > POST > GET > test mode 逐级削减。

**3) API / 接口**
```
内部：allow(key, rules[]) → {allowed, remaining, retry_after_ms, reason}
配置：PUT /internal/ratelimits/{account}  {global_rps, endpoint_overrides{}, concurrency}
响应头：429 + Retry-After + Stripe-Rate-Limited-Reason
```

**4) 算法选择**
- **Token bucket**（Stripe 用）：允许短突发（bucket 容量），补充速率 = rps；Redis 存 `{tokens, last_refill_ts}`，Lua 脚本原子「refill + take」。
- Sliding window log：精确但 O(N) 内存；sliding window counter：两个固定窗口加权，近似精确、内存小。
- 并发限制：Redis INCR/DECR + 请求结束释放；为防泄漏设 TTL 或用带过期的 ZSET 记录在途请求。

**5) 数据模型 / 存储**
- Redis（或 ElastiCache）集群，key = `rl:{account}:{scope}`，按 account hash 分片（同账户的所有 key 落同一分片，Lua 可原子操作）。
- 规则配置存 DB，推送到网关本地缓存（策略管理慢路径 vs 执行快路径分离——Exponent rubric 第 4 维）。

**6) 一致性与多区域**
- 单 region 内：Redis 集中计数，略有过限（多实例并发）可接受。
- 多 region：不做全局强一致；每 region 独立配额（配额/region 数）或本地近似 + 异步汇总；解释「限流是近似保护，宁可略放过也不要跨区同步的延迟」。
- 本地 + 远端两级：每个网关实例本地 token bucket（吸收热点），Redis 做全局校准。

**7) 失败处理**
- Redis 不可用：**fail-open**（放行）+ 报警，同时降级到本地内存限流（Stripe 博客：限流器要有 feature flag 可一键关闭）。
- Lua 超时/慢：设置短超时（如 5 ms）超时即放行。
- 重试风暴：客户端应指数退避 + 抖动（Stripe 文档要求）；服务端并发限制器专门治这个。
- 上线：**dark launch**——先只记录不拒绝，观察误杀率再打开（Stripe 博客）。

**8) 规模**
- Stripe 每月仅 test mode 就拒绝数百万请求（博客）；假设网关 100k rps，Redis 单分片可承载 ~100k ops/s，按 account 分 8–16 片；每 key 几十字节，百万账户 ≈ 100 MB。

**9) 监控**
- 每账户/每端点 429 率、限流器判定延迟、Redis 错误率与 fail-open 次数、shedder 触发次数、误杀投诉。

**10) 追问预案**
- 「固定窗口边界双倍流量」→ 滑动窗口或 token bucket。
- 「多实例超限」→ Redis 原子 Lua；或接受近似。
- 「限流器挂了」→ fail-open + 本地降级 + 告警；解释为什么不是 fail-closed（支付 API 可用性优先）。
- 「大商户 flash sale」→ Stripe 做法是提前联系提高限额 + 客户端 token bucket 自限速。

### 4.5 设计订阅计费与发票系统（Subscription Billing & Invoicing）

**取材**：Stripe 文档《How subscriptions work》（访问 2026-09-01，https://docs.stripe.com/billing/subscriptions/overview ）；Stripe 文档 Rate limits（订阅相关限额）；vervecopilot/ophyai/getsdeready 题目描述；4.2 的幂等与 webhook 设计。

**1) 需求**
- 功能：客户订阅 plan/price（月/年）；到期自动生成 invoice 并扣款；升降级按比例（proration）；试用期；取消（立即/期末）；失败重试（dunning/smart retries）；发票可发邮件手动支付；webhook 通知状态变化。
- 非功能：**每个计费周期恰好一张发票、恰好一次扣款**（幂等）；月初续费洪峰（Stripe 文档特别提到）；状态与发票、PaymentIntent 三者一致；可审计。

**2) API**
```
POST /v1/customers, POST /v1/products, POST /v1/prices {unit_amount, currency, recurring{interval, interval_count}}
POST /v1/subscriptions {customer, items[{price, quantity}], trial_period_days?, collection_method[charge_automatically|send_invoice], payment_behavior, proration_behavior}
POST /v1/subscriptions/:id  {items, proration_behavior[create_prorations|none|always_invoice], cancel_at_period_end}
DELETE /v1/subscriptions/:id
GET  /v1/invoices/:id, POST /v1/invoices/:id/pay, POST /v1/invoices/:id/finalize, POST /v1/invoices/:id/void
所有 POST 支持 Idempotency-Key
```
Stripe 真实限额可引用：每订阅每分钟 ≤10 张新发票、每天 ≤20 张、每小时 ≤200 次数量更新。

**3) 数据模型**
- `customers(id, account_id, default_payment_method, email, ...)`
- `products(id, name)`, `prices(id, product_id, unit_amount, currency, interval, interval_count, active)`
- `subscriptions(id, customer_id, status, current_period_start, current_period_end, trial_end, cancel_at_period_end, default_payment_method, collection_method, latest_invoice_id, version)`
- `subscription_items(id, subscription_id, price_id, quantity)`
- `invoices(id, customer_id, subscription_id, period_start, period_end, status[draft|open|paid|void|uncollectible], amount_due, amount_paid, attempt_count, next_payment_attempt, payment_intent_id, finalized_at, due_date)`，唯一 `(subscription_id, period_start)` **防止一周期两张发票**
- `invoice_line_items(id, invoice_id, price_id, quantity, amount, proration bool, period_start, period_end)`
- `invoice_items(pending，用于 proration 与一次性费用)`
- `payment_attempts(id, invoice_id, payment_intent_id, attempted_at, outcome)`
- `entitlements(customer_id, feature_id, active)`（Stripe 用 entitlement 决定权限）

**4) 状态机（Stripe 官方）**
```
subscription: incomplete → active           （23 h 内付清首张发票）
              incomplete → incomplete_expired（23 h 未付，发票 void）
              trialing → active | paused（试用结束无支付方式）
              active → past_due（最新 finalized 发票扣款失败/未尝试）
              past_due → active（付清）| canceled | unpaid（smart retries 用尽后按设置）
              unpaid → active（到期前付清）
              任意 → canceled（终态；停止新发票与自动收款）
invoice:      draft → open（finalize）→ paid | void | uncollectible
支付结果映射：succeeded→paid→active；card_error→requires_payment_method→open→incomplete；需 3DS→requires_action→open→incomplete
```

**5) 核心流程**
- **周期滚动**：调度器扫描 `current_period_end <= now` 的订阅（按时间分桶的索引/队列，避免月初全表扫）；为每个订阅：在事务内创建 draft invoice（唯一约束防重）+ 汇总 items + pending invoice_items（proration）→ 约 1 h 后 finalize（Stripe 给商户加行项目的窗口）→ 创建 PaymentIntent（幂等键 = invoice_id）→ 结果通过 webhook `invoice.paid` / `invoice.payment_failed` 通知。
- **Proration**：升级时对剩余周期计算「未用旧价退回 + 新价补收」两条 invoice_items，可立即开票或并入下期；公式 `amount × remaining_seconds / period_seconds`，整数舍入策略固定并记录。
- **Dunning / smart retries**：失败后 `next_payment_attempt` 按规则（如 3/5/7 天）重试；用尽后按商户设置转 canceled/unpaid/保持 past_due；每次尝试写 payment_attempts；发邮件提醒更新卡。
- **取消**：`cancel_at_period_end` 只打标；立即取消则 void 未付发票并可选按比例退款。

**6) 幂等与一致性**
- 发票生成幂等：唯一 `(subscription_id, period_start)`；扣款幂等：PaymentIntent 幂等键 = invoice_id + attempt_count。
- 订阅对象更新用乐观锁 `version`；Stripe 实际对对象加锁，冲突 429 lock_timeout。
- 所有状态变化写 outbox → 事件 `customer.subscription.updated`、`invoice.created/finalized/paid/payment_failed/payment_action_required`。

**7) 失败处理**
- 扣款超时/未知：走 4.2 的查询-再决定；发票保持 open。
- 调度器崩溃：任务幂等，可重跑；用「租约」防多个调度器重复处理同一订阅。
- 月初洪峰：提前预生成 draft，把 finalize+charge 平滑分散到窗口内（Stripe 文档建议商户 webhook 端异步处理即因此）。
- 时区/日期：`current_period_end` 用 UTC 存；31 日等不存在日期取月末（Stripe payouts 文档同样规则）。

**8) 对账**
- 每日：Σ invoices.paid 金额 = ledger 收入分录；orphan PaymentIntent（有扣款无发票）报警；过期 incomplete 自动 expire。

**9) 规模**
- 1 亿活跃订阅、月付为主 → 每天约 330 万张发票，月初可达 10× → 调度分桶 + 队列削峰；invoices 按 customer_id 分片、按月分区。

**10) 监控**
- 续费成功率、dunning 回收率、发票生成延迟、未 finalize 的 draft 积压、`processing` 滞留、webhook 投递失败。

**11) 追问预案**
- 「同一周期开了两张发票」→ 唯一约束 + 幂等。
- 「升级中途改价怎么算」→ proration 公式 + 舍入规则 + 落 invoice_items。
- 「客户改卡后如何自动补扣」→ `invoice.payment_failed` → 更新 default_payment_method → 手动 `/pay` 或等 next_payment_attempt。
- 「延迟确认支付方式（ACH）」→ 订阅直接 active，失败后 void 发票但订阅仍 active（Stripe 官方行为）。

### 4.6 设计「账户间转账」/ Stripe Connect 分账与 Payout

**取材**：Stripe 文档 Payouts（访问 2026-09-01，https://docs.stripe.com/payouts ）；Stripe 文档 Separate charges and transfers（索引页）；Stripe Ledger 博客；Alex Xu 支付章 pay-out flow；ByteByteGo wallet 设计；ophyai「marketplace payment split」；Exponent「design a system to move money between accounts」类描述。

**1) 需求**
- 功能：平台收款后把资金按比例转给一个或多个连接账户（transfer）；连接账户按计划或即时提现到银行（payout）；支持 `transfer_group` 关联一笔 charge 与多笔 transfer；transfer 可撤销（reversal）；负余额时从银行反向扣款（debit payout）。
- 非功能：**转账原子**（一方扣、一方加，不多不少）；不能透支 available balance（除非允许负余额）；幂等；可审计；T+n 资金可用性；payout 失败可重试/回滚；跨币种。
- 事实：Stripe 余额分 **pending / available**，结算时间 T+2/T+3 决定 pending→available；payout 计划 manual/daily/weekly/monthly，非工作日顺延；instant payout ~30 min、每天 ≤10 次、单次 ≤ $1M；最低金额 $0.01/€1/¥1；负余额时 Stripe 创建 debit payout；Payouts API 限 15 create/s、30 并发。

**2) API**
```
POST /v1/transfers   Idempotency-Key  {amount, currency, destination: acct_xxx, transfer_group?, source_transaction?}
POST /v1/transfers/:id/reversals {amount?}
GET  /v1/balance  → {available:[{amount,currency}], pending:[...]}
GET  /v1/balance_transactions?type=&payout=
POST /v1/payouts  Idempotency-Key  {amount, currency, method[standard|instant], destination?}
POST /v1/payouts/:id/cancel   （仅 pending 可取消）
内部：POST /internal/transfers {from_account, to_account, amount, currency, external_id}
```

**3) 数据模型**
- `accounts(id, type[platform|connected|stripe_internal|bank_clearing], country, default_currency, payout_schedule, ...)`
- `balances(account_id, currency, pending, available, version)`（物化，来源是 ledger）
- `balance_transactions(id, account_id, type[charge|transfer|transfer_reversal|payout|payout_failure|refund|adjustment], amount, fee, net, currency, available_on, status[pending|available], source_id, created_at)` — Stripe 真实对象
- `transfers(id, source_account, destination_account, amount, currency, transfer_group, source_transaction, status, reversed_amount, idempotency_key)`
- `payouts(id, account_id, amount, currency, method, status[pending|in_transit|paid|failed|canceled], arrival_date, failure_code[no_account|account_closed|insufficient_funds|debit_not_authorized|invalid_currency], bank_file_batch_id)`
- ledger entries（4.3）：转账 = `debit platform_available / credit connected_available`；payout = `debit connected_available / credit bank_outgoing_clearing`；银行确认后 `debit bank_outgoing_clearing / credit external_bank`。

**4) 状态机**
```
transfer: created → (funds moved 同步) → reversed(部分/全部)
payout:   pending → in_transit → paid
                 ↘ failed（回滚：credit 回 available + 记 payout_failure balance_transaction）
          pending → canceled
balance_transaction: pending → available（available_on 到期由调度器批量翻转）
```

**5) 转账原子性（核心）**
- 同一分片：单 DB 事务：`SELECT ... FOR UPDATE` 两账户（**固定按 id 顺序加锁防死锁**）→ 校验 `from.available >= amount`（或允许负余额策略）→ 写两条 ledger entries + 更新两条 balances（version+1）→ 写 outbox → commit。
- 跨分片/跨区域：**两阶段 saga**：① from 账户「预留」（hold：available -= amount, held += amount，写 pending transfer）② to 账户入账 ③ from 释放 hold 并终结；任一步失败走补偿（释放 hold）。ByteByteGo 的「reserve → charge → commit or rollback」。用 external_id 幂等，每一步可重放。
- 绝不用分布式 2PC 锁住支付主路径；Alex Xu 与 h7w 都推荐 saga + 补偿。

**6) 幂等**
- transfers/payouts 都要求 Idempotency-Key（4.2 机制）；内部 external_id 唯一。
- 银行文件生成幂等：每个 payout 只能进入一个 batch（`bank_file_batch_id` 非空即跳过）；批次重跑不重复出款。

**7) 失败处理**
- 银行退回（failed）：异步到达（可能数天），写 `payout_failure` 反向分录恢复 available，通知商户（webhook `payout.failed`），必要时冻结自动 payout。
- 负余额：退款/争议超过入账 → available < 0 → 创建 debit payout 从商户银行扣款（Stripe 官方）；若失败则挂账 + 风控。
- transfer 撤销时目标账户余额不足：允许目标账户负余额或拒绝（策略可配置；Stripe 允许平台承担）。
- 币种：跨币种 transfer 走 FX clearing 账户，锁定汇率并记录。
- 分区/故障：账户 home region 单写；payout 批处理有 leader lease。

**8) 对账**
- 每日：Σ payouts.paid = 银行对账单出款；Σ transfers = 平台与连接账户 ledger 互为镜像；pending→available 翻转数 = 到期 balance_transactions 数；bank_outgoing_clearing 归零。
- 完整性：每个 charge 的 `transfer_group` 下 Σtransfers ≤ charge.net。

**9) 规模**
- 数百万连接账户，每日 payout 数百万笔，按国家/币种/银行通道分批生成文件（ACH 批次有 cut-off，US instant 5 pm ET）；balances 按 account_id 分片；balance_transactions 按 account_id + 月份分区。

**10) 监控**
- payout 失败率按 failure_code、in_transit 超期、负余额账户数与总额、hold 滞留、对账差异、批次生成延迟。

**11) 追问预案**
- 「两账户在不同分片怎么原子」→ saga + hold + 幂等 + 补偿；解释为什么不 2PC。
- 「pending 和 available 有什么区别」→ 结算时间；payout 只能动 available。
- 「payout 三天后银行退回怎么办」→ 反向分录 + webhook + 冻结策略。
- 「怎么防止商户提走还没结算的钱」→ available 才可提；风控可加保留金（reserve）账户。

---

## 5. 通用框架与其他公司题单

### 5.1 Hello Interview「Delivery Framework」（应届/初级默认框架）

来源：https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery （访问 2026-09-01）

| 步骤 | 时间 | 要做什么 |
|---|---|---|
| 1. Requirements | ~5 min | 功能需求写成「Users should be able to…」，只保留 top 3；非功能写成「The system should…」并量化（CAP 取舍、延迟目标如 feed < 200 ms、持久性、安全、合规）；**容量估算只在影响设计决策时做**（「calculate storage, DAU, QPS only to conclude 'ok, so it's a lot'」是反例） |
| 2. Core Entities | ~2 min | 列出核心名词（User/Tweet/Follow），不过早细化 |
| 3. API / System Interface | ~5 min | 默认 REST，复数资源名（`POST /v1/tweets`、`GET /v1/feed`）；**user id 永远来自 auth token 不来自 body** |
| 4. Data Flow（可选） | ~5 min | 数据处理型系统写 fetch → parse → extract → store |
| 5. High-Level Design | 10–15 min | 逐个 API 画框和箭头，在数据库旁写 schema 字段；先满足核心需求再叠复杂度 |
| 6. Deep Dives | ~10 min | 逐条核对非功能需求、边界与瓶颈；**初级候选人：面试官会引导；高级候选人：主动发现并领导讨论** |

Hello Interview 对 Stripe 题的分级：Mid-level 讲通核心流程；Senior 深入安全/持久性/异步处理；Staff+ 讲失败场景与资金完整性保证。— https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system

### 5.2 各公司应届/初级是否考 SD 及深度

来源：DesignGurus《What FAANG Expects at Each Level (L3–L6)》（2026-04-18，https://designgurus.substack.com/p/system-design-for-new-grad-vs-l5 ）；DesignGurus《Google's System Design Interview》（2026-03-19，https://designgurus.substack.com/p/googles-system-design-interview-in ）；Hello Interview Google L4 / Meta E3 / Meta E4 指南；Blind Amazon 帖 ×3；systemdesignhandbook《Amazon SDE 1 System Design》（2026-02）。

| 公司 / 级别 | 是否有 SD 轮 | 形式与深度 |
|---|---|---|
| **Google L3（应届）** | 无 | 全 coding + Googliness（DesignGurus 2026；Hello Interview） |
| **Google L4** | 可选：3 coding 或 2 coding + 1 SDI（DesignGurus 2026-03）；Hello Interview 称「no dedicated SD round at L4，reserved for L5+」，设计问题偶尔嵌在 coding 里 | 45 min 单面试官；强调数据库选型；回避 Google 自家产品；近期题：职业社交网络的 connection-degree 系统、近实时日志/指标管线；也有 YouTube、Maps；2026 起加 AI/ML 系统设计、恢复现场面试、增加 GHA 预筛 |
| **Meta E3（应届）** | 无 | OA（CodeSignal 90 min，1 题 4 阶段如 in-memory DB）+ 2 coding + 1 behavioral（Hello Interview E3 指南） |
| **Meta E4** | 有，1 轮 45 min，二选一：Product Architecture 或 System Design；**E4 是首个含设计轮的级别，设计/行为弱会降到 E3**（Hello Interview E4） | 题：Design LeetCode（Blind 2024-12 一手）、Instagram Auction、Top-K Songs、Instagram、Ticket Booking、Ad Click Aggregator、Online Game Leaderboard；评四维：Problem Navigation / Solution Design / Technical Excellence / Technical Communication |
| **Amazon SDE-1（应届）** | 「有时有」——多数是 **OOD/LLD**（Parking Lot、Elevator、Airport Traffic Controller、Online Banking，要写 getter/setter 级代码）；偶有 HLD（分布式日志系统，Blind 2020 帖多人表示罕见、「因 org 而异」） | systemdesignhandbook：SD 以 coding 轮追问形式出现，只要求「说清系统做什么、主要组件、如何交互」；例题 URL shortener、Order tracking、Notification feature；看 LP（frugality、customer obsession） |
| **Amazon SDE-2** | 有 | URL shortener、e-commerce 商品搜索、订单/物流通知服务、API rate limiting、带复制的 KV store（DesignGurus 2026 题库） |
| **Stripe 应届** | 无独立轮，见 §1 | 设计能力在 Integration 轮 + coding 追问（幂等去重、接口设计） |

DesignGurus 对应届的通用建议：题目「narrow, bounded」（URL shortener、basic chat）；得分点是结构化澄清、覆盖 client/API/server/DB 基本组件、能解释选择、坦诚知识盲区；「most FAANG companies do not expect you to be good at system design. They expect you to show potential」；「Do not spend 80% of your prep time on system design when it is 20% of your evaluation」。

### 5.3 应届/初级标准题单（每题一行要点）

综合 DesignGurus 题库（2026）、Hello Interview Meta E4 题单、systemdesignhandbook Amazon SDE1、Blind Amazon 帖、Exponent 通用列表。

**HLD 入门 8 题（Google L4 可选轮 / Meta E4 / Amazon SDE2 常见）**
1. **URL Shortener** — 短码生成（base62 计数器 vs hash）、读多写少、缓存 + 301/302 选择、过期。
2. **Rate Limiter** — token bucket/sliding window、Redis 原子、分布式一致性、fail-open。（同时是 Stripe 题）
3. **Notification System** — 多渠道（push/SMS/email）、队列削峰、模板、用户偏好、重试 + DLQ、幂等去重。（Stripe「支付事件通知」变体）
4. **Key-Value Store** — 一致性哈希、复制 + quorum、WAL/SSTable、gossip 检测故障。
5. **Order Tracking / 简单订单系统** — 订单状态机、库存扣减防超卖（乐观锁）、事件通知。
6. **Chat / Messaging（basic）** — WebSocket 长连接、消息存储与顺序、在线状态、已读回执。
7. **Ticket Booking（Ticketmaster）** — 座位锁定（TTL hold）、防双卖、热门开售排队/虚拟等候室。
8. **Ad Click Aggregator / Top-K / Leaderboard** — 流式计数（Kafka + Flink）、近似 Top-K、Redis ZSET 排行、窗口聚合。

**Product Architecture 类（Meta E4）**
9. **Design LeetCode** — 代码沙箱隔离执行、判题队列、排行、防作弊。
10. **Design Instagram / News Feed** — fan-out on write vs read、媒体存储 + CDN、feed 排序。
11. **Instagram Auction / Bidding** — 出价并发一致性、结束时刻处理、通知。
12. **Top-K Songs Widget（Spotify）** — 流式统计 + 缓存刷新。

**Amazon SDE-1 常见 OOD/LLD**
13. **Parking Lot** — 类设计、策略模式（计费/分配）、并发。
14. **Elevator System** — 调度算法、状态机。
15. **Airport Traffic Controller** — 资源分配、队列、优先级（Blind 2024-05 一手）。
16. **Online Banking（LLD）** — 账户/交易类、转账原子、幂等（与 Stripe ledger 思维相通）。
17. **Distributed logging for streaming service（HLD，罕见）** — 日志采集、实时报警管线（Blind 2020 一手）。

**Amazon SDE-2 / 高级（作为参考上限）**
18. Product search（倒排索引、相关性）；19. Real-time inventory 防超卖；20. Real-time fraud detection（与 Stripe Radar 题同构）；21. Distributed job scheduler；22. Recommendation engine（离线训练 + 在线 serving）。

### 5.4 备考顺序建议（[推断]，针对 Stripe 应届 + 保底 FAANG）

1. 先把 **4.2 幂等支付 API** 的「先 claim 再外呼 + recovery point」讲熟——它同时是 Stripe coding 轮「去重请求」题和 Integration 轮 webhook 处理的底层逻辑。
2. 再练 **4.1 Webhook**（唯一有多条一手记录的 Stripe SD 题）和 **4.4 Rate limiter**（Stripe/Amazon/Google 通用）。
3. **4.3 Ledger** 作为「Stripe 味」深挖题准备 15 min 版本：双记账 + 不可变 + clearing 归零 + 对账。
4. 通用题按 5.3 的 1–8 各准备一个 20 min 版本，套 Hello Interview 六步框架。
5. 每题都准备三个失败场景的回答：重试/重复、部分失败、依赖挂了——Stripe 面试的后 30 min 只问这些（Emily 2026-05-20；Exponent 2026）。

---

## 附录 A：来源索引（按类型）

**一手面经**
- Emily, Medium, 2026-05-20 — https://medium.com/@emilyhustlenyc/every-question-i-was-asked-in-stripes-system-design-interview-f6f19c2e62d6
- Abhishek Kumawat, LeetCode Discuss（New Grad 2026, 被拒）, 2026-02-09 — https://leetcode.com/discuss/post/7566910/
- 匿名, LeetCode Discuss（Onsite, Debug round 细节）, 2026-02-21 — https://leetcode.com/discuss/post/7595344/ （正文被拦截）
- Diyaag, Medium（Intern 2025–2026）, 2025-11 — https://medium.com/@diyaag2020/my-stripe-interview-experience-2025-2026-a-journey-to-the-final-round-19990fa6876a
- Blind: tshyvotg 2021-03-11; 4ayknryk 2021-04-27; pgrbvtmo 2021-05-07; umo0fobx 2021-06-19; p5vmbuvm 2021-09-06; iw4qxp2i 2022-06-15; fhqnsnny 2024-04-03; kak4gqwj 2024-10-06; ps7pgzwy 2025-03-18; hq5h6ewo 2025-04-07; i8a2p1m5 2025-08-30 — 均为 https://www.teamblind.com/post/<id>
- Blind Amazon: pnb36mba 2019-08-05; bivwoa3t 2020-05-18; gdkt7ot4 2024-05-01
- Blind Meta: elsjhbad 2024-12-23
- Glassdoor QTN_4393528 / QTN_7723981（webhook 题，仅标题）

**Stripe 官方**
- https://stripe.com/blog/idempotency （2017-02-22）
- https://stripe.com/blog/rate-limiters （2017-03-30）
- https://stripe.com/blog/api-versioning （2017-08-05）
- https://stripe.dev/blog/ledger-stripe-system-for-tracking-and-validating-money-movement （2024-02-16）
- https://docs.stripe.com/webhooks ; /api/idempotent_requests ; /rate-limits ; /payments/paymentintents/lifecycle ; /billing/subscriptions/overview ; /payouts （访问 2026-09-01）
- brandur.org/idempotency-keys（Stripe 前工程师，2017-10-27）

**培训/汇总站**
- Exponent: blog/stripe-system-design-interview（2026-06）; guides/stripe-swe-interview（2026-08）; questions?company=stripe&type=system-design（2026-09-01）
- Hello Interview: problem-breakdowns/payment-system; in-a-hurry/delivery; guides/meta/e4; guides/meta/e3; guides/google/l4
- interviewing.io/stripe-interview-questions
- systemdesignhandbook: guides/stripe-system-design-interview; guides/design-a-webhook-system（2026）; blog/amazon-sde-1-system-design（2026-02）
- Educative blog（2026-03-10）; getsdeready（2024-12-17）; vervecopilot（2026-05-01）; techinterview.org（2026-04-16 / 2026-07-02）; linkjob（2025）; prepfully（2026-08-13）; codinginterview.com; ophyai（2026-07）; techprep（2026）; interviewkickstart（2025-12-18）; mentorcruise（2026 版，无 SD 题）; nodeflair（403）; svix（2026-08-26）; systemdesignschool
- Substack: engineeringenablement（2026-07-21）; betterengineers（2026-07-23）; designgurus ×3（2026-03-19 / 04-18 / 题库）; systemdr（2026-06-02）; pragmaticengineer（Alex Xu Vol.2 支付章，2022-03-17）
- ByteByteGo: guides/reconciliation-in-payment; guides/how-to-avoid-double-payment; blog.bytebytego.com/p/payment-reconciliation; mintlify.wiki ByteByteGo system-design-101 payment case study
- Medium h7w（2026-04-03）
- YouTube TechPrep: 《Design Stripe》 https://www.youtube.com/watch?v=djc2vfpCvso ; 《Rate Limiter》 https://www.youtube.com/watch?v=dpEOhfEEoyw （oEmbed 仅取到标题与频道，无描述/日期）

## 附录 B：未能访问的来源
- 一亩三分地：stripe-software-engineer-556482、thread-1095724、thread-1145788、collection/232774 — 反爬验证页。
- 1o24bbs《Stripe 吐血面经总结》 — 连接被拒。
- Glassdoor 详情页 — Cloudflare「Humans only」。
- Hello Interview 社区 Stripe 题列表（12,918 reports） — 需 JS 渲染。
- Hello Interview rate-limiter breakdown、Hello Interview amazon/sde1 指南 — 404。
- igotanoffer Amazon SD 页 — 403。
