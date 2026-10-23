---
id: hl-bq-q21-followups
node: behavioral.question-bank
type: qa
step: 44
---
## Q
"自己造的东西"之后的追问：跨库 stream 怎么处理？为什么直接推 main？
Cross-database streams? Why direct-push to main?

## A
- **Cross-database streams?** 先克隆**复制库（replication DB）**，换 slot 之后**自动修复**。
- **Why direct-push to main?** **个人仓库**，不碰团队代码。
