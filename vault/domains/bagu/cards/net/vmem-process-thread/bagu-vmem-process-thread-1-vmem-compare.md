---
id: bagu-vmem-process-thread-1-vmem-compare
node: b.net.vmem-process-thread
type: qa
step: 1
---
## Q
**虚拟内存与进程线程协程 · 页表、缺页、写时复制**｜追问

面试官：「虚拟内存是什么，缺页中断怎么处理？进程、线程、协程有什么区别？为什么服务的虚拟内存很大而 RSS 很小？」

## A
**基本回答。** 每个进程看到连续的私有地址空间（64 位实际可用 48 位，128TB），MMU 用页表把虚拟页映射到物理页帧（页通常 4KB），TLB 缓存最近的页表项。访问的页不在内存就缺页中断：次缺页（页已在内存或首次分配，只建映射）微秒级，主缺页（从 swap 或文件读盘）毫秒级，大量主缺页说明内存不够或在抖动。好处：进程隔离、按需分配（`malloc` 只划地址，触碰才给物理页）、写时复制（`fork` 后父子共享页，写入才复制）、`mmap`。所以 VSZ 可以很大而 RSS 很小。物理内存和 swap 耗尽时 OOM Killer 按 `oom_score` 杀占用大的，容器超 cgroup 限制被 SIGKILL，退出码 137。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚拟页</text>
<text x="118" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">页表</text>
<text x="246" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">物理内存</text>
<rect x="8" y="24" width="76" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">虚拟页 0</text>
<line x1="84" y1="38" x2="118" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,38.0 111.6,40.9 111.6,35.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="24" width="84" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">帧 5</text>
<line x1="202" y1="38" x2="246" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="246.0,38.0 239.6,40.9 239.6,35.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="246" y="24" width="86" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="289.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">物理帧 5</text>
<rect x="8" y="58" width="76" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">虚拟页 1</text>
<line x1="84" y1="72" x2="118" y2="72" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,72.0 111.6,74.9 111.6,69.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="58" width="84" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">帧 2</text>
<line x1="202" y1="72" x2="246" y2="72" stroke-width="1.2" stroke="currentColor"/>
<polygon points="246.0,72.0 239.6,74.9 239.6,69.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="246" y="58" width="86" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="289.0" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">物理帧 2</text>
<rect x="8" y="92" width="76" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="110.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">虚拟页 2</text>
<line x1="84" y1="106" x2="118" y2="106" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,106.0 111.6,108.9 111.6,103.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="92" width="84" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="160.0" y="110.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不在内存</text>
<line x1="202" y1="106" x2="246" y2="106" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="246.0,106.0 239.6,108.9 239.6,103.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="246" y="92" width="86" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="289.0" y="110.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘（swap）</text>
<rect x="8" y="126" width="76" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46.0" y="144.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">虚拟页 3</text>
<line x1="84" y1="140" x2="118" y2="140" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,140.0 111.6,142.9 111.6,137.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="126" width="84" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="144.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">帧 7</text>
<line x1="202" y1="140" x2="246" y2="140" stroke-width="1.2" stroke="currentColor"/>
<polygon points="246.0,140.0 239.6,142.9 239.6,137.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="246" y="126" width="86" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="289.0" y="144.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">物理帧 7</text>
<text x="10" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">TLB 缓存最近的页表项，命中就不走页表</text>
<text x="10" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">次缺页：微秒级；主缺页（读磁盘）：毫秒级</text>
</svg>
虚拟页 2 不在内存，访问时缺页，内核从磁盘读入。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<rect x="8" y="10" width="324" height="164" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="16" y="28" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">进程：独立地址空间，切换最重</text>
<rect x="18" y="40" width="148" height="100" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="26" y="58" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">线程 1：内核调度</text>
<rect x="26" y="68" width="60" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="56.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协程</text>
<rect x="94" y="68" width="60" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="124.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协程</text>
<text x="26" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">协程：用户态切换</text>
<text x="26" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">几百纳秒</text>
<rect x="176" y="40" width="148" height="100" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="184" y="58" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">线程 2：内核调度</text>
<rect x="184" y="68" width="60" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="214.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协程</text>
<rect x="252" y="68" width="60" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="282.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">协程</text>
<text x="184" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">协程：用户态切换</text>
<text x="184" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">几百纳秒</text>
<text x="16" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程共享进程的地址空间，切换几微秒</text>
<text x="10" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">进程切换：换页表、TLB 失效、缓存变冷</text>
</svg>
进程：独立地址空间，切换最重（换页表、TLB 失效、缓存变冷，线程过多时 `vmstat` 看 `cs` 列），IPC 通信，崩溃只死自己；线程：共享地址空间，内核调度，切换几微秒，共享内存要加锁，崩溃拖垮整个进程；协程：共享线程，用户态调度，切换几百纳秒，一个不让出就卡住整个线程，不能并行。栈由编译器管理、自动释放，线程栈默认 8MB；堆灵活但有碎片和 GC；泄漏持续增长，最终溢出。
**业务场景。** Redis 做 `bgsave` 时 `fork` 子进程，父子共享所有物理页，父进程写某页才复制，写得越多复制越多，内存最坏可接近翻倍；大实例 `fork` 复制页表本身也有停顿。
**容易错。**
- **把虚拟内存当实际占用：** 占物理内存的是 RSS。
- **以为所有缺页都慢：** 次缺页只是建映射。
- **以为线程切换和进程切换一样重。**
