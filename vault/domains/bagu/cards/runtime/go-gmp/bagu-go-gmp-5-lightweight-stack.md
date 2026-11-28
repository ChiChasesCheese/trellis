---
id: bagu-go-gmp-5-lightweight-stack
node: a.runtime.go-gmp
type: qa
step: 5
---
## Q
**Go 调度 · goroutine 为什么比线程轻，栈怎么增长**｜追问

面试官：「为什么一个 Go 进程可以有几十万个 goroutine，线程却不行？goroutine 的栈不够用了怎么办？」

## A
**基本回答。** 三点：栈小且可增长，初始约 2KB，线程栈通常固定 MB 级；调度在用户态，切换只保存少量寄存器，约几百纳秒，线程切换约几微秒；阻塞在 channel 或网络 IO 时不占线程。栈不够时，函数入口检查余量，不足就分配一块两倍大的新栈，旧栈内容拷过去并修正指针；GC 时用得少的栈会被收缩。实测 10 万个阻塞的 goroutine 每个栈约 2051 字节，合计约 200MB；同样数量的线程按默认 8MB 栈要预留约 800GB 地址空间，系统一般不允许。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 284">
<text x="144" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">goroutine</text>
<text x="272" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">线程</text>
<rect x="8" y="26" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">初始栈</text>
<rect x="72" y="26" width="144" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="144.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">约 2KB，可增长</text>
<rect x="224" y="26" width="108" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通常固定 MB 级</text>
<rect x="8" y="60" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">切换</text>
<rect x="72" y="60" width="144" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="144.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">约几百纳秒</text>
<rect x="224" y="60" width="108" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">约几微秒</text>
<rect x="8" y="94" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">阻塞时</text>
<rect x="72" y="94" width="144" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="144.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不占线程</text>
<rect x="224" y="94" width="108" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">占着一个线程</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">栈不够用时：</text>
<rect x="8" y="160" width="56" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36.0" y="178.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2KB</text>
<rect x="100" y="160" width="100" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150.0" y="178.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新栈 2 倍大</text>
<line x1="64" y1="174" x2="100" y2="174" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="100.0,174.0 93.0,177.2 93.0,170.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">拷贝旧栈内容，并修正指针</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">垃圾回收时，用得少的栈会被收缩</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10 万个 goroutine 约 200MB</text>
<text x="8" y="270" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同数量线程按 8MB 栈约 800GB 地址空间</text>
</svg>
上半部分对比 goroutine 和线程；下半部分是栈不够用时的处理，最后是 10 万个并发时的内存账。
**业务场景。** 爬虫为每个 URL 起一个 goroutine，一次提交一万个：goroutine 本身不是瓶颈，但无限制时目标站点被瞬间打爆；用固定数量的 worker 加信号量限并发，并对同一站点限速。
**容易错。**
- **以为便宜就能无限起：** 下游和内存仍有限。
- **以为没用的 goroutine 会被回收：** 永远阻塞在没人写入的 channel 或没人释放的锁上就是泄漏；用 `context` 传取消信号、`select` 里加 `ctx.Done()`，用 pprof 的 goroutine 分析看数量是否持续增长、堆栈停在哪。
