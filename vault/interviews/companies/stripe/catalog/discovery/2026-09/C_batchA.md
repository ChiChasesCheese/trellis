# Table C 二轮排查 · 批 A（2026-09-03）

对象：C1 Observability · C4 Factory Cost · C6 User Roles / RBAC Role Resolver · C7 Matching Contacts。
访问日期统一为 **2026-09-03**（下表不再逐条重复标注，除非另有说明）。

---

## 检索方法与覆盖面

**跑过的检索式（节选，完整列表见各条目"失败的检索式"）**
- `Stripe "Observability" interview OA HackerRank` / `site:1point3acres.com Stripe Observability` / `1point3acres stripe "Observability" OA 题` / `1point3acres stripe OA "监控" OR "告警" OR "日志"` / `leetcode discuss stripe "metrics" OR "logging" OR "tracing" OR "alerts" OA 2026`
- `Stripe "Factory Cost" interview question phone screen` / `Stripe "Factory Cost" leetcode OR blind OR glassdoor` / `site:1point3acres.com Stripe "Factory Cost"` / `stripe "factory" cost calculation manufacturing interview coding problem` / `prachub.com stripe factory cost` / `stripe "distance penalties" factory cost dynamic programming interview`
- `Stripe "RBAC" OR "Role Resolver" interview coding question` / `Stripe "User Roles" phone screen interview onsite coding` / `1point3acres 题库 stripe "RBAC" 角色` / `"design and implement a Role-Based Access Control" stripe hierarchical account structure interview` / `stripe interview "resolve_role" OR "RoleResolver" github` / `stripe "effective permissions" account hierarchy roles interview coding`
- `Stripe "Matching Contacts" interview email domain preferences` / `"reading speed is the main constraint" stripe interview` / `"Matching Contacts by Email Domain and Preferences" stripe` / `github stripe interview "matching_contacts" OR "linked_user" OR "record_linking"`
- 站点定向遍历：`interviewdb.io/question/stripe/<slug>`（逐个猜测 factory-cost / observability / user-roles / matching-contacts / rbac-role-resolver）；`prachub.com/questions?company=Stripe&page=1..6`（全部 117 条题目标题过了一遍关键词）；GitHub 代码搜索式 `resolve_role`、`role_resolver`、`factory_cost`、`observability`、`matching_contacts`、`linked_user`、`record_linking` + stripe。

**站点可访问性**
- **interviewdb.io**：可通过 WebFetch 抓取，但题目详情页是纯前端渲染（React/SPA），WebFetch 拿到的是加载占位符（"Loading practice workspace…" / "No questions are available yet"），只能确认标题、stage 标签（Coding/OA、Coding/Phone…）、相对更新时间是真实存在的，**拿不到题面正文**。逐个 slug 验证：`/question/stripe/factory-cost`、`/question/stripe/observability`、`/question/stripe/user-roles`、`/question/stripe/matching-contacts`、`/question/stripe/rbac-role-resolver` 均返回同款占位页（前四个页面 `<title>` 与目标标题完全匹配，确认页面真实存在；`rbac-role-resolver` 这个 slug 本身不存在，会重定向到总列表页——即 interviewdb 上并没有单独叫"RBAC Role Resolver"的题，那个标题只出现在 1point3acres）。
- **1point3acres.com**：全站对 WebFetch 返回 **403 Forbidden**（`/interview/problems/post/*`、`/bbs/thread-*` 均如此），本批次未能直接抓取正文，只能依赖 WebSearch 返回的标题/URL 做存在性确认；WebSearch 附带的"摘要"多次出现明显是**搜索引擎自己的通用释义**（例如把"RBAC Role Resolver"这个标题套上一段通用 RBAC 教科书式描述），**不可采信为原文**，本报告中凡引用 1p3a 内容一律标注为"标题确认，正文未获取"。
- **prachub.com**：可通过 WebFetch 正常抓取，且**部分题目正文是完全公开的**（含 part 划分、函数签名、样例），另一部分题目页面本身也是异步加载 + 登录墙，只能拿到自动生成的一句话 "Quick Overview"。本批次把 `prachub.com/questions?company=Stripe` 的全部 6 页 / 117 条标题过了一遍关键词匹配，抓到了 4 条与目标高度相关的题目（见下）。
- **web.archive.org**：工具层直接拒绝该域名（"Claude Code is unable to fetch from web.archive.org"），无法用于绕过 1p3a 的 403。
- **csoahelp / programhelp / oavoservice / linkjob / interviewfox / extrabrain**：多轮搜索均未命中与本批 4 题相关的内容（搜索结果里出现的是这些站点关于其他题目——Shipping Cost、KYC、Fraud Detection 等——的既有报道，catalog 里已收录）。
- **lodely.com / vervecopilot.com**：本批检索中两次自动出现在结果里（都市泛用的"Top 30 Stripe interview questions"列表），内容与 catalog 判定一致——**AI 生成题目农场，排除**，未作为证据使用。
- **teamblind / reddit / leetcode discuss**：全文搜索未命中 Observability / Factory Cost / RBAC / Matching Contacts 任一关键词的独立报告。

---

## C1 · Observability

- **结论**：**完全没有**题面，仅标题存在性得到二次确认（直接访问 interviewdb.io 详情页），未发现任何新的第三方来源。

- **证据**：

| 来源 URL | 访问日期 | 原文摘录 | 置信度 |
|---|---|---|---|
| https://www.interviewdb.io/question/stripe/observability | 2026-09-03 | 页面 `<title>`："Observability \| Stripe Interview Question \| InterviewDB"；正文区域仅有 "No questions are available yet" / "Loading practice workspace..." 占位符 | high（确认标题真实存在）／题面本身 0 |
| https://www.interviewdb.io/question/stripe（列表页） | 2026-09-03 | 未在本次抓到的列表片段中出现"Observability"这一行（列表按字母序分页，抓到的片段止于 F 开头），说明该条目在更靠后的分页——与 catalog 已有 "reported Aug 2026" 的记录一致 | medium |

- **可复原的题面要素**：
  - 规则：未知
  - 输入格式：未知
  - 输出格式：未知
  - part 划分：未知
  - 阶段：OA（interviewdb 标签为 Coding，具体 OA/Phone 无法在本次抓取中确认——之前 catalog 记录为 OA，这次未看到该行的 stage 标签，无法证伪或证实）

- **若要重建成训练题，应覆盖的知识点**（推测性，因为没有任何规则文本，只能按"Observability"这个域名做合理猜测）：对照 skills_matrix.md，如果这题走 Stripe 一贯的"事件流 + 聚合 + 阈值告警"套路，大概率会覆盖 **S02**（行式解析）、**S04**（group-by 聚合）、**S05**（阈值语义）、**S10**（事件流处理）、**S12**（时间桶/窗口）、**S24**（可观测性域知识：metrics/labels/alert）。这与本次在 PracHub 上找到的同域系统设计题《Design a Count-Metrics Monitoring Platform》（见"新发现"）的关键词高度吻合，但那是 onsite 系统设计题，不能替代这条 OA 题的题面——只能作为"这题大概率长什么样"的旁证，**不能当作 C1 已解决**。

- **失败的检索式**：`Stripe "Observability" interview OA HackerRank`、`Stripe interviewdb.io Observability question`、`site:1point3acres.com Stripe Observability`、`1point3acres stripe "Observability" OA 题`、`1point3acres stripe OA "监控" OR "告警" OR "日志"`、`leetcode discuss stripe "metrics" OR "logging" OR "tracing" OR "alerts" OA 2026`、`stripe OA 2026 "alert" OR "metric" OR "dashboard" parsing coding hackerrank`、`github stripe interview questions "observability"`、`csoahelp stripe observability OR factory cost OR RBAC`、`darkinterview.com stripe factory cost OR observability OR rbac OR "user roles"`、`oavoservice.com stripe factory OR observability OR role`、`site:prachub.com stripe observability`。

---

## C4 · Factory Cost

- **结论**：**只找到部分线索**——比 catalog 现状（纯标题）前进了一步：确认了阶段、大致时间、算法类型和一句话主题，但仍未拿到规则文本/函数签名/样例。

- **证据**：

| 来源 URL | 访问日期 | 原文摘录 | 置信度 |
|---|---|---|---|
| https://www.interviewdb.io/question/stripe/factory-cost | 2026-09-03 | 页面 `<title>`："Factory Cost \| Stripe Interview Question \| InterviewDB"；列表页对应行标签为 "Coding/Phone · 1 month ago" | high（标题+阶段确认）／题面 0 |
| https://prachub.com/interview-questions/minimize-total-factory-cost-with-distance-penalties | 2026-09-03 | "This question evaluates dynamic programming and sequence optimization skills, focusing on modeling cumulative build costs with adjacency distance penalties and handling variants such as skipping a factory." （这是 PracHub 自动生成的 "Quick Overview" 一句话简介，页面正文本身需登录/未加载完成，规则、函数签名、样例均未展示） | medium（confirms 存在同域题目，日期 2026-03-29 最后更新，Technical Screen＝Phone，Medium 难度；但这条题目标题与 C4 不完全相同，是否为同一题需要人工登录 PracHub 核实） |
| https://www.1point3acres.com/interview/problems/post/7100090（"Factory Cost Optimizer"） | 2026-09-03 | 标题通过 3 次独立 WebSearch 结果重复命中同一 URL+标题，确认页面真实存在；但 1p3a 全站对 WebFetch 返回 403，抓不到正文。WebSearch 自带的"supply chain optimization system for a manufacturing company"一句话描述判断为**搜索引擎自身生成的泛化释义，非页面原文**，不采信 | low（仅标题存在性）|

- **可复原的题面要素**：
  - 规则：部分已知——PracHub 概述提示这是"累计建厂成本 + 相邻工厂距离惩罚 + 可跳过某个工厂"的动态规划题（类似 House Robber / 状态转移带"跳过"选项的变体），但具体的成本公式、距离惩罚公式、"跳过"的约束条件均未知
  - 输入格式：未知
  - 输出格式：未知
  - part 划分：未知（PracHub 单独归类为一道题，未标注 part 数）
  - 阶段：**Phone / Technical Screen**（interviewdb 与 PracHub 两个独立来源一致）
  - 时间：interviewdb "1 month ago"（相对 2026-09 抓取即约 2026-08）；PracHub 页面 "last updated 2026-03-29"——两个日期不一致，可能是同一题的不同轮报告，也可能是两道不同的"Factory Cost"题（PracHub 标题是"Minimize total factory cost with distance penalties"，与 interviewdb 的裸标题"Factory Cost"、1p3a 的"Factory Cost Optimizer"并非逐字相同），**未能确证三者是同一题**，只能说主题高度重合。

- **若要重建成训练题，应覆盖的知识点**：如果 PracHub 概述准确，这题核心是"线性序列上的动态规划 + 相邻惩罚项 + 允许跳过一个决策点"，在 skills_matrix.md 的 S/A 编号里**没有精确对应项**——最接近的是 **A10**（LC 465 类最小成本 DP／DFS 剪枝）思路，但那是图上匹配而非线性序列 DP；建议将其视为新增算法模式（类似 LC 198 House Robber 或 LC 91 Decode Ways 的"跳过一步"变体）补进 Table B/skills_matrix，同时覆盖 **S06**（金额用整数分/取整）、**S08**（结果排序/去重—如果有多组查询）。

- **失败的检索式**：`Stripe "Factory Cost" interview question phone screen`、`Stripe "Factory Cost" leetcode OR blind OR glassdoor`、`site:1point3acres.com Stripe "Factory Cost"`、`stripe "factory" cost calculation manufacturing interview coding problem`、`prachub.com stripe factory cost`、`site:prachub.com stripe factory`、`prachub.com "minimize-total-factory-cost-with-distance-penalties"`（Google 未索引该 URL）、`stripe "distance penalties" factory cost dynamic programming interview`、`github stripe interview "factory_cost" OR "FactoryCost"`。

---

## C6 · User Roles / RBAC Role Resolver

- **结论**：**只找到部分线索**——两个独立站点（1point3acres、PracHub）各自收录了一道"账户层级 + 角色/权限解析"题，标题不完全相同但主题高度一致，时间点集中在 2026 年上半年；仍未拿到规则文本/函数签名/样例。

- **证据**：

| 来源 URL | 访问日期 | 原文摘录 | 置信度 |
|---|---|---|---|
| https://www.interviewdb.io/question/stripe/user-roles | 2026-09-03 | 页面 `<title>`："User Roles \| Stripe Interview Question \| InterviewDB"；正文占位符同 C1（"No questions are available yet"） | high（标题存在性）／题面 0 |
| https://www.interviewdb.io/question/stripe/rbac-role-resolver | 2026-09-03 | 该 slug 不存在独立页面，请求被重定向/回落到通用列表页标题 "Stripe Interview Questions (Updated Aug 2026)"——说明 interviewdb 上没有单独的"RBAC Role Resolver"词条，这个标题只在 1point3acres 出现 | high（证伪：RBAC Role Resolver 并非 interviewdb 词条，catalog 里 C6 的 "interviewdb.io" 来源标注需要修正为仅 "User Roles"，"RBAC Role Resolver" 应只归 1p3a） |
| https://www.1point3acres.com/interview/problems/post/7100148（标题 "RBAC Role Resolver"） | 2026-09-03 | 标题通过多次独立 WebSearch 命中同一 URL 确认存在；1p3a 全站 403，正文未获取。WebSearch 自带描述"design and implement a Role-Based Access Control (RBAC) system that manages user roles across a hierarchical account structure"判断为**搜索引擎泛化释义**（措辞与教科书式 RBAC 介绍高度雷同，且搜索工具自己也承认"完整内容未被抓到"），不采信为原文 | low（仅标题存在性）|
| https://prachub.com/coding-questions/resolve-user-roles-across-account-hierarchy | 2026-09-03 | "This question evaluates understanding of hierarchical data structures, role-based access control semantics, and set/map operations for computing effective permissions across account ancestors."（PracHub 自动生成的 Quick Overview；正文因登录墙/异步加载未获取，多次重试均同样结果） | medium（confirms 独立于 1p3a 之外，PracHub 上也有一道同主题题目：Software Engineer / Coding & Algorithms / Medium / **Technical Screen（Phone）** / 发布日期 **2026-05-12**）|

- **可复原的题面要素**：
  - 规则：部分已知——两个来源共同指向"账户存在层级关系（父子账户），要计算某账户在层级链上的**有效权限**（ancestors 的角色/权限并集或覆盖规则）"，属于树形结构 + 集合运算题，但具体的角色定义、覆盖优先级（子账户角色是否覆盖父账户角色？取并集还是就近覆盖？）、输入输出格式均未知
  - 输入格式：未知
  - 输出格式：未知
  - part 划分：未知
  - 阶段：**Phone / Technical Screen**（PracHub 明确标注；interviewdb 侧标签未在本次抓取片段中看到）
  - 时间：PracHub 2026-05-12；1p3a 侧时间未知（catalog 原有的 "1p3a 题库" 来源仍是标题级）

- **若要重建成训练题，应覆盖的知识点**：对照 skills_matrix.md，若题干确如两处概述所述，核心应覆盖 **S03**（把账户/角色建模为记录+字典）、**S08**（层级遍历的确定性顺序）、**A16**（并查集/连通分量的近亲——但这里更可能是树的祖先链而非无向图，需要新增"树形祖先聚合/权限继承"这一模式，目前 A01–A16 里没有精确对应项）；如果覆盖规则涉及"多个角色取权限并集"，还会用到 **S04**（分组聚合）思路。建议后续标注为"待补充 A17：层级权限继承（tree ancestor aggregation）"。

- **失败的检索式**：`Stripe "RBAC" OR "Role Resolver" interview coding question`（仅返回标题）、`Stripe "User Roles" phone screen interview onsite coding`、`1point3acres 题库 stripe "RBAC" 角色`、`"design and implement a Role-Based Access Control" stripe hierarchical account structure interview`、`stripe interview "resolve_role" OR "RoleResolver" github`、`stripe interview "resolveRole" OR "role_resolver.py" OR "role_resolver.java"`、`stripe "effective permissions" account hierarchy roles interview coding`、`stripe teamblind "role" access control interview coding`、`programhelp.net stripe factory OR observability OR role OR RBAC`、`linkjob.ai stripe "user roles" OR "RBAC" OR "role resolver"`、`prachub.com "resolve-user-roles-across-account-hierarchy"`（Google 未索引该 URL）。

---

## C7 · Matching Contacts

- **结论**：**找到高置信度的完整题面**（三部分规则、权重数值、函数输入均已复原），比 catalog 现有的 en_forums.md §24（medium 置信度、来自 linkjob 的转述）更进一步——这次是从 PracHub 直接抓到的结构化题面原文，且同一题在 PracHub 上出现了**两次独立报告**（2026-06-21 与 2026-07-08），时间点与 1point3acres 题库记录的"phone screen, last asked 2026-06-10"高度吻合，三方互相印证。

- **证据**：

| 来源 URL | 访问日期 | 原文摘录 | 置信度 |
|---|---|---|---|
| https://prachub.com/coding-questions/find-linked-user-records-by-similarity | 2026-09-03 | "For each field among {name, email, company}: If A.field == B.field (string equality), add weights[field] to the score." / "This question evaluates the ability to compute weighted field-based similarity and reason about adjacency relationships in an undirected graph" | **high**（结构化题面，含函数输入 rows/weights/threshold/target_user_id，权重 name=0.2 email=0.5 company=0.3，与 en_forums.md §24 的转述数值完全一致；Software Engineer / Technical Screen(Phone) / Medium / 发布 2026-06-21） |
| 同上（Part 1 引用） | 2026-09-03 | "return all record IDs directly linked to the target's record. The result must not include target_user_id itself." | high |
| 同上（Part 3 引用） | 2026-09-03 | "return all record IDs in the same connected component as the target — every record reachable from the target by any number of edges" | high |
| https://prachub.com/coding-questions/find-linked-user-records-by-weighted-similarity | 2026-09-03 | 同一主题的第二次独立报告，"Last updated: Jul 8, 2026"，同为 Technical Screen / Medium | high（时间上早于/接近 1p3a 记录的 "last asked 2026-06-10"，属独立第二次复现，佐证题目在 2026 年年中反复出现） |
| https://www.interviewdb.io/question/stripe/matching-contacts | 2026-09-03 | 页面 `<title>` 确认标题存在，正文占位符同 C1 | medium（仅确认"Matching Contacts"这个具体措辞的标题也独立存在于 interviewdb，与 PracHub 的"Find linked user records by (weighted) similarity"标题不同但规则相同——说明同一道题在不同聚合站上被起了不同的名字） |
| catalog/raw/en_forums.md §24（已有，本次复核） | 2026-09-03 | "Rows of users {id, name, email, company}; field weights name 0.2, email 0.5, company 0.3; threshold 0.5; two records linked if sum of weights of matching fields ≥ threshold." | high（与 PracHub 抓到的原文数值一致，互相印证，非重复计数） |

- **可复原的题面要素**：
  - 规则：**已知**——字段完全相等（字符串比较）时按权重累加分数，总分 ≥ threshold 判定两条记录"直接关联"（无向）
  - 输入格式：**已知**——`rows`（含 id/name/email/company 的记录列表）、`weights`（字段→权重字典）、`threshold`（0–1 浮点数）、`target_user_id`
  - 输出格式：**已知**——返回满足条件的记录 id 列表，升序排列，不含 target 自身
  - part 划分：**已知**——3 part：Part 1 直接关联（一跳）；Part 2 间接关联（≤2 跳，即经过一个中间节点）；Part 3 完整连通分量（任意跳数的传递闭包）
  - 阶段：Phone / Technical Screen（两个 PracHub 独立报告 + 1p3a 题库一致）
  - 样例：已知（Part 1/2/3 各有具体数字样例，如 "记录1和2共享 email+company（0.8≥0.5）→答案[2]"），但 PracHub 页面对"逐字段完整原始表格数据"的转述受工具引用长度限制（每次引用≤125字符），本报告只保留了摘要值，未逐字抄录全部原始记录表——如需精确复现建议人工访问该 URL 截取完整表格。

- **若要重建成训练题，应覆盖的知识点**：对照 skills_matrix.md 与已有 `q18_collusion_ring`（A9），这题本质是 **A16**（并查集/连通分量）+ **S03**（记录建模为字典）+ **S04**（按权重加权聚合评分）+ **S08**（结果排序）的组合，与 A9 Six Degrees of Collusion 是近亲，可以直接复用 q18 的框架改造字段和评分函数，风险点在于 Part 2 的"≤2 跳"边界条件（是否含 target 直接邻居、是否去重）需要靠拿到的样例校验。

- **失败的检索式**（这条整体是成功的，仅记录走过的弯路）：`Stripe "Matching Contacts" interview email domain preferences`（无结果）、`"Matching Contacts by Email Domain and Preferences" stripe`（无结果，命中的都是 Stripe 官方邮件文档）、`site:1point3acres.com Stripe "Matching Contacts"`（只返回列表页，未展开）、`github stripe interview "matching_contacts" OR "linked_user" OR "record_linking"`（未命中独立仓库，但间接印证了 linkjob 已有转述）。

---

## 新发现的、Table C 里没有的 Stripe 题

排查 PracHub 全站 117 条 Stripe 标题时，撞见了几条 catalog 完全没有收录、且**拿到了较完整题面**或强证据的题目，价值较高，逐条记录：

### N1 · Bitfont / 位图字体渲染（对应 catalog C27 "Bitfont Renderer" 的实锤题面）
- **来源**：https://prachub.com/coding-questions/convert-bitmap-into-ascii-characters ｜ 访问 2026-09-03
- **阶段**：Onsite ｜ 难度 Medium ｜ 发布日期 2026-03-29
- **原文摘录**：
  - "Render the given text by placing glyphs side-by-side, inserting exactly one '.' column between adjacent characters"
  - "Return the rendered result as a list of height strings (top to bottom)"
  - "Interpret each glyph's bitstring in row-major order: rows of length width, from top to bottom"
- **题面**：字体是字符→"row-major bitstring"的映射（`1`→`#`，`0`→`.`），给定待渲染文本（长度≤10000）和 width/height（各 1–32），把每个字符的字形横向拼接、字符间插入一列 `.` 作为分隔；空格是全 `.` 的空白字形；非空格字符缺失或比特串长度不对要抛 `ValueError`。
- **置信度**：high（结构化题面，字段/异常条件完整）
- **建议**：这基本可以直接当作 catalog C27 的题面来源，建议在下一轮把 C27 从"title only"提升为有陈述的条目，`problems/` 下可新增 `q4x_bitfont_renderer`。

### N2 · Design a Superhero (Incident) Dispatch System（全新的 onsite 系统设计题）
- **来源**：https://prachub.com/interview-questions/design-a-superhero-dispatch-system （2026-02-12 报告）与 https://prachub.com/interview-questions/design-a-superhero-incident-dispatch-system （2026-05-31 报告，同一题的第二次独立报告）｜ 访问 2026-09-03
- **阶段**：Onsite 系统设计 ｜ 难度 Medium
- **原文摘录**："This question evaluates system design and distributed systems competencies, including geospatial indexing, real-time location ingestion, low-latency matching algorithms, stateful trip lifecycle management, scalability, and fault tolerance."
- **题面梗概**：设计一个"超级英雄救援调度"后端——类似 Uber/Lyft 的地理匹配+派单，但请求量远低于打车平台、可靠性权重远高于吞吐量（"a dropped or double-assigned emergency is a much worse failure than a dropped ride request"）；需要覆盖 civilian/hero/incident/offer/assignment 数据模型、按半径查询 hero 位置与可用性、事件状态机、并发抢单的一致性控制、通知/超时/重试、可观测性。
- **置信度**：medium-high（两次独立报告，主题描述具体且一致；不是本次任务的 4 个目标，纯属排查中撞见）
- **建议**：加入 Table C 或直接建 Table 的"系统设计"分区。

### N3 · Design a Count-Metrics Monitoring Platform（与 C1 Observability 主题相邻，但是 onsite 系统设计，非 OA）
- **来源**：https://prachub.com/interview-questions/design-a-count-metrics-monitoring-platform ｜ 访问 2026-09-03 ｜ 发布 2026-08-09
- **原文摘录**（中文转述，工具引用长度限制未能拿到完整英文长句）：生产者发出带时间戳和标签的事件（如 `request_completed`），需支持按时间窗口查计数/速率、按标签分组、设置阈值告警；明确约束"不能丢失已确认事件，但允许短暂查询延迟"。
- **置信度**：medium（confirms Stripe 面试确实有"metrics 监控平台"主题，但这是 onsite 系统设计题，与 C1 标注的 OA 阶段不是同一道题，只能作为域名旁证）
- **另有同主题条目**：`design-a-distributed-metrics-counter`、`design-a-local-activity-counter-service`（均未详细抓取，仅确认标题存在）。

### N4 · Evaluate Ordered Access-Control Rules（与 C6 主题相邻，规则引擎类，非"角色层级"）
- **来源**：https://prachub.com/interview-questions/evaluate-ordered-access-control-rules ｜ 访问 2026-09-03 ｜ 发布 2026-09-02（**发布时间是本次抓取的前一天，非常新**）
- **阶段**：Technical Screen（Phone）｜ 难度 Medium
- **原文摘录**：
  - "Each rule is ACTION if EXPRESSION, where ACTION is ACCEPT or BLOCK. An expression contains boolean identifiers or integer comparisons joined by AND and OR; AND has higher precedence."
  - 函数签名：`evaluate_access_rules(rules: list[str], facts: list[list[str]]) -> str`
  - 样例：`rules=["ACCEPT if trusted_partner AND amount <= 10000", "BLOCK if amount > 10000"]`, `facts=[["trusted_partner","true"],["amount","12000"]]` → `"BLOCK"`
- **题面**：按顺序求值一组 `ACTION if EXPRESSION` 规则（布尔标识符或整数比较，AND 优先级高于 OR），facts 提供变量取值，返回第一条匹配规则的 ACTION，都不匹配则 `"NO_MATCH"`。
- **置信度**：high（结构化题面，含函数签名与两个完整样例）
- **备注**：这题和 catalog 里的 **A5 Radar Rule（`should_accept_transaction` 布尔规则语法）**是近亲/几乎同构，规则语法（AND/OR + 比较符 + ACCEPT/BLOCK）与 A5 高度重合；与 C6 的"角色层级/RBAC"主题不同（C6 是权限继承，这题是规则引擎），**不能当作 C6 的题面**，但因为标题含 "Access-Control" 容易与 RBAC 混淆，特此记录以免误用。

### N5 · 其他仅标题命中、与 Table A 已知题重复或轻微变体（供交叉引用，未展开抓取）
- `resolve-user-roles-across-account-hierarchy`（见 C6 正文）
- `minimize-total-factory-cost-with-distance-penalties`（见 C4 正文）
- `find-linked-user-records-by-weighted-similarity`（见 C7 正文）
- `propagate-runtime-id-across-api-requests`（新，疑似 debug/integration 轮的分布式 trace id 传递题，未抓取正文）
- `debug-an-asynchronous-sdk-race-condition-with-a-customer`（新，疑似 Bug Squash 轮变体）
- `generate-available-30-minute-time-slots`（新，排班/时间槽生成题，可能是 A13 部署窗口的近亲，未抓取）
- `implement-multi-part-cost-calculator`（新，标题过于通用，可能与 A22/A26 重复，未抓取）

---

## 来源登记（供 catalog/SOURCES.md 汇总）

| 站点 | URL | 类型（一手面经/题库/聚合站） | 本次是否可访问 | 建议复验周期 |
|---|---|---|---|---|
| InterviewDB | https://www.interviewdb.io/question/stripe 及各 `/question/stripe/<slug>` | 题库（众包标题+标签，正文需登录/付费或未上线） | 可访问，但正文是前端占位符，WebFetch 拿不到题面 | 每 4–6 周（标题列表会更新 "N ago" 标签） |
| 1point3acres 题库/面经 | https://www.1point3acres.com/interview/... | 一手面经 + 题库 | **403，WebFetch 全站不可访问**；只能靠 WebSearch 摘要做存在性确认 | 每次批次都需要重试（可能是临时 UA/风控问题，非永久性） |
| PracHub | https://prachub.com/companies/stripe 及各题目页 | 题库（部分题目公开完整正文，部分需登录） | 可访问，公开题目质量高（含函数签名/样例） | 每 2–4 周（本站更新频繁，本次抓到的 117 条里有 2026-09-02 发布的新题） |
| csoahelp / programhelp.net | 各篇文章 | 聚合站/代面经服务 | 可访问，但本批次 4 题均未命中新内容 | 常规月度复验即可 |
| darkinterview.com | 单题页 | 聚合站 | 本批次搜索未命中相关内容，未直接 WebFetch | 常规月度复验即可 |
| oavoservice.com | 单题页 | 聚合站/代面经服务 | 本批次搜索未命中相关内容 | 常规月度复验即可 |
| linkjob.ai / interviewfox.ai / extrabrain.app | 聚合文章 | 聚合站 | 可访问，本批次未命中新内容 | 常规月度复验即可 |
| lodely.com / vervecopilot.com | — | AI 生成题目农场 | **判定不可信，本批次已排除，未采信任何内容** | 不建议复验，除非重新评估可信度 |
| web.archive.org | — | 存档镜像（用于绕过 403 的备选方案） | **工具层直接拒绝该域名**，本环境不可用 | 不适用 |

---

## 总结（结论一览）

| 编号 | 结论 | 关键新证据 |
|---|---|---|
| C1 Observability | 未找到 | 仅二次确认标题存在（interviewdb 详情页），题面仍为 0 |
| C4 Factory Cost | 部分线索 | PracHub "Minimize total factory cost with distance penalties"（DP+距离惩罚+可跳过一个工厂，Phone，2026-03）+ 1p3a "Factory Cost Optimizer"（仅标题） |
| C6 User Roles / RBAC | 部分线索 | PracHub "Resolve user roles across account hierarchy"（账户层级+有效权限计算，Phone，2026-05-12）+ 1p3a "RBAC Role Resolver"（仅标题；确认 interviewdb 上没有独立的 RBAC 词条） |
| C7 Matching Contacts | **完整题面** | PracHub "Find linked user records by (weighted) similarity"（两次独立报告，2026-06-21 / 2026-07-08）：权重 name0.2/email0.5/company0.3、threshold、3 part（直接/≤2跳/连通分量），与 en_forums.md §24 数值完全吻合 |
