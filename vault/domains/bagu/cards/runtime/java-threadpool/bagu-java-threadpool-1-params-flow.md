---
id: bagu-java-threadpool-1-params-flow
node: a.runtime.java-threadpool
type: qa
step: 1
---
## Q
**线程池 · 核心参数和任务执行流程**｜必会

面试官：「说一下 ThreadPoolExecutor 有哪些参数？提交一个任务进来，线程池按什么顺序处理？」

## A
**基本回答。** 七个参数：`corePoolSize`、`maximumPoolSize`、`keepAliveTime` 加单位（非核心线程空闲多久回收）、`workQueue`、`threadFactory`（可给线程命名）、`handler`（拒绝策略）。顺序是「先入队，再扩线程」：线程数小于核心数就新建；否则入队；队列满且线程数小于最大数才新建非核心线程；还满就拒绝。队列优先吸收突发，所以无界队列时最大线程数永远不生效。`execute` 抛的异常让线程终止并打印；`submit` 的异常被包进 `Future`，不调 `get` 就静默吞掉。`shutdown()` 不再收新任务并等已有的做完，`shutdownNow()` 尝试中断执行中的并返回队列里未执行的。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 318">
<rect x="8" y="6" width="130" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="73.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交一个任务</text>
<line x1="73" y1="32" x2="73" y2="48" stroke-width="1.2" stroke="currentColor"/>
<polygon points="73.0,48.0 76.2,41.0 69.8,41.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="48" width="130" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="73.0" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程数 &lt; 核心数？</text>
<line x1="138" y1="64" x2="190" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,64.0 183.0,60.8 183.0,67.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="164" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是</text>
<rect x="190" y="48" width="142" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="261.0" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新建核心线程</text>
<line x1="73" y1="80" x2="73" y2="106" stroke-width="1.2" stroke="currentColor"/>
<polygon points="73.0,106.0 76.2,99.0 69.8,99.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="80" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">否</text>
<rect x="8" y="106" width="130" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="73.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列没满？</text>
<line x1="138" y1="122" x2="190" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,122.0 183.0,118.8 183.0,125.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="164" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是</text>
<rect x="190" y="106" width="142" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="261.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">放入队列等待</text>
<line x1="73" y1="138" x2="73" y2="164" stroke-width="1.2" stroke="currentColor"/>
<polygon points="73.0,164.0 76.2,157.0 69.8,157.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="80" y="156" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">否</text>
<rect x="8" y="164" width="130" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="73.0" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程数 &lt; 最大数？</text>
<line x1="138" y1="180" x2="190" y2="180" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,180.0 183.0,176.8 183.0,183.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="164" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是</text>
<rect x="190" y="164" width="142" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="261.0" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新建非核心线程</text>
<line x1="73" y1="196" x2="73" y2="222" stroke-width="1.2" stroke="currentColor"/>
<polygon points="73.0,222.0 76.2,215.0 69.8,215.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="80" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">否</text>
<rect x="8" y="222" width="130" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="73.0" y="241.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拒绝策略 handler</text>
<text x="8" y="276" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">核心 2、最大 4、队列 2 的实测：</text>
<text x="8" y="294" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1、2 占核心；3、4 入队；5、6 新线程</text>
<text x="8" y="312" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 7 个被拒绝</text>
</svg>
任务从上往下过三道关：核心线程没满就新建；队列没满就入队（高亮，最容易记反）；队列满了再看能不能扩到最大线程数；都不行才拒绝。
**举个例子。** 核心 2、最大 4、队列 2，任务都执行很久（实测）：任务 1、2 各新建一个核心线程；3、4 入队，队列满；5、6 新建非核心线程，线程数到 4；第 7 个线程全忙且队列满，触发拒绝，默认抛 `RejectedExecutionException`。换成无界队列，3 之后全入队，永远走不到 5，最大线程数 4 成摆设。
**业务场景。** 通知服务发短信，核心 20、队列 200、最大 40：促销时请求先占满队列再扩到 40 线程，超出才拒绝，而不是无限堆积。
**容易错。**
- **以为先扩到最大线程数再入队：** 顺序反了，队列满了才扩线程。
