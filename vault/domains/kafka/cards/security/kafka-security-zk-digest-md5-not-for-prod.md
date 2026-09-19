---
id: kafka-security-zk-digest-md5-not-for-prod
node: security.audit-hardening
type: qa
step: 4
source: kafka-2e
---
## Q
ZooKeeper 支持用 SASL/DIGEST-MD5 做用户名密码身份验证，但这种方式不适合用在生产环境，为什么？

## A
SASL/DIGEST-MD5 本身存在已知的安全漏洞，而且不会自己加密传输的凭证，如果不叠加额外的传输加密，密码可能被网络窃听截获。即便配合 TLS 加密使用，出于已知漏洞的考虑，生产环境仍应优先选择基于 Kerberos 的 SASL/GSSAPI 身份验证，而不是 SASL/DIGEST-MD5。
