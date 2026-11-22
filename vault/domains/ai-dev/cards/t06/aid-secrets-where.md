---
id: aid-secrets-where
node: t06.secrets-prompt-repo-log
type: qa
step: 1
tags: [摘要]
---
## Q
**Secrets · 不进 prompt、不进 repo、不进 log**｜摘要 · 必会

agent 要跑集成测试，需要数据库密码。你把密码贴进了 prompt，或者放在仓库的 `.env` 里让它读。有什么问题？

## A
**agent 读到的一切都进了 context，并随每次请求发给模型服务商；还可能被写进日志、提交、会话记录。**

| 渠道 | 风险 | 做法 |
|---|---|---|
| **prompt** | 密码进入对话和会话记录 | 不贴；让它引用环境变量名 |
| **repo** | 提交后永久在历史里；agent 也可能把它再写进别的文件 | `.env` 进 `.gitignore`；仓库里只放 `.env.example`（只有变量名） |
| **log** | agent 为了调试 `echo $SECRET` 或打印请求头 | 脱敏；测试用专用的低权限凭据 |
| **工具输出** | `env`、`cat .env` 的输出回到 context | 用 deny rule 让它读不到 |

```json
{ "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.local)", "Read(./secrets/**)"] } }
```

**更根本的做法：** 给 agent 的凭据权限最小、可轮换、生命周期短（只读、只限测试库）；真正的生产密钥放在密钥管理器，agent 根本接触不到。

**别做：** 只靠 CLAUDE.md 写"不要读 .env"——那是请求，不是强制（见 t03）。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Limit access with permission rules）；《Security》（Secure credential storage）

</details>
