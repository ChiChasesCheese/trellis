---
id: aie-excessive-agency
node: t06.excessive-agency-least-privilege
type: qa
step: 1
tags: [摘要]
---
## Q
**Excessive agency 与 least privilege**｜摘要 · 必会

一个"只读文档摘要"的 agent，被注入后居然删了文件。从权限设计看，问题可能出在哪三个地方？

## A
**Excessive Agency（OWASP LLM06）：** LLM 系统被授予的能力过大，在收到意外、模糊或被操纵的输出（幻觉、注入、被攻陷的插件）后，能做出有破坏性的动作。三个根因：

| 根因 | 例子 |
|---|---|
| **Excessive functionality**（功能过多） | 只需要读文档的扩展，同时能修改、删除文件；已停用的扩展还留着 |
| **Excessive permissions**（权限过大） | 只读的 tool 却用能写能删的数据库账号连接；按用户的 tool 却用一个通用高权限账号 |
| **Excessive autonomy**（自主性过大） | 高影响动作（删用户文档）没有确认就执行 |

**least privilege（最小权限）的做法：**
- 最小化 agent 能调用的 tool 数量，每个 tool 只实现需要的功能；
- 避免开放式 tool（通用 shell、任意 URL 访问），用粒度细的；
- 最小化 tool 在下游系统上的权限；**以具体用户的身份**、用该用户的最小权限执行；
- 高影响动作要求人工批准；
- **complete mediation：** 由**下游系统自己授权**每个请求，不依赖 LLM 的判断；
- **读与写分离：** 读用只读凭据，写走另一条受控通道。

**注：** 日志、监控、限流不能阻止 excessive agency，但能限制损害。

<details class="pt" markdown="1"><summary>出处</summary>

OWASP LLM06:2025 Excessive Agency（https://genai.owasp.org/llmrisk/llm062025-excessive-agency/）；Huyen《AI Engineering》ch5 §System-level defense

</details>
