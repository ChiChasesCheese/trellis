---
id: bagu-mem-oom-1-oom-check
node: a.linux.mem-oom
type: qa
step: 1
---
## Q
**内存高与 OOM · 怎么确认进程是被杀的**｜必会

面试官：「线上有个服务内存很高，后来进程突然没了，你怎么查？」

## A
**基本回答。** 先分清「进程没了」是哪一种：被内核的 OOM Killer（内存不足杀手）强杀，还是应用自己崩了。排查四步：先 `free -h` 看 `available`（不是 `free`）；再 `ps aux --sort=-%mem` 看谁占得多；然后 `dmesg -T` 搜 `killed process` 或 `out of memory`，确认是不是被 OOM Killer 杀的；对还活着的进程，再看 `/proc/<pid>/status` 里的 `VmRSS`（常驻内存）和 `VmSwap`（被换出到磁盘的量）。容器里直接看 Pod 状态：`OOMKilled`，退出码 137（`128 + 9`，即 SIGKILL）。进程是被强杀的，来不及写日志，所以应用日志里常常没有任何报错，证据只在内核日志和退出码里。具体命令放在后面的代码一节。
OOM 分两种：整机内存不足；或超过容器 cgroup 限制（cgroup v2 下 `memory.events` 的 `oom_kill` 加一），容器可以在整机还有大量空闲时被杀。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<rect x="50" y="8" width="240" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内存不足（整机或容器上限）</text>
<line x1="170" y1="36" x2="170" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,52 166.8,45 173.2,45" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="50" y="52" width="240" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内核 OOM Killer 挑一个进程</text>
<line x1="170" y1="80" x2="170" y2="89" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,96 166.8,89 173.2,89" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="50" y="96" width="240" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SIGKILL（信号 9），无法捕获</text>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">进程来不及写日志，证据只留在三处：</text>
<rect x="4" y="160" width="108" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="58" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用日志</text>
<text x="58" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通常是空的</text>
<rect x="116" y="160" width="108" height="48" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dmesg -T</text>
<text x="170" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">killed process</text>
<rect x="228" y="160" width="108" height="48" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="282" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Pod 状态</text>
<text x="282" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">OOMKilled，137</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">要查内核日志和退出码，不是应用日志</text>
</svg>
上半是进程怎么没的：内存不够，内核挑一个进程，用无法拦截的 SIGKILL 杀掉。下半是证据在哪里：应用日志是空的（虚线框），线索在 `dmesg` 和 Pod 的退出状态里。
**举个例子。** 订单服务的 Pod 凌晨被反复重启：
1. **先看应用日志：** 干净，没有异常栈，也没有关闭日志。这反而是线索：不是代码抛异常退出，而是被外部强杀。
2. **再看 Pod 状态：** `kubectl describe pod` 里 Last State 是 Terminated，Reason 是 `OOMKilled`，Exit Code 是 137。
3. **解码 137：** 137 − 128 = 9，对应 SIGKILL，和 OOM Killer 吻合。
4. **到节点上确认：** `dmesg -T | grep -i -E 'killed process|out of memory'`，能找到被杀的进程名和时间，与 Pod 重启时间对上。
5. **判断是哪种 OOM：** 容器所在 cgroup 的 `oom_kill` 计数加一，说明是超过了容器自己的内存限制，而不是整台机器的内存耗尽。
**容易错。**
- **应用日志没报错就以为不是内存问题：** 正相反。被 SIGKILL 的进程来不及写日志，日志干净恰好是被强杀的典型表现。
- **看到 137 就以为是 JVM 堆溢出：** 137 是操作系统杀的，JVM 自己抛 `OutOfMemoryError` 不会产生 137。
- **只看整机内存：** 容器有自己的内存上限，整机还剩很多时也会因超过容器限制被杀。
- **把 `free` 那一列当剩余内存：** 缓存会占掉空闲内存，要看 `available`。
