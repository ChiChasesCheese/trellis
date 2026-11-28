---
id: bagu-epoll-io-models-1-io-models
node: a.net.epoll-io-models
type: qa
step: 1
---
## Q
**I/O 模型 · 阻塞、非阻塞、同步、异步怎么区分**｜必会

面试官：「Linux 有哪几种 I/O 模型？阻塞和非阻塞、同步和异步分别指什么？」

## A
**基本回答。** 一次读分两步：① 等数据就绪，② 数据从内核拷到用户态。五种模型：阻塞 I/O（睡到数据来）、非阻塞 I/O（没好立刻返回 `EAGAIN`，要自己反复问，空转费 CPU）、I/O 多路复用（进程睡在 `select` / `poll` / `epoll` 一个调用上盯很多个 fd）、信号驱动（好了发信号）、异步 I/O（内核把等待和拷贝都做完再通知，Linux 上是 io_uring）。阻塞与否看没就绪时睡眠还是立刻返回；同步与异步看第 ② 步谁做：前四种都要进程自己拷，都是同步。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="140" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">① 等数据就绪</text>
<text x="272" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">② 数据拷到用户态</text>
<text x="4" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">阻塞 I/O</text>
<rect x="76" y="22" width="128" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">睡眠到数据来</text>
<rect x="208" y="22" width="128" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="272" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">进程睡眠等拷贝</text>
<text x="4" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">非阻塞 I/O</text>
<rect x="76" y="62" width="128" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">反复问</text>
<text x="140" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没好就 EAGAIN</text>
<rect x="208" y="62" width="128" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="272" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">进程睡眠等拷贝</text>
<text x="4" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">多路复用</text>
<rect x="76" y="102" width="128" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一个调用盯多个 fd</text>
<rect x="208" y="102" width="128" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="272" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">进程睡眠等拷贝</text>
<text x="4" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">信号驱动</text>
<rect x="76" y="142" width="128" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不用等</text>
<text x="140" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">好了发信号</text>
<rect x="208" y="142" width="128" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="272" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">进程睡眠等拷贝</text>
<text x="4" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">异步 I/O</text>
<rect x="76" y="182" width="128" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="140" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不用等</text>
<rect x="208" y="182" width="128" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内核拷完再通知</text>
<text x="4" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">前四种第 ② 步都要进程自己等</text>
<text x="4" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只有异步 I/O 连拷贝也交给内核</text>
</svg>
看第 ② 列：只有最后一行异步 I/O 的拷贝由内核做完，其余进程都要自己等。
**业务场景。** 长连接网关扛 10 万连接：一连接一线程要 10 万线程，每线程栈约 1 MB，光栈接近 100 GB，调度也拖垮机器；一线程轮询非阻塞 `read`，大部分返回 `EAGAIN`，CPU 全花在空问；用 `epoll_wait` 睡着，100 个连接有数据才被唤醒处理这 100 个。实际常搭配：epoll 通知就绪，fd 设非阻塞来读写。
**容易错。**
- **把非阻塞当异步：** 非阻塞只是不睡眠，拷贝仍要自己做。
- **以为多路复用是异步：** `epoll_wait` 本身阻塞，读写由进程做，属于同步。
- **拿 epoll 监听普通文件：** 文件总是可读，立刻就绪；磁盘异步用 io_uring 或线程池。
