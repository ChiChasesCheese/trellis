---
id: aid-mcp-cli
node: t03.mcp-cli
type: qa
step: 1
tags: [摘要]
---
## Q
**连接外部工具 · CLI 优先，MCP 其次**｜摘要 · 必会

agent 需要读 issue tracker、开 PR、查错误面板。接 MCP server，还是直接用命令行？

## A
**MCP（Model Context Protocol）＝一种让 agent 连接外部服务的标准协议；一个 MCP server 向 agent 提供若干 tool。**

| 情况 | 选 |
|---|---|
| 系统有 CLI（`gh`、`aws`、`kubectl`） | **CLI**：agent 已经会用，不需要说明；不认识的 CLI，让它看 `--help` |
| 没有 CLI 的系统 | MCP server |

**MCP 的两笔账：**
- **context：** 已连接的 server 把工具名和说明放进 context，哪怕你没用；不用的就关掉。（2026-11 官方：工具定义默认延迟加载，用到再取，所以只有名字和 server 说明占位置。）
- **信任：** MCP server 是别人写的、能执行动作的代码，也是提供文本给 agent 的来源。官方建议自己写或用你信任的提供方；项目里的 `.mcp.json` 会触发一次批准提示。

**别做：** 为了"以后可能用到"接一堆 server。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Connect the tools Claude needs）；《Security》（MCP security）；《How Claude Code works》（When context fills up）

</details>
