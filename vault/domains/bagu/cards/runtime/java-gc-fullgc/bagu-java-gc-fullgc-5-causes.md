---
id: bagu-java-gc-fullgc-5-causes
node: a.runtime.java-gc-fullgc
type: qa
step: 5
---
## Q
**Full GC 排查 · 常见原因：大对象、Metaspace、内存泄漏、显式 System.gc**｜必会

面试官：「Full GC 频繁，常见的根因有哪些？它们在日志里分别长什么样？」

## A
**基本回答。** 常见根因及日志症状：泄漏（无界缓存、静态集合被 Roots 持有，每次 GC 后降下来的地板越抬越高，最终 OOM）；大对象（一次查询或读取加载超大对象，直接进老年代，单次分配出现尖峰并触发 Full GC）；线程池里 `ThreadLocal` 没 `remove`（线程不死，值一直在）；动态生成类过多撑满 Metaspace（日志写 Metaspace）；显式 `System.gc()`（括号里写 System.gc()）；堆太小或晋升过快（对象没熬够年龄就被挤进老年代）。不同根因处理完全不同，先看日志别上来就加堆：泄漏加堆只是推后故障，大对象加堆让单次停顿更长。OOM 要分种类：`Java heap space`、`Metaspace`、`unable to create native thread`（线程太多）、`Direct buffer memory`（Netty 常见）；容器 OOMKilled 是进程被系统直接杀掉，没有 Java 异常，只能看容器事件和内存监控。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次 GC 之后，老年代还剩多少</text>
<line x1="14" y1="150" x2="160" y2="150" stroke-width="1.2" stroke="currentColor"/>
<line x1="14" y1="150" x2="14" y2="36" stroke-width="1.2" stroke="currentColor"/>
<polyline points="20,130 50,75 50,108 80,68 80,92 110,60 110,76 140,44" fill="none" stroke-width="1.5" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="194" y1="150" x2="332" y2="150" stroke-width="1.2" stroke="currentColor"/>
<line x1="194" y1="150" x2="194" y2="36" stroke-width="1.2" stroke="currentColor"/>
<polyline points="200,128 240,128 250,52 260,128 328,128" fill="none" stroke-width="1.5" style="stroke:var(--accent,#3b6fd4)"/>
<text x="87" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">泄漏：地板越抬越高</text>
<text x="263" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大对象：瞬间的尖峰</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Metaspace、System.gc()：原因写在日志括号里</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先看日志认出症状，再对症下药</text>
</svg>
左图是泄漏：每次 GC 后降下来的地板越抬越高。右图是大对象：平时平稳，一次分配就冲出尖峰并触发 Full GC。
**业务场景。** 图片服务把用户上传的 5MB 图片整个读成 byte 数组，大对象直接进老年代，高峰时同时处理很多请求，老年代很快填满、Full GC 连连；改成流式分块读写，内存里只放一小块缓冲，老年代增长明显变慢。其他减压办法：限制缓存大小、少创建临时对象、对象池谨慎使用。
