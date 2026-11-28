%% trellis:begin %%
# 语言运行时与并发
*B 其余知识点*

Java、Go、Python 各自的集合、并发、GC 与调度模型。

## Topics
- [[domains/bagu/map/b.runtime.java-sync-lock|synchronized、ReentrantLock 与锁升级]]
- [[domains/bagu/map/b.runtime.java-volatile-cas-jmm|volatile、CAS 与 Java 内存模型（JMM, happens-before）]]
- [[domains/bagu/map/b.runtime.java-threadlocal|ThreadLocal 原理与内存泄漏]]
- [[domains/bagu/map/b.runtime.java-aqs-juc|AQS 与并发工具类（CountDownLatch, Semaphore, CompletableFuture, 并发容器）]]
- [[domains/bagu/map/b.runtime.java-jvm-memory-classload|JVM 内存区域、对象布局与类加载（双亲委派）]]
- [[domains/bagu/map/b.runtime.java-virtual-threads|虚拟线程（Virtual Thread, JDK 21）与现代 Java 特性]]
- [[domains/bagu/map/b.runtime.java-reflection-proxy-spi|反射、动态代理、SPI 与序列化]]
- [[domains/bagu/map/b.runtime.java-language-basics|Java 语言基础：String、equals/hashCode、异常、泛型、IO 模型]]
- [[domains/bagu/map/b.runtime.java-money-bigdecimal|金额计算：为什么不用 double，BigDecimal 与 Long（Money Representation）]]
- [[domains/bagu/map/b.runtime.java-deadlock-threads|线程基础与死锁（Thread Lifecycle, Deadlock）]]
- [[domains/bagu/map/b.runtime.go-channel-map|Go 的 channel 实现、select 与 map 并发安全]]
- [[domains/bagu/map/b.runtime.go-gc|Go 的垃圾回收（三色标记、写屏障、GOGC）]]
- [[domains/bagu/map/b.runtime.go-leak-mutex|goroutine 泄漏、Mutex 与常见并发题]]
- [[domains/bagu/map/b.runtime.go-language-pitfalls|Go 语言易错点：slice、new 与 make、内存逃逸、defer]]
- [[domains/bagu/map/b.runtime.py-gil|Python 的 GIL 是什么，怎么绕过]]
- [[domains/bagu/map/b.runtime.py-concurrency-choice|asyncio、多线程、多进程怎么选]]
%% trellis:end %%

## Notes
