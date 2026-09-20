---
id: problems-auth-service-jwks-overlap-window
node: problems.foundations.auth-service
type: qa
step: 6
tags: [grown]
---
## Q
In an authentication service that verifies access tokens locally against JWKS-published public keys, why is an instant key switch (revoke old, publish new, sign with new, all at once) dangerous, and what should happen instead?

## A
At a large verification QPS, gateways and internal services each cache their own copy of the JWKS document, and those caches cannot all refresh in the same instant. An instant switch means tokens signed with the old key — still unexpired and legitimately valid — get rejected by any verifier that has already refreshed to the new key, producing spurious 401s. The fix is an overlap window: publish the new public key in JWKS first (without signing with it yet) so caches can pick it up, then switch signing to the new key while still publishing the old public key until every token signed with the old key has naturally expired. Each token's header carries a `kid` so verifiers look up the correct key rather than assuming only one exists.

## Q zh
在一个本地对照 JWKS 发布的公钥验证 access token 的认证服务中，为什么瞬时切换密钥（同时撤旧、发新、用新签名）是危险的，应该怎么做？

## A zh
在很大的验证 QPS 下，网关和各内部服务各自缓存一份 JWKS 文档，这些缓存不可能在同一瞬间全部刷新。瞬时切换意味着用旧密钥签发、尚未过期、本应合法有效的令牌，会被已经切到新密钥的验证方拒绝，产生大量误报的 401。修复方法是重叠窗口：先只在 JWKS 里发布新公钥（尚不用它签名），让各处缓存有时间刷新；然后切到用新密钥签名，但 JWKS 里继续保留旧公钥，直到用旧密钥签发的全部令牌自然过期。每个令牌的 header 携带 `kid`，让验证方按需查找正确的密钥，而不是假设只有一把。
