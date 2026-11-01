---
id: hi-pt-tt-merchant-webhook-delivery-1-backlog-number
node: tt.sd.tt-merchant-webhook-delivery.points
type: qa
step: 1
---
## Q
**商户回调（Webhook）投递系统 · 驱动设计的数字：36 万条积压**｜出自：商户回调（Webhook）投递系统 › 需求

webhook 平台每天 2000 万事件、峰值约 2800 次/秒。某商户每秒 100 个事件，宕机一小时会怎样？这个数字决定设计的重点是什么？

## A
**数字。** 360,000 条积压、约 360 MB；整体在途请求一两千个连接，小集群就够。
**结论。** 吞吐不是主问题，隔离和积压存储才是：积压只能堵它自己，且放在存储里，不放在内存和队列头部。
