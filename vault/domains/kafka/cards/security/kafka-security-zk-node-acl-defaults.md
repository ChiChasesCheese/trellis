---
id: kafka-security-zk-node-acl-defaults
node: security.audit-hardening
type: qa
step: 5
source: kafka-2e
---
## Q
给 Kafka broker 配置了 `zookeeper.set.acl=true` 后，ZooKeeper 中保存普通元数据的节点默认是什么访问策略？保存 SCRAM 用户名密码凭证的节点呢？

## A
普通元数据节点默认是「公开可读、只有 broker 能修改」：任何人都能查看节点内容，但只有 broker 的身份能写入或修改，如果内部管理员想绕过 broker 直接通过 ZooKeeper 客户端改元数据，需要额外配置 ACL 授权给管理员主体。但像保存 SCRAM 密码凭证这类敏感路径，默认是不公开的，防止任何非 broker 身份的用户读取到里面的密码哈希等敏感信息。
