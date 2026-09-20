---
nodes: [problems.social.notification-system]
url: https://firebase.google.com/docs/cloud-messaging/customize-messages/setting-message-lifespan
---
# Set the lifespan of a message

值得读：FCM 官方文档，给出消息存活时间（`time_to_live`）的确切默认值和上限（都是 4 周
/2,419,200 秒），以及 `ttl=0` 时消息在无法立即送达时会被直接丢弃而不是存储重试。比其他
二手资料更精确的地方在于明确了 collapsible 消息按 `collapse_key` 折叠的具体触发条件；
本题解用它来区分"提供商愿意存多久"和"我方需要去重多久"是两个不同的时间窗口，容易被
混淆成同一个数字。
