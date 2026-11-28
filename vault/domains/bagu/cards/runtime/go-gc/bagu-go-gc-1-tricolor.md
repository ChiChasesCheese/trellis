---
id: bagu-go-gc-1-tricolor
node: b.runtime.go-gc
type: qa
step: 1
---
## Q
**Go GC · 三色标记、写屏障与 GOGC**｜追问

面试官：「Go 的 GC 是怎么工作的？线上 GC 变频繁、内存又紧张，你怎么调？」

## A
**基本回答。** Go 用并发三色标记清除：白是未访问，灰是已访问但引用没扫完，黑是扫完；标记结束仍是白的就是垃圾。标记与业务并发，只有开头和结尾两次极短的 STW。并发时业务可能把白对象挂到已扫完的黑对象下，黑对象不再被扫，白对象会被误回收，写屏障记录这类指针修改来防漏标。触发时机：堆涨到上次回收后存活大小的 `1 + GOGC/100` 倍，`GOGC` 默认 100 即翻倍。`GOMEMLIMIT`（1.19+）设软内存上限，容器里防 OOM。不分代、不移动对象，停顿低但吞吐有损，后台标记约占 25% CPU。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">三色标记进行到一半（根 → A → B → C）</text>
<rect x="8" y="26" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根</text>
<rect x="84" y="26" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="112.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 黑</text>
<rect x="160" y="26" width="56" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="188.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B 灰</text>
<rect x="236" y="26" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="264.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C 白</text>
<line x1="64" y1="39" x2="84" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="84.0,39.0 77.6,41.9 77.6,36.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="140" y1="39" x2="160" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="160.0,39.0 153.6,41.9 153.6,36.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="216" y1="39" x2="236" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,39.0 229.6,41.9 229.6,36.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="112" y1="52" x2="112" y2="100" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="112.0,100.0 109.1,93.6 114.9,93.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="122" y="80" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">业务线程新写入 A→D</text>
<rect x="84" y="100" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="112.0" y="117.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D 白</text>
<rect x="166" y="94" width="166" height="38" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="249.0" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写屏障：把 D 标灰</text>
<text x="249.0" y="124.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">记下来，不会漏标</text>
<line x1="166" y1="113" x2="140" y2="113" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="140.0,113.0 146.4,110.1 146.4,115.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="10" y1="146" x2="330" y2="146" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发时机：堆涨到上次存活量的 1+GOGC/100 倍</text>
<rect x="8" y="174" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="191.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">上次存活 100MB</text>
<line x1="108" y1="187" x2="128" y2="187" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.0,187.0 121.6,189.9 121.6,184.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="128" y="174" width="204" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="230.0" y="191.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GOGC=100：涨到 200MB 再回收</text>
<text x="10" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">GOMEMLIMIT：软内存上限，容器里防 OOM</text>
</svg>
上半部分：A 已扫完（黑），B 在扫（灰），C 还没访问（白）；业务线程让 A 新指向 D，写屏障把 D 标灰。下半部分：回收的触发时机，以及容器里再加一道内存上限。
**业务场景。** 排行榜服务堆里常驻大量小对象，流量翻倍后 GC 每秒触发多次、CPU 被吃掉两成多。先减少分配（逃逸分析让对象留栈上，`go build -gcflags=-m` 查看；`sync.Pool` 复用；slice 预分配），再把 `GOGC` 调到 200（上轮存活 100MB，200MB 变 300MB 才触发，GC 少了、堆更大）并设 `GOMEMLIMIT`，延迟稳定；没有固定最优值，要压测。
**容易错。**
- **以为 `GOMEMLIMIT` 是硬上限：** 软上限，接近时 GC 更勤，不保证不 OOM。
- **把 Go GC 当成 Java G1：** G1 分代、分 Region、会移动对象，停顿可预测但参数多；Go 只有 `GOGC` 与 `GOMEMLIMIT` 两个旋钮。
