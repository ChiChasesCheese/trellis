---
id: security-poisoning-unkeyed-input
node: security-cost.poisoning
type: qa
---
## Q
The origin uses `X-Forwarded-Host` to build an absolute redirect, but the CDN cache key ignores that header. What attack becomes possible?

## A
Web cache poisoning: an attacker supplies a malicious unkeyed value, causes the origin response to contain it, and stores that response under a key later shared by victims. Remove untrusted influence, canonicalize the host at the trusted proxy, or include the bounded representation-varying input in the key. Testing only cache HIT/MISS misses the key-to-origin mismatch.

## Q zh
origin 使用 `X-Forwarded-Host` 构建 absolute redirect，但 CDN cache key 忽略该 header。可能发生什么攻击？

## A zh
会发生 web cache poisoning：attacker 提供 malicious unkeyed value，让 origin response 包含它，并把该 response 存到之后与 victim 共享的 key 下。应移除 untrusted influence、在 trusted proxy canonicalize host，或把 bounded 且会改变 representation 的 input 放入 key。只测试 cache HIT/MISS 无法发现 key-to-origin mismatch。
