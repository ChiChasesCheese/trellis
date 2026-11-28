---
id: hi-c-sd-change-data-capture-n09-email-example
node: sd.deep-dives.change-data-capture.notes
type: qa
step: 9
---
## Q
**变更数据捕获 · 订单发货发邮件：为什么 CDC 不合适**｜摘要 · 必会

监听 orders 表，看到 PROCESSING 变成 SHIPPED 就发邮件，有什么隐患？去重能解决吗？

## A
- **看起来合理：** 消费者明明看得到订单变成了 SHIPPED。
- **缺失的信息：** CDC 只知道某行变了，不知道为什么。数据迁移改写历史订单、修复脚本改错数据，都会产生一模一样的变更。
- **隐含耦合：** `status = SHIPPED` 不再只是描述状态，而是被其他系统默认为「发生了 OrderShipped 事件」。
- **副作用不幂等：** 对 Elasticsearch 重写相同状态没事；给客户再发一封发货邮件、再扣一次款就是事故。
- **去重没用：** 从数据库看，这是日志不同位置上的不同写入，没有可以拿来去重的键。缺的是一个有自己事件 ID 的、持久的业务事实。
