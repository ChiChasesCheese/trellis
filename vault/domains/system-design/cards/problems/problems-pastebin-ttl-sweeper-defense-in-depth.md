---
id: problems-pastebin-ttl-sweeper-defense-in-depth
node: problems.foundations.pastebin
type: qa
step: 6
tags: [grown]
---
## Q
In a pastebin design, expired pastes are cleaned up by a background sweeper that scans an expires_at-sorted index and deletes rows in batches. If this sweeper process goes down for a while, why does that cause wasted storage rather than incorrect serving of expired content?

## A
Because the read path independently re-checks a paste's expires_at at serve time, on every request, regardless of whether the sweeper has physically deleted the row yet. This is a deliberate defense-in-depth split: the sweeper's job is resource reclamation (deleting rows and, once a referenced blob's reference count hits zero, the underlying object-storage bytes), while correctness (never serving expired content) is enforced independently at read time. A sweeper outage therefore only means expired rows pile up and storage isn't reclaimed promptly — it never means a client can read content past its expiration.

## Q zh
在一个 pastebin 设计中，过期粘贴由一个后台 Sweeper 扫描按 expires_at 排序的索引、批量删除过期行来清理。如果这个 Sweeper 进程停摆一段时间，为什么造成的后果是存储浪费，而不是把已过期的内容错误地提供给读者？

## A zh
因为读路径在每次请求返回内容前，都会独立地、实时地再检查一次这条粘贴的 expires_at，不管 Sweeper 是否已经把这一行物理删除。这是刻意做的纵深防御分工：Sweeper 的职责是资源回收（删除行，以及在某个被引用 blob 的引用计数归零后回收底层对象存储的字节），而「绝不提供已过期内容」这条正确性保证在读取时独立执行、强制生效。因此 Sweeper 停摆只意味着过期行会堆积、存储得不到及时回收，绝不会导致客户端读到已经过期的内容。
