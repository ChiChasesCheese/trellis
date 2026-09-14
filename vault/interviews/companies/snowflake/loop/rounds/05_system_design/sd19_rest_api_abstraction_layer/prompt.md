# REST API Abstraction Layer / Internal Service-Client SDK（REST API 的 RPC 抽象层）

公司内部有几十个后端服务，每个都暴露自己的 REST/JSON 接口：鉴权方式不一样（有的要 OAuth token、有的要内部签名），分页方式不一样（有的用 offset、有的用 cursor），错误格式不一样，限流返回 429 的时机和 `Retry-After` 语义也不一样。现在每个调用方团队都在手写 HTTP 调用，重复写重试、超时、日志，出了问题很难追踪。请你设计一个**抽象层**：调用方写 `billing.getInvoice(id)` 这样像本地函数一样的 RPC 调用，底下由这一层把它翻译成正确的 REST 请求，并统一处理鉴权、重试、超时、分页、错误和可观测性。要支持 Java、Python、Go 三种调用方语言；后端服务会不断增加新接口、偶尔做不兼容的改版；有些调用是写操作（比如扣费），不能因为重试被执行两次。请设计这个系统。

---

**面试环境说明**：Snowflake 技术电面或 onsite 的 System Design 轮，45–60 分钟。可能偏"库 / SDK 设计"而非大规模分布式——先问清楚面试官想要客户端库、网关，还是两者。

**题目原始报告与来源**：
- **MED（两个聚合站独立收录，无一手正文）**：
  - PracHub "REST API Abstraction Layer" / "Internal Service-Client SDK"（Hard，258 人做过，2026-04-05）。见 `../../../catalog/raw/system_design.md` §3。
  - TrueInterview "Design an RPC Abstraction Layer for REST APIs"（System Design，Medium，2026-05）。见 `../../../catalog/raw/github_repos.md` §2 第 22 行。
- 题面细节（多语言、不兼容改版、写操作幂等）为 **(reconstructed)**，依据两个标题的共同核心。
- 与 Snowflake 的关系 **[推断]**：Snowflake 的 connectors / drivers（JDBC、ODBC、Python、Go）本身就是"同一协议、多语言客户端"的问题；内部 control plane 服务之间也有大量 REST 调用。
