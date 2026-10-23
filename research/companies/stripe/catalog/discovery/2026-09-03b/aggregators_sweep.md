# 英文聚合站 + Blind + LeetCode 重扫（2026-09-03）

三轮排查（`catalog/discovery/2026-09/` 的批 A/B/rounds_material）之后的第四轮，目标是**穷尽**表中标 200/202 的站，而不是抽样。访问日期全部为 **2026-09-03**，不再逐条重复标注。所有抓取均用
`UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"` 的 `curl`，未用 WebFetch（WebFetch 对 teamblind/prachub 返回的是转述摘要，会丢信息）。

## 方法论更正（本轮最大的一条纪律修正）

批 A/B 报告里说"prachub 的 `content` 字段是候选人原始报告"，本轮发现这话**只对一部分页面成立**。prachub 的 Next.js 页面里 `content` 字段实际上分两种：

1. **候选人原始转载**（真实来源，多数带"求加米""还在等最终的结果"这类 1point3acres 论坛用语，或 `本帖最后由 XXX 于 … 编辑` 这类论坛页眉）——这种页面在原始 HTML 里能找到 `console_solution_locked":true,"content":"<候选人原文>","content_enhanced"` 这个精确的字段序列；
2. **prachub 自己生成的技术规格外壳**（面向 SEO 的 `data-seo-content="question-body"` 区块，写法工整、样例齐全，但`content` 字段是空字符串 `""` 或指向一个 React 占位引用如 `"$31"`，`content_raw` 才是这段生成文本）。

本轮对 60 个 `coding-questions` 页逐个做了这个区分（脚本：定位 `console_solution_locked":true,"content":"..."` 锚点，取到 `,"content_enhaced"` 前的文本，非空即为候选人原文）。**大量此前可能被当成"题面已核实"的 prachub 页面，其实是外壳**——本报告对每条都标注了是哪一种。

---

## 各站可达性与实际抓取结果

| 站点 | 状态 | 翻了多少页 | 拿到多少条 Stripe 内容 | 备注 |
|---|---|---|---|---|
| prachub.com | 200 | `/companies/stripe?page=1..6`（page 7 起 404，确认到底）；另加 `/coding-questions/<slug>` 单题页 ~48 个、`/interview-experiences/<slug>` 全部 3 个 | 列表页共 **119 条唯一 slug**（60 coding-questions + 56 interview-questions + 3 interview-experiences，无重复分页）；单题页里 **13 条**拿到候选人原始转载（见下表），另有多条只拿到 prachub 生成外壳 | 本轮主力站；3 篇 `interview-experiences` 长文全部读完，价值最高 |
| interviewdb.io | 200 | `/question/stripe?page=1..4`（page 4 空，确认到底） | 37 条唯一标题，**与批 A/B 已核对的清单完全一致，无新增标题** | 详情页仍是前端占位符，只能取标题+相对时间 |
| teamblind.com | 200 | `/search/stripe`、`/search/stripe%20oa`、`/search/stripe%20onsite` 三次搜索 + 18 个命中帖逐一 curl 全文 | 无新的题面原文，但拿到 **process/时间线类信息 ~12 条**（团队匹配延迟、cooldown、AI 编码轮范围、IDE 使用规则等，见下文"轮次级观察"） | 搜索默认按"相关+近期"排序，这次命中的多是 process 讨论帖而非具体题目帖——说明近几周的技术题面帖已经被前几轮挖得差不多 |
| leetcode.com/graphql | 200（`topic(id)`、`topicComments(topicId)` 均可用，无需登录） | 用 WebSearch 找到 4 个未在 catalog 出现的帖子 ID（7566910、5899185、7314171、6896919），逐个查询 | 6896919 帖子不存在（404-等价错误）；7566910、7314171 的 `post.content`/`post.contentPreview` 均返回占位符 `"article-topic"`，正文拿不到，只能拿到评论区提问（无实质新信息）；5899185 拿到全文但只是"求资料"帖，无题面 | 确认"`article-topic`"是 LeetCode 把部分帖子迁移到另一套 CMS 后的占位符，本环境目前**没有**找到能读到这类帖子正文的字段/端点 |
| levels.fyi | 200（4 个页面：整体页 + L1/L2/L3 分级页） | 全部读完 | 拿到当前中位数 TC 三档，见下文专节 | — |

---

## 已收录题目的新增细节

### A2 · Jupyter / WebSocket Load Balancer（`q09_jupyter_load_balancer`）—— 新增 1 条独立 #ref
- **来源**：https://prachub.com/coding-questions/implement-stateful-connection-router-simulator（curl 抓取，候选人原始转载，`interview_round:"Online Assessment"`，`created_at:"2025-12-06"`）
- **原文摘录**（中文，候选人原帖，节选）："一共五个部分，计时60min…Part 1: 处理 CONNECT 请求，分配目标 server（按 round-robin）…Part 4: 支持 maxConnectionsPerTarget…如果所有 target 都满，则忽略连接…Part 5: SHUTDOWN target…所有在该 target 上的连接全部 eviction（按 eviction 顺序输出）"
- **置信度**：high（候选人原始转载，含"求加点米"论坛用语，非 prachub 生成外壳）
- **判定**：这不是新题，是 A2 的又一次独立复现——5-part 结构（CONNECT round-robin → 重复 CONNECT 幂等 → DISCONNECT → 容量上限 maxConnectionsPerTarget → SHUTDOWN+批量 eviction）与 catalog 现有的"least-loaded → DISCONNECT → sticky → capacity → SHUTDOWN re-route"骨架一致，但这次给出了**具体的容量满时行为（跳到下一个 server，而不是报错）**和**SHUTDOWN 的 eviction 顺序**这两个此前没记录的细节。建议 #refs 由 13 → **14**。

### A11 · Account Balance Ledger（`q13_account_balance_ledger`）—— 新增 1 条独立 #ref
- **来源**：https://prachub.com/coding-questions/compute-account-balances-with-rejection-and-overdraft（候选人原始转载，署名 `jimmybutler4624`，`本帖最后由 jimmybutler4624 于 2025-12-23 14:21 编辑`，`interview_round:"Onsite"`）
- **原文摘录**："The third part begins by enabling a debit platform to handle insufficient account balances. If an account has insufficient funds, it will deduct funds from the associated account (the platform account); if that account is also empty, the transaction is rejected."
- **置信度**：high（候选人原始转载）
- **判定**：与 catalog 的 3-part 结构（balances → reject negative → platform loans/max_reserve）完全吻合，是独立第 7 条 #ref。**附带信息**：同一候选人在同一帖里说"The integration section is about bicycle maps"——即这场 onsite 里 Account Balance Ledger（coding）与 BikeMap（integration，= C28）是**同一天/同一候选人**的两轮，首次把这两题的共现关系坐实。#refs 由 6 → **7**。

### A13 · Weekly Deployment Window Scheduler（`q29_deployment_windows`）—— 补全冻结日后发现的题面全文
catalog 的"2026-09-03 二轮排查增量"表里已经记了"Find Weekly Deployment Windows Across Time Zones（Hard），2026-08-27，PracHub"，但当时只有标题。本轮拿到了**同一份报告的两个独立发布位置**的全文：

- https://prachub.com/coding-questions/find-weekly-deployment-windows-across-time-zones（中文原文，候选人 `Eil宁` 于 2026-8-24 编辑）
- https://prachub.com/interview-experiences/stripe-software-engineer-interview-experience-utc-deployment-windows-and-a-10-of-11-assessment（英文改写版，`created_at:2026-08-28`）—— **这两者是同一份候选人报告的中英文两个版本，不是两条独立 #ref**

- **原文摘录**（中文原始版）："核心 Tricky 点跨周时区映射：UTC = Local − Offset 计算后可能出现 negative（上一周）或 >10080（下一周）的情况…建议将全局打点数组扩展为 3 倍大小（如 [-10080, 20160]），用偏移索引映射规避越界。" / "题目目前只看到两个 Part，总共有 11 个 Test Cases…最终拿了 10/11。"
- **置信度**：high
- **判定**：这是 A13 的一个**新的、更难的变体**（早于/接近冻结日 2 天，已在 catalog 记录），本轮补上了完整算法要点（三倍数组扩展技巧、长区间贪心拆分成 K 个窗口）和候选人自己的类比（"也可以看看 LC1229 和 56"，即 Meeting Scheduler + Merge Intervals），可直接用于升级 `q29` 的第二难度层级。**不新增 #ref 计数**（已在原表记过一次，本轮只是把摘要换成全文）。

### A14 · Datacenter Request Router（`q17_datacenter_router_haversine`）—— 拿到完整候选人复述题面（重大细节增量）
- **来源**：https://prachub.com/interview-experiences/stripe-software-engineer-interview-experience-three-part-oa-on-data-center-routing（`created_at:2026-08-25`）
- **原文摘录**："REGISTER <region> <latitude> <longitude> <capacity>: registers a data center, with a default health state of healthy." / "Routing target selection: prefer the nearest healthy region; if distances are tied, pick by alphabetical order." / "Output format: <selected region> <distance to that region> <candidate healthy region list (sorted per the rules, space-separated)>"
- **置信度**：high
- **判定**：catalog 现有 A14 只记了"3 (registry + validation → Haversine → ROUTE nearest healthy with capacity)"的粗粒度骨架；这份报告给出了**REGISTER/SET_HEALTHZ 的完整校验规则（纬度[-90,90]、经度[-180,180]、capacity>0、重复注册/未注册报 ERROR）**和**平局按字母序**这条此前未记录的规则。建议把这条并入 A14 正文，#refs 由 4 → **5**。

### A18 · Join Dataset（`q14_join_dataset`）—— 拿到完整候选人复述题面（此前只有标题级）
- **来源**：https://prachub.com/coding-questions/implement-a-csv-dataset-join（候选人原始转载，`created_at:2026-08-22`，**距冻结日很近，说明这题在 2026-08 仍在被问**）
- **原文摘录**："实现joinDataSet()…Part 1：basic dataset join，注意customer 和processor都需要排序，并且fieldName需要出现在每一个file上。Part 2：left join…Part 3：multiple matches，一个customer有好几个processor的方式，返回multiple rows…Part 4：skipUnmatched…提干非常的长，且有小细节。时间实在是来不及了最后没写完。"
- **置信度**：high（候选人原始转载，且候选人自己链接了一个更早的 1point3acres 相关帖 `thread/1033126`，提示这题有更早的姊妹题）
- **判定**：catalog 现有 A18 只写了"3 (inner join → left join → one-to-many)"，#refs=2、medium 置信度。本轮确认是 **4 part**（basic → left join → multiple matches → skipUnmatched，第 4 part 才用到 `skipUnmatched` 参数），且候选人明确说"排序是隐藏要求"。建议 part 数由 3 改 **4**，置信度由 medium → **high**，#refs 由 2 → **3**。

### A22 · Shipping Cost（`q22_shipping_cost`）—— 新增 2 条独立 #ref
- **来源 1**：https://prachub.com/coding-questions/compute-shipping-cost-with-tiered-pricing-2（候选人原始转载，VO，"三道coding题（全是原题，Shipping Cost2）"）。原文摘录："coding3：两种计费方式…若有则直接取固定价，若没有就用incremental逐件累加…后续还有个反问环节：包括Stripe内部是否允许并支持使用AI工具等。"
- **来源 2**：https://prachub.com/coding-questions/implement-tiered-shipping-calculator（候选人原始转载，JS 版，"1问 给了个object 根据地点商品数量算总价…3问 object 里的价格加了一个前n个买入flat rate"）
- **置信度**：high（均为候选人原始转载）
- **判定**：两条都与 catalog 的 matrix 版本（flat → tiered → fixed+incremental）吻合，是独立复现，其中来源 1 附带一条**新的流程信息**：面试官明确说了"正确性>可读性>性能"的排序，反问环节会问 Stripe 内部 AI 工具使用政策（呼应 LOOP_GUIDE §6 的 AI 轮）。#refs 由 25 → **27**。

### A30 · Invoice / Payment Reconciliation（`q25_invoice_reconciliation`）—— 新增 2 条独立 #ref
- **来源 1**：https://prachub.com/coding-questions/design-payment-to-invoice-matcher-with-priorities（候选人原始转载）。原文摘录："第一部分的时候payment里面的一部分包含invoice id…第二部分的时候payment里面没有invoice id了，需要通过amount来match找到对应的invoice，有多个amount的话就选取最早的invoice…第三部分的时候payment里面的amount也许有偏差，会给一个forgiveness value…类似于'有准确的invoice id就不要amount match，有exact amount match就别管forgiveness'。"
- **来源 2**：https://prachub.com/coding-questions/match-payments-to-invoices-by-memo-or-amount（候选人原始转载）。原文摘录："若备注为标准格式则按发票ID匹配，否则按支付金额匹配（金额相同时选择到期日最早的发票）。"
- **置信度**：high
- **判定**：两条都与 catalog 3-part 结构（memo id → amount+earliest due → forgiveness）完全吻合，来源 1 额外给出了**匹配优先级的显式规则**（"有 memo id 就不用 amount 匹配"）和一条通用建议（"能用 integer 就别用 float，能截 substring 就别用 regex"）。#refs 由 6 → **8**。

### C8 · Review Assignment via Git Diff + CSV Owners —— 从"仅标题"升级为**已复原**
- **来源**：https://prachub.com/coding-questions/assign-reviewers-from-changed-files（候选人原始转载）
- **原文摘录**："Integration: review-assignment. 写一个代码，使用JGit，对比一个git repo 的两个branch。拿到改变过的文件名list之后，根据一个CSV文件提供的文件owner，返回拥有最多改变文件的owner。简单说就是类似PR发布后，自动寻找reviewer。" / "Debug： SnakeYAML. Bug 1, flag: on 复制代码 无法解析。 Bug 2， CSV解析结果漏掉了引号" / "AI coding: 在hackerrank里，有一个ai 对话框，让你根据要求写prompt 来解决代码。自己手写80%概率写不完，主要依赖AI。"
- **置信度**：high（候选人原始转载）
- **判定**：catalog 原 C8 是"title only"。现在拿到完整题面：**Integration 轮**用 JGit 比较两分支 diff、按 CSV 的 file→owner 映射统计谁改动文件最多，返回该 owner（类似自动分配 code reviewer）；同一场面试还报告了 **Bug Squash 轮的 SnakeYAML 两个具体 bug**（`flag: on` 解析失败、CSV 解析丢引号——与 LOOP_GUIDE §4 的库列表吻合，但"漏引号"是新的具体 bug 描述）和 **AI Coding 轮**的第一手细节（HackerRank 内嵌 AI 对话框，"自己手写 80% 完不成，主要靠 AI"）。建议把 C8 移出 Table C，升级为 Table A 新行（可称 A43，或按 loop/rounds 命名新增 `int0x_review_assignment_jgit`），置信度 **high**。

### C27 · Bitfont Renderer 家族 —— 新增第 4 个变体，进一步坐实"多版本并存"
- **来源**：https://prachub.com/coding-questions/convert-bitmap-into-ascii-characters（`created_at:2025-07-29`，Onsite）。该页有两层内容：候选人的一句话原始描述（Draft.js 区块："Given an array/string of 0-1 bits representing a bitmap font, write code to render each character as a grid using '.' for 0 and '#' for 1, and concatenate multiple characters to print whole words efficiently."）+ prachub 生成的详细规格（row-major bitstring、每字符间插入一列 `.`、空格是全 `.` 空白字形、非法输入抛 ValueError）。
- **置信度**：medium（候选人的一句话是真实来源，但那句话本身信息量很小；下面的详细规则大概率是 prachub 补全的，不能全信为原题格式）
- **判定**：这是 batch A 已发现的 N1 的**同一个页面**（未新增 URL），但本轮确认了该页存在候选人的原始一句话描述（此前 batch A 只看到 prachub 生成的规格，没意识到上面还有候选人原句）。**结论不变**：C27 仍是"家族，无单一标准题面"，本轮没有新证据推翻这个判断，但这次至少确认这个"0/1 位图 + `.`/`#` 渲染"版本确有真实候选人来源做种子，不是纯 AI 编造。

### C9 · Incident Monitor —— 无新增（沿用批 B 结论）
本轮重新访问 https://prachub.com/coding-questions/detect-trigger-and-resolve-events 确认内容与批 B 记录一致，未发现新版本或新报告。维持"部分线索"判定。

---

## 新题（CATALOG 里没有的）

### N-DS1 · Data Scientist / Data Analyst 岗位的整条面试流程 —— **全新赛道，此前 catalog 完全没有覆盖**
本轮在 prachub 上翻到 6 道标"Stripe SQL Question"或 Data Scientist 岗的题（`write-sql-for-snapshot-features-and-labels`、`write-sql-to-detect-recurring-non-subscription-users`、`write-sql-to-monitor-weekly-chargeback-spikes`、`design-an-idempotent-sql-etl-for-late-data`、`design-metrics-and-write-sql-for-a-case`、`implement-streaming-per-user-reservoir-sampling`），全部标注 `position:"Data Scientist"`。**重要方法论提示**：其中至少 2 对页面的候选人原文字段**完全相同**（例如 `write-sql-for-snapshot-features-and-labels` 与 `implement-streaming-per-user-reservoir-sampling` 的 content 字段是同一段中文报告），说明 prachub 把**同一位候选人的一段泛泛而谈的面经**，套用到了好几个自己生成的、题目内容各不相同的技术规格页面上——**这些题的"具体规则"部分置信度应普遍下调为 low**，能信的只有候选人原文那一段"过程描述"。

- **过程新发现**（来源：https://prachub.com/coding-questions/write-sql-to-monitor-weekly-chargeback-spikes，候选人原文，Onsite，DA 岗）："第一轮: HM phone call…第二轮:take home project，给一个分国家,行业的交易量数据,去进行时间序列的预测…Onsite: Project Review…Product sense…SQL: 给了几个表格,用到join和aggregate function…Business partner…Experience: 大老板纯行为面" —— 置信度 **medium**（候选人原文，但只此一份，DA 岗流程首次被记录）
- **判定**：建议 catalog 新增一节"DS/DA 岗位流程"（若目标读者是 SWE 岗则可标注"非本仓库主线，仅供参考"），不建入 Table A（Table A 是 SWE bespoke coding 题定义域）。

### N-1 · Find linked merchants by shared fields
- **来源**：https://prachub.com/coding-questions/find-linked-merchants-by-shared-fields（`interview_round:"Technical Screen"`，`created_at:2026-01-06`）
- **原文摘录**（prachub 生成外壳，非候选人原文）："This question evaluates the ability to model and detect entity linkages via exact field matching and weighted scoring as well as to reason about reachability in a graph formed by those links."
- **置信度**：low（无候选人原文，仅 prachub 概述）
- **判定**：主题与 A9（Collusion）/ C7（Matching Contacts）高度重合，但对象是"merchant"而非"user"，字段权重也可能不同。因为拿不到候选人原文，暂不建议单独立项，标注为"A9/C7 家族的疑似变体"，留待下一轮核实。

### N-2 · Propagate runtime ID across API requests
- **来源**：https://prachub.com/coding-questions/propagate-runtime-id-across-api-requests（`interview_round:"Technical Screen"`，`created_at:2026-01-22`）
- **置信度**：low（无候选人原文，仅标题+prachub 概述："This question evaluates distributed tracing / correlation-id propagation across HTTP client calls"，转述不逐字引用）
- **判定**：疑似 integration/debug 轮的分布式 trace-id 传递题（batch A 已在 N5 提过标题，本轮确认其 `interview_round` 是 Technical Screen 而非 integration，且仍无法拿到候选人原文）。**未找到**实质规则，维持"标题孤证"。

### N-3 · Bridge（被 Stripe 收购）有独立于母公司主线之外的面试轨道
- **来源**：https://www.teamblind.com/post/Bridgestripe-coding-interview-experience-4nemt0po
- **原文摘录**："I recently interviewed at Bridge (acquired by Stripe)…After the initial technical screening, I was passed on to two coding interviews and I would say I was able to complete upto step 2 and meaningful progress in step 3…was it typical lc questions? or stripe style implementation questions? — It was not typical LC question."
- **置信度**：medium（候选人自述，单一来源，无题面细节，只有流程形状）
- **判定**：Bridge（稳定币公司，2025 年被 Stripe 收购）目前有**自己独立的技术面流程**（"技术初筛 + 两轮 coding，每轮都是多 step 递进"），风格上与 Stripe 主线一致（"不是典型 LC 题"，多 step 递进），但题库大概率不同。建议记一笔"若面 Bridge 团队，题库可能不在本 catalog 覆盖范围内"，不建具体题目。

### N-4 · Debug Validation Error Aggregation（Bug Squash 轮新库：Python Colander）
- **来源**：https://prachub.com/coding-questions/debug-validation-error-aggregation（`interview_round:"Onsite"`，`created_at:2026-05-14`，difficulty hard）
- **原文摘录**（prachub 生成概述，无候选人原文）："This question evaluates debugging, error-handling, and message-normalization skills in Python schema-validation libraries, focusing on aggregation of Colander-style Invalid exceptions into dotted-path error dictionaries."
- **置信度**：low（无候选人原文，只有 prachub 概述）
- **判定**：如果属实，这是 LOOP_GUIDE §4 "库按语言分流：Python `requests`/`Mako`" 列表里**没有的新库**——Colander（Pyramid 生态的表单校验库）。**未找到候选人原文**，建议先记一笔待验证，不直接改 LOOP_GUIDE。

### N-5 · Debug an Asynchronous SDK Race Condition with a Customer（Bug Squash / 客户支持向调试题）
- **来源**：https://prachub.com/interview-questions/debug-an-asynchronous-sdk-race-condition-with-a-customer（分类页跳转到 `interview-questions`，非 `coding-questions`，说明 prachub 自己也没把它当成标准编码题分类）
- **置信度**：low（页面本身内容极少，`meta_description`："Diagnose an intermittent SDK race that returns data from a previous asynchronous request."，无候选人原文、无 part 划分）
- **判定**：标题孤证，可能是新的"debug 轮"变体（区别于开源库 bug squash，这个描述像是 SDK 层面的竞态条件调试，可能更贴近 support engineering 或 customer-facing debug 场景）。未建题。

### N-6（沿用批 A 已发现，未升级）· 系统设计新题
本轮在 ie1（Senior+ 报告）里再次确认了"metrics monitoring system, simplified to just counts"作为 system design 轮真实考过的主题，与批 A 的 N3（Design a Count-Metrics Monitoring Platform）互相印证，来源升级为 **2 个独立候选人**（原 N3 的 prachub 页面 + 本轮 ie1 的第一人称叙述）。原文摘录（ie1）："System design: a pretty standard interview — design a metrics monitoring system. He simplified the metrics down to just counts, so basically the two chapters in Alex Xu's book on ad click counting and metrics monitoring were enough to answer it."

---

## levels.fyi 薪酬复核

直接 curl 抓取（非 WebSearch 摘要）以下 4 个页面并从 `og:description` meta 标签取得官方口径的"中位数总包"：

| 页面 | URL | 原文摘录（`og:description`） |
|---|---|---|
| L1 | https://www.levels.fyi/companies/stripe/salaries/software-engineer/levels/l1 | "The median total compensation package for a L1 at Stripe is **$209,973**." |
| L2 | https://www.levels.fyi/companies/stripe/salaries/software-engineer/levels/l2 | "The median total compensation package for a L2 at Stripe is **$289,675**." |
| L3 | https://www.levels.fyi/companies/stripe/salaries/software-engineer/levels/l3 | "The median total compensation package for a L3 at Stripe is **$435,992**." |

置信度：**high**（页面直接抓取，非搜索引擎转述）。

### 与 `loop/LOOP_GUIDE.md` §9 的差异

LOOP_GUIDE §9 原文："美国 L1 TC ≈ $210K（base ~$147K + stock ~$40K/yr + bonus）；L2 ~$278K"

| 级别 | LOOP_GUIDE 现有数字 | 本轮实测中位数 | 差异 |
|---|---|---|---|
| L1 | ≈ $210K | $209,973 | **基本一致**，无需改动 |
| L2 | ~$278K | $289,675 | **高出约 $11,675（+4.2%）**，建议更新 |
| L3 | （未记录） | $435,992 | **guide 完全没有这一档**，建议补充 |

**印度班加罗尔数据未能复核**：尝试 `https://www.levels.fyi/companies/stripe/salaries/software-engineer/levels/l1/locations/bangalore-india`，返回 200 但 `og:description` 是空模板（"Learn how much a L1 makes at Stripe in ."，地区未填充，可能是该 URL 参数格式不对或该细分组合数据点太少），未能验证 guide 里"班加罗尔 L1 ≈ 59L"这个数字，本轮不予更新，留待下次用正确的 URL 结构重试。

**其他薪酬数据点（来自 teamblind，置信度 low，仅供交叉参考）**：
- https://www.teamblind.com/post/stripe-swe-phone-screen-dub4tnbn — 评论区互相矛盾："They said 180-220k TC" vs "L2 median is 270 which is insane"（后者与本轮 levels.fyi L2 中位数 $289,675 量级接近，前者更像 L1 offer）
- https://www.teamblind.com/post/stripe-bar-is-ridiculous-yw52z5sf — 楼主签名档 "TC- $670k"（未注明级别，疑似 Staff/Principal 或夸大，不采信为具体级别数据）

---

## 轮次级观察（流程/时间线/AI 轮变化）

1. **AI 编码轮范围可能比 LOOP_GUIDE 记录的更广**。ie1（Senior+ 候选人，2026-08-25 报告）说"Two phone screens, coding with AI"——即该候选人的**两轮电面都是 AI 辅助编码**，而不是 LOOP_GUIDE §6 描述的"只有一个独立的 30 分钟 AI Programming Exercise，其余轮次严禁 AI"。这与 C8/assign-reviewers-from-changed-files 报告的"AI coding 轮在 HackerRank 里有独立对话框"部分吻合（AI 轮确实存在），但 ie1 暗示 Senior+ 候选人可能被安排了不止一轮 AI 辅助面试。**单一来源，medium 置信度，建议下一轮专门找更多 Senior+ 报告交叉验证**，暂不改写 LOOP_GUIDE 正文。
2. **Bug Squash 轮新增一个具体 bug 描述**：SnakeYAML 的"CSV 解析结果漏掉引号"（见 C8 小节），补充在 LOOP_GUIDE §4 现有的"四类典型 bug"里，属于其中的"逻辑错误"类。
3. **OA 阶段的执行环境限制被具体化**：teamblind `stripe-oa-tips-iw8632ms` 评论确认"OA 必须在 HackerRank 网页里直接写代码，用外部 IDE 复制粘贴可能触发抄袭检测；Technical Screen 阶段可以用自己的 IDE"——比 LOOP_GUIDE §3 现有的"CoderPad 或自己 IDE 共享屏幕（可选）"更明确地把 OA 和电面的规则分开了。
4. **team match 延迟的一个长尾案例**：https://www.teamblind.com/post/stripe-l3-team-match-swe-passed-onsite-2ov4b8tc — L3 London 候选人 onsite 通过后**等了 4 个多月**没有 team match（"there have been only 2 open roles in the last 3-4 months"），比 LOOP_GUIDE §9 记录的"2–6 周，可能撤回"长得多。置信度 medium（单一候选人自述，YOE 8，可能受地区/年份特殊性影响），建议 §9 补一句"存在数月级的长尾案例，尤其欧洲团队 headcount 紧张时期"。
5. **OA 阶段的 cooldown 时长出现矛盾证据**：https://www.teamblind.com/post/stripe-oa-passed-all-test-cases-but-hit-with-a-1-year-cooldown-r2mcra36 标题直接写"passed all test cases but hit with a 1-year cooldown"——即 OA 100% 通过后仍在后续流程被拒，且被告知的 cooldown 是**1 年**，而不是 LOOP_GUIDE §0"6 个月（早期轮被拒）"。同贴另一条评论提到"most likely they flagged AI generated code"作为猜测性解释（无官方确认）。**置信度 medium，单一来源标题+正文自述，未见第二个独立来源印证 1 年这个具体数字**，建议标注为待观察项而非直接改写现有结论。
6. **JS/全栈岗的 onsite 组合首次被完整记录**：https://prachub.com/coding-questions/generate-user-notifications-from-schedules（=同一候选人的 https://prachub.com/coding-questions/plan-bicycle-routes-on-a-city-map）——候选人报告"代码一轮 通知单生成（=A3 变体）→ 代码二轮 自行车地图（=C28 BikeMap）→ 系统设计轮 本地活动计数器（呼应 N3/N-6）→ 调试轮 未见过的前端框架找 DOM 属性错误 → HR 人品轮"。这是本仓库第一次拿到 JS/全栈岗完整 onsite 轮次顺序的第一手报告。
7. **确认"原题复用"策略仍然有效**：https://prachub.com/coding-questions/compute-shipping-cost-with-tiered-pricing-2 候选人明确说"面试Stripe要提前熟悉一下题库，提前就熟悉一遍代码，很有可能会遇到原题"——三道 VO coding 题全部命中已知题库（Shipping Cost 变体），候选人全部做完。这是对本仓库"背题库有用"这个前提假设的一条正面证据。

---

## 覆盖率评估（对照 80% 目标，要有分母）

用 prachub 的 `coding-questions` 分类作分母，理由：这是本轮唯一能拿到**完整、无重复、可翻到底**的结构化列表（60 条，两次翻页确认到 404 为止），比 teamblind/leetcode 的"搜索命中"式抽样更接近一次穷举。

**分类结果（60 条 coding-questions slug 逐条比对 CATALOG Table A/B/C 全文 + 本轮新识别的 N 系列）**：

| 类别 | 条数 | 说明 |
|---|---|---|
| 已被 Table A/B/C 现有条目覆盖（标题/规则可对应到已有编号） | **49** | 含本轮新复原细节的 A2/A11/A14/A18/A22/A30、已知的 A3/A7/A9/A12/A21/A23/A25/A26/A34/A37/B6，以及已被 Table C 记录的 C6/C7/C8/C9/C12/C27 |
| Data Scientist/DA 岗 SQL 题（不在 Table A 的 SWE bespoke 编码题定义域内） | **6** | N-DS1，且置信度普遍偏低（同一候选人素材被套用到多个题目页） |
| 真正的孤儿/待核实新题（无法归入任何现有编号，且证据不足以独立立项） | **5** | N-1 find-linked-merchants、N-2 propagate-runtime-id、N-4 debug-validation-error-aggregation、N-5 debug-async-sdk-race、以及 `implement-multi-part-cost-calculator`（prachub 生成外壳，无法判断是否对应 A22/A26 已知题或全新题） |

即：**在 prachub 这个可穷举的结构化题库里，60 条 SWE 编码题中有 49 条（≈82%）已经能对应到 catalog 现有编号**，5 条（≈8%）是证据不足以独立立项的孤儿标题，6 条（10%）是 catalog 目前不覆盖的 DS/DA 赛道（如果目标岗位是 SWE，这 6 条不计入相关分母）。

**结合此前几轮的结论换算成"总体撞题概率"估计**：
- 若把分母限定在"prachub SWE 编码题"这个可验证的子集，本仓库题库对这个子集的**标题级覆盖率 ≈ 82%（49/60）**，已经达到甚至略超过用户的 80% 目标——但这只是"标题/主题对应"，不等于"规则细节完全一致"（本轮同时发现好几个已收录题目在 part 数、具体行为上有此前遗漏的细节，如 A18 的 part 数从 3 修正为 4）。
- 这个 82% 是**单一站点、单一时间点**的估计，不能外推到 teamblind/leetcode/1point3acres 覆盖的题目全集——例如 C13（Beta Invite）、C20（reddit 帖）这类题目完全不在 prachub 语料里，说明 prachub 本身也不是全集。
- 综合看，**80% 这个目标在"prachub 可枚举子集"上大概率能达到，但在"跨全部信息源的真实题库"上，仍然存在几个已知的结构性盲区**（1point3acres 全站不可达、reddit 全站不可达、medium 全站不可达），这些站点历史上贡献过 catalog 里不少 high 置信度条目（如 F1 的 1p3a thread-844359），当前抓取能力覆盖不到它们的**新增**内容,只能靠 WebSearch 摘要做存在性确认。**如实说：本轮没有能力把"总体撞题概率"精确量化到一个跨全信源的单一数字，只能给出 prachub 子集内的 82% 作为一个下限参考。**

---

## 失败的检索式

- `gotthamloop stripe interview questions`（WebSearch，0 相关命中——teamblind 一条评论提到"check gotthamloop for Stripe's bank"，疑似笔误或玩笑网站名，未能核实是否为真实站点，不采信）
- `site:leetcode.com/discuss stripe interview 2026`（WebSearch）——命中的帖子里有 2 个（7566910、7314171）的 GraphQL `post.content` 只返回占位符 `"article-topic"`，正文不可达；用 `topicComments` 只能拿到读者提问，无法定位/过滤出 OP 本人回复（`CommentNode` 类型上没有 `isOp` 字段，与批 B 的记录不一致，可能是 schema 版本变化或字段名需要重新探测）
- LeetCode GraphQL 帖子 ID `6896919`（来自 WebSearch 标题 "Stripe SDE OA + Interview Experience"）——`topic(id:6896919)` 返回 "That topic does not exist"，ID 可能是 WebSearch 摘要给出的错误/过期 ID
- `https://www.levels.fyi/companies/stripe/salaries/software-engineer/levels/l1/locations/bangalore-india` —— 返回 200 但地区未填充数据，未能复核 LOOP_GUIDE 里的印度薪酬数字
- interviewdb.io `page=4` 及以上 —— 空列表，确认列表在 37 条处到底，未发现新增标题（含此前 batch B 已确认不存在的 "incident-monitor"、"rbac-role-resolver" 独立词条）
- prachub.com `/companies/stripe?page=7` 及以上 —— 404，确认列表到 page 6 结束

---

## 来源登记（供 SOURCES.md）

| 站点 | URL 模式 | 类型 | 本次是否可访问 | 关键方法论备注 |
|---|---|---|---|---|
| prachub.com | `/companies/stripe?page=1..6`、`/coding-questions/<slug>`、`/interview-questions/<slug>`、`/interview-experiences/<slug>` | 题库 + 候选人转载 + 长文面经 | 是（curl 直接可用，无需登录） | **关键**：候选人原文藏在 `console_solution_locked":true,"content":"<原文>","content_enhanced"` 这个字段序列里；若 `content` 是 `""` 或 `"$NN"` 占位引用，则该页正文全部来自 prachub 自己生成的 `content_raw`/`data-seo-content` 外壳，不能当候选人原文引用。`/interview-experiences/` 是三篇独立的长文面经（本轮全部读完），信息密度高于短题目页 |
| interviewdb.io | `/question/stripe?page=1..4` | 题库标题列表 | 是（列表页；详情页仍是占位符） | 37 条标题已确认到底（page4 空），本轮无新增 |
| teamblind.com | `/search/<query>`、`/post/<slug>` | 论坛 | 是（curl + 浏览器 UA 直接 200，正文/评论嵌在 Next.js RSC payload 里） | `/search/` 端点可用不同关键词组合（如 `stripe oa`、`stripe onsite`）得到不同结果集，非单一"stripe"能覆盖全部；评论字段用 `\\"text\\":\\"..."` 定位 |
| leetcode.com/graphql | `POST /graphql`，`query{topic(id){title post{content contentPreview}}}`、`query{topicComments(topicId){data{id post{content}}}}` | API | 是（`topic`/`topicComments` 两个字段可用；`CommentNode` 上目前测不出 `isOp` 字段，需要下次重新探测 schema） | 部分帖子（尤其标题含"Interview Experience"的长文类）的 `post.content` 只返回占位符 `"article-topic"`，本环境暂无找到读取其正文的方法 |
| levels.fyi | `/companies/stripe/salaries/software-engineer`、`/levels/{l1,l2,l3}` | 薪酬数据 | 是（curl 直接 200，`og:description` meta 标签里有官方口径的中位数总包） | 地区细分 URL（如 `/locations/bangalore-india`）本轮测试未返回有效数据，格式或数据量可能不满足展示条件，需要下次换 URL 结构重试 |
