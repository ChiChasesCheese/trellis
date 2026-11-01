---
id: hi-pt-disposable-email-7-expire-read
node: qb.sd.disposable-email.points
type: qa
step: 7
---
## Q
**临时邮箱服务 · 到期即不可读**｜出自：临时邮箱服务 › 整体设计

既然库有 TTL，为什么读取接口还要检查 `expiresAt`？

## A
**为什么。** 部分数据库的过期删除是惰性的，不能靠它保证「到期即不可读」。
**做法。** Redis key 到期后 SMTP 入口立即拒绝；邮件库靠 TTL 清除；读取接口再核对 `expiresAt`；附件按到期日加前缀，用生命周期规则和每日任务清理。
