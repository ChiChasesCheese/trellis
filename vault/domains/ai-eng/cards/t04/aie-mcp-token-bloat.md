---
id: aie-mcp-token-bloat
node: t04.mcp
type: qa
step: 1
tags: [实践]
---
## Q
**MCP · 生产里的坑**｜实践 · 必会

团队给 agent 接了十几个 MCP server，一共几百个工具。上线后发现每次请求还没开始干活就用掉一大截 token，还时常选错工具。为什么？怎么改？

## A
**MCP（Model Context Protocol）：** 让 agent 以统一协议连接外部工具和数据源的开放标准。

**两个 token 问题（Anthropic 2025）：**
1. **工具定义占上下文：** 多数客户端一次把所有工具的定义全部载入；工具成千上万时，请求前就要处理几十万 token；
2. **中间结果穿过模型：** 例如把两小时会议转写从 A 系统搬到 B 系统，内容要经过模型两遍，约多 5 万 token。

**对策：**

| 办法 | 效果 |
|---|---|
| **code execution：** 把 MCP 工具写成代码 API（每个工具一个文件），agent 按需读取要用的文件，在执行环境里先过滤数据再给模型 | 文中例子：工具加载从 15 万 token 降到 2,000；1 万行表格模型只看 5 行 |
| 只暴露当前任务需要的工具 | 少占上下文，少选错 |
| 工具描述精炼，名称无歧义 | 同 ACI 一节的原则 |

**别忘了：**
- 执行 agent 生成的代码需要**安全的执行环境**（sandbox、资源限制、监控），这是新增的运维成本；
- 远程 MCP server 要做认证，凭据按用户范围下发；工具描述来自外部，属于不可信输入（可能含注入）。

**出处：** Anthropic《Code execution with MCP》anthropic.com/engineering/code-execution-with-mcp（2026-11-21 读）；modelcontextprotocol.io
