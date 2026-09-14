---
id: cache-key-minimal-complete
node: caching.keys
type: qa
---
## Q
What does it mean for a CDN cache key to be both complete and minimal?

## A
**Complete**: every request attribute that can change the representation—scheme/host/path/query and selected headers or tenant/auth partition—is represented, preventing collisions and leaks. **Minimal**: exclude attributes that do not change the response, preventing needless fragmentation. Derive the key from an explicit origin contract and log a safe hash/debug form of the selected variant.

## Q zh
CDN cache key 同时做到 complete 与 minimal 是什么意思？

## A zh
**Complete**：所有会改变 representation 的 request attribute——scheme/host/path/query，以及选定 header 或 tenant/auth partition——都进入 key，防止 collision 与 leak。**Minimal**：排除不会改变响应的属性，避免无谓 fragmentation。key 应来自明确 origin contract，并记录安全 hash/debug form 以识别实际 variant。
