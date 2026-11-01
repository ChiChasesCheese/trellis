---
id: hi-pt-disposable-email-4-create-mailbox
node: qb.sd.disposable-email.points
type: qa
step: 4
---
## Q
**临时邮箱服务 · 创建邮箱与 TTL**｜出自：临时邮箱服务 › 整体设计

创建邮箱时怎么保证不覆盖已有地址，并让它 5 小时后自动失效？

## A
**要点。** Redis 里 `SET mbx:{address} {meta} NX EX 18000`：`NX` 保证不覆盖已有的，`EX` 设置 5 小时存活；数据库里的 `expiresAt` 是同一个时间。返回地址和访问令牌。
