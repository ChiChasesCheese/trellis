---
id: hft-java-memory-model-lazyset
node: java.memory-model
type: qa
step: 4
---
## Q
为什么 `setRelease`（也叫 `lazySet`）比 `volatile` 写便宜？交易系统里用在哪？

## A
`volatile` 写要多禁止一种重排：“写之后的读不能越到写之前”（StoreLoad），CPU 必须排空写缓冲，x86 上要一条全栅栏指令，约十几到几十个周期。

`setRelease` 只保证“它之前的操作不会晚于它变得可见”。x86 本来就不重排“读读、写写、读写”，所以 release 写和 acquire 读在 x86 上就是普通的 `mov`，只约束编译器，没有 CPU 栅栏开销。（在 ARM 上差别没有 x86 这么大。）

典型用法：单生产者先把数据写进环形缓冲区的槽位，再用 `setRelease` 发布序号；消费者用 `getAcquire` 读到序号，就一定能看到槽位里的数据。Disruptor 发布序号的思路就是这样。
