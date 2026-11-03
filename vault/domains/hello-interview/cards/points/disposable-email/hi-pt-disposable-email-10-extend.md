---
id: hi-pt-disposable-email-10-extend
node: qb.sd.disposable-email.points
type: qa
step: 10
---
## Q
**临时邮箱服务 · 延长邮箱与 TTL**｜追问 · 出自：临时邮箱服务 › 取舍与追问

追问：邮箱支持延长时，已存邮件的 TTL 不能原地延长，怎么处理？

## A
**做法。** 更新 Redis 的 EXPIRE 和数据库的 `expiresAt`；邮件写入时按「最大允许寿命」设 TTL（例如 24 小时），逻辑到期由 `expiresAt` 控制。
