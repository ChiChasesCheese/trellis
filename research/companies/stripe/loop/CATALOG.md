# Stripe 面试 Loop 题目总表（OA 之后：电面 → onsite → HM/behavioral）

> 汇总自 `loop/raw/` 6 份尽调：`en_forums.md`（Blind/LeetCode/Medium/Taro/interviewing.io…）、`cn_forums.md`（一亩三分地题库 `__NEXT_DATA__` 原题、learncswithus、programhelp、csoahelp）、`hr_hm_behavioral.md`、`system_design.md`、`github_repos.md`、`stripe_official_and_api.md`。采集日 2026-09-01。
> **ID 是唯一主键**：`ps` 电面 · `cd` onsite coding · `bs` bug squash · `int` integration · `sd` system design · `rc/hm/bq` 非编码轮。练习目录 `loop/rounds/<round>/<id>_slug/`，知识树 `loop/tree/interview-loop.yaml`，轮次指南 `loop/LOOP_GUIDE.md`。
> **与 OA 题库的关系**：HackerRank OA 题在 `catalog/CATALOG.md` + `problems/qNN`；电面/onsite 与 OA 共用题库的题**不在这里重做**，只做交叉引用（列 "OA 交叉"）。
> 置信度：high = ≥2 独立一手来源或原题全文；medium = 单一手 + 二手印证；low = 仅题名/摘要。#refs = 独立来源数（同站多页算 1）。

## 0. 轮次速览（细节见 LOOP_GUIDE）

| 轮次 | 时长 | 形式 | 校招/实习 | L2+ 社招 | 本表节 |
|---|---|---|---|---|---|
| Recruiter 电话 | 30 min | fit/logistics | ✓ | ✓ | §G |
| Technical Phone Screen（"team screen"） | 60（45 编码 + 15 Q&A） | 1 题 3–4 part 递进，自己 IDE/CoderPad，**无自动测例** | ✓ | ✓ | §A |
| Onsite · Programming Exercise | 45–60 | 同电面但更长；2026 新增 AI 版 30 min | ✓ | ✓ | §B |
| Onsite · Bug Squash | 45–60 | 真实开源库 + 失败测试，自己 IDE | 多数有 | ✓ | §C |
| Onsite · Integration | 60 | 私有 repo + API 文档 + 联网（禁 AI），4–5 part | ✓ | ✓（Staff 以上换 Presentation） | §D |
| Onsite · System Design | 45 | 一大段业务描述，Whimsical | **通常无** | ✓ | §E |
| HM chat / Behavioral | 30–45 | Operating Principles 对照 | ✓（onsite 后 3–4 天） | ✓ | §G |

## A. Technical Phone Screen（`loop/rounds/03_phone_screen/`）

| ID | 题名 · 别名 | Part 递进 | 最近报道 | #refs | 置信度 | OA 交叉 | 来源 |
|---|---|---|---|---|---|---|---|
| ps01 | **Transaction stream levels** · "交易流水统计" | 4：按用户汇总 → 60s 滑窗超阈值 → 时刻 t 的 TopK → `[small,large,small]` 模式检测 | 2025-10-25 | 1（learncswithus，细节完整） | medium | q13 ledger 相邻 | cn_forums §3 |
| ps02 | **Shipping cost pricing** · "Shipping Cost Calculator" · tiered/accounting | 3：固定单价 → 阶梯 `(min,max,cost)` → `incremental`/`fixed` 混合 | 2025-10-20 · 1p3a post/7100079 · linkjob intern 2025 | 3 | high | q22 是**路径版**运费（不同题） | cn_forums §3；en_forums P9；1p3a thread/1093626 |
| ps03 | **Brace expansion** · "Expansion" | 3：`{a,b}` 展开 → 不匹配/单 token/无括号 → 嵌套 + 多组笛卡尔积 | 2024-06（LC 5341224）· interviewdb 2026 活跃 · hackerprep "last seen 4 months" | 4 | high | — | en_forums P4 |
| ps04 | **Transaction data validation** · "Data Validation" · "Fraud Reports" | 4：字段非空 → 金额范围 + 支付方式黑名单 → 与历史画像 ≥50% 匹配 → 优先级最多 2 个错误码、列对齐 | 2025-11-30（LC 7384225）· interviewdb 2026-07 | 2 | high | q15 KYC 是列校验/循环依赖（不同题） | en_forums P6 |
| ps05 | **Numeronym validation** · `i18n`/`a11y`/`k8s` | 3：形式校验 → 按词典校验展开 → 生成并消歧 | FinalRound（标 "Final Round"）· Exponent 2026 | 2 | medium | — | en_forums P16 |
| ps06 | **Receivables registration** · "Stripe API Receivables Registration"（巴西应收款） | 2 + 追问：CSV 按 `(merchant, card_type, payout_date)` 聚合 → 坏行/负额/周末顺延；追问幂等、流式、多币种 | 2024-10-04（csoahelp） | 1 | medium（代面站，但 I/O 具体） | q20 transaction fees/reconciliation 相邻 | cn_forums §3/§6 |
| ps07 | **Redact card numbers from logs** · "blur credit card numbers" · "Card Parsing" | 4：13–19 位数字串遮后 4 位 → 空格/`-` 分隔 → Luhn + 品牌前缀去误报 → 流式 10^5 行 | interviewing.io（coding 样题）· interviewdb "Card Parsing" 2026 | 3 | medium | q05 覆盖 Luhn/`*`/`?` 补全 | en_forums P13、C8 |
| ps08 | **Min/Max with comparator** | 4：最小 → 参数化 min/max → comparator → ties 全返回 | 2020-01（rampatra，都柏林） | 1 | medium（老题，结构典型） | — | en_forums P14 |

**已在 OA 题库、电面也常考（直接练 `problems/qNN`）：**

| OA ID | 题 | 电面报道 |
|---|---|---|
| q19 | Accept-Language parser（4 part：精确 → 前缀 → `*` → `q=`） | LC 4742657 2024-02；Glassdoor；1p3a post/7100091；**电面最高频** |
| q21 | Currency conversion（直达 → 一跳 → 最优 → 任意路径） | staffengprep；interviewing.io；1p3a thread/1078223（确认电面）；linkjob 2026 |
| q08 | Closing time / min penalty（Y/N 日志 → 最优时刻 → BEGIN/END 嵌套） | LC 2585038 2022；Blind bj5ehdwf；1p3a thread/1028744；interviewdb 2026 |
| q25 | Invoice reconciliation（memo → 金额+最早到期 → 容差） | LC 6696304 2025-04；interviewdb "Payment Invoices — Phone" |
| q22 | Shipping route（直达 → 一次中转 → 最便宜） | LC 5883672 2024-10 |
| q18 | Collusion / linked users（加权相似 → 1 跳 → 连通分量） | linkjob 2025-12 |
| q15 | KYC / CSV validation（非空 → 长度 → 黑名单 → 跨列 → 循环依赖） | Exponent P12；1p3a thread/1154573（**实际在 VO**） |
| q32 | Money transfer rebalancing（≥100 → 验证 → 最少笔数 → 审计） | programhelp VO 2025-08；LC 7521596 |
| q31 / q39 / q24 / q23 | Wishlist mutual rank / Server uptime log / Server allocator / Rate limiter | 2021–2024 电面高频（见 catalog/CATALOG.md） |

## B. Onsite · Programming Exercise（`loop/rounds/06_coding_onsite/`）

| ID | 题名 · 别名 | Part 递进 | 最近报道 | #refs | 置信度 | OA 交叉 | 来源 |
|---|---|---|---|---|---|---|---|
| cd01 | **Subscription email scheduler** · "Email Subscription" · "Email Notification Scheduler" · "membership 通知" | 3：按 plan 日期发 welcome/expiring → 改 plan → 续费/延期；追问去重、限流、乱序、取消 | 2025-12（linkjob NG VO）· 1p3a post/7100084 · 1p3a problems/4d6938ea、ac5e5760 · 1p3a thread/1100699（intern VO） | 6 | high | **q07** 是 OA 版（send_schedule/Changed/Renewed）；cd01 做 VO 版字段与追问 | en_forums C1；cn_forums §5/§9 |
| cd02 | **PaymentLedger 类** · "轻量支付交易记录系统" | 3：`add_payment/add_refund/get_total_revenue/get_payments_by_date` → 部分退款 + `payment_id` 去重 → 时间范围/非法时间戳/持久化追问 | 2025 Q4（programhelp intern VO） | 1 | medium | q13 account balance 相邻 | cn_forums §6 |
| cd03 | **AccountScheduler** · `locked_until` | 3：t 时刻可用性 → `acquire(id, duration)` → 不指定 id 时 LRU 自动选 | 2025-12（linkjob） | 1 | medium | q24 server allocator 相邻 | en_forums C4 |
| cd04 | **Rate limiter 4-part** | 4：basics → saving memory → tricky situations → multiple threads | 1p3a post/7100089（TOC）· 1p3a 题库 onsite 2025-12-06 · interviewing.io | 3 | high（递进模板确认） | **q23** 是滑窗/令牌桶 OA 版；cd04 重心在内存与并发 | cn_forums §6；en_forums C8 |
| cd05 | **Business account data verification** · KYC rule engine | 2：`when`/`requires`/`one_of` 规则引擎 + `a.b`、`owners[].x` 路径 → 字典序输出缺失字段 / `VERIFIED` | 1p3a problems/ad817329（**完整规格**）· thread/1155516（VO 挂经） | 2 | high | q15 是列级校验 | cn_forums 附二 |
| cd06 | **Suspicious users sliding window** · "1 分钟 >3 笔" | 2：O(n²) → 哈希 + 滑窗 O(n) | 2025-09（programhelp VO） | 1 | medium | ps01 Part 2 同族 | en_forums C5 |
| cd07 | **Transactions + rules（AI Programming Exercise）** · accept/block + if 条件 | 3：关键词匹配 → 字符串规则 → AND/OR 布尔；**用 AI 写、自己测** | 2026-06-09（interviewdb AI guide）· interviewfox 2026 | 2 | medium | q12 radar rules 是 OA 版规则语法 | en_forums §9、C11 |

**其他 onsite coding 报道（未建题，练 OA 对应）**：Optimal account balancing = q32；Transaction balances + 拒绝 + 平台借款 = q13；CSV per-user total + 重构加测试（linkjob 2026-02）；Recurring payment scheduler 设计题（linkjob 2026）；IAM 简版 / PII 访问控制（interviewing.io/Prepfully，题名）；"Factory Cost"（interviewdb，题名）。

## C. Onsite · Bug Squash（`loop/rounds/04_bug_squash/`）

| ID | mini 库（自含，200–600 行） | 注入的真实 bug 模式 | 真实库对应 | #refs | 置信度 |
|---|---|---|---|---|---|
| bs01 | **mini template engine**（Mako 型） | ① AST visitor 缺某节点类型 → 运行时错 ② 模板 URI 规范化只剥单个前导 `/`，lookup 剥全部 → 目录穿越绕过 | Mako #434/#435（2026-04，1–3 行修复）；Exponent "missing visitor function" | 4 | high |
| bs02 | **mini HTTP client**（requests 型） | ① `BytesIO` body 无 `len`/未 rewind → 上传截断 ② `iter_slices(None)` TypeError | requests #2589、#3532、#3369；Blind hkzsddkz/bxonqpkp | 4 | high |
| bs03 | **mini YAML + CSV parser**（SnakeYAML/CSV 型） | ① YAML 1.1 `on/off/yes/no` 隐式布尔（"Norway problem"）② RFC 4180 引号内逗号/双引号/换行丢失 | 1p3a problems/9be00044、3edbdc05（题面全文，要求 ≥3/≥5 回归测试）；linkjob SnakeYAML | 3 | high |
| bs04 | **ConfigManager 并发** | ① 懒加载竞态：线程拿到 `None` ② 粗粒度全局锁 ③ teardown 后残留文件句柄/缓存 | learncswithus 2025-11-17；Exponent "unguarded read-modify-write race"；linkjob 2026 | 3 | medium |
| bs05 | **asyncio 数据拉取竞态**（React 版移植） | 快速切换 `resource_id` 时旧响应覆盖新数据；需取消/忽略过期、loading 状态不被旧请求关闭 | 1p3a problems/977b9f31（题面全文）；thread/1144573（JS VO） | 2 | high（形态）/ Python 移植为推断 |

**被报道的真实库（按语言）**：Python `requests`、`Mako`、YAML/HTML parser（staffengprep）；Java `SnakeYAML`、`Moshi`（1p3a post/7100086）、`Jackson`（传闻）；JS `Express`、`Day.js`、React 组件；Ruby `Sass`。评分主线：复现 → 假设 → debugger 验证 → 最小修复 → 回归测试；"solving the bug isn't the primary objective"（Stripe 员工）。

## D. Onsite · Integration（`loop/rounds/05_integration/`）

| ID | 题名 | Part 递进 | 最近报道 | #refs | 置信度 | mockserver |
|---|---|---|---|---|---|---|
| int01 | **BikeMap** · "Bike Map API Integration" | 5：GeoJSON 取前 10 坐标（`[lng,lat]` 陷阱）→ POST 坐标取 PNG 落盘 → 画路线 → 地标最近点（O(n·m) vs 索引）→ 批处理/缓存 CLI（"few reach"） | 2026-06-07（oavoservice）· 2025-12（linkjob）· 2025-11（learncswithus）· 1p3a post/7100082、thread/1096856 · Blind h8lemeaq（"不总是 bikemap"） | 7 | **high（最高频 integration 题）** | `maps` |
| int02 | **Payments reconciliation client** · "transaction reconciliation script" | 4：cursor 分页拉全量 → 429 + `Retry-After` 退避 → `Idempotency-Key` 退款重放 → webhook `Stripe-Signature` 验签 | Simplify 2026（校招 VO 转述）· Leon "四大边界" · programhelp "call API + store DB" 2025-08 · 官方 docs | 4 | medium（组合题；各要素一手） | `payments` |
| int03 | **Multi-JSON ETL** | 3：读 3 个 JSON → 字典 → 双向转换/join → 缺失/重复 | 2025-12-06（linkjob，3.9/5）· Exponent 类型 · 1p3a problems/e05350e5 | 3 | medium | — |
| int04 | **Review assignment via git diff + CSV owners**（JGit 原题，Python 用 subprocess git） | 3：两分支变更文件 → CSV owners 映射 → 最多变更 owner（平局字典序） | 1p3a problems/1eb955cf（题面全文） | 1 | medium | — |

**其他报道**：request replayer（1p3a 801857 onsite 文档）；Payment Reconciliation 对接清算 API（1p3a post/7100087）；读文件 → POST → 打印响应（2020 都柏林 Java）；实习 2025 "文件抽字段 → 调外部 API → 合并输出"；前端版读 JSON 渲染/Blob 下载（GreatFrontend）。官方 `stripe-interview` org 的 Python prep repo 预装 `requests`。

## E. Onsite · System Design（`loop/rounds/07_system_design/`）

| ID | 题 | 追问主线 | 最近报道 | #refs | 置信度 |
|---|---|---|---|---|---|
| sd01 | **Webhook delivery** | 10k/s；商户全 500；noisy neighbor（hang 30s）；任意 URL → SSRF/DNS rebinding；exactly-once；dashboard；公平限流 | 2026-05-20（Medium emily，Staff 面试官）· 1p3a post/7100095 · collegesidekick 801857 · staffengprep | 5 | **high** |
| sd02 | **Idempotent payment / charge API** | 幂等键 + 24h；DB 唯一约束 vs Redis；并发 cache miss；外部授权后部分失败；状态机；对账 | linkjob 2026-02 · techinterview 2026-07 · LC 6896919（去重系统 coding 版） | 3 | high |
| sd03 | **Ledger service** | 双记账、不可变（反冲）、幂等写、point-in-time 余额、高吞吐单商户、多 AZ | programhelp VO 2025-08 · prachub 2025-07 · collegesidekick · Exponent · Stripe Ledger 博客 2024-02 | 5 | high |
| sd04 | **Distributed rate limiter**（API 网关） | token bucket vs sliding window、Redis、按客户端公平、退化 | Exponent · interviewing.io · techinterview · Paul Tarjan 博客 | 4 | high |
| sd05 | **Subscription billing & invoicing** | 周期、proration、dunning、发票状态机、时区 | ophyai 2026-07 · raw/system_design §4.5 | 1 | medium（培训站） |
| sd06 | **短题三连：Connect 分账/payouts · Feature flag SDK · Metrics counter library** | 平台/商户余额与负余额；flag 评估 SDK；服务侧指标聚合 | ophyai 2026-07 · 1p3a post/7100093、7100094 · thread/1123389 · staffengprep | 4 | medium |

**其他题名**：Monitoring/APM（2020 都柏林、Exponent）；Auth/identity 重设计；distributed LRU；TopK；Fraud/ATO 预测 ML 系统（1p3a post/7100076、7100078，方向题）；Payment refund service（programhelp）。评分：Exponent 五维（framing / API & data model / failure modes & scale / separation of concerns / delivery）；一手拒因 = "insufficient reasoning about failure modes"。

## G. 非编码轮（`loop/rounds/01_recruiter/`、`02_hm/`、`08_behavioral/`）

| ID | 内容 | 来源 |
|---|---|---|
| rc | Recruiter 题库（背景/动机/薪资/地点/时间线）+ 反问清单 + 薪酬速查（L1 美国 TC ≈ $210K；班加罗尔 L1 ≈ 59L）+ cooldown 6–12 月 | hr_hm_behavioral §Recruiter；en_forums §1、流程与时间线 |
| hm | HM chat 题库（项目深挖、deadline、模糊需求、ownership、沟通风格）+ Operating Principles（6 条对外版 + 内部完整版）映射表 + 6 故事覆盖矩阵 | hr_hm_behavioral §HM、§Operating Principles；cn_forums §2 |
| bq | Behavioral 题库（Stripe 专属去重 + 跨公司 20 题）+ STAR-L 模板（90s/3min）+ 自评 rubric | hr_hm_behavioral §Behavioral、§题库总表 |

## H. 来源可信度与存疑

- **一手最强**：一亩三分地题库 `interview/problems/<uuid>` 原题全文（cn_forums 附二，10 题）；LeetCode/Medium/Taro 个人面经（年份明确）；Blind 上自称 Stripe 员工的评论；Medium emily 的 SD 逐问记录；femisowems GitHub 仓库（6 题带测试，2026-05）。
- **二手但细节具体**：learncswithus / programhelp / csoahelp / oavoservice / linkjob / interviewdb（代面/付费站，有营销动机；题目 I/O 与英文侧互相印证、无矛盾）。
- **官方**：docs.stripe.com（幂等/分页/webhook/限流/版本）、工程博客（Ledger、idempotency、rate limiters）——是 int02/sd 系列的"标准答案"依据；**官方无面试流程页**，"bug squash/integration" 是民间叫法。
- **存疑/未收录**：sinatra/jq/flask/redis-py/lodash 作为 bug squash 库无证据；"flaky payments API with retries" 无一手对应（int02 为组合题）；1024bbs 三帖不可达；Medium 中文《我與 Stripe》两地 onsite 帖 403；Glassdoor 全站被 Cloudflare 拦。
- **轮次归属漂移**：同题（receivables、KYC、money transfer/bikemap）在不同来源被归到不同轮次；以 recruiter 口头说法为准，不要机械对应。
