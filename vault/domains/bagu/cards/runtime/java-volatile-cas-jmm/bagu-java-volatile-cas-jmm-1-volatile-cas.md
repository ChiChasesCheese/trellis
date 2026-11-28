---
id: bagu-java-volatile-cas-jmm-1-volatile-cas
node: b.runtime.java-volatile-cas-jmm
type: qa
step: 1
---
## Q
**volatile、CAS 与 happens-before**｜必会

面试官：「volatile 做了什么？能保证 `count++` 线程安全吗？CAS 有什么问题？」

## A
**基本回答。** volatile 保证可见性（写立即刷到主内存，读时重新取）和禁止重排序（内存屏障），不保证复合操作原子：`count++` 是读、加、写三步，会丢更新。典型用途是停止标志，以及双重检查单例的 `instance` 必须 volatile：`new` 分配内存、初始化、赋引用三步可能被重排成先赋引用，别的线程会看到没初始化完的对象。happens-before：前一操作的结果对后一操作可见，如解锁先于后续对同一把锁的加锁，volatile 写先于后续读，`start` 前的操作先于线程内的操作。CAS 是 CPU 原子指令：当前值等于期望值才更新，`AtomicInteger` 靠它无锁自增。CAS 的问题：ABA（A→B→A 看不出，用 `AtomicStampedReference` 加版本号）、高竞争自旋耗 CPU（写多读少的计数器用 `LongAdder` 分段累加）、一次只能改一个变量。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">count 初始 5，两个线程各 count++ 一次</text>
<text x="66" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程 A</text>
<text x="166" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程 B</text>
<text x="274" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">内存 count</text>
<text x="8" y="63" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">①</text>
<rect x="24" y="44" width="84" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="66" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读到 5</text>
<rect x="236" y="44" width="76" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="274" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="8" y="99" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">②</text>
<rect x="124" y="80" width="84" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="166" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读到 5</text>
<rect x="236" y="80" width="76" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="274" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="8" y="135" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">③</text>
<rect x="24" y="116" width="84" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="66" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">算 6 并写回</text>
<rect x="236" y="116" width="76" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="274" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="8" y="171" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">④</text>
<rect x="124" y="152" width="84" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="166" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">算 6 并写回</text>
<rect x="236" y="152" width="76" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="274" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="8" y="204" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">两次 ++，结果是 6，丢了一次更新</text>
<text x="8" y="224" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">volatile 保证可见，但不保证读—改—写原子</text>
<text x="8" y="242" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">CAS：期望值 5 才写 6，否则重试</text>
</svg>
两个线程都读到 5，各自算出 6，先后写回；最终内存是 6 而不是 7，丢了一次更新。
**举个例子。** 实测（JDK 25）：8 线程各 `++` 10 万次，期望 800000。`volatile int` 只得 257826；`AtomicInteger` 和 `LongAdder` 都是 800000。Atomic 的自增是：读 5，CAS(5→6)，别人已改成 6 则失败，重读再 CAS(6→7)。
**业务场景。** 播放计数在本机用 `LongAdder` 累加再批量写 Redis；用 volatile int 统计条数会丢更新。
**容易错。**
- **用 volatile 做计数器：** 要用 `AtomicInteger` 或 `LongAdder`。
