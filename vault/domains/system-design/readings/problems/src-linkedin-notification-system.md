---
nodes: [problems.social.notification-system]
url: https://www.linkedin.com/blog/engineering/messaging-notifications/air-traffic-controller-member-first-notifications-at-linkedin
---
# Air Traffic Controller: Member-First Notifications at LinkedIn

值得读：LinkedIn 工程博客，讲真实生产系统 Air Traffic Controller 如何用按 member id
分区的流处理（Samza + Kafka + 本地 RocksDB 状态）统一决策每条通知的渠道、聚合与发送
时机，并给出上线后的真实收益（推送 P90 端到端延迟从约 12 秒降到约 1.5 秒，投诉减半）。
和本题解不同之处：ATC 把排序/去重/偏好判断都揉进一个统一的"决策引擎"以追求联合优化，
本题解为了组件可独立替换（比如单独换短信提供商），把队列隔离、去重、偏好过滤拆成了
独立组件。
