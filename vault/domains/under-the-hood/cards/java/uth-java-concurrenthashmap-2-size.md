---
id: uth-java-concurrenthashmap-2-size
node: java.concurrenthashmap
type: qa
step: 2
---
## Q
**ConcurrentHashMap 怎么数元素个数**｜Java · OpenJDK 25

多线程同时 `put`，`size()` 用一个原子计数器行吗？`ConcurrentHashMap` 是怎么做的？

## A
**背景。** 每次 `put` 都要给元素个数加 1。如果所有线程都去改同一个原子计数器（原子，即一次改完、不会被打断），它们的 CAS 会撞在同一个内存位置上，不断失败重试。

**结构。** 一个 `baseCount` 加一个 `CounterCell[]` 数组：先 CAS 更新 `baseCount`；失败说明有竞争，就按线程随机探针选一个 `CounterCell` 单独累加。这就是 `LongAdder` 的思路。`size()` 把它们加起来。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<rect x="12" y="28" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T1</text>
<rect x="12" y="74" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T2</text>
<rect x="12" y="120" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T3</text>
<rect x="120" y="28" width="96" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="168" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">baseCount</text>
<text x="168" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先 CAS</text>
<line x1="56" y1="41" x2="120" y2="41" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,41.0 114.0,44.0 114.0,38.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="287" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CounterCell[]</text>
<rect x="252" y="74" width="70" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="287" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cell 0</text>
<rect x="252" y="108" width="70" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="287" y="125" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cell 1</text>
<rect x="252" y="142" width="70" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="287" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cell 2</text>
<line x1="56" y1="87" x2="252" y2="87" stroke-width="1.2" stroke="currentColor"/>
<polygon points="252.0,87.0 246.0,90.0 246.0,84.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="56" y1="133" x2="252" y2="121" stroke-width="1.2" stroke="currentColor"/>
<polygon points="252.0,121.0 246.2,124.4 245.8,118.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="150" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">竞争 分散累加</text>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">size() = baseCount + 所有 cell 之和</text>
</svg>
```

**细节。**

- `CounterCell` 标了 `@Contended`，各占自己的缓存行（CPU 缓存的最小单位），避免互相拖慢。
- `size()` 是 `baseCount` 加上所有单元的和，并发时只是近似值。
- 扩容多线程协助：每个线程领一段桶搬迁，每段至少 16 个。

**为什么。** 一个全局原子变量让所有线程的 CAS 撞在同一个缓存行上；分散计数把争用也分散了。

**对应 LeetCode：** 无直接对应的题
