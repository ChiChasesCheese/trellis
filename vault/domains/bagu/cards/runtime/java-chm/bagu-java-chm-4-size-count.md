---
id: bagu-java-chm-4-size-count
node: a.runtime.java-chm
type: qa
step: 5
---
## Q
**ConcurrentHashMap · size 怎么计数，baseCount 和 CounterCell 是什么**｜追问

面试官：「ConcurrentHashMap 的元素个数是怎么维护的？为什么不直接用一个 AtomicInteger？」

## A
**基本回答。** 用 `baseCount` 加 `CounterCell[]`，和 `LongAdder` 同一思路。无竞争时 CAS 直接给 `baseCount` 加一；CAS 失败说明有竞争，按线程散列到某个 cell 上加，不再抢同一个变量（所有线程 CAS 一个 AtomicInteger 会大量失败自旋，白耗 CPU）。`size()` 是 `baseCount` 加所有 cell 之和，要遍历求和，并发修改时只是估计值，所以更推荐返回 long 的 `mappingCount()`。计数结果还会触发扩容检查。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">三个线程同时加一</text>
<rect x="8" y="30" width="64" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40.0" y="47.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 1</text>
<rect x="8" y="78" width="64" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40.0" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 2</text>
<rect x="8" y="126" width="64" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 3</text>
<rect x="170" y="26" width="160" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">baseCount</text>
<text x="250.0" y="53.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">无竞争时直接 CAS</text>
<line x1="72" y1="44" x2="168" y2="42" stroke-width="1.2" stroke="currentColor"/>
<polygon points="168.0,42.0 160.9,38.9 161.1,45.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="120" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先试</text>
<text x="170" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CounterCell[]：竞争时分摊</text>
<rect x="170" y="92" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="194.0" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c0</text>
<rect x="226" y="92" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250.0" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c1</text>
<rect x="282" y="92" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="306.0" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c2</text>
<line x1="72" y1="92" x2="168" y2="106" stroke-width="1.2" stroke="currentColor"/>
<polygon points="168.0,106.0 161.5,101.8 160.6,108.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="72" y1="140" x2="224" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="224.0,122.0 216.7,119.6 217.4,126.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">CAS 失败 = 有竞争，线程按散列选一个 cell 加</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">size() = baseCount + 所有 cell 之和</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">求和时别人还在改，所以只是估计值</text>
</svg>
线程 1 先试主计数 baseCount；线程 2、3 遇到竞争，分别散列到 c0、c1 上加；总数是主计数加所有 cell。
**业务场景。** 三个线程同时放元素：线程 1 CAS 把 baseCount 从 0 改 1 成功，线程 2、3 CAS 失败，分别散列到 c0、c1 各加 1，互不等待；size = 1+1+1 = 3，边写边算时只是估计。指标服务每秒几十万次计数，所有线程 CAS 同一个 AtomicLong 会吃掉大量 CPU，换 LongAdder 写吞吐明显提高，只在周期上报时求和，仪表盘看趋势容忍近似。
**容易错。**
- **以为 LongAdder 处处更好：** 读要遍历求和，读频繁或需要精确原子读写时用 `AtomicLong`。
