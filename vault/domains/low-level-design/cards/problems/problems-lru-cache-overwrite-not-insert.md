---
id: problems-lru-cache-overwrite-not-insert
node: problems.components.lru-cache
type: qa
step: 5
tags: [grown]
---
## Q
实现 LRU 缓存的 `put` 时，一个容易埋下的 bug 是什么样的？把“覆盖写入一个已存在的 key”和“插入一个新 key”用同一条代码路径处理，会出什么问题？

## A
如果 `put` 不区分“key 已存在”和“key 不存在”这两种情况，统一按“可能需要先腾地方再插入”处理，会导致更新一个已有 key 时也去检查容量、甚至触发一次不必要的淘汰。这在写密集的场景下会让缓存慢慢“自己把自己吃空”：每次更新一个已有 key 都被误判成插入，真正该保留的旧条目被冤枉地淘汰掉了。正确做法是先判断 key 是否已存在——已存在只更新值并标记为最近使用，不触碰容量判断和淘汰逻辑；只有真正的新 key 才会在容量已满时触发淘汰。
