---
id: bagu-py-gil-1-gil
node: b.runtime.py-gil
type: qa
step: 1
---
## Q
**Python GIL · 是什么、为什么、怎么绕过**｜追问

面试官：「Python 的 GIL 是什么？为什么多线程跑 CPU 密集任务不快？怎么绕过？有 GIL 就线程安全吗？」

## A
**基本回答。** GIL（global interpreter lock）是 CPython 的全局互斥锁，同一时刻只有一个线程执行 Python 字节码。存在原因：CPython 引用计数不是线程安全的，一把全局锁比给每个对象加锁简单，单线程也更快。线程做阻塞 IO（读文件、网络、`sleep`）时释放 GIL，纯计算时每 5ms（`sys.getswitchinterval()`）请求切换；所以 IO 密集多线程有效，CPU 密集没有加速。绕过：多进程（`ProcessPoolExecutor`，各有 GIL，代价是进程间通信要序列化）、C 扩展（NumPy、pandas 在 C 里计算不持有 GIL）、异步 IO。GIL 不等于线程安全：只保证单条字节码原子，`x += 1` 是读、加、写多条，切换时会丢更新，`list.append` 这类单次操作才是原子的，复合逻辑仍要 `threading.Lock`。
**2026 亮点。** 3.12 起子解释器可有独立 GIL（PEP 684）；3.13 起有可选的自由线程构建（PEP 703），3.14 成为受支持构建，但不是默认。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">纯计算：每 5ms 请求切换一次</text>
<text x="8" y="42" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">线程 1</text>
<rect x="62" y="24" width="66" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="95.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持有 GIL</text>
<rect x="128" y="24" width="66" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="161.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等 GIL</text>
<rect x="194" y="24" width="66" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="227.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持有 GIL</text>
<rect x="260" y="24" width="66" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="293.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等 GIL</text>
<text x="8" y="78" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">线程 2</text>
<rect x="62" y="60" width="66" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="95.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等 GIL</text>
<rect x="128" y="60" width="66" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="161.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持有 GIL</text>
<rect x="194" y="60" width="66" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="227.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等 GIL</text>
<rect x="260" y="60" width="66" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="293.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持有 GIL</text>
<text x="10" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">阻塞 IO：先放掉 GIL，别的线程接着跑</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">线程 1</text>
<rect x="62" y="120" width="66" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="95.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">算</text>
<rect x="128" y="120" width="132" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="194.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">阻塞 IO，放掉 GIL</text>
<rect x="260" y="120" width="66" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="293.0" y="137.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等 GIL</text>
<text x="8" y="174" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">线程 2</text>
<rect x="62" y="156" width="66" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="95.0" y="173.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等 GIL</text>
<rect x="128" y="156" width="198" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="227.0" y="173.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持有 GIL，一直算</text>
<text x="10" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实测（3.14，4 个任务）：纯计算串行 0.26s</text>
<text x="10" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4 线程 0.27s（没加速），4 进程 0.17s</text>
</svg>
上半部分：两个线程做纯计算，轮流持有 GIL；中间：线程 1 阻塞 IO 时放掉 GIL，线程 2 一直算；底部是实测耗时。
**举个例子。** 实测（3.14，4 个任务）：纯计算串行 0.26s、4 线程 0.27s（比串行还略慢）、4 进程 0.17s；IO 型 4 个各睡 0.5s，4 线程共 0.61s。丢更新：x 初值 0，线程 1 读到 0 后被切换，线程 2 完整执行读、加、写得 1，线程 1 用旧值 0 加 1 又写回 1，两次加 1 只加了一次；用 `Lock` 包住整个读、加、写，结果是 2。
**业务场景。** 图片压缩服务用多线程没提速，全是 CPU 计算；改进程池后吞吐随核数增长。
