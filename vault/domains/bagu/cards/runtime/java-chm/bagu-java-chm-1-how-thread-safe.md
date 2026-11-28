---
id: bagu-java-chm-1-how-thread-safe
node: a.runtime.java-chm
type: qa
step: 1
---
## Q
**ConcurrentHashMap · JDK 8 怎么保证线程安全**｜必会

面试官：「ConcurrentHashMap 在 JDK 8 里是怎么做到线程安全的？和给 HashMap 整体加一把锁有什么区别？」

## A
**基本回答。** 数组加链表或红黑树，锁粒度细到单个桶：桶为空用 CAS（比较并交换，CPU 的原子指令，失败就重试）放入，不加锁；桶非空对桶头节点 `synchronized`，在锁里遍历并修改；读不加锁，靠 volatile 保证可见；扩容时别的线程发现正在搬迁会一起帮忙。只有落在同一个桶的写才互斥，不同桶完全并行，大多数 put 落在空桶，一次 CAS 就完成。对比 `Collections.synchronizedMap`/Hashtable 一把锁，所有读写互斥。JDK 7 是分段锁（Segment），JDK 8 才是桶级锁加 CAS。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数组里每个桶是各自独立的小战场</text>
<rect x="8" y="30" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="28.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="58" y="30" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">空</text>
<text x="126" y="48" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">空桶：CAS 放入，不加锁</text>
<rect x="8" y="68" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="28.0" y="84.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="58" y="68" width="40" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78.0" y="84.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<line x1="98" y1="81" x2="110" y2="81" stroke-width="1.2" stroke="currentColor"/>
<polygon points="110.0,81.0 103.0,77.8 103.0,84.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="110" y="68" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="84.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<text x="160" y="86" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">锁头节点 A</text>
<rect x="8" y="106" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="28.0" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="58" y="106" width="40" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78.0" y="122.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<text x="110" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">另一线程锁 C，互不影响</text>
<line x1="8" y1="150" x2="332" y2="150" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读 get：不加锁，靠 volatile 看到最新值</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对比整体加锁（synchronizedMap）：</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一把锁管所有桶，所有读写排队</text>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">CHM：只有落在同一个桶的写才互斥</text>
</svg>
每一行是一个桶：空桶（桶 0）直接 CAS 放入；非空桶（桶 1）锁住头节点 A；另一个线程可以同时锁别的桶（桶 2）；读完全不加锁。
**业务场景。** 聊天网关用 ConcurrentHashMap 存「用户 ID → 连接」，十万连接同时上下线：不同用户落在不同桶，空桶一次 CAS，已有节点的桶才锁头节点，`get` 不加锁；一把全局锁的 Map 在连接风暴下上线请求排成一队。实测 8 个线程各 put 两万个不同 key，HashMap 只剩 5 万左右，ConcurrentHashMap 正好 16 万。
**容易错。**
- **以为线程安全就能随便组合：** 只保证单个方法原子，先 `get` 再 `put` 不原子，要用 `merge`、`compute` 这类复合方法。
