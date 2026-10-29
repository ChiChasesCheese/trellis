---
id: uth-redis-event-loop-persistence-1-event-loop
node: redis.event-loop-persistence
type: qa
step: 1
---
## Q
**单线程的 Redis 为什么够快**｜Redis · 8.10

执行命令基本只用一个线程，Redis 为什么还能扛住很高的吞吐？

## A
**背景。** 几千个客户端连着，大部分时间每个都在等。一个客户端配一个线程，线程一多，切换和加锁的开销就压过了真正的工作。办法：只用一个线程，问操作系统“这几千个连接里现在哪些有数据”（多路复用，I/O multiplexing），只处理有事的。

**结构。** 事件循环（event loop）：一个线程反复“等 I/O 就绪 → 处理命令 → 跑定时任务”，等 I/O 靠操作系统的多路复用。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">一个线程反复转圈</text>
<rect x="20" y="30" width="130" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="85" y="49.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等 I/O 就绪</text>
<text x="85" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">epoll / kqueue / select</text>
<rect x="190" y="30" width="130" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="255" y="49.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读请求 + 解析</text>
<rect x="190" y="100" width="130" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="255" y="119.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">执行命令 (单线程)</text>
<rect x="20" y="100" width="130" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="85" y="119.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写回结果 + 定时任务</text>
<line x1="150" y1="45" x2="190" y2="45" stroke="currentColor" stroke-width="1"/>
<polygon points="190,45 184.0,47.7 184.0,42.3" fill="currentColor"/>
<line x1="255" y1="60" x2="255" y2="100" stroke="currentColor" stroke-width="1"/>
<polygon points="255,100 252.3,94.0 257.7,94.0" fill="currentColor"/>
<line x1="190" y1="115" x2="150" y2="115" stroke="currentColor" stroke-width="1"/>
<polygon points="150,115 156.0,112.3 156.0,117.7" fill="currentColor"/>
<line x1="85" y1="100" x2="85" y2="82" stroke="currentColor" stroke-width="1"/>
<polygon points="85,82 87.7,88.0 82.3,88.0" fill="currentColor"/>
<text x="8" y="160" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">数据在内存里; 命令逐个执行, 数据结构不用加锁</text>
<text x="8" y="178" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">io-threads 默认 1; 调大后套接字读写交给 I/O 线程</text>
<text x="8" y="196" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一个慢命令 (KEYS *) 会让所有客户端排队</text>
</svg>
```

**细节。**

- 按平台选：Linux 用 `epoll`，macOS / BSD 用 `kqueue`，兜底是 `select`
- 数据在内存里；单线程执行，数据结构不用加锁
- `io-threads` 默认是 1；调大后，套接字读写和协议解析交给 I/O 线程

**为什么。** 单线程免去锁和上下文切换；想用多核就多开几个实例。

**坑。** 一个慢命令（如 `KEYS *`）会让所有客户端排队。

**对应 LeetCode：** 无直接对应的题（I/O 模型）
