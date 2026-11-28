---
id: bagu-link-notification-system-scale-1-map
node: links.notification-system-scale
type: qa
step: 1
---
## Q
**通知系统（支持单发与群发，百万级每秒） · 会被追问哪些八股**｜必会

设计通知系统（支持单发与群发，百万级每秒）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 关键通知和群发要物理隔离。基础是：队列选型、积压处理、消费端幂等与不丢、渠道隔离、第三方限速、长连接推送合并。

**下钻路线。**
- 投递队列选哪个 → 群发要吞吐选 Kafka，延迟发送与渠道路由选 RabbitMQ，[[b.mq.selection|Kafka、RabbitMQ、RocketMQ 怎么选]]
- 峰值积压怎么办 → 先判断原因，再扩容和降级，[[a.mq.backlog|消息积压怎么办]]
- 消费者崩溃重启 → 手动提交位点加通知幂等，丢还是重复取决于提交时机，[[a.mq.no-loss|消息不丢失]]
- 同一用户通知要有序 → 消费端按用户哈希到内部队列再并发，[[a.mq.ordering|消息顺序性怎么保证]]
- 两台 worker 取到同一条 → 去重表加唯一键，用户只收一次，[[a.idem.idempotency-design|幂等是什么、怎么实现]]
- 邮件、短信、推送三个渠道 → 每渠道独立线程池，短信商变慢不拖累推送，[[b.protect.bulkhead|隔离]]
- 给第三方通道限速 → 令牌桶分优先级，营销群发不能挤占验证码额度，[[a.protect.rate-limit-algorithms|限流算法]]
- 群发给所有在线用户 → 每个网关只收一份再本地分发，[[a.net.websocket-push|消息推送]]

**业务场景。** 支付成功的回执短信不能被营销群发压在队列后面，所以验证码与回执走独立队列和独立额度。
**系统设计。** [[links.tt-merchant-webhook-delivery|商户回调（Webhook）投递系统（至少一次、重试、顺序、签名）]]：同样的重试与隔离，对象是商户服务器，多了签名；[[links.messenger-chat-system|聊天/即时通讯系统（WhatsApp / Messenger）]]：同样按网关合并投递，但要会话内有序。
