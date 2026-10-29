---
id: uth-compose-singleflight-2-parts
node: compose.singleflight
type: qa
step: 2
---
## Q
**进行中的调用表**｜Go · golang.org/x/sync v0.24

`singleflight.Group` 由哪几个结构组成？先到和后到的请求分别碰哪几个？

## A
**结构。** 一张表 `m`：key → `call`（一次进行中的调用），由一把锁 `mu` 保护。`call` 里有一个 `WaitGroup`（计数器：计数归零之前，调用 `Wait` 的线程都睡眠）、结果 `val` 和 `err`，以及后到者个数 `dups`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<rect x="120" y="22" width="210" height="128" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="128" y="38" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">m: key -> call (锁 mu 保护)</text>
<rect x="130" y="48" width="190" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="225.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k -> call</text>
<rect x="130" y="80" width="190" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="138" y="96" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">call</text>
<text x="138" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">wg: 后到者在这里睡眠</text>
<text x="138" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">val, err: 先到者的结果</text>
<rect x="10" y="48" width="66" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"  stroke-width="1"/>
<text x="43.0" y="65.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 先到</text>
<line x1="76" y1="61" x2="118" y2="61" stroke="currentColor" stroke-width="1"/>
<polygon points="118,61 110,57 110,65" fill="currentColor"/>
<rect x="10" y="82" width="66" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="43.0" y="99.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B 后到</text>
<line x1="76" y1="95" x2="118" y2="95" stroke="currentColor" stroke-width="1"/>
<polygon points="118,95 110,91 110,99" fill="currentColor"/>
<rect x="10" y="116" width="66" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="43.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C 后到</text>
<line x1="76" y1="129" x2="118" y2="129" stroke="currentColor" stroke-width="1"/>
<polygon points="118,129 110,125 110,133" fill="currentColor"/>
<text x="10" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A: 登记 call, 在锁外执行 fn</text>
<text x="10" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">B, C: 查到 call, 在 wg 上等待</text>
<text x="10" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">fn 结束: 写 val, err; wg.Done 唤醒; 删 m[k]</text>
</svg>
```

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| `Do(k, fn)` 先到 | 加锁，`m` 里没有 k，登记新 `call`，解锁；锁外跑 `fn`；再加锁，`wg.Done`，删 `m[k]` | O(1) + `fn` |
| `Do(k, fn)` 后到 | 加锁，`m` 里有 k，`dups` 加一，解锁，`wg.Wait` | O(1) + 等待 |
| `Forget(k)` | 加锁，删 `m[k]` | O(1) |

**为什么。** 两个结构各管一件事：`m` 回答"这个 key 有人在做吗"，`WaitGroup` 负责"没做完就先睡"。

**对应 LeetCode：** 无直接对应的题
