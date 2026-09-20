---
id: kafka-security-e2e-encryption-why
node: security.protocols-auth-encryption
type: qa
step: 6
source: kafka-2e
---
## Q
Kafka 的 SSL/SASL_SSL 传输加密（TLS）已经能防止网络窃听，为什么面对高度敏感数据或 PII（个人身份信息）时，还建议在生产者/消费者的序列化器（serializer）/反序列化器（deserializer）里额外做「端到端加密」？

## A
TLS 只保护数据在网络上传输的过程：消息到达 broker 后会以明文写入磁盘日志，也可能出现在 broker 内存的堆转储里，这意味着拥有磁盘或平台访问权限的管理员（包括云服务商）理论上仍能读到明文内容。端到端加密把加解密下放到客户端：生产者用来自密钥管理系统（KMS，key management system）的共享密钥在序列化时加密消息，消费者用同一密钥在反序列化时解密，broker 全程只存储和转发密文、拿不到密钥。这样即使平台管理员或云供应商有磁盘/内存访问权限也无法看到消息内容，满足更严格的合规要求。
