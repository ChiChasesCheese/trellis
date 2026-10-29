---
id: uth-compose-go-sync-map-4-real
node: compose.go-sync-map
type: qa
step: 4
---
## Q
**真实实现多做了什么**｜Go · sync.Map 旧实现（1.25 及以前）

真实的 `sync.Map` 怎样处理删除和遍历？Go 1.24 以后它为什么换了实现？

## A
**细节。**

- 删除不能改 `read` 的表结构，只把 `entry` 的指针置空；下次建 `dirty` 时，空项标成 `expunged`（已清除）、不复制进去；给已清除的 key 重新写值，必须加锁放回 `dirty`
- `Range` 发现 `amended` 为真，就先把 `dirty` 整体提升：遍历本来就是 O(N)，顺便摊掉一次复制；它不保证一致快照
- Go 1.24 起默认换成并发哈希字典树（`HashTrieMap`，每层 16 叉，读不加锁，写只锁所在节点）；1.24、1.25 可用 `GOEXPERIMENT=nosynchashtriemap` 切回旧实现，1.26 起源码里只剩新实现
- 标准库用法：`encoding/json` 用它缓存"类型 → 编码函数"，每种类型只写一次，之后无数次读

**为什么。** 官方文档只推荐两种场景：key 写一次、读多次（只增长的缓存），或各 goroutine 操作互不相交的 key。旧实现每遇到新 key 就要整表复制，提升之前的读还要加锁；新实现发布说明里说"不再需要爬坡期才能达到低争用的读"。

**坑。** 先 `Load` 再 `Store` 不是原子的，要用 `LoadOrStore`、`CompareAndSwap`；键和值都是 `any`，取出来要自己做类型断言。

**对应 LeetCode：** 无直接对应的题
