---
id: bagu-java-hashmap-collections-4-not-thread-safe
node: a.runtime.java-hashmap-collections
type: qa
step: 3
---
## Q
**HashMap · 为什么线程不安全，多线程下会出什么问题**｜必会

面试官：「多个线程同时往一个 HashMap 里 put，会出什么问题？JDK 7 和 JDK 8 表现一样吗？」

## A
**基本回答。** put 是「看桶空不空、放节点、改计数」多步，没有同步，线程可在任意两步间被打断：两个线程都看到桶是空的，后放的覆盖先放的；同时扩容各自搬迁会丢节点；元素计数也不准。JDK 7 头插法会反转链表，并发扩容时一个线程带着过期记录继续搬，链表可能连成环（A→B 被搬成 B→A 后，旧线程又让 B 指回 A），之后 `get` 走到该桶无限循环、CPU 打满。JDK 8 改尾插不成环，但仍丢数据。最难查在于没有任何异常：实测 8 个线程各 put 两万个不同 key，应有 16 万，三次运行只剩约 5.6 万、4.4 万、6.3 万。fail-fast 的 `ConcurrentModificationException` 只是尽力检测，不能当线程安全。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 290">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个线程同时 put 进同一个空桶</text>
<text x="79" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程 1</text>
<text x="261" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程 2</text>
<rect x="19" y="46" width="120" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 看到桶是空的</text>
<rect x="201" y="76" width="120" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="261.0" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 看到桶是空的</text>
<rect x="19" y="106" width="120" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="121.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 放入 hot</text>
<rect x="201" y="136" width="120" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="261.0" y="151.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 放入 vip</text>
<line x1="170" y1="48" x2="170" y2="150" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="170.0,150.0 173.2,143.0 166.8,143.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="170" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时间</text>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">结果：桶里只剩 vip，hot 悄悄丢了</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">JDK 7 头插法并发扩容，链表可能成环</text>
<rect x="96" y="238" width="44" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="118.0" y="253.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="196" y="238" width="44" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="218.0" y="253.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<line x1="140" y1="244" x2="196" y2="244" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196.0,244.0 189.0,240.8 189.0,247.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="196" y1="256" x2="140" y2="256" stroke-width="1.2" stroke="currentColor"/>
<polygon points="140.0,256.0 147.0,259.2 147.0,252.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="284" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">get 走进环里，永远出不来，CPU 打满</text>
</svg>
上半是 JDK 8 也会发生的丢数据：两个线程都看到桶是空的，后放的覆盖先放的；下半是 JDK 7 特有的环。
**业务场景。** 多个请求线程同时刷新商品标签的 HashMap 缓存，高峰期个别标签偶发查不到、没有报错；换成 ConcurrentHashMap 后消失。内存预聚合点击：用 ConcurrentHashMap 加 LongAdder，或每线程一份局部 map 再合并。替代：读写频繁用 ConcurrentHashMap，读多写少整体替换不可变副本并用 volatile 发布；`Collections.synchronizedMap` 与 Hashtable 都是整表一把锁，并发差；要有序用 `ConcurrentSkipListMap`。
**容易错。**
- **以为只有 JDK 7 有问题：** JDK 8 不成环，仍丢数据、计数不准。
