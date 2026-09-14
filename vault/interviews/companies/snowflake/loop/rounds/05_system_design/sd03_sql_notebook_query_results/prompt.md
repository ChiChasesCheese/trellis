# SQL Notebook / 查询结果分发

我们要给用户做一个类似笔记本（notebook）的界面，用户可以在里面写 SQL 查询然后运行——你可以把它想成一个运行 SQL 的交互式环境，而不是一次性批处理。用户点击"运行"之后，这条查询可能几百毫秒就跑完，也可能跑几分钟甚至更久，取决于数据量和查询复杂度，所以前端不能傻等一个 HTTP 请求几分钟不返回。查询跑完之后，结果集可能很小（几行），也可能非常大（几百万行），notebook 前端不可能也不应该一次性把几百万行都塞进浏览器内存里渲染。同时，这个系统是给一个团队甚至一个组织共用的，会有很多用户同时在各自的 notebook 里跑各自的查询，大家共享底层的计算资源（可以类比成一个查询排队等待被计算集群执行的模型），我们既要让大家公平地排上队，也不能让一个用户的超大查询把其他人的小查询卡死很久排不上。请设计支撑这套 notebook 体验的后端系统：从用户提交查询、系统安排执行、用户轮询或者被通知查询状态、到最终把（可能很大的）结果集分批展示给用户。

---

**面试环境说明**：这是 Snowflake 技术电面 System Design 轮的一部分（常与另一轮 coding 组成"两轮 back-to-back 各 60 min"结构），时长 45–60 分钟。白板工具未证实；面试官风格两极分化，需要按"可能没有引导"的假设去准备，主动暴露设计里的假设与边界条件。

**题目原始报告与来源**（置信度见 `catalog/raw/system_design.md` §1.3）：
- **一手（电面 SD，两轮 back-to-back 之一，高置信度）**：题面为 "a notebook similar to SQL that supports users running queries"，讨论重点是 **client 如何拿到查询结果**（长查询的轮询/推送、结果分页、大结果集的流式返回）—— 1p3a thread-1187965，经 Telegram 镜像读到（**高**，复用 `../../raw/process_research.md` §3.2 #6）。
- **新增一手**：另一条 2026 全职 fullstack 电面报告标题为 "System Design: SQL notebook interface"，与同场 coding 轮（一道 React/TypeScript Kanban 板题）一起出现（**高**，日期/结果未知，仅摘要，正文 403）。
- **聚合站对应题**："Design an Interactive Query Execution Notebook"，题面 "Design a notebook-like service in which users submit SQL queries and receive results"，PracHub 标注 42 人做过（**低**，但与两条一手报告的题面高度吻合，可信度上调为可参照真题）。
- 该题族三条独立来源，整体置信度 **HIGH**。追问汇总（原文已给出）：长查询的异步执行模型（submit → poll status → fetch result）、结果集过大时的分片/流式传输、多用户共享 notebook 的并发编辑/执行隔离、查询排队与仓库资源调度的关系（可联系 Snowflake 真实的 virtual warehouse 排队机制）。
