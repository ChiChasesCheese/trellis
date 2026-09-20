---
id: problems-notification-service-channel-is-not-an-enum
node: problems.components.notification-service
type: qa
step: 2
tags: [grown]
---
## Q
通知服务里的渠道（email / SMS / push / webhook）该写成 `Enum` 还是开放的字符串加注册表？这和『有限状态用 Enum』的通则冲突吗？

## A
写成**开放字符串 + `dict[str, Provider]` 注册表**，不冲突。`Enum` 的价值是**穷尽**：钞票面额、订单状态、日志级别的取值集合是封闭的。而渠道的集合按定义是开放的——机考的最后一关就是『加一个渠道不改已有代码』。写成 `class Channel(Enum)`，加 webhook 就必须改这个枚举和它所在的模块，当场失分。

代价要老实认：拼错 `"emial"` 不会在类型层面被抓住，只会在运行时变成一个 `SUPPRESSED_NO_PROVIDER` 的结果——所以这个状态必须存在且可观测，绝不能静默跳过。这是一次用类型安全换扩展性的交易，说出口比装作没有代价好。模板同理：模板是数据，注册一条 `(名字, 渠道) → (标题, 正文)` 即可，不必为每个模板写一个类。
