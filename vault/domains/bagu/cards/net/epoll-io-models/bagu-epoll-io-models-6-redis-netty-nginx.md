---
id: bagu-epoll-io-models-6-redis-netty-nginx
node: a.net.epoll-io-models
type: qa
step: 6
---
## Q
**落地 · Redis、Netty、Nginx 各怎么用**｜追问

面试官：「Redis、Netty、Nginx 分别是怎么用这套机制的？」

## A
**基本回答。** 三者都是 Reactor 加 epoll，事件循环里不阻塞。Redis：单 Reactor 单线程，命令串行、无锁；6.0 起可选 `io-threads` 并行读写 socket，命令执行仍单线程，只在瓶颈是网络 I/O 时有收益；代价是任何耗时命令（遍历百万元素）会让后面的请求全部排队。Netty：主从多 Reactor，boss 组接入连接，worker 组每个 EventLoop 绑一个线程管一批连接；在 EventLoop 里调阻塞方法会卡住它那批连接，慢活交给业务线程池。Nginx：master 加多个 worker 进程，每个 worker 单线程跑自己的 epoll，互不共享状态，一个挂了不影响别的；静态文件用 `sendfile`，数据从页缓存直接到网卡，省两次拷贝。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="4" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Redis</text>
<rect x="60" y="2" width="200" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="160" y="21" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一个线程：epoll + 执行命令</text>
<text x="4" y="50" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6.0 起可选 io-threads 并行读写 socket，命令仍单线程</text>
<text x="4" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Netty</text>
<rect x="60" y="66" width="56" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">boss</text>
<line x1="117" y1="81" x2="129" y2="81" stroke-width="1.2" stroke="currentColor"/>
<polygon points="129.0,81.0 122.0,84.2 122.0,77.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="130" y="66" width="62" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="161" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker1</text>
<rect x="198" y="66" width="62" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="229" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker2</text>
<rect x="266" y="66" width="62" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker3</text>
<text x="4" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Nginx</text>
<rect x="60" y="130" width="56" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">master</text>
<line x1="117" y1="145" x2="129" y2="145" stroke-width="1.2" stroke="currentColor"/>
<polygon points="129.0,145.0 122.0,148.2 122.0,141.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="130" y="130" width="62" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="161" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker1</text>
<rect x="198" y="130" width="62" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="229" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker2</text>
<rect x="266" y="130" width="62" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker3</text>
<text x="4" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">共同点：事件循环里不阻塞，慢活移出去</text>
<text x="4" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Netty 一个 worker 绑一个线程；Nginx 一个 worker</text>
<text x="4" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是一个进程，各跑自己的 epoll</text>
</svg>
三行是三种结构，共同点是每个框里一个线程（或进程）跑一个事件循环，且循环不做阻塞的事。
**业务场景。** Redis 里执行遍历百万元素的命令，单线程被占几百毫秒，期间已到内核缓冲区的其他请求没人读，超时报错；同样的慢逻辑写在 Netty worker 里，只停它那一批连接，其他 worker 不受影响。
**容易错。**
- **以为 6.0 起命令也多线程执行：** 只有网络读写多线程。
- **以为 Nginx 是多线程：** 是多进程，每个 worker 单线程。
- **以为单线程就慢：** Redis 命令是内存操作，单线程免锁免切换；问题在大 key 和耗时命令。
