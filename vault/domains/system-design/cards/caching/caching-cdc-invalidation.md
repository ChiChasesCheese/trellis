---
id: caching-cdc-invalidation
node: caching.invalidation
type: qa
---
## Q
Why drive cache invalidation from the database's change stream (CDC/binlog) instead of application code — and what gap remains?

## A
App-side invalidation must be remembered on *every* write path, and it silently fails when an app server crashes between DB commit and cache delete — stale until TTL. Tailing the binlog (Facebook's McSqueal pattern) makes every **committed** write reliably emit an invalidation: one choke point instead of N code paths, at-least-once with replay after consumer failure (deletes are idempotent, so duplicates are free).

Remaining gap: pipeline lag — a reader can re-populate the old value in the window before the invalidation arrives, so you still keep a TTL backstop (or leases, [[caching-lease-cas]]).

## Q zh
为什么从数据库的变化流（CDC/binlog）驱动缓存失效而不是应用代码 — 还有什么差距？

## A zh
应用侧失效必须在 *每个* 写路径上被记住，当应用服务器在 DB 提交和缓存删除之间崩溃时它默默失败 — 过时直到 TTL。跟踪 binlog（Facebook 的 McSqueal 模式）使每个 **已提交** 的写可靠地发出失效：一个瓶颈而不是 N 个代码路径，至少一次在消费者失败后重放（删除是幂等的，所以重复是免费的）。

剩余差距：管道延迟 — 读者可以在失效到达的窗口中重新填充旧值，所以你仍然保持 TTL 后台（或租约，[[caching-lease-cas]]）。
