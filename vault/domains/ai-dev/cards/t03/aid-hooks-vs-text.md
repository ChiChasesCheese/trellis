---
id: aid-hooks-vs-text
node: t03.hooks-permissions
type: qa
step: 1
tags: [摘要]
---
## Q
**确定性规则 vs 建议性规则**｜摘要 · 必会

"不要读 .env""改完文件要格式化""不要动 migrations 目录"——这三条放 CLAUDE.md，还是放别处？

## A
**两类指令：**
- **建议性（non-deterministic）：** prompt、CLAUDE.md、skills（按需加载的流程说明）——模型读到，自己决定怎么做，几乎总是照做，但**不保证**；
- **确定性（deterministic）：** hook、deny rule、managed setting——harness 每次都执行，不管模型怎么想。

| 方式 | 是什么 |
|---|---|
| **hook** | harness 在固定时点（工具调用前 PreToolUse、调用后 PostToolUse、agent 要结束时 Stop）执行你的脚本 |
| **permission rule（权限规则）** | allow / ask / deny 三种；**deny rule 在每种权限模式下都生效**，包括 auto 和跳过确认 |

**三条的归属：**

| 规则 | 放哪 | 怎么写 |
|---|---|---|
| 不读 `.env` | deny rule | `"deny": ["Read(./.env)"]` |
| 改完要格式化 | PostToolUse hook | 匹配 `Edit|Write`，跑 prettier |
| 不动 migrations | PreToolUse hook | 路径在 `migrations/` 下就退出码 2 |

**界线：** 一条规则**零例外**才做成强制。"优先用具名 export"有例外，留在 CLAUDE.md；强制规则做太多，反而僵化。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Deterministic and non-deterministic instructions；Enforce the rules that can't have exceptions）

</details>
