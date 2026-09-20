---
id: kafka-internals-kraft-broker-fencing
node: internals.kraft-mode
type: qa
step: 5
source: kafka-2e
---
## Q
在 KRaft 架构中，一个 broker 注册到控制器仲裁（controller quorum）之后即使被关闭下线，注册状态也不会自动消失，要靠管理员显式注销。如果一个 broker 还在线，但没能及时跟上最新元数据，会发生什么？这样设计是为了防止什么问题？

## A
这种在线但元数据落后的 broker 会被**隔离（fenced）**，不允许再处理来自客户端的请求。这是为了防止客户端把请求发给一个「已经不是分区首领、但自己还不知道」的过时节点——如果不隔离，客户端可能凭旧元数据继续往一个早已失去首领身份的 broker 写消息或读消息，从而读写失败或造成数据不一致。
