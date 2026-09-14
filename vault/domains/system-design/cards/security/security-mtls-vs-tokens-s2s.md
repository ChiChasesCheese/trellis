---
id: security-mtls-vs-tokens-s2s
node: security.authz
type: qa
---
## Q
For service-to-service auth, mTLS and signed tokens (JWTs) are often used *together*. What does each prove that the other cannot?

## A
- **mTLS** proves **workload identity at the channel level**: "this connection really is from billing-service" (cert issued via SPIFFE/mesh CA), plus encryption. But it says nothing about the individual request — every request on the pipe looks the same.
- **Tokens** carry **per-request claims**: which end user this call is on behalf of, scopes, audience, expiry. But a token alone doesn't authenticate the channel and can be replayed if exfiltrated.

So: mTLS answers *"which service is calling?"*, tokens answer *"with what authority, for whom, for this request?"*. Deep systems need both — see [[security-confused-deputy]] for why service identity alone is insufficient.

## Q zh
对于服务间认证，mTLS 和签名 token（JWT）经常一起使用。各证明什么是另外无法做的？

## A zh
- **mTLS** 证明**通道级的工作负载身份**：「这个连接真的来自 billing-service」（cert 通过 SPIFFE/mesh CA 发行），加加密。但它对单个请求什么都不说 — 管子上每个请求看起来一样。
- **Token** 携带**按请求声明**：这个调用代表哪个最终用户、scope、audience、过期。但仅 token 不认证通道，如果外渗可重放。

所以：mTLS 回答*「哪个服务在调用？」*，token 回答*「什么权限，代表谁，这个请求？」*。深系统需要都 — 看 [[security-confused-deputy]] 为什么服务身份单独不够。
