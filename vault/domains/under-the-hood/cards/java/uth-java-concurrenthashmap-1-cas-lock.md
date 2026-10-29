---
id: uth-java-concurrenthashmap-1-cas-lock
node: java.concurrenthashmap
type: qa
step: 1
---
## Q
**ConcurrentHashMap 的 put 怎么加锁**｜Java · OpenJDK 25

多个线程同时改一张哈希表会出什么问题？Java 8 之后 `ConcurrentHashMap` 的 `put` 一个 key 时到底锁了什么？`get` 要加锁吗？

## A
**背景。** 多个线程同时改同一个 `HashMap` 会互相覆盖、甚至破坏结构。最省事的办法是整张表一把锁，所有线程排队，安全但慢。更好的办法：只锁真正会冲突的那一小部分。

**结构。** 和 `HashMap` 一样的桶数组加链表或红黑树，但并发控制细到**单个桶**：目标桶为空，用 CAS（比较并交换：确认它还是空的才写入，否则重试）直接放入新节点，不加锁；桶非空，只锁这个桶的头节点。例：线程甲写桶 3、线程乙写桶 7，互不干扰。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="20" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">桶数组</text>
<rect x="20" y="28" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="64" y="28" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="108" y="28" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="152" y="28" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="196" y="28" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="240" y="28" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="42" y1="80" x2="42" y2="56" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="42.0,56.0 45.0,62.0 39.0,62.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="42" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">CAS</text>
<text x="42" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">无锁放入</text>
<rect x="152" y="76" width="44" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="174" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">N1</text>
<line x1="174" y1="54" x2="174" y2="76" stroke-width="1.2" stroke="currentColor"/>
<polygon points="174.0,76.0 172.0,72.0 176.0,72.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="152" y="116" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="174" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">N2</text>
<line x1="174" y1="102" x2="174" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="174.0,116.0 172.0,112.0 176.0,112.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="152" y="156" width="44" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="174" y="173" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">N3</text>
<line x1="174" y1="142" x2="174" y2="156" stroke-width="1.2" stroke="currentColor"/>
<polygon points="174.0,156.0 172.0,152.0 176.0,152.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="206" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">synchronized</text>
<text x="206" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只锁头节点</text>
<text x="206" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">get 不加锁</text>
</svg>
```

**细节。**

- 桶非空时，对桶头节点 `synchronized (f)`，在里面遍历链表追加或覆盖。
- `get` 完全不加锁：节点的 `val` 和 `next` 都是 `volatile`（写入后其他线程立刻可见）。
- 早期版本按段（`Segment`）加锁；现在只留一个不起作用的 `Segment` 类做序列化兼容。

**为什么。** 锁粒度从一段降到一个桶，两个线程只有写同一个桶才会互斥。

**对应 LeetCode：** 无直接对应的题
