---
id: cache-key-cookie-cardinality
node: caching.keys
type: qa
---
## Q
Why is adding the entire `Cookie` header to a cache key usually not a safe personalization strategy?

## A
It creates near-user-level cardinality, destroys hit ratio, consumes metadata, and still relies on every relevant cookie being interpreted consistently. Prefer bypass/private caching for personalized pages or extract a reviewed, low-cardinality variant/tenant identifier with strict isolation. Never drop auth inputs merely to recover hit ratio.

## Q zh
为什么把整个 `Cookie` header 加入 cache key 通常不是安全的 personalization 策略？

## A zh
它会制造接近 user-level 的 cardinality，摧毁 hit ratio、消耗 metadata，而且仍依赖所有相关 cookie 被一致解释。personalized page 更适合 bypass/private cache；或抽取经过审查、低 cardinality 的 variant/tenant identifier，并保持严格 isolation。绝不能为了恢复 hit ratio 而丢掉 auth input。
