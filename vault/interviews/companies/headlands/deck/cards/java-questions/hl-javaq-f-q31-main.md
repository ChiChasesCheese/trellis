---
id: hl-javaq-f-q31-main
node: java-questions.f-concurrency
type: qa
step: 21
---
## Q
什么是虚拟线程（virtual thread）？它和平台线程有什么区别？什么时候不该用？
What are virtual threads? How do they differ from platform threads, and when should you NOT use them?

## A
一句话：虚拟线程是 JVM 调度的轻量线程，挂在少量**载体平台线程**上；阻塞操作（I/O、sleep、锁）时**卸载**载体线程让别人用，所以可以一个请求一个线程、同时有几十万个。

- **平台线程**：1 : 1 对应 OS 线程（栈约 1 MB 虚拟地址，创建 / 切换要进内核，数千个就吃力）。
- **虚拟线程**：M : N（栈是堆上可增长的对象，阻塞时被卸载，载体线程去跑别的虚拟线程）。
- **适合**：大量 I/O 阻塞的并发（每请求一线程的服务、扇出调用）。
- **不适合**：CPU 密集（核数才是限制）；长时间在 `synchronized` 内阻塞；依赖 `ThreadLocal` 缓存大对象；把它们放进池里。
