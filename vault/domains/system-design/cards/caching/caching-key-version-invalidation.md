---
id: caching-key-version-invalidation
node: caching.invalidation
type: qa
---
## Q
You need to invalidate a whole *group* of cache entries at once (every page of a user's feed) without tracking each key. Pattern and costs?

## A
**Generation (versioned) keys**: embed a per-group version in every key — `feed:{user}:v42:page3`. To invalidate the group, bump the version; old entries become unreachable instantly and age out via LRU/TTL — no enumeration, no purge.

- An extra read for the current version on each access — keep it in the same cache (or a local copy).
- A bump makes the entire group cold at once — a deliberate miss spike, so pair with warming or size the backend for it.

## Q zh
你需要一次性失效整个 *组* 的缓存条目（用户 feed 的每一页）而不跟踪每个键。模式和成本？

## A zh
**生成（版本化）键**：在每个键中嵌入一个每组版本 — `feed:{user}:v42:page3`。要失效该组，请碰撞版本；旧条目立即变得无法到达并通过 LRU/TTL 老化 — 没有枚举，没有清除。

- 每次访问时读取当前版本的额外读取 — 将其保持在相同的缓存中（或本地副本）。
- 碰撞使整个组一次冷 — 一个有意的 miss 峰值，所以与预热配对或调整后端大小。
