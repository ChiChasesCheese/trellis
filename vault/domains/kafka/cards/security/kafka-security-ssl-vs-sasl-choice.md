---
id: kafka-security-ssl-vs-sasl-choice
node: security.protocols-auth-encryption
type: qa
step: 2
source: kafka-2e
---
## Q
要让客户端和 broker 互相验证身份并加密数据，既可以用 SSL 协议（依赖为每个客户端签发的 TLS 证书做双向认证），也可以用 SASL_SSL（TLS 负责加密+服务器认证，SASL 负责客户端认证）。什么情况下应该选 SASL_SSL 而不是纯 SSL 客户端证书认证？

## A
SSL 双向认证要求给每一个客户端签发、分发、定期轮换 TLS 证书，客户端数量一多，证书管理成本就会失控。SASL（simple authentication and security layer，简单身份验证和安全层）把认证逻辑抽成独立机制，可以用用户名密码（PLAIN/SCRAM）、Kerberos 票据（GSSAPI）或 OAuth 令牌（OAUTHBEARER）等更贴近企业现有身份系统的方式认证客户端，同时仍由 TLS 负责加密和服务器身份验证。因此当组织已有集中式的 Kerberos、LDAP 或 OAuth 身份基础设施，或客户端数量大、维护证书不现实时，应选 SASL_SSL；只有少数长期存在、愿意维护证书体系的服务才适合用纯 SSL 客户端认证。
