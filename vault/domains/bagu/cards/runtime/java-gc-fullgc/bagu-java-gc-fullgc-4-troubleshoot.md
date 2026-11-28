---
id: bagu-java-gc-fullgc-4-troubleshoot
node: a.runtime.java-gc-fullgc
type: qa
step: 4
---
## Q
**Full GC 排查 · GC 日志、jstat、堆转储**｜必会

面试官：「线上接口偶发几秒卡顿，监控显示 Full GC 很频繁。你怎么一步步排查？」

## A
**基本回答。** 四步：`jstat -gcutil <pid> 1000` 每秒看各区使用率和 Full GC 次数；`-Xlog:gc*` 打开 GC 日志，括号里写触发原因（System.gc()、Metaspace、分配失败、晋升失败），不能一概当成老年代满了；看 Full GC 之后老年代占用降没降：不降是对象被一直持有（泄漏），降了又很快填满是分配或晋升太快，查大对象和堆大小；不降就导堆转储（`jmap -dump` 或 `-XX:+HeapDumpOnOutOfMemoryError`），用 MAT 先看 Leak Suspects，再按 retained heap 排序看支配树，最后用 Path to GC Roots 找谁持有。线上要提前配 `HeapDumpOnOutOfMemoryError`，手动转储会暂停进程，堆越大越久；`jmap -histo:live` 会先触发一次 Full GC，线上慎用。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<rect x="8" y="6" width="324" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="21.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① jstat -gcutil &lt;pid&gt; 1000</text>
<text x="170.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">看老年代使用率、Full GC 次数</text>
<rect x="8" y="58" width="324" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="73.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② -Xlog:gc* 打开 GC 日志</text>
<text x="170.0" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">括号里写着触发原因</text>
<rect x="8" y="110" width="324" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ Full GC 之后，老年代占用降了吗？</text>
<line x1="170" y1="44" x2="170" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,58.0 166.8,51.0 173.2,51.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="96" x2="170" y2="110" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,110.0 166.8,103.0 173.2,103.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="86" y1="140" x2="86" y2="160" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="86.0,160.0 82.8,153.0 89.2,153.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="254" y1="140" x2="254" y2="160" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,160.0 250.8,153.0 257.2,153.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="96" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不降</text>
<text x="264" y="154" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">降了</text>
<rect x="8" y="162" width="156" height="52" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86.0" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对象被一直持有</text>
<text x="86.0" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 堆转储 + MAT</text>
<rect x="176" y="162" width="156" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254.0" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">降了又很快填满</text>
<text x="254.0" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查大对象、堆大小</text>
<text x="8" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不降 = 泄漏；降了又填满 = 分配太快</text>
</svg>
从上往下四步：先看次数，再看日志，然后判断回收后占用降没降；不降就去堆转储里找谁在持有，降了又填满就查大对象和堆大小。
**业务场景。** 大促期间接口偶发数秒卡顿，jstat 显示老年代一直 90% 以上、Full GC 每分钟都涨。日志 `Pause Full (G1 Compaction Pause) 95M->95M(128M)`：回收前后都是 95M，一点没回收，说明被持有；而 `Pause Full (System.gc()) 3M->1M(14M)` 是代码或框架显式调用，不是内存不够。前者用 MAT 打开，支配树里一个商品缓存占大半堆，Path to GC Roots 指向没有上限的静态 Map，修复后 Full GC 消失。
**容易错。**
- **只数 Full GC 次数：** 关键是回收后占用，监控里应同时看次数、停顿时长和回收后老年代趋势。
