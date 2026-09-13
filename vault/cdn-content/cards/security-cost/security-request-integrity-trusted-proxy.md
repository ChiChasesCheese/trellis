---
id: security-request-integrity-trusted-proxy
node: security-cost.request-integrity
type: qa
---
## Q
An origin trusts the first `X-Forwarded-For` value from any client for rate limiting. What should replace this policy?

## A
Accept forwarding identity only from authenticated or network-restricted trusted proxies. At ingress, remove client-supplied copies and append a canonical chain; at origin, derive client identity from the known proxy boundary and validate chain length. Keep the origin inaccessible directly, or an attacker can forge the header and bypass every edge policy.

## Q zh
origin 信任任意 client 提供的第一个 `X-Forwarded-For` value，并用它做 rate limiting。应换成什么 policy？

## A zh
只接受来自 authenticated 或 network-restricted trusted proxy 的 forwarding identity。在 ingress 移除 client-supplied copy 并追加 canonical chain；在 origin 根据已知 proxy boundary 派生 client identity，并验证 chain length。同时禁止 direct origin access，否则 attacker 可以伪造 header，绕过所有 edge policy。
