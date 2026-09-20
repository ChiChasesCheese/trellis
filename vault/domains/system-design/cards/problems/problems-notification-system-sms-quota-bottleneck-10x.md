---
id: problems-notification-system-sms-quota-bottleneck-10x
node: problems.social.notification-system
type: qa
step: 8
tags: [grown]
---
## Q
At 10x scale (daily active users growing 10x), why does an SMS channel typically become a bottleneck before the notification system's compute or storage layers do, and what changes to address it?

## A
SMS delivery is rate-limited by the provider per sending number or account (e.g. Twilio's documented 1 message/second per long code, 100/second per short code), and this quota does not scale automatically with your traffic the way adding more compute or storage nodes does — at 10x volume the number of provider numbers or short codes needed to sustain peak SMS QPS grows roughly linearly, quickly becoming operationally and financially impractical to manage as long codes. The fix is horizontal pooling across multiple SMS provider accounts and short codes, with rate-limit buckets subdivided by region so that a promotional SMS burst in one country cannot exhaust the quota shared with OTP traffic in another.

## Q zh
在日活用户增长到 10 倍的场景下，为什么短信渠道往往比通知系统的计算层或存储层更早成为瓶颈？需要做什么改变来应对？

## A zh
短信发送受提供商按发送号码或账号限速（例如 Twilio 文档记载的长号码每秒 1 条、短代码每秒 100 条），这个配额不会像增加计算或存储节点那样随流量自动扩展——在 10 倍流量下，维持峰值短信 QPS 所需的号码或短代码数量大致线性增长，很快就会在运维和成本上无法用长号码方式管理。解决办法是横向池化多个短信提供商账号和短代码，并按地区细分限速桶，避免某一国的促销短信突发耗尽和另一国 OTP 流量共享的配额。
