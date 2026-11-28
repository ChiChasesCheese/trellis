---
id: bagu-java-aqs-juc-1-aqs-latch-cf
node: b.runtime.java-aqs-juc
type: qa
step: 1
---
## Q
**AQS 与并发工具类 · CountDownLatch、Semaphore、CompletableFuture**｜追问

面试官：「AQS 的核心思想是什么？CountDownLatch、Semaphore、CyclicBarrier 有何区别？CompletableFuture 怎么编排并处理异常？」

## A
**基本回答。** AQS 是同步器的骨架：一个 `volatile int state` 加 FIFO 等待队列，抢不到就入队 park，释放时唤醒后继；子类只实现 `tryAcquire`/`tryRelease`。state 的含义因工具而异：Latch 是还没完成的事件数，Semaphore 是剩余许可数，ReentrantLock 是重入次数。CountDownLatch 一次性倒计数，减到 0 放行，不可重置；Semaphore 控制同时访问的许可数；CyclicBarrier 让 N 个线程互等、到齐一起走，可重复用。CompletableFuture 编排异步：`thenCombine` 合并两个结果，`allOf` 等全部，`exceptionally`/`handle` 兜底，`orTimeout`（JDK 9）设超时。默认用公共 ForkJoinPool，阻塞 IO 要传自定义线程池。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 186">
<rect x="8" y="12" width="324" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">state：volatile int，表示同步状态</text>
<text x="8" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">FIFO 等待队列：抢不到就入队 park</text>
<rect x="8" y="70" width="96" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 1 park</text>
<rect x="122" y="70" width="96" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 2 park</text>
<rect x="236" y="70" width="96" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 3 park</text>
<line x1="104" y1="84" x2="115" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122.0,84.0 115.0,87.2 115.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="218" y1="84" x2="229" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,84.0 229.0,87.2 229.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="120" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">释放时唤醒后继；子类只写 tryAcquire / tryRelease</text>
<rect x="8" y="132" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="148.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CountDownLatch</text>
<text x="60" y="163.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">state=N 倒数</text>
<rect x="118" y="132" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="148.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Semaphore</text>
<text x="170" y="163.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">state=许可数</text>
<rect x="228" y="132" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280" y="148.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ReentrantLock</text>
<text x="280" y="163.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">state=重入次数</text>
</svg>
AQS 的骨架：一个 state 加一条队列，底部三个工具对 state 的含义不同。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="8" y="12" width="110" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户服务</text>
<rect x="8" y="52" width="110" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单服务</text>
<rect x="8" y="92" width="110" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="63" y="111" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">优惠券服务</text>
<rect x="196" y="40" width="138" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="62.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">allOf / thenCombine</text>
<text x="265" y="77.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">汇总结果</text>
<line x1="118" y1="27" x2="189.439" y2="53.5606" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196.0,56.0 188.3,56.6 190.6,50.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="118" y1="67" x2="189.001" y2="66.0897" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196.0,66.0 189.0,69.3 189.0,62.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="118" y1="107" x2="189.495" y2="78.5853" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196.0,76.0 190.7,81.6 188.3,75.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">优惠券睡 2 秒 → orTimeout(300ms)</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ exceptionally 给兜底值</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">整体 404ms 返回</text>
</svg>
CompletableFuture 编排：三个下游并行，优惠券这一路设了 300 毫秒超时加兜底，整体不被慢的拖住。
**业务场景。** 详情接口并行调用用户、订单、优惠券三个服务，各用 CompletableFuture 加自定义线程池；优惠券睡 2 秒，设 `orTimeout(300ms)` 加 `exceptionally` 返回「无优惠券」，`allOf` 汇总，实测 404ms 返回。用 CountDownLatch 也能等齐，但拿不到返回值、不好处理异常，编排用 CompletableFuture 更顺手。
**容易错。**
- **在公共 ForkJoinPool 里跑阻塞 IO：** 会拖垮公共池。
- **异步任务不设超时和兜底：** 一个慢依赖拖住整个接口。
**相关。** 并发容器：`CopyOnWriteArrayList` 写时复制适合读多写少；有界 `BlockingQueue` 做背压；`DelayQueue` 按到期时间出队；Disruptor 快在预分配环形数组、无锁、避免伪共享（不同线程改同一缓存行里的不同变量而互相拖慢）。
