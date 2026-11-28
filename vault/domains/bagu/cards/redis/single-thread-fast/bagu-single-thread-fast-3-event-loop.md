---
id: bagu-single-thread-fast-3-event-loop
node: a.redis.single-thread-fast
type: qa
step: 4
---
## Q
**I/O 多路复用 · 事件循环一轮做什么**｜追问

面试官：「你提到 epoll。一个线程怎么管几万个连接？事件循环一轮干哪些事？」

## A
**基本回答。** 多路复用让内核替你盯很多 socket，线程只在有 socket 就绪时干活。epoll 把 fd（文件描述符，系统给每个连接的编号）登记在内核里，内核维护就绪链表，`epoll_wait` 只返回就绪的，成本跟就绪数相关；select/poll 每次要把全部 fd 交给内核逐个检查，O(n)，select 还有 1024 上限。Linux 用 epoll，macOS 用 kqueue。不用一连接一线程：几万个线程栈和调度开销，而大部分连接大部分时间空闲。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="8" y="8" width="232" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① beforeSleep</text>
<text x="124" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写回复、刷 AOF、快速过期检查</text>
<rect x="8" y="62" width="232" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② epoll_wait</text>
<text x="124" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">阻塞，最长到下一个定时事件</text>
<rect x="8" y="116" width="232" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="124" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 可读事件</text>
<text x="124" y="147" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读、解析、执行，回复放缓冲区</text>
<rect x="8" y="170" width="232" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 时间事件</text>
<text x="124" y="201" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">serverCron：定期过期、rehash</text>
<line x1="124" y1="48" x2="124" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="124,62 120.8,55.0 127.2,55.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="124" y1="102" x2="124" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="124,116 120.8,109.0 127.2,109.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="124" y1="156" x2="124" y2="170" stroke-width="1.2" stroke="currentColor"/>
<polygon points="124,170 120.8,163.0 127.2,163.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="240" y1="190" x2="270" y2="190" stroke-width="1.2" stroke="currentColor"/>
<line x1="270" y1="190" x2="270" y2="28" stroke-width="1.2" stroke="currentColor"/>
<line x1="270" y1="28" x2="240" y2="28" stroke-width="1.2" stroke="currentColor"/>
<polygon points="240,28 247.0,24.8 247.0,31.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="278" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">循</text>
<text x="278" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">环</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回复发不完才注册可写事件</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">慢客户端只撑大自己的缓冲区</text>
</svg>
事件循环一圈四步；高亮的第三步才是执行命令，第四步每 1000/hz 毫秒触发一次后台维护。
**事件循环一轮。**
- **beforeSleep：** 把上一轮攒的回复写出去，按 `appendfsync` 刷 AOF，做一次快速过期检查。
- **epoll_wait：** 阻塞，最长等到下一个定时事件。
- **可读事件：** 读 socket、解析、执行，结果放进该客户端的回复缓冲区。
- **时间事件：** `serverCron` 每 1000/hz 毫秒（`hz` 默认 10，即 100 毫秒）：定期过期删除、渐进式 rehash、持久化检查。
- **慢客户端：** 回复一次发不完才注册可写事件；它撑大的只是自己的缓冲区，超过 `client-output-buffer-limit` 就被断开。
**业务场景。** 开播瞬间一个实例上 3 万个观众连接，其中 40 个同时拉榜单：`epoll_wait` 一次只返回这 40 个 fd，不扫另外两万九千多个；第 7 个观众网络差，回复暂时发不完，挂一个可写事件，不挡别人。
**容易错。**
- **以为 epoll 是多线程：** 它是内核的就绪通知，Redis 仍是一个线程在循环里处理。
- **以为慢客户端会拖慢所有人：** 只撑大它自己的缓冲区；拖慢所有人的是慢命令。
