---
id: kafka-security-protocol-choice
node: security.protocols-auth-encryption
type: qa
step: 1
source: kafka-2e
---
## Q
Kafka broker 在监听器（listener，broker 用来接收客户端连接的网络端点）上可配置 PLAINTEXT、SSL、SASL_PLAINTEXT、SASL_SSL 四种安全协议之一。为什么内部监听器（只有集群内部、受物理保护的机器才能访问）可以用 PLAINTEXT，而暴露在公网的外部监听器绝不能用？

## A
PLAINTEXT 和 SASL_PLAINTEXT 的传输层不加密，数据以明文在网络上传输；SASL_PLAINTEXT 虽然做了身份验证，但认证凭证和之后的消息内容都可能被窃听。只有 SSL 和 SASL_SSL 用 TLS 做传输加密，能防止窃听和篡改。内部监听器所在网络已被物理隔离、只有授权人员可达，即使不加密也没有窃听风险，所以可以用 PLAINTEXT 节省 TLS 握手的 CPU 开销；外部监听器要经过不可信网络，必须选 SSL 或 SASL_SSL，否则密码和消息都会暴露给网络上的攻击者。
