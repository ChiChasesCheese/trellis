---
id: security-signed-key-rotation
node: security-cost.signed-content
type: qa
---
## Q
How do you rotate signed-URL keys without invalidating every legitimate in-flight URL or accepting a compromised key forever?

## A
Publish a new key ID, start signing with it, and verify both old and new keys for a bounded overlap shorter than the maximum token lifetime. Then stop accepting the old key and remove it from verifiers after propagation is proven. Support emergency revocation separately, keep origin private so old URLs cannot bypass edge verification, and observe verification by key ID without logging tokens.

## Q zh
如何 rotate signed-URL key，既不让所有合法 in-flight URL 立即失效，也不永久接受 compromised key？

## A zh
发布新 key ID，开始用它签名，并在一个有界 overlap 内同时 verify old/new key；overlap 应短于 maximum token lifetime。确认传播后停止接受 old key，再从 verifier 移除。单独支持 emergency revocation，保持 origin private，防止 old URL 绕过 edge verification，并按 key ID 观测 verification，但不记录 token。
