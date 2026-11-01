---
id: hi-pt-disposable-email-2-api
node: qb.sd.disposable-email.points
type: qa
step: 2
---
## Q
**临时邮箱服务 · 核心接口与入口**｜出自：临时邮箱服务 › 核心实体与接口

临时邮箱有哪些实体和接口？除了 Web API 还有什么入口？

## A
**实体。** 邮箱（address、createdAt、expiresAt、访问令牌）、邮件（正文与附件存引用）、附件放对象存储。
**接口。** `POST /mailboxes {prefix?}` 返回地址、令牌、到期时间；列邮件、读/删单封、`extend` 延长；`/stream` 用 SSE 推新邮件。
**入口。** SMTP 服务（25 端口），域名的 MX 记录指向它。只收不发。
