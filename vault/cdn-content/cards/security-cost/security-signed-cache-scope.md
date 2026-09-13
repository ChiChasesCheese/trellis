---
id: security-signed-cache-scope
node: security-cost.signed-content
type: qa
---
## Q
Should a signed URL's raw token be part of the cache key for private content?

## A
Usually not: it destroys sharing by creating one object per token. Verify the signature and authorization first, then cache under a trusted content identity plus the minimum authorization scope—only if users in that scope may share the same bytes. Bound cache TTL by content and authorization policy, prevent serving after revocation requirements, and never let an unverified request read the private entry.

## Q zh
对于 private content，signed URL 的 raw token 应该进入 cache key 吗？

## A zh
通常不应该，因为它会为每个 token 创建一个 object，破坏 sharing。先验证 signature 和 authorization，再使用 trusted content identity 加最小 authorization scope 作为 cache key；前提是该 scope 内用户确实可以共享相同 byte。cache TTL 受 content 与 authorization policy 共同约束，满足 revocation requirement，并绝不能让 unverified request 读取 private entry。
