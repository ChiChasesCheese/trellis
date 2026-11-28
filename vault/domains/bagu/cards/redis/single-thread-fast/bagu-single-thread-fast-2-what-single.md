---
id: bagu-single-thread-fast-2-what-single
node: a.redis.single-thread-fast
type: qa
step: 2
---
## Q
**线程模型 · 「单线程」到底指哪一部分**｜必会

面试官：「Redis 6.0 不是引入多线程了吗？进程里到底有几类线程，哪些是并行的？」

## A
**基本回答。** 「单线程」指执行命令这一步由主线程串行完成。其他执行单元：后台线程（关文件、AOF 的 fsync、异步释放内存）；fork 出的子进程（bgsave、AOF 重写），是进程不是线程；6.0 起可选的 I/O 线程，只负责 socket 读写和协议解析，不执行命令。「搬数据」外包、「碰数据」留给主线程，所以数据结构不用加锁，`MULTI` 和 Lua 的原子性仍成立。配置 `io-threads N`，默认 1 即不开；6.x、7.x 默认只用多线程写回复，读要另开 `io-threads-do-reads yes`，8.0 起该开关废弃，读写都走 I/O 线程。线程数要给主线程留核（4 核设 2–3，8 核约 6），官方称吞吐可达约两倍。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 224">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个 Redis 进程里有哪些执行单元</text>
<rect x="8" y="34" width="62" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="39" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<line x1="70" y1="52" x2="90" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90,52 83.0,55.2 83.0,48.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="90" y="26" width="96" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="138" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">I/O 线程</text>
<text x="138" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读写 socket</text>
<text x="138" y="70.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">解析协议</text>
<line x1="186" y1="52" x2="204" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="204,52 197.0,55.2 197.0,48.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="204" y="26" width="128" height="52" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="268" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主线程</text>
<text x="268" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">串行执行命令</text>
<text x="138" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6.0 起可选，默认不开</text>
<rect x="8" y="112" width="154" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">后台线程</text>
<text x="85" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">关文件、AOF fsync</text>
<text x="85" y="158.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">异步释放内存</text>
<rect x="178" y="112" width="154" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子进程（fork）</text>
<text x="255" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">bgsave</text>
<text x="255" y="158.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">AOF 重写</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">搬数据可以并行，碰数据只在主线程</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以数据结构不用加锁</text>
</svg>
上排是请求的路径：I/O 线程读 socket 并解析，主线程执行命令；下排是不执行命令的两类角色：后台线程和 fork 出的子进程。
**业务场景。** 打赏高峰都是简单 `ZINCRBY`，主线程 CPU 打满且耗在 read/write 系统调用上，开 I/O 线程有效；若是大集合 `SMEMBERS` 打满，开了也没用，先看 `INFO commandstats` 和 `SLOWLOG`。
**容易错。**
- **以为 6.0 之后命令也多线程执行了：** 多线程的只是 socket 读写和解析。
- **以为大 key 慢命令靠它能解决：** I/O 线程不分担命令执行。
