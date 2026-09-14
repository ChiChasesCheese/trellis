---
id: cache-invalidation-versioned
node: caching.invalidation
type: qa
---
## Q
Why are content-addressed or versioned URLs safer than purging mutable asset URLs during deployment?

## A
The new bytes get a new key, so old and new assets never collide and can coexist during rollout/rollback. HTML or a manifest atomically points to the desired version; long immutable TTLs become safe. Purge is still needed for mutable entry points or emergencies, but correctness no longer depends on global purge propagation finishing instantly.

## Q zh
为什么 deployment 时，content-addressed/versioned URL 比 purge mutable asset URL 更安全？

## A zh
新 bytes 使用新 key，所以新旧 asset 不会 collision，并能在 rollout/rollback 期间共存。HTML 或 manifest 原子地指向目标 version；此时 long immutable TTL 安全可用。mutable entry point 或紧急情况仍需 purge，但 correctness 不再依赖 global purge propagation 瞬间完成。
