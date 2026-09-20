---
id: problems-distributed-cache-lease-thundering-herd
node: problems.foundations.distributed-cache
type: qa
step: 2
tags: [grown]
---
## Q
In a distributed cache's GET/SET API, why does a cache miss return a lease token to only the first requester, and how does this token prevent two distinct failure modes?

## A
Without coordination, a hot key expiring triggers every concurrent requester to independently query the backing database and then write the result back — a thundering herd that can overwhelm the database. With leases, the first request to miss on a key receives a unique token and permission to query the database and populate the cache; subsequent concurrent requesters for the same key are told to wait instead of also querying the database. The token also prevents stale sets: a SET is only accepted if it carries the currently-valid lease for that key, so a slow database read that returns after a newer write has already happened is silently rejected instead of overwriting fresher data with stale data.

## Q zh
在一个分布式缓存的 GET/SET API 中，为什么未命中只把 lease token 发给第一个请求方？这个 token 如何同时防止两种不同的故障模式？

## A zh
如果没有这种协调，一个热门 key 过期的瞬间，所有并发请求方都会各自独立查询数据库再各自写回缓存——形成能压垮数据库的惊群效应（thundering herd）。有了 lease 机制，第一个未命中的请求会拿到一个唯一 token 以及查库并回填缓存的权限；同一 key 的后续并发请求会被告知等待，而不是各自也去查库。这个 token 同时防止了脏写（stale set）：只有携带该 key 当前有效 lease 的 SET 才会被接受，所以一次比更新的写晚返回的慢查询会被静默拒绝，而不是用旧数据覆盖掉更新的数据。
