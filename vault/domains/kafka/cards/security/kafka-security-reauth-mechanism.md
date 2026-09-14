---
id: kafka-security-reauth-mechanism
node: security.protocols-auth-encryption
type: qa
source: kafka-2e
---
## Q
客户端用 GSSAPI（Kerberos）或 OAUTHBEARER 这类使用有限生存期凭证的 SASL 机制认证后，broker 的后台登录线程会不断获取新凭证；但一条已经建立好的旧连接，为什么不会自动感知它当初用的凭证已经过期或被撤销？该如何解决？

## A
Kafka 默认只在**建立新连接**时校验凭证：连接一旦通过身份验证，就会在其生命周期内一直沿用当初获得的身份（KafkaPrincipal），直到因超时或网络错误自然断开为止，broker 不会主动去检查这条连接背后的凭证是否已经过期或被吊销。解决办法是给 broker 配置 `connections.max.reauth.ms`（正整数）：broker 会在 SASL 握手时告诉客户端「会话生存期 = 凭证剩余生存期 与该配置值 二者中较小的一个」，超过这个时间仍未重新认证的连接会被 broker 强制终止，从而防止凭证过期或用户被吊销后旧连接无限期存活。
