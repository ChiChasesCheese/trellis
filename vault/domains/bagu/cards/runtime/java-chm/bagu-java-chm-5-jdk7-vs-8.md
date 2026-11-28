---
id: bagu-java-chm-5-jdk7-vs-8
node: a.runtime.java-chm
type: qa
step: 6
---
## Q
**ConcurrentHashMap · JDK 7 的分段锁和 JDK 8 有什么不同**｜追问

面试官：「早期 ConcurrentHashMap 用分段锁，后来为什么改了？热点 key 在新版里就没问题了吗？」

## A
**基本回答。** JDK 7：整个 map 分成若干 Segment，每个继承 `ReentrantLock`、自己是一个小哈希表；写先定位 Segment 再锁这一段，分段数创建时固定、之后不能改，默认 16 段，最多 16 个线程同时写，每段还要单独扩容，同一段内仍互相阻塞。JDK 8：去掉 Segment，锁粒度降到单个桶（空桶 CAS、非空桶锁头节点），加红黑树和多线程协助扩容，并发度等于桶数、随数组变大而变大。热点 key 没解决：同一个 key 永远落在同一个桶，所有线程排队抢同一把锁。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 280">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">JDK 7</text>
<text x="178" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">JDK 8</text>
<rect x="8" y="28" width="140" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Segment 0</text>
<rect x="8" y="64" width="140" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Segment 1</text>
<rect x="8" y="100" width="140" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="78.0" y="117.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">……</text>
<rect x="8" y="136" width="140" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="153.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Segment 15</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每段一把锁，默认 16 段</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最多 16 个线程同时写</text>
<rect x="178" y="28" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="198.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="228" y="46" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各自独立</text>
<rect x="178" y="64" width="40" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="198.0" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="228" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一把锁</text>
<rect x="178" y="100" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="198.0" y="117.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="228" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各自独立</text>
<rect x="178" y="136" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="198.0" y="153.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="228" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各自独立</text>
<text x="178" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">一个桶一把锁</text>
<text x="178" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">并发度 = 桶数</text>
<line x1="8" y1="218" x2="332" y2="218" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">热点 key 永远落在同一个桶，仍要排队</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">计数类热点：value 换成 LongAdder</text>
</svg>
左边是 JDK 7：固定 16 段，每段一把锁；右边是 JDK 8：每个桶各管各的；底部是两个版本都躲不开的热点 key。
**业务场景。** 一条热门广告的点击不断累加，所有线程对它 `merge`：JDK 7 锁住它所在的 Segment，同段其他 key 也被拖住；JDK 8 只锁它所在的桶，但热点本身仍排队。计数类热点把 value 换成 `LongAdder`：`m.computeIfAbsent(k, x -> new LongAdder()).increment()`，累加分散到各 cell，不再锁桶，点击聚合的 CPU 占用下降；其他热点要在业务层拆成子 key 分散写、最后合并，或做本地聚合。
