---
id: hl-javaq-f-q29-say60
node: java-questions.f-concurrency
type: qa
step: 34
---
## Q
用英文 60 秒回答：How does `HashMap` work internally? Resizing, collisions, treeification, why is the capacity a power of two?

## A
结构：桶数组加位与取下标（所以容量是 2 的幂）→ spread 异或高 16 位 → 0.75 扩容翻倍 → 桶内 8 个且表至少 64 才树化（反射验证）→ 树需要 Comparable → 热路径用打包 long 加开放寻址。

> "`HashMap` is an array of buckets; the index is the spread hash masked by capacity minus one, which is why capacity is a power of two - a bit-and instead of a modulo, and on resize each node either stays or moves by exactly the old capacity. The spread step XORs the high 16 bits into the low ones. At 0.75 load it doubles. If a bucket gets eight or more nodes it converts to a red-black tree, but only when the table has at least 64 buckets - below that it resizes instead; I verified that by reflecting into the table: the bin became a `TreeNode` at the eleventh colliding put. Trees need `Comparable` keys to be efficient; otherwise lookups scan. For a ticker-symbol map on a hot path I'd pack symbols into longs and use open addressing over primitive arrays."
