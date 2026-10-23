---
id: hl-j10-semaphore-limit
node: java21.j10-virtual-threads
type: qa
step: 10
---
## Q
原来用 `newFixedThreadPool(20)` 顺便限制了对下游网关的并发，换成虚拟线程每任务一个后怎么保持这个上限？写出代码。

## A
线程池的副作用是「线程数 = 并发上限」。去掉池后，限流要**显式**写，用信号量（`Semaphore`）：

```java
Semaphore inFlight = new Semaphore(20);
inFlight.acquire();            // 满了在此排队；虚拟线程阻塞很廉价
try { return gateway.fetch(sym); } finally { inFlight.release(); }
```
实验：500 个任务各调一次网关（模拟 50 ms），网关只允许 20 并发，最大同时在途恰为 20。重点是限流变成了显式、可读的一行，不是耗时数字。也可用大小为 20 的连接池或客户端并发限制代替。
