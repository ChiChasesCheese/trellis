---
id: hft-java-garbage-free-verify
node: java.garbage-free
type: qa
step: 4
---
## Q
怎样验证一段 Java 热路径真的是零分配，而不是凭感觉相信？

## A
因为逃逸分析不保证生效，必须测量，常见四种办法：
- 用 `ThreadMXBean.getThreadAllocatedBytes`：循环前后各读一次当前线程已分配字节数，差值应为 0，可以写成单元测试，防止以后有人改坏；
- 用 JFR 的分配事件，看是谁在分配；
- 看 GC 日志：稳态下 `-Xlog:gc` 不应再出现年轻代回收；
- 用 JMH 的 `-prof gc`，看 `gc.alloc.rate.norm`（每次操作分配的字节数）。

一个实验里，用这种方法测出开启逃逸分析时每次约 0.3 字节，关闭后每次 32 字节，一眼就能分出有没有真正零分配。
