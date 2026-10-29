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
**背景。** 快照只能恢复到上次拍照的那一刻，之后的写入会丢。另一种办法：把每条写命令追加到文件末尾，重启时按顺序重放一遍（AOF，append only file）。问题是文件只增不减：同一个键改了一千次，就有一千条记录。

**结构。** 7.0 起是多文件 AOF（Multi Part AOF）：一个清单文件（manifest），一个 BASE 基础快照，加若干个 INCR 增量文件。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">多文件 AOF (7.0 起)</text>
<rect x="10" y="28" width="90" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="55" y="44.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">manifest 清单</text>
<rect x="10" y="66" width="90" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="55" y="82.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">BASE 快照</text>
<rect x="110" y="66" width="70" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="145" y="82.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">INCR 1</text>
<rect x="188" y="66" width="70" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="223" y="82.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">INCR 2</text>
<text x="268" y="83" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">...</text>
<text x="8" y="112" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">重写时: 子进程生成新 BASE, 父进程同时写新 INCR</text>
<rect x="10" y="124" width="90" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="55" y="140.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">新 BASE'</text>
<rect x="110" y="124" width="70" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="145" y="140.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">新 INCR</text>
<text x="8" y="174" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">完成后旧的 BASE 和 INCR 变成历史文件, 自动删除</text>
<text x="8" y="192" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">appendfsync 默认 everysec: 每秒 fsync 一次</text>
</svg>
```

**细节。**

- BASE 是上次重写时的数据快照，INCR 是之后执行的所有写命令
- 重写时，子进程（同样靠 `fork`）生成新的 BASE，父进程同时开始写新的 INCR 文件
- 完成后旧的 BASE 和 INCR 变成历史文件，自动删除
- `appendfsync` 默认 `everysec`：每秒调用一次 `fsync`（把缓冲写到磁盘）

**为什么。** 重写与日常追加写不同的文件，避免了重写期间的额外开销。

**对应 LeetCode：** 无直接对应的题（崩溃恢复与日志）
