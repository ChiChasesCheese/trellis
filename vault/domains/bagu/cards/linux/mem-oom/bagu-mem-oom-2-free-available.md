---
id: bagu-mem-oom-2-free-available
node: a.linux.mem-oom
type: qa
step: 2
---
## Q
**free 命令 · available 和 buff/cache 怎么看**｜必会

面试官：「free 显示空闲只剩几百兆，是不是快 OOM 了？」

## A
**基本回答。** 不一定。Linux 的做法是：空闲内存不用就浪费了，所以拿去做文件缓存（buff/cache，把读过的磁盘文件留在内存里，下次不用再读磁盘），需要时可立即回收。所以判断是否紧张要看 `available`，它估算的是「不用把别的东西换出到磁盘，也能分给新程序的内存」；`free` 那一列只是完全没人用的部分，小很正常。
分辨占用大户：进程 RSS 高是应用本身；缓存高正常；`slab`（内核对象缓存，如大量 dentry）高是内核对象；swap 持续增长说明真不够了。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一台机器的两种读数</text>
<text x="8" y="40" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">MemFree ≈ 950 MB（完全没人用）</text>
<rect x="8" y="48" width="190" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="103" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">free 约 950 MB</text>
<text x="8" y="104" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">MemAvailable ≈ 1.6 GB（不换出也能给新程序）</text>
<rect x="8" y="112" width="190" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="103" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">free 约 950 MB</text>
<rect x="198" y="112" width="130" height="38" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="263" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可回收缓存</text>
<text x="263" y="142.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">约 650 MB</text>
<line x1="8" y1="158" x2="8" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="328" y1="158" x2="328" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="8" y1="164" x2="328" y2="164" stroke-width="1.2" stroke="currentColor"/>
<text x="168" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">available ≈ free + 可回收的缓存</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">回收方式：干净页直接丢，脏页先写回磁盘</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">不能回收：进程的匿名内存（堆、栈）</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">共享内存 /dev/shm 算缓存，但不能轻易回收</text>
</svg>
`available` 比 `free` 多出来的那一段，就是可以随时回收的文件缓存。真正腾不出来的是进程自己的匿名内存。
**举个例子。** 读 `/proc/meminfo`：`MemFree` 约 950 MB，`MemAvailable` 约 1.6 GB。
1. **差值是什么：** 1.6 GB − 950 MB，约 650 MB，就是可以回收的缓存。
2. **新程序要 1.2 GB：** 小于 `available`，内核先回收一部分缓存（干净页直接丢，脏页先写回），能满足，不会 OOM。
3. **新程序要 2 GB：** 超过 `available`，缓存回收完也不够；有 swap 就把一部分匿名页换出，没有 swap 就只能触发 OOM Killer 杀进程。
4. **告警该看什么：** 看 `available`（估算值，所以留余量）和 swap 是否持续增长，而不是 `free`。
**容易错。**
- **以为 free 只剩几百兆就快 OOM：** 缓存占着的部分随时能让出，要看 `available`。
- **以为 buff/cache 全部都能回收：** 共享内存、`/dev/shm` 也算缓存，却不能轻易回收。
- **用 `used` 或使用率做告警：** 缓存会把使用率顶得很高，造成大量误报，真正的内存不足反而被淹没。
- **把 slab 高当成缓存正常：** `slab` 是内核对象，持续涨要查内核侧，不是文件缓存。
**业务场景。** 监控按 `used` 告警，使用率常年 95%，值班被反复吵醒，实际 `available` 还有 40%。告警改基于 `available` 后误报消失。
