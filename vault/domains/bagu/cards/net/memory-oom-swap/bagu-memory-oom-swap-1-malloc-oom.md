---
id: bagu-memory-oom-swap-1-malloc-oom
node: b.net.memory-oom-swap
type: qa
step: 1
---
## Q
**内存管理 · malloc、Swap 与 OOM Killer**｜追问

面试官：「malloc 是怎么分配内存的？容器内存超限被杀，退出码 137，OOM Killer 怎么选进程，怎么保护关键进程？」

## A
**基本回答。** `malloc` 小块（默认阈值 128KB，会动态调整）用 `brk()` 推堆顶再切；大块用 `mmap()` 匿名映射。`free` 后 brk 的小块留在 malloc 内存池里复用，只有 mmap 的大块还给系统，所以 RSS 不一定降。两条路都只划虚拟地址，第一次访问触发缺页才给物理页；overcommit（`vm.overcommit_memory` 0 启发式 / 1 尽量允许 / 2 严格）下 `malloc` 成功不等于有内存。物理内存和 Swap 都耗尽时 OOM Killer 杀进程：得分约为占用物理页加上 `oom_score_adj` 折算值，占用越大越先死。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">高地址</text>
<rect x="6" y="20" width="170" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="91" y="37" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">栈</text>
<rect x="6" y="54" width="170" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="91" y="72.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">mmap 区</text>
<text x="91" y="87.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大块（阈值默认 128KB）</text>
<rect x="6" y="106" width="170" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="91" y="121" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">空闲地址空间</text>
<rect x="6" y="136" width="170" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="91" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆</text>
<text x="91" y="170.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">brk() 移动堆顶，切小块</text>
<rect x="6" y="190" width="170" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="91" y="207" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据段、代码段</text>
<text x="6" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">低地址</text>
<text x="186" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">free 后整块</text>
<text x="186" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">还给操作系统</text>
<text x="186" y="154" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">free 后留在</text>
<text x="186" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">malloc 内存池里</text>
<text x="186" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">RSS 不一定降</text>
<text x="6" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">malloc 只划地址，第一次访问触发缺页才给物理页</text>
</svg>
小块从堆里切，大块单独映射，`free` 后去向不同。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 166">
<text x="210" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">容器上限 2GB</text>
<line x1="210" y1="20" x2="210" y2="134" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<rect x="10" y="28" width="200" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆 2GB（-Xmx2g）</text>
<rect x="210" y="28" width="124" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="272" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆外+栈+元空间</text>
<text x="10" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">总和超过上限：被杀，退出码 137</text>
<rect x="10" y="90" width="150" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆 1.5GB</text>
<rect x="160" y="90" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="185" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">其余</text>
<text x="10" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">总和不超过上限：稳定</text>
<text x="10" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（示意，不按比例）</text>
</svg>
容器上限算整个进程的内存，不只是堆：`-Xmx2g` 加堆外、线程栈、元空间就超限，被 cgroup 的 `memory.max` SIGKILL，退出码 137（128 + 9），宿主机还有空闲也一样。
**细节。** Swap 把不常用的匿名页换到磁盘，代价是再访问时主缺页延迟剧增；`vm.swappiness` 默认 60，越大越倾向换出。保护关键进程：`/proc/<pid>/oom_score_adj` 范围 -1000 到 1000，-1000 不会被杀，只适合 sshd 这类系统服务。确认被 OOM 杀：`dmesg` 里有 `Killed process`。
**业务场景。** 对账服务容器限制 2GB、堆也设 2GB，加堆外后超限，退出码 137；堆降到 1.5GB 后稳定。另一例：`malloc` 1GB 立刻成功，只写了前 100MB，RSS 只涨约 100MB。
**容易错。**
- **以为 malloc 成功就有内存。**
- **以为 -Xmx 等于容器该用的内存：** 它只管堆。
- **给业务进程设 -1000：** 它泄漏时杀不掉，反而拖垮整机。
- **泄漏当溢出：** 泄漏是申请后不释放、可用内存持续减少，溢出是申请不到；瞬时用量过大也会溢出。
