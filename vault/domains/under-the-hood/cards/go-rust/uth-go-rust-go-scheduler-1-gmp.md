---
id: uth-go-rust-go-scheduler-1-gmp
node: go-rust.go-scheduler
type: qa
step: 1
---
## Q
**goroutine 排在哪里等 CPU**｜Go · 1.27 运行时

Go 调度器里的 G、M、P 各是什么？可运行的 goroutine 存在哪种队列里？

## A
**背景。** 程序里可以有成千上万个 goroutine，操作系统线程却又重又少。Go 运行时自己排队：让许多 goroutine 轮流在少量线程上跑。如果大家排同一条队，就得抢同一把锁，所以要把队伍拆开。

**结构。** G 是 goroutine，M 是系统线程，P 是调度上下文（数量即 `GOMAXPROCS`，默认逻辑核数）；每个 P 自带一个本地运行队列。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 225">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">G = goroutine, M = 系统线程, P = 调度上下文</text>
<rect x="10" y="26" width="70" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="45" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">M1 线程</text>
<line x1="45" y1="48" x2="45" y2="60" stroke="currentColor" stroke-width="1"/>
<polygon points="45,60 42.3,54.0 47.7,54.0" fill="currentColor"/>
<rect x="10" y="60" width="150" height="88" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="18" y="78" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">P1</text>
<text x="50" y="78" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">runnext</text>
<rect x="106" y="66" width="24" height="16" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="118" y="77.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">g</text>
<text x="18" y="102" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">本地队列 (环形, 256)</text>
<rect x="18" y="110" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="33" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">g</text>
<rect x="52" y="110" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="67" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">g</text>
<rect x="86" y="110" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="101" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">g</text>
<rect x="120" y="110" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="135" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">g</text>
<rect x="180" y="26" width="70" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="215" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">M2 线程</text>
<line x1="215" y1="48" x2="215" y2="60" stroke="currentColor" stroke-width="1"/>
<polygon points="215,60 212.3,54.0 217.7,54.0" fill="currentColor"/>
<rect x="180" y="60" width="150" height="88" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="188" y="78" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">P2</text>
<text x="220" y="78" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">runnext</text>
<rect x="276" y="66" width="24" height="16" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="288" y="77.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">g</text>
<text x="188" y="102" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">本地队列 (环形, 256)</text>
<rect x="188" y="110" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="203" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">g</text>
<rect x="222" y="110" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="237" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">g</text>
<rect x="256" y="110" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="271" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">g</text>
<rect x="290" y="110" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="10" y="162" width="320" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="170" y="179.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全局队列 (溢出区, 本地队列放满时搬一半过来)</text>
<text x="8" y="210" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个 P 各管各的队列, 平时几乎不抢锁</text>
</svg>
```

**细节。**

- 本地队列是长度 256 的环形数组（`runq [256]guintptr`），靠原子操作而非锁访问
- 另有 `runnext` 槽：刚被当前 G 唤醒的 G 优先运行，适合来回通信的一对 goroutine
- 本地队列放满时，把一半（128 个）连同新来的搬到全局队列

**为什么。** 每个 P 各管各的队列，调度时几乎不抢锁；全局队列只当溢出区。

**对应 LeetCode：** 无直接对应的题（运行时调度结构）
