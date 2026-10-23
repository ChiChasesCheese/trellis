---
id: hl-cache-jmh
node: foundations.cpu-cache-locality
type: qa
step: 32
---
## Q
为什么严肃的 Java 性能测量要用 JMH？自己写的粗糙基准有什么问题，面试里怎么引用自己测的数字？

## A
**JMH**（Java Microbenchmark Harness）处理预热、分叉进程、黑洞（blackhole）消费结果，避免 JIT 预热和死代码消除误导。

粗糙基准的问题：同一个 JVM 内取若干次最小值，没隔离其他进程、没绑核，只用 `volatile` 的 `sink` 防死代码消除，多次运行有 ±30% 以上波动（伪共享更大）。

面试说法：「我测过，量级是……，我知道这不是严谨的 JMH 结果」，比报一个精确但不可信的数字更好。
```java
@Benchmark public long sumLongArray() {
    long s = 0; for (long v : data) s += v; return s;
}
```
