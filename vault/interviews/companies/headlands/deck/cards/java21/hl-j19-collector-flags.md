---
id: hl-j19-collector-flags
node: java21.j19-runtime-zgc-jit
type: qa
step: 8
---
## Q
JDK 21 里选择 G1、ZGC、分代 ZGC、Parallel、Epsilon 各写什么参数？哪个是容易漏的陷阱？

## A
| 参数 | 含义 |
|---|---|
| `-XX:+UseG1GC` | G1，JDK 21 默认 |
| `-XX:+UseZGC` | ZGC，**JDK 21 里默认是非分代的老版本** |
| `-XX:+UseZGC -XX:+ZGenerational` | **分代 ZGC**，JDK 21 要两个都写（默认 `ZGenerational = false`） |
| `-XX:+UseParallelGC` | 吞吐优先，不适合低延迟 |
| `-XX:+UseEpsilonGC` | 不回收的「空」收集器，用于短命进程或基准测试 |

陷阱：只写 `-XX:+UseZGC` 在 21 得到旧的非分代版本。测试运行命令 `java --enable-preview -XX:+UseZGC -XX:+ZGenerational ...`。
