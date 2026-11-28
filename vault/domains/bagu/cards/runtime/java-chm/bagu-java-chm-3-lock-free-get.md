---
id: bagu-java-chm-3-lock-free-get
node: a.runtime.java-chm
type: qa
step: 3
---
## Q
**ConcurrentHashMap · get 为什么不用加锁**｜必会

面试官：「写要加锁，读为什么不用？读到一半被别的线程改了怎么办？」

## A
**基本回答。** 读靠 volatile 而不是锁：桶数组 `table`、每个节点的 `val` 和 `next` 都是 volatile，写线程的修改立刻对读线程可见（不会读到 CPU 缓存里的过期值）。每次写只改一个节点的字段或追加一个节点，对读线程是原子可见的单步变化，没有「改了一半」的中间状态，所以读到的要么是修改前、要么是修改后的值。扩容中读到 ForwardingNode 就转去新表查。代价是弱一致：`get` 可能看不到刚发生的并发 put；迭代器反映创建时的状态，也可能看到之后的部分修改，但不抛 `ConcurrentModificationException`；要精确全局快照它做不到。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="8" y="20" width="92" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="31.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写线程</text>
<text x="54.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">put 改一个</text>
<text x="54.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点字段</text>
<rect x="124" y="20" width="92" height="46" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="31.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点</text>
<text x="170.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">val、next</text>
<text x="170.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">是 volatile</text>
<rect x="240" y="20" width="92" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286.0" y="31.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读线程</text>
<text x="286.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">get 直接读</text>
<text x="286.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不加锁</text>
<line x1="100" y1="43" x2="122" y2="43" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122.0,43.0 115.0,39.8 115.0,46.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="240" y1="43" x2="218" y2="43" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="218.0,43.0 225.0,46.2 225.0,39.8" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个键的两次读：</text>
<text x="8" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">t1  get(k) → 50   （改之前）</text>
<text x="8" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">t2  put(k, 100)   写线程改完</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">t3  get(k) → 100  （立刻可见）</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读到的要么是旧值，要么是新值，不会是半截</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">扩容中读到 ForwardingNode → 去新表查</text>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代价：弱一致，可能看不到刚发生的 put</text>
</svg>
图的上半是三方关系：写线程改节点，节点的字段是 volatile，读线程直接读；下半是同一个键的两次读，先读到旧值，写完后立刻读到新值。
**业务场景。** 短链接重定向把「短码 → 长链接」放进程内，每秒几十万次读、偶尔一次写：读无锁，延迟不受写影响；管理员改链接时只是单步 volatile 写，之后任何读立刻看到新值，改的那一刻恰好在读到旧值也合法。多节点之间靠缓存失效或 TTL，是最终一致。
**容易错。**
- **以为 volatile 能让组合操作原子：** 它只保证单次读写的可见性，先 `get` 再 `put` 照样不原子。
