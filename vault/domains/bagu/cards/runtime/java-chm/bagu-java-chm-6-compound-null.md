---
id: bagu-java-chm-6-compound-null
node: a.runtime.java-chm
type: qa
step: 4
---
## Q
**ConcurrentHashMap · 复合操作能保证原子吗，key 和 value 为什么不能为 null**｜必会

面试官：「用 ConcurrentHashMap 做在线用户的计数，先 get 再 put 加一，线程安全吗？它的 key 和 value 为什么不能是 null？」

## A
**基本回答。** 不安全。ConcurrentHashMap 只保证单个方法原子，「先 `get` 再 `put`」两步之间别的线程可能已改，两个线程都读到旧值、各写回加一，后写覆盖先写，丢一次。要用 `merge`、`compute`、`putIfAbsent`、`computeIfAbsent`，把读改写包进同一次桶锁。key 和 value 不允许 null：`get` 返回 null 时分不清是没有这个 key 还是值就是 null，单线程 HashMap 可以再 `containsKey` 补查，并发下两步之间状态可能变，补查无意义。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 276">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先 get 再 put 加一，初始值 5</text>
<text x="79" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程 1</text>
<text x="261" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程 2</text>
<rect x="19" y="44" width="120" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">get → 5</text>
<rect x="201" y="70" width="120" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="261.0" y="85.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">get → 5</text>
<rect x="19" y="96" width="120" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="111.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">put(6)</text>
<rect x="201" y="122" width="120" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="261.0" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">put(6)</text>
<line x1="170" y1="46" x2="170" y2="140" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="170.0,140.0 173.2,133.0 166.8,133.0" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="170" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时间</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两次加一，结果是 6，丢了一次</text>
<line x1="8" y1="202" x2="332" y2="202" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">merge(k, 1, Integer::sum)</text>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读改写整步在桶锁内完成，结果 7</text>
<text x="8" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">null：get 返回 null 分不清「没有」还是「值是 null」</text>
</svg>
上半：两个线程都读到 5，各自写回 6，一次加一丢了；下半：用 `merge`，整个读改写在桶锁内完成，结果是 7。
**业务场景。** 按用户统计请求次数做限流：先查再放，计数偏小，阈值被击穿。实测 8 个线程各对同一 key 加两万次，先 get 再 put 得 20323，应是 16 万；`m.merge(k, 1, Integer::sum)` 正好 16 万。
```java
// 错：get 与 put 之间别的线程可能已经改了
Integer v = m.get(k); m.put(k, v == null ? 1 : v + 1);
// 对：整个读改写在桶锁内原子完成
m.merge(k, 1, Integer::sum);
```
**容易错。**
- **computeIfAbsent 的函数在持桶锁时执行：** 要短、无副作用；里面修改同一个 map 会抛 `IllegalStateException: Recursive update` 或死锁，耗时计算会阻塞同桶其他操作。
