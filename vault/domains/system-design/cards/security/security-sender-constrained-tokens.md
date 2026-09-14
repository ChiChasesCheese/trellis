---
id: security-sender-constrained-tokens
node: security.authn.tokens
type: qa
---
## Q
What weakness do bearer tokens have by construction, and how do sender-constrained tokens (DPoP, mTLS-bound) fix it?

## A
A **bearer** token authorizes *whoever holds it* — exfiltrate it (logs, XSS, compromised proxy) and it replays perfectly until expiry.

**Sender-constrained** tokens bind the token to a key only the legitimate client holds:

- **DPoP**: client generates a keypair; the token is bound to the public key, and every API call carries a short-lived signed proof (covering method + URL + timestamp). A stolen token without the private key is useless.
- **mTLS-bound**: token is bound to the client certificate's thumbprint; the API checks the TLS client cert matches.

Used where token theft is the top risk: financial-grade APIs (FAPI), high-value service credentials. Cost: key management and one signature per request.

## Q zh
Bearer token 从构造上有什么弱点，发送方约束 token（DPoP、mTLS 绑定）怎样修复？

## A zh
**bearer** token 授权*无论谁持有它* — 外渗它（日志、XSS、破坏代理）它完美重放直到过期。

**发送方约束** token 将 token 绑定到仅合法客户端持有的 key：

- **DPoP**：客户端生成密钥对；token 绑定到公钥，每个 API 调用携带短生命周期签名证明（覆盖方法 + URL + 时间戳）。无私钥的偷 token 无用。
- **mTLS 绑定**：token 绑定到客户端证书的指纹；API 检查 TLS 客户端 cert 匹配。

用于 token 盗窃是顶风险的地方：金融级 API（FAPI）、高价值服务凭证。成本：key 管理和每请求一个签名。
