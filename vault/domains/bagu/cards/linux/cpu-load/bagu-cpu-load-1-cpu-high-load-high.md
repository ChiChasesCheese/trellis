---
id: bagu-cpu-load-1-cpu-high-load-high
node: b.linux.cpu-load
type: qa
step: 1
---
## Q
**CPU 高与 load 高 · 定位到代码与等 IO**｜必会

面试官：「某个服务 CPU 99%，怎么定位到代码？另一台机器 load 很高但 CPU 使用率不高，又是什么原因？」

## A
**基本回答。** CPU 高：先 `top` 看分布，再 `top -H -p` 找最忙的线程，转十六进制对照 `jstack` 的 `nid` 看栈。load 高而 CPU 低：load average 统计的是运行中（R）加不可中断睡眠（D）的任务数，多半在等 IO。
`top` 里 `us` 用户态、`sy` 内核态、`wa` 等 IO、`si` 软中断、`st` 被宿主机抢占。没有 jstack 用 `jcmd <pid> Thread.print` 或 Arthas `thread -n 3`；最忙的是 GC 线程转 `jstat -gcutil`；Go 用 pprof，Python 用 py-spy；火焰图横向越宽越占 CPU。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 132">
<rect x="6" y="14" width="104" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58" y="32.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">R 运行或排队</text>
<text x="58" y="47.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计入 load</text>
<rect x="118" y="14" width="104" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="32.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D 等 IO 完成</text>
<text x="170" y="47.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计入 load</text>
<rect x="230" y="14" width="104" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="32.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">S 普通睡眠</text>
<text x="282" y="47.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不计入</text>
<text x="6" y="86" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">load 长期超过 CPU 核数：任务在排队</text>
<text x="6" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4 核机器 load 长期超过 4 就是在排队</text>
<text x="6" y="122" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">D 状态多、CPU 空：多半在等磁盘或 NFS</text>
</svg>
load average 数的是 R 和 D 两种状态的任务；普通睡眠的不算。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 286">
<rect x="70" y="6" width="200" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务慢：先 top 看分布</text>
<line x1="140" y1="32" x2="91.7" y2="47.8" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,50 90.7,44.8 92.6,50.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="200" y1="32" x2="248.3" y2="47.8" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,50 247.4,50.9 249.3,44.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="50" width="158" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">us 高：CPU 真在算</text>
<rect x="176" y="50" width="158" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">load 高，CPU 不高</text>
<line x1="85" y1="80" x2="85.0" y2="89.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,96 81.8,89.0 88.2,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="255" y1="80" x2="255.0" y2="89.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,96 251.8,89.0 258.2,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="96" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">top -H -p &lt;pid&gt;</text>
<text x="85" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">找最忙的线程 TID</text>
<rect x="176" y="96" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">vmstat 1 看 b 列</text>
<text x="255" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">iostat -x 看 await</text>
<line x1="85" y1="140" x2="85.0" y2="149.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,156 81.8,149.0 88.2,149.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="255" y1="140" x2="255.0" y2="149.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,156 251.8,149.0 258.2,149.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="156" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">printf '%x' TID</text>
<text x="85" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">转十六进制</text>
<rect x="176" y="156" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ps -eo pid,stat,</text>
<text x="255" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">wchan,cmd 筛 D 状态</text>
<line x1="85" y1="200" x2="85.0" y2="209.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,216 81.8,209.0 88.2,209.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="255" y1="200" x2="255.0" y2="209.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,216 251.8,209.0 258.2,209.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="216" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="234.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">jstack &lt;pid&gt;</text>
<text x="85" y="249.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">找 nid=0x… 看栈</text>
<rect x="176" y="216" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="234.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">pidstat -d / iotop</text>
<text x="255" y="249.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">找出大 IO 进程</text>
<text x="6" y="280" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两条路都先分清：是在算，还是在等</text>
</svg>
左边是 CPU 真的忙：从线程一路追到代码行。右边是 CPU 在空等 IO：找出谁在等、等什么。
**举个例子。** 先看 CPU 高。下面的 TID 是举例用的数值：
1. **top 看分布：** 某 Java 服务 `us` 接近 99%，是用户态在算。
2. **找最忙线程：** `top -H -p <pid>`，最忙的线程 TID 是 12345。
3. **转十六进制：** `printf '%x\n' 12345` 得到 `3039`。
4. **看栈：** `jstack <pid> | grep -A 20 3039`，栈停在一段正则匹配里，原来是正则灾难性回溯造成的死循环。
5. **修复：** 改写正则并加匹配超时。
再看 load 高 CPU 低：
6. **top 看分布：** `us` 很低、`wa` 偏高，说明 CPU 在等 IO。
7. **vmstat 与 iostat：** `b` 列持续有阻塞进程，`iostat -x` 里 `await` 高、`%util` 接近 100%，盘饱和了。
8. **找 D 状态：** `ps -eo pid,stat,wchan,cmd` 筛出 D 状态进程，再用 `pidstat -d` 找出写得最猛的那个，处理它的 IO。
**容易错。**
- **以为 load 高就是 CPU 忙：** Linux 的 load 里还包含等 IO 的 D 状态，CPU 空闲、load 很高的机器通常是在等磁盘。
- **只看 load 数字不看核数：** 同样的 load 值，在 4 核和 64 核上意义完全不同，要和核数比。
- **把十进制 TID 直接拿去搜 jstack：** jstack 里是十六进制 `nid`，必须先转。
- **只抓一次栈：** 瞬间的栈可能刚好不在热点，间隔几秒多抓几次对比。
- **想用 kill -9 杀 D 状态进程：** 它在等 IO，信号不响应，要等 IO 返回或修复存储。
