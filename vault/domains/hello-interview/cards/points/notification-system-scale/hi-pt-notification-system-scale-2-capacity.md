---
id: hi-pt-notification-system-scale-2-capacity
node: qb.sd.notification-system-scale.points
type: qa
step: 2
---
## Q
**百万级通知系统 · 容量粗算**｜必会 · 出自：百万级通知系统 › 需求

通知系统峰值每秒 100 万条投递，其中关键约 80 万、促销约 20 万，单条消息约 1 KB。Kafka 分区数和推送工作进程大约要多少？

## A
**数字。** 峰值入队 1 GB/秒；Kafka 单分区按 20 MB/秒算至少 50 个分区，留三倍余量取 150 个以上；推送 worker 单实例按 5000 条/秒需约 200 个实例。
**特点。** 促销请求本身很少，但每个请求展开成上千个投递。
