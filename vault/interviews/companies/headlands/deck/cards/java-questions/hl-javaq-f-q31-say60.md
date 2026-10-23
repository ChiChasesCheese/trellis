---
id: hl-javaq-f-q31-say60
node: java-questions.f-concurrency
type: qa
step: 36
---
## Q
用英文 60 秒回答：What are virtual threads? How do they differ from platform threads, and when should you NOT use them?

## A
结构：JVM 调度到少量载体线程、阻塞时卸载 → 实测 10 万个线程约 1.6 秒 → 不适合 CPU 密集、不要池化、21 里 synchronized 会 pin → 低延迟热路径仍用绑核的平台线程。

> "Virtual threads, final in Java 21, are threads scheduled by the JVM onto a small pool of carrier threads. When one blocks on I/O, sleep or a lock, it's unmounted so the carrier can run another, which makes thread-per-request affordable at hundreds of thousands of threads. I ran 100,000 virtual threads each sleeping a second and it finished in about 1.6 seconds, whereas a 200-thread pool took 11 seconds for just 2,000 such tasks. They don't help CPU-bound work, you shouldn't pool them, and in 21 blocking inside `synchronized` pins the carrier. For a latency-critical hot path I'd still use dedicated pinned platform threads; virtual threads fit I/O-heavy infrastructure."
