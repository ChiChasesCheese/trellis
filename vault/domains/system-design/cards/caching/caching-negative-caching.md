---
id: caching-negative-caching
node: caching.strategies
type: qa
---
## Q
Lookups for keys that *don't exist* miss the cache every time and hit the DB. What's the fix, and its two risks?

## A
**Negative caching**: on a DB miss, store a "not found" marker under the key with a short TTL — repeated lookups (dead links, scrapers, id enumeration) get absorbed instead of each costing a DB query.

- **Create-after-miss invisibility**: an item created while its negative entry lives is hidden until the TTL expires → explicitly delete the negative entry on create.
- **Junk-key growth**: attackers can fill the cache with markers for random keys → keep negative TTLs short and let eviction handle volume.

DNS bakes the same idea in natively — [[networking-dns-negative-caching]].

## Q zh
*不存在* 的键的查找每次都缺少缓存并命中 DB。修复是什么，它的两个风险是什么？

## A zh
**负缓存**：在 DB miss 时，以短 TTL 存储"未找到"标记在键下 — 重复查找（死链接、爬虫、id 枚举）被吸收而不是每个成本一个 DB 查询。

- **创建后 miss 不可见性**：在其负条目存在时创建的项目被隐藏直到 TTL 过期 → 在创建时明确删除负条目。
- **垃圾键增长**：攻击者可以用随机键的标记填充缓存 → 保持负 TTL 短并让驱逐处理体积。

DNS 本身烘焙相同的想法 — [[networking-dns-negative-caching]]。
