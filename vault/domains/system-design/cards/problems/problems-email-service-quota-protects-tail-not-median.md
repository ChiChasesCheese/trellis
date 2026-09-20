---
id: problems-email-service-quota-protects-tail-not-median
node: problems.media.email-service
type: qa
step: 7
tags: [grown]
---
## Q
In an email service's capacity model, a median account is computed to need roughly 71 years of average storage growth to fill a 15GB quota, while an account producing 20x the average attachment volume would fill it in about 3.6 years. What does this gap imply about what a storage quota is actually for, and where in the delivery pipeline should the quota check sit?

## A
The gap implies the quota exists to bound the cost of a small heavy-usage tail, not to constrain typical accounts — for the median account the quota is essentially never binding, so designing it as a blunt across-the-board storage cap misreads its purpose. The quota check belongs as a pre-write gate on the mailbox-write path (checked before a new message is committed to a user's MailboxEntry), not as a passive overflow condition discovered after storage fills up. Crucially, exceeding quota must never cause the SMTP edge to reject an inbound message from an external sender — that sender did nothing wrong — so an over-quota account's new mail should still be accepted and durably stored, just routed into a pending-cleanup state with the recipient prompted to free space, keeping the recipient's storage problem from leaking out as a protocol-level delivery failure for someone else.

## Q zh
在一个邮件服务的容量模型里，算出中位数账号大约需要 71 年的平均存储增长速度才能填满 15GB 配额，而一个附件产出量是平均值 20 倍的账号大约 3.6 年就能填满。这个差距说明存储配额真正的作用是什么？配额检查应该放在投递管道的哪个位置？

## A zh
这个差距说明配额存在的意义是限制少数重度使用长尾的成本，而不是约束典型账号——对中位数账号而言配额基本从未真正起作用，所以把它设计成一刀切的全局存储上限，是误解了它的用途。配额检查应该作为邮箱写入路径上的一道前置门槛（在新邮件被提交进用户的 MailboxEntry 之前检查），而不是存储写满之后才被动发现的溢出条件。关键的是，超配额绝不能导致 SMTP 边缘拒收外部发件人发来的邮件——那不是发件人的责任——所以一个超配额账号的新邮件仍应被接受并持久化存储，只是转入「待清理」状态并提示用户清理空间，避免把收件人自己的存储问题泄漏成协议层面对另一个人的投递失败。
