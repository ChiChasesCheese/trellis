---
id: kafka-security-sasl-plain-must-use-ssl
node: security.protocols-auth-encryption
type: qa
step: 4
source: kafka-2e
---
## Q
为什么使用 SASL/PLAIN 机制时，必须搭配 SASL_SSL 协议，而不能用不加密的 SASL_PLAINTEXT？

## A
SASL/PLAIN 认证时，客户端会把用户名和密码以明文形式发送给 broker。如果传输层不加密（SASL_PLAINTEXT），网络上的窃听者可以直接截获这些明文凭证，进而冒充合法用户。搭配 SASL_SSL 后，认证过程和之后的所有数据都跑在 TLS 加密通道里，即使被截获也只是密文，凭证不会泄露。这也是为什么 PLAINTEXT/SASL_PLAINTEXT 只应该用在完全私有、可信的网络里。
