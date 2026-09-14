---
id: kafka-security-zk-multi-principal-or-logic
node: security.audit-hardening
type: qa
source: kafka-2e
---
## Q
Kafka broker 端的 AclAuthorizer 判断规则是「只要有一条匹配的 DenyACL 就拒绝」，具有更高优先级的收紧效果。但如果给 ZooKeeper 同时启用 SASL 和 SSL 两种协议做客户端身份验证，导致一个连接关联了多个主体（principal），ZooKeeper 的授权判断规则和 Kafka 有什么不同？

## A
ZooKeeper 采用的是更宽松的「或」逻辑：一个连接如果同时通过 SASL 和 SSL 两种方式认证从而关联了多个主体，只要这些主体中**任意一个**对某个资源有访问权限，ZooKeeper 就会授予这次访问，并不存在像 Kafka 的 DenyACL 那样能收紧权限的优先规则。这意味着给 ZooKeeper 同时启用两种认证协议时，实际生效的权限是两边权限的并集而不是交集，需要注意不要因此意外放宽了访问范围。
