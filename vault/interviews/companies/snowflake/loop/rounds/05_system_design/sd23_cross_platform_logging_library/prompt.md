# Cross-Platform Logging Library（跨平台日志库）

公司有很多种客户端和服务：Java 和 Go 写的后端、Python 写的数据工具、C++ 写的查询引擎、还有跑在客户机器上的驱动程序（JDBC / ODBC / Python connector）。每个团队都有自己的日志写法，格式不统一，排查一个跨服务的问题要在五种格式里找。请你设计一个**跨平台日志库**：各语言调用方式一致（级别、结构化字段、上下文传播），日志能统一送到中心平台检索。约束：库不能拖慢业务线程（查询引擎的热路径对延迟非常敏感）；中心平台不可用时不能让应用崩溃或内存无限增长；客户机器上的驱动日志可能包含 SQL 文本和凭据，要能脱敏；需要能在不重新发布应用的情况下临时调高某个模块的日志级别；日志量高峰时可能每台机器每秒十万条。请设计这个库以及它和中心平台的交互。

---

**面试环境说明**：Snowflake 技术电面或 onsite 的 System Design 轮，45–60 分钟。偏"库设计 + 客户端侧可靠性"，不是设计 Elasticsearch。

**题目原始报告与来源**：
- **MED-LOW（单一聚合站，有日期）**：TrueInterview "Cross-Platform Logging Library"（System Design，Medium，2026-03-23）。见 `../../../catalog/raw/github_repos.md` §2 第 32 行。题面付费，可见部分只有标题。
- 题面中的语言清单、驱动脱敏、动态调级、吞吐数字全部为 **(reconstructed)**。
- 与 Snowflake 的关系 **[推断]**：Snowflake 驱动有 `tracing` 级别参数与客户端日志文件；Snowflake 自身提供 Event Tables（`SYSTEM$LOG`、OpenTelemetry 兼容的日志 / 追踪）。
