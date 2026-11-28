---
id: bagu-java-sync-lock-1-sync-vs-reentrantlock
node: b.runtime.java-sync-lock
type: qa
step: 1
---
## Q
**synchronized 与 ReentrantLock · 区别和锁升级**｜必会

面试官：「synchronized 和 ReentrantLock 有什么区别？synchronized 的锁升级是什么过程？」

## A
**基本回答。** synchronized 是 JVM 关键字，自动释放；ReentrantLock 基于 AQS，必须在 `finally` 里 `unlock`。两者都可重入。ReentrantLock 多了可中断获取（`lockInterruptibly`）、超时 `tryLock(timeout)`、可选公平锁、多个 `Condition`；JDK 6 之后性能接近，默认用 synchronized。synchronized 锁升级：无竞争时在 mark word 记偏向线程（JDK 15 起默认关闭）；轻微竞争升轻量级锁，CAS 自旋、不阻塞；竞争加重膨胀为重量级锁，借操作系统互斥量，抢不到的线程阻塞；竞争期间只升不降。AQS 是一个 `volatile int state` 加 FIFO 等待队列，失败的线程入队并 park，释放时唤醒后继；`Semaphore`、`CountDownLatch` 同样基于 AQS。
**2026 亮点。** JDK 21 虚拟线程在 `synchronized` 块内阻塞会钉住载体线程（pinning），JDK 24 才修复，配合虚拟线程的代码优先用 ReentrantLock。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 330">
<text x="8" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">synchronized 锁升级（竞争越重，锁越重）</text>
<rect x="8" y="26" width="324" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">偏向：无竞争，mark word 记线程</text>
<text x="170" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">JDK 15 起默认关闭</text>
<line x1="170" y1="66" x2="170" y2="81" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,88.0 166.8,81.0 173.2,81.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">出现竞争</text>
<rect x="8" y="88" width="324" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="104.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">轻量级锁：CAS 自旋抢锁</text>
<text x="170" y="119.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程不阻塞，一直试</text>
<line x1="170" y1="128" x2="170" y2="143" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,150.0 166.8,143.0 173.2,143.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">竞争加重</text>
<rect x="8" y="150" width="324" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="166.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重量级锁：操作系统互斥量</text>
<text x="170" y="181.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">抢不到的线程阻塞</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">AQS（ReentrantLock 的底层）</text>
<rect x="8" y="234" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="252" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">state：volatile int（0 = 没人持有）</text>
<rect x="8" y="274" width="96" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="292" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 1 park</text>
<rect x="122" y="274" width="96" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="292" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 2 park</text>
<rect x="236" y="274" width="96" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284" y="292" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 3 park</text>
<line x1="104" y1="288" x2="115" y2="288" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122.0,288.0 115.0,291.2 115.0,284.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="218" y1="288" x2="229" y2="288" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236.0,288.0 229.0,291.2 229.0,284.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="322" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">FIFO 队列：抢不到入队，释放时唤醒后继</text>
</svg>
上半部分是 synchronized 的锁升级，从轻到重；下半部分是 ReentrantLock 底层的 AQS：一个 state 加一条等待队列。
**举个例子。** 拍卖系统两个线程对拍品 A 出价：线程 1 独占时几乎无开销；线程 2 来了就原地 CAS 自旋，线程 1 很快释放，没有线程切换；持锁变长后自旋白耗 CPU，锁膨胀为重量级，线程 2 阻塞等唤醒。线程 2 想「等 100 毫秒拿不到就放弃」要用 `tryLock(100, MILLISECONDS)`，synchronized 做不到。
```java
lock.lock();
try {
    // 临界区
} finally {
    lock.unlock();   // 必须在 finally 里，否则异常时锁永远不释放
}
```
**容易错。**
- **用 synchronized 做多实例互斥：** JVM 锁只在单个进程内有效，集群里库存扣减会超卖，要用分布式锁或数据库乐观锁（version 字段，冲突少时好；悲观锁冲突多时好）。
- **以为 synchronized 一上来就是重量级锁：** 无竞争时只是在 mark word 记一笔。
