---
id: uth-compose-go-sync-map-2-parts
node: compose.go-sync-map
type: qa
step: 2
---
## Q
**只读表 + 脏表**｜Go · sync.Map 旧实现（1.25 及以前）

`sync.Map` 的 `read`、`dirty`、`misses` 各是什么？`Load` 和 `Store` 分别走哪条路？

## A
**结构。** `read`（原子指针，指向一张发布后不再增删 key 的表）；`dirty`（要持锁才能改的表，含 `read` 的全部有效项和新 key）；`misses`（读不到 `read` 而去查 `dirty` 的次数）；标志 `amended`（`dirty` 里有 `read` 没有的 key）。两张表装的是同一批 `entry`（值的原子指针），改值不必改两处。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 252">
<rect x="10" y="22" width="150" height="128" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="18" y="40" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">read</text>
<text x="18" y="56" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发布后不增删 key</text>
<rect x="180" y="22" width="150" height="128" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="188" y="40" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">dirty</text>
<text x="188" y="56" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">持锁才能改</text>
<rect x="104" y="66" width="46" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="127.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="190" y="66" width="46" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="213.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="150" y1="76" x2="190" y2="76" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="104" y="92" width="46" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="127.0" y="106.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="190" y="92" width="46" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="213.0" y="106.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<line x1="150" y1="102" x2="190" y2="102" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="190" y="118" width="46" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"  stroke-width="1"/>
<text x="213.0" y="132.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<text x="244" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新 key</text>
<text x="18" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">amended = true</text>
<text x="170" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚线: 同一个 entry (值的原子指针)</text>
<rect x="10" y="180" width="320" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="18" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">misses: 读不到 read 而去查 dirty 的次数</text>
<text x="10" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Load: 先看 read; 没中且 amended 才加锁查 dirty</text>
<text x="10" y="242" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">misses >= len(dirty): dirty 整体变成 read</text>
</svg>
```

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| `Load` 命中 `read` | `read` | O(1)，无锁 |
| `Load` 没中，`amended` 为假 | `read` | O(1)，无锁，直接说没有 |
| `Load` 没中，`amended` 为真 | `read`、加锁、`dirty`、`misses` 加一 | O(1)，加锁 |
| `Store` 已有 key | `read`，原子改 `entry` | O(1)，无锁 |
| `Store` 新 key | 加锁、`dirty`（没有就先复制 `read`）、`amended` 置真 | O(1)，首次复制 O(N) |
| 提升 | `misses ≥ len(dirty)` 时 `read = dirty`、`dirty = nil` | O(1) |

**对应 LeetCode：** 无直接对应的题
