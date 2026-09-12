---
id: kafka-security-e2e-audit-header-integrity
node: security.audit-hardening
type: qa
source: kafka-2e
---
## Q
如果想对一条消息做端到端的审计追踪（记录它经过了哪些处理环节），建议把审计元数据放在消息的什么位置？又如何防止这些审计元数据在传输过程中被篡改？

## A
建议把审计元数据放进消息标头（message header）中，这样审计信息随消息本身一起在整条 Kafka 数据流中流转，不需要额外的旁路系统也能追溯一条消息经过的处理环节。为了防止标头内容在传输或存储中途被篡改，可以使用端到端加密（在生产者、消费者两端加解密，broker 不参与）来保护消息标头的完整性，确保这些审计元数据本身也是可信的。
