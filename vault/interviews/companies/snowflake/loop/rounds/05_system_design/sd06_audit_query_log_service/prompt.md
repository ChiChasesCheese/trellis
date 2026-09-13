# Audit / Query-Event Log Service（多租户、防篡改）

我们需要给平台上所有对数据资源的访问行为建一个统一的审计日志系统——每次有人查询、读取、修改了哪张表、哪个列，都要留下一条记录：谁、什么时候、访问了什么、做了什么操作。这个系统是多租户的，每个客户只能看到自己名下资源的审计记录，绝对不能看到别的客户的。审计日志这个东西的特殊之处在于，它本身要作为"出了问题时的证据"，所以必须做到**防篡改**——不能允许任何人（包括我们自己内部有权限的运维人员）事后偷偷改一条已经写入的记录去掩盖什么，写入之后就应该是不可变的。除了"谁访问过什么"这种正向查询，客户还经常会问一个相反方向的问题："过去 30 天里，我这些表/列里有哪些完全没有被任何人访问过？"——这是一个数据治理场景（找出可以下线或者需要重新审视权限的冷数据），这个反向查询和正向查询要用的索引结构完全不一样。最后，审计数据是持续产生、体量巨大的，不可能永久保留，需要有明确的保留策略——但同时又要满足一些客户的合规要求，某些审计记录可能要求保留数年。请设计这个 Audit / Query-Event Log Service。

---

**面试环境说明**：这是 Snowflake 技术电面或 onsite 的 System Design 轮，时长 45–60 分钟。白板工具未证实；面试官风格两极分化。这道题和一道 LC 212（Word Search II）coding 题在同一场 senior 电面里"二合一"出现过，说明这道题也可能出现在时间被压缩（coding + design 合并一轮）的场景，需要能在更短时间内讲清楚核心设计。

**题目原始报告与来源**（置信度见 `catalog/raw/system_design.md` §1.7）：
- **索引标题**：`../../raw/process_research.md` §3.2 #10 记录 1p3a 面经索引里的标题 "Design Audit Logs Service"（无法读到正文）—— 1point3acres.com（**中**，复用）。
- **聚合站细节**："Design an Audit Logs Service"，题面 "scalable, multi-tenant audit logging system, covering event storage"；另一独立描述该题族的评分点是 **"tamper-evident retention, and efficiency"** —— PracHub / WebSearch 摘要（**低-中**）。
- **同场出现**：LC 4727339（Word Search II 逐字）+ 审计日志设计，出现在 senior 电面的"二合一"场次（**高**，coding 部分逐字确认；SD 部分题面来自同一份记录）。
- **与 Snowflake 自身产品对照**：Snowflake 官方有内建的 `SNOWFLAKE` 共享数据库暴露审计信息，增量导出依赖时间戳列——本题很可能是这个真实痛点的简化版（**推断**，见 `01-company-brief.md` §1 治理相关内容）。
- 整体置信度 **MED-HIGH**。
