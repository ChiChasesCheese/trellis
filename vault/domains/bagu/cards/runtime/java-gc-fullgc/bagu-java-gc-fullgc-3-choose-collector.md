---
id: bagu-java-gc-fullgc-3-choose-collector
node: a.runtime.java-gc-fullgc
type: qa
step: 3
---
## Q
**垃圾回收 · G1、ZGC、CMS 怎么选，各自的停顿特点**｜必会

面试官：「你们服务的垃圾收集器怎么选？G1 和 ZGC 的差别是什么？」

## A
**基本回答。** 没有收集器三项全赢（吞吐、停顿、堆大小）。Parallel 吞吐优先，回收时应用整个停下，停顿较长，适合批处理。G1（JDK 9 起默认）把堆分成许多等大 Region，每次只挑垃圾最多的几块回收，按目标停顿 `-XX:MaxGCPauseMillis`（默认 200ms）控制，适合通用在线服务；目标只是尽力而为：并发标记没跑完老年代就满了，或晋升失败（to-space exhausted，没有空 Region 接收存活对象），会退化成 Full GC，停顿陡增。ZGC 把标记和整理放到并发阶段，停顿通常亚毫秒、几乎与堆大小无关，适合低延迟和大堆，代价是吞吐略低于 G1、更吃 CPU；JDK 21 要 `-XX:+UseZGC -XX:+ZGenerational` 才分代，JDK 23 起默认分代，JDK 24 移除非分代模式。CMS 已在 JDK 14 移除，被问先说明它没了。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 266">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">G1：堆切成许多 Region，只回收垃圾多的</text>
<rect x="8" y="26" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="26.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="48" y="26" width="36" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="66.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回收</text>
<rect x="88" y="26" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="106.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="128" y="26" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="146.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="168" y="26" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="186.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="208" y="26" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="226.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="248" y="26" width="36" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="266.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回收</text>
<rect x="288" y="26" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="306.0" y="44.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="8" y="60" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="26.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="48" y="60" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="66.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="88" y="60" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="106.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="128" y="60" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="146.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="168" y="60" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="186.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="208" y="60" width="36" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="226.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回收</text>
<rect x="248" y="60" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="266.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="288" y="60" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="306.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留</text>
<rect x="8" y="106" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="122.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Parallel</text>
<text x="88" y="123" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">吞吐优先，停顿较长，批处理</text>
<rect x="8" y="138" width="70" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="43.0" y="154.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">G1</text>
<text x="88" y="155" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">目标停顿默认 200ms，通用服务</text>
<rect x="8" y="170" width="70" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="43.0" y="186.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ZGC</text>
<text x="88" y="187" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">并发整理，亚毫秒，低延迟、大堆</text>
<rect x="8" y="202" width="70" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="218.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CMS</text>
<text x="88" y="219" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">JDK 14 已移除，不再选</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">JDK 21：-XX:+UseZGC -XX:+ZGenerational</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">JDK 23 起分代默认，JDK 24 移除非分代</text>
</svg>
上半部分是 G1 的 Region 网格：每次只挑垃圾多的几块（亮的）回收；下半部分是三个收集器各自适合的场景。
**业务场景。** 离线对账跑一晚上只关心总耗时，选 Parallel；普通订单接口偶发百来毫秒停顿可接受，用默认 G1；在线对局的走棋服务，G1 偶发上百毫秒停顿让个别走棋延迟超标、影响双方计时公平，换 ZGC 后停顿降到亚毫秒，P99 更平稳。
**容易错。**
- **以为 ZGC 全面优于 G1：** 吞吐略低，更吃 CPU，不是白捡的。
