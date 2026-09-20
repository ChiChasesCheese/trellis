---
id: kafka-security-sasl-mechanism-choice
node: security.protocols-auth-encryption
type: qa
step: 3
source: kafka-2e
---
## Q
Kafka 内置支持 GSSAPI、PLAIN、SCRAM-SHA-256/512、OAUTHBEARER 四种 SASL 机制。已经有企业级 Kerberos 基础设施、不想额外部署密码存储、以及客户端已经用 OAuth 2.0 签发令牌，这三种场景分别该选哪种机制？

## A
已有 Kerberos（可对接 Active Directory 或 OpenLDAP）基础设施时选 **GSSAPI**，它直接用 Kerberos 票据完成客户端与服务器的双向认证；不想引入额外密码服务器时选 **SCRAM**（SCRAM-SHA-256/512），它把加盐后的哈希密码内置保存在 broker 端（配合安全的 ZooKeeper），不需要额外密码库；客户端体系已经基于 OAuth 2.0 时选 **OAUTHBEARER**，客户端携带短生命周期的不记名令牌（bearer token）认证，避免长期密码带来的泄露风险。PLAIN 只是最简单的用户名密码机制，通常需要自定义回调接外部密码库，且因为会在网络上传明文密码，必须搭配加密传输层使用。
