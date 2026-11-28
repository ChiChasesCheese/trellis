---
id: bagu-py-concurrency-choice-1-asyncio-thread-process
node: b.runtime.py-concurrency-choice
type: qa
step: 1
---
## Q
**Python 并发 · asyncio、线程、进程怎么选**｜追问

面试官：「要同时调上千个渠道账单接口，还要解析大对账文件。asyncio、多线程、多进程怎么选？asyncio 有什么坑？」

## A
**基本回答。** 大量并发网络 IO 用 asyncio；只能同步调用的阻塞库用线程池；CPU 密集用多进程；混合场景 asyncio 做 IO、进程池做计算。asyncio 是单线程事件循环（底层 epoll）调度协程，遇到 `await` 让出、IO 就绪后恢复，一个连接只占几 KB，可上万并发；切换点只在 `await`，几乎没有竞态（跨 `await` 的复合操作仍要小心）。线程由 OS 抢占式调度，共享数据要加锁，还受 GIL 限制。最大的坑：协程里调阻塞函数（`time.sleep`、同步 `requests.get`、重计算）会卡住整个循环，要用异步库（`httpx`、`aiohttp`）或 `asyncio.to_thread`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="8" y="10" width="170" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上千个渠道接口并发</text>
<line x1="178" y1="25" x2="196" y2="25" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="196.0,25.0 189.6,27.9 189.6,22.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="196" y="10" width="136" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="264.0" y="29.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">asyncio</text>
<rect x="8" y="50" width="170" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="69.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只能同步调用的阻塞库</text>
<line x1="178" y1="65" x2="196" y2="65" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="196.0,65.0 189.6,67.9 189.6,62.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="196" y="50" width="136" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="264.0" y="69.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程池</text>
<rect x="8" y="90" width="170" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">解析大对账文件（CPU）</text>
<line x1="178" y1="105" x2="196" y2="105" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="196.0,105.0 189.6,107.9 189.6,102.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="196" y="90" width="136" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="264.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">进程池</text>
<rect x="8" y="130" width="170" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="149.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">IO 加计算的混合场景</text>
<line x1="178" y1="145" x2="196" y2="145" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="196.0,145.0 189.6,147.9 189.6,142.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="196" y="130" width="136" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="264.0" y="149.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">asyncio 加进程池</text>
<line x1="10" y1="176" x2="330" y2="176" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">asyncio：一个线程里的事件循环</text>
<rect x="8" y="204" width="324" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="18" y="212" width="72" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="230.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协程 A</text>
<rect x="134" y="212" width="72" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="230.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协程 B</text>
<rect x="250" y="212" width="72" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286.0" y="230.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协程 C</text>
<line x1="90" y1="234" x2="134" y2="234" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="134.0,234.0 127.6,236.9 127.6,231.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="206" y1="234" x2="250" y2="234" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250.0,234.0 243.6,236.9 243.6,231.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="112" y="228" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">await</text>
<text x="228" y="228" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">await</text>
<text x="10" y="270" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">协程里写 time.sleep：整个循环卡住</text>
<text x="10" y="288" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3 个 sleep(1) 共约 3s；to_thread 约 1s</text>
</svg>
上半部分是按场景选方案；下半部分是事件循环：协程遇到 await 就让出、轮流运行；某个协程调了阻塞函数，所有协程一起卡住。
**举个例子。** 对账服务拉 1000 个渠道账单，每个约 1 秒：同步 requests 串行约 1000 秒；50 线程的线程池约 20 秒；asyncio 加异步库约 1 秒（1000 个 `asyncio.sleep(1)` 实测约 1s）。协程里混进 `time.sleep(1)`，3 个协程共约 3s，换成 `asyncio.to_thread` 约 1s。下载后的大账单解析是 CPU 计算，丢进进程池，避免卡事件循环。
**容易错。**
- **以为 asyncio 能加速 CPU 密集：** 只有一个线程，计算仍串行，要用进程池。
