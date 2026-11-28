---
id: bagu-single-thread-fast-1-why-fast
node: a.redis.single-thread-fast
type: qa
step: 1
---
## Q
**单线程为什么快 · 凭什么一个线程扛得住**｜必会

面试官：「Redis 不是单线程吗？一个线程怎么扛得住打赏榜每秒几十万次 ZINCRBY，它快在哪？」

## A
**基本回答。** 命令由一个主线程执行，瓶颈不在 CPU，所以不慢。三个原因：数据全在内存（几次内存访问，底层是哈希表、跳表这类简单结构）；用 epoll 这类 I/O 多路复用（让内核盯住很多连接，哪个有数据了再通知），一个线程盯住几万个连接；命令串行执行，没有锁，也没有线程切换。一条 GET 在服务端只要几微秒，真正贵的是网络往返和内存带宽；简单命令单实例约 8–10 万次每秒，pipeline（多条命令一次发出、一次收回）可到几十万。
**2026 亮点。** Valkey 8 / Redis 8 重写了 I/O 线程：socket 读写、解析、回包都能交给 I/O 线程，命令执行依旧单线程，厂商基准里单实例 SET 可到百万级每秒，所以「8–10 万」是保守口径；代价是多占 CPU。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个主线程，同时管几万个连接</text>
<rect x="8" y="30" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接 1</text>
<line x1="68" y1="43" x2="92" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="92,78 85.4,74.0 90.7,70.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="62" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="78.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接 2</text>
<line x1="68" y1="75" x2="92" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="92,78 84.7,80.3 85.5,74.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="94" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接 N</text>
<line x1="68" y1="107" x2="92" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="92,78 90.0,85.4 85.1,81.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="94" y="48" width="80" height="60" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="134" y="66.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">epoll</text>
<text x="134" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只告诉你</text>
<text x="134" y="96.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">谁就绪了</text>
<line x1="174" y1="78" x2="194" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="194,78 187.0,81.2 187.0,74.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="196" y="48" width="70" height="60" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="231" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主线程</text>
<text x="231" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">串行执行</text>
<line x1="266" y1="78" x2="282" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="282,78 275.0,81.2 275.0,74.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="284" y="58" width="48" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="308" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内存</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">它为什么不慢：</text>
<rect x="8" y="148" width="104" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 数据在内存</text>
<rect x="118" y="148" width="104" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 多路复用</text>
<rect x="228" y="148" width="104" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 串行无锁</text>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一条 GET 只要几微秒，瓶颈是网络和内存带宽</text>
</svg>
几万个连接先交给 epoll，只把「有数据可读」的交给主线程；主线程一条条执行，数据就在内存里；下面三格是它不慢的三个原因。
**业务场景。** 打赏榜每次 `ZINCRBY` 只改跳表一个节点，微秒级；三个请求同时到，主线程依次执行 100+10、+20、+5，不会出现两个线程同时读到 100 的丢更新。单实例扛不住几十万每秒时，客户端 pipeline、本地聚合一小段增量再写，或按主播分片。但有人在同一实例跑 `KEYS gift:*` 扫千万个 key，所有写入都被卡住。
**容易错。**
- **以为 Redis 只用一个 CPU 核：** fork 的子进程（bgsave、AOF 重写）、后台线程、I/O 线程都在用别的核，只有执行命令是串行。
- **以为多线程执行命令一定更快：** 限制 Redis 的是内存和网络；多线程要给所有数据结构加锁，还会削弱事务、Lua 的原子性。
- **以为单线程能无限扛：** 单实例有上限，一条慢命令还会拖住所有人。
