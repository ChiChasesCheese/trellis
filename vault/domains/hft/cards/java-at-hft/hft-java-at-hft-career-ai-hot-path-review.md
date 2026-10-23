---
id: hft-java-at-hft-career-ai-hot-path-review
node: java-at-hft.career-ai
type: qa
step: 2
---
## Q
为什么 AI 生成的 Java 代码在热路径上特别需要懂行的人审查？

## A
AI 常见的输出会用 Stream、`Optional`、`String.format`、`HashMap<Long, ...>`、每次调用都 `new` 对象，功能完全正确，但每次执行都产生垃圾。设每次调用产生 400 字节、每秒 100 万次，就是 400 MB/s 的垃圾，年轻代很快被填满，GC 每隔一两秒就来一次。

另一类问题是并发：随手加 `synchronized`，或把 `volatile` 当作能保证原子性，或者漏掉可见性保证，造成读线程永远看不到更新。

这些在单元测试里全部通过，只有在高负载下才暴露。需要懂 JIT、GC 和内存模型的人，才能一眼看出问题，并用分配统计和基准去验证。
