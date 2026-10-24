---
id: pl-rt-startup-pitfall-container-heap
node: runtime.startup-footprint
type: qa
step: 9
---
## Q
为什么 Java 或 Go 服务在容器里常被 OOM Kill（内存超限被杀），而代码里并没有内存泄漏？

## A
容器给进程设一个内存上限（cgroup limit），进程的 RSS 一超过就被内核杀掉。垃圾回收型运行时的内存**不是随用随还**：它会在回收之前让垃圾占着余量，再加上堆外内存，峰值很容易超过你估计的“数据大小”。

用同一个测试可以看出（持有 200 MB 活跃数据，再丢弃 2 GB 的临时缓冲，一次测量）：
```java
List<byte[]> keep = new ArrayList<>();
for (int i = 0; i < 200; i++) keep.add(new byte[1 << 20]);   // 200 MB live
for (int i = 0; i < 2000; i++) sink = new byte[1 << 20];     // 2 GB of garbage
```
- `java Live`（默认参数）：峰值 RSS 约 2176 MB；
- `java -Xmx300m Live`：约 201 MB；
- Go 同样的负载：默认约 510 MB；`GOMEMLIMIT=250MiB` 约 243 MB。

默认的堆上限是物理内存（或容器限额）的 1/4：本机 16 GB 内存，所以允许长到 4 GB，垃圾在回收前一直占着。在 512 MB 的容器里默认堆上限只有约 128 MB，活跃数据 200 MB 放不下，直接 `OutOfMemoryError`；于是很多人把 `-Xmx` 调到接近容器限额（比如 `-Xmx512m`），再叠加堆外内存，就越过限额被内核杀掉。

常见原因清单：
1. **`-Xmx` 设得接近容器限额**（或没设而宿主机很大、运行时看不到限额），忘了堆外内存：线程栈（每线程约 1–2 MB）、元空间、直接缓冲区、JIT 代码缓存、原生库。经验：堆设为限额的 60–75%。
2. **线程太多**：每个线程有栈，1000 个平台线程约 1–2 GB 虚拟地址、数百 MB 常驻。
3. **Go 的 GC 余量**：活跃数据 × 2 加上栈和运行时，不设 `GOMEMLIMIT` 就可能越过限额。
4. **Python 的碎片和小对象**：分配器不总把内存还给系统，RSS 只升不降。
5. **监控指标错位**：看堆使用量而不是进程 RSS，两者差了一大截。

诊断方法：监控 RSS 而不是堆；Java 开启原生内存跟踪（`-XX:NativeMemoryTracking=summary`）；Go 看 `runtime.MemStats` 的 `Sys`；压测时用接近生产的限额跑。
