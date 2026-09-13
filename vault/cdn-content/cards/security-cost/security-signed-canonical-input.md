---
id: security-signed-canonical-input
node: security-cost.signed-content
type: qa
---
## Q
The signer and CDN verifier normalize query order and percent encoding differently. Why can a cryptographically strong signature still fail security?

## A
The signature authenticates bytes, not shared intent. Parser disagreement can make two semantic requests share one signature or let the verifier authorize a different resource than the origin serves. Define one canonical signing input covering scheme/host/path/query, expiry, method, and scope; reject duplicates or ambiguous encoding; and use the same test corpus in signer, edge, and origin.

## Q zh
signer 与 CDN verifier 对 query order 和 percent encoding 的 normalization 不同。为什么 cryptographically strong signature 仍可能失去安全性？

## A zh
signature 认证的是 byte，不是共同 intent。parser disagreement 可能让两个 semantic request 共用一个 signature，或让 verifier authorize 的 resource 与 origin 实际返回不同。应定义统一 canonical signing input，覆盖 scheme/host/path/query、expiry、method 与 scope；reject duplicate 或 ambiguous encoding；并在 signer、edge 和 origin 使用同一 test corpus。
