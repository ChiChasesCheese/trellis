---
id: hft-java-disruptor-padding
node: java.disruptor
type: qa
step: 3
---
## Q
Disruptor 的 `Sequence` 对象为什么要在前后填充（padding）？

## A
生产者的游标和各消费者的序号，是被不同 CPU 核频繁写入的 `long`。如果两个序号落在同一条 64 字节缓存行（一条缓存行能放 8 个 `long`），一个核写它，就会让另一个核缓存里的这一整行失效，两个核反复争夺同一条缓存行，这叫**伪共享**（false sharing），每次可能额外耗费数十到上百纳秒，明明各写各的变量却互相拖慢。

Disruptor 在每个序号的 `value` 前后各垫了 7 个 `long`（共 56 字节），保证每个序号独占一整条缓存行，别的变量落不到同一行。JDK 里的 `@Contended` 注解是同样思路的官方写法。这类优化不改变逻辑，只改变内存布局，所以只有测量才能发现。
