---
id: bagu-java-threadpool-4-executors-pitfall
node: a.runtime.java-threadpool
type: qa
step: 4
---
## Q
**线程池 · 为什么不推荐 Executors 内置线程池**｜必会

面试官：「Executors.newFixedThreadPool 用起来很方便，为什么很多规范禁止用？」

## A
**基本回答。** `newFixedThreadPool` 和 `newSingleThreadExecutor` 用无界的 `LinkedBlockingQueue`，任务堆积撑爆内存；`newCachedThreadPool` 最大线程数是 `Integer.MAX_VALUE`，突发时创建海量线程。无界队列把过载变成内存无限增长、延迟无限变长，永远看不到拒绝、触发不了扩线程，推迟到 OOM。生产直接 `new ThreadPoolExecutor`：有界队列加明确的拒绝策略，让过载时快速失败、调用方降级或重试；线程工厂命名（如 `notify-sender-%d`），`jstack` 里一眼看出是哪个池；拒绝次数、队列长度接近上限就告警。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 276">
<rect x="8" y="8" width="324" height="58" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="25.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">newFixedThreadPool、newSingleThreadExecutor</text>
<text x="170.0" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列无界（LinkedBlockingQueue）</text>
<text x="170.0" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">任务堆积，内存撑爆，OOM</text>
<rect x="8" y="78" width="324" height="58" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">newCachedThreadPool</text>
<text x="170.0" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最大线程数 = Integer.MAX_VALUE</text>
<text x="170.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">突发时创建海量线程</text>
<line x1="170" y1="136" x2="170" y2="152" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,152.0 173.2,145.0 166.8,145.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="152" width="324" height="58" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="169.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">生产：直接 new ThreadPoolExecutor</text>
<text x="170.0" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有界队列 + 命名的线程工厂</text>
<text x="170.0" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+ 明确的拒绝策略</text>
<text x="8" y="234" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">无界队列让过载变成内存无限增长</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">永远看不到拒绝，问题被推迟到 OOM</text>
</svg>
前两个方法各藏着一个「无上限」：一个是队列，一个是线程数；最后高亮的是生产里该用的写法。
**举个例子。** 调度系统执行节点用 `newFixedThreadPool`：下游变慢后线程全被占住，新任务进无界队列，没有拒绝、没有告警，堆到几百万个任务对象，Full GC 越来越频繁，最后 OOM。换成有界队列后，满了就拒绝，节点回报调度器重新分配，几十个任务积压时问题就暴露了。
**容易错。**
- **以为无界队列是「不会丢任务」：** 它只是把问题推迟到 OOM。
- **只换有界队列、不设拒绝策略：** 默认抛异常，调用方不处理也会出事，要明确设计。
