---
id: hi-pt-feature-flag-service-4-distribution-pipeline
node: qb.sd.feature-flag-service.points
type: qa
step: 4
---
## Q
**功能开关服务 · 规则集的发布与分发链路**｜出自：功能开关服务 › 整体设计

管理员修改开关后，新规则如何到达服务端 SDK？SDK 在内存里如何持有它，连接断开时怎么办？

## A
**链路。** 管理 API 写关系库并生成新的不可变版本，快照服务把环境完整规则集序列化为压缩文件，带版本号写对象存储经 CDN 分发，同时流服务推送版本号变了的通知。
**SDK。** 启动拉一次快照放内存，收到通知后拉新快照并原子替换，取值不发网络请求。连接断开时退回每 30 秒轮询。
