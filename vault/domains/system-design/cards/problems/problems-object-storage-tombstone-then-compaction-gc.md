---
id: problems-object-storage-tombstone-then-compaction-gc
node: problems.foundations.object-storage
type: qa
step: 6
tags: [grown]
---
## Q
In an object storage design at 1 exabyte scale, deletes run at a steady 5 million per day, which projects to about 67 petabytes of physical bytes needing reclamation per year at a 1.4x erasure-coding storage multiplier. Why does the DELETE request itself only mark the object's metadata record as a tombstone rather than immediately freeing the underlying disk bytes, and what reclaims the space?

## A
An object's physical bytes commonly share the same underlying stripe or storage file with other, still-live objects (this is deliberate, to avoid the overhead of one tiny file per object), so there is no single byte range that can be safely erased in place at DELETE time without touching other objects' data - and even where it could be done, tying DELETE's response latency to a disk-erase operation would make deletes slow and I/O-heavy. Instead DELETE only flips a tombstone flag in metadata and returns immediately; a separate background compaction process later copies the still-live objects out of a stripe or file into a new one, skipping tombstoned and superseded entries, then atomically swaps the old file out - the same shape as LSM-tree compaction, and at 67PB/year this reclamation has to be a continuously running, rate-limited, monitored subsystem rather than an incidental side effect of delete.

## Q zh
在一个 1 EB 规模的对象存储设计中，删除请求稳定保持每天 500 万次，按 1.4 倍纠删码存储倍数换算，预计每年需要回收约 67PB 的物理字节。为什么 DELETE 请求本身只把对象的元数据记录标记为墨碑（tombstone）而不是立即释放底层磁盘字节？空间最终由什么回收？

## A zh
一个对象的物理字节通常和其他仍存活的对象共享同一个底层条带或存储文件（这是故意的，为了避免每个对象一个小文件带来的开销），所以在 DELETE 时没有一段字节能在不影响其他对象的前提下安全地就地擦除；即使能做到，把 DELETE 的响应延迟和一次磁盘擦除操作绑在一起也会让删除变得慢且 I/O 重。因此 DELETE 只在元数据里翻一个墨碑标记就立即返回；另有一个后台压实（compaction）进程之后把条带或文件里仍存活的对象复制到一个新文件里，跳过墨碑和已被覆盖的条目，然后原子性地把旧文件换掉——和 LSM 树的 compaction 是同一个形状，而在 67PB/年这个量级下，这个回收过程必须是一个持续运行、限速、可监控的子系统，而不是删除操作的顺带副产品。
