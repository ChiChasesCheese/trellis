---
id: uth-redis-event-loop-persistence-3-aof
node: redis.event-loop-persistence
type: qa
step: 3
---
## Q
**AOF 越写越大怎么办**｜Redis · 7.0 起

AOF 记录每条写命令，文件会无限变长，Redis 怎么重写它？

## A
**结构。** 7.0 起是多文件 AOF（Multi Part AOF）：一个清单文件（manifest），一个 BASE 基础快照，加若干个 INCR 增量文件。

**细节。**

- BASE 是上次重写时的数据快照，INCR 是之后执行的所有写命令
- 重写时，子进程（同样靠 `fork`）生成新的 BASE，父进程同时开始写新的 INCR 文件
- 完成后旧的 BASE 和 INCR 变成历史文件，自动删除
- `appendfsync` 默认 `everysec`：每秒调用一次 `fsync`

**为什么。** 重写与日常追加写不同的文件，避免了重写期间的额外开销。

**对应 LeetCode：** LC 1146 快照数组 · LC 981 基于时间的键值存储
