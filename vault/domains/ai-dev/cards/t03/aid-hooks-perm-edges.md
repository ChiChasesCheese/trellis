---
id: aid-hooks-perm-edges
node: t03.hooks-permissions
type: qa
step: 2
tags: [考点]
---
## Q
**Deny rule 的边界**｜考点 · 必会

你配了 `"deny": ["Read(./.env)"]`。agent 用 `cat .env` 读不到；但让它写一个 Python 脚本打开 `.env` 再运行，能读到。为什么？应该怎么补？

## A
**规则匹配的是工具调用，不是意图。**

| 手段 | 能拦吗 | 原因 |
|---|---|---|
| `Read(./.env)` 工具 | 能 | 直接命中规则 |
| `cat .env` | 能 | Claude Code 认得常见的读文件命令 |
| 自己写脚本打开文件 | **不能** | 规则看不懂脚本内部 |

**补法：** 在操作系统层隔离：sandbox（沙箱：限制 shell 命令能访问的目录和网络的运行环境，t06 详讲）；并且 `.env` 里的密钥本来就不该放在 agent 能到的地方（t06 secrets）。

```json
{
  "permissions": {
    "allow": ["Bash(pnpm tsc --noEmit)"],
    "ask":   ["Bash(git push *)"],
    "deny":  ["Read(./.env)", "Read(./secrets/**)"]
  }
}
```

**原则：** 层层设防——deny 规则拦住常规路径，sandbox 限制 shell 的实际能力，密钥管理器让文件里根本没有密钥。

**出处：** Claude Code docs《Best practices》（Limit access with permission rules and the sandbox）
