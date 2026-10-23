---
id: hl-os-cpu-affinity
node: foundations.os-processes-threads-ipc
type: qa
step: 9
---
## Q
低延迟系统的 CPU 亲和性（affinity）/ 绑核怎么做？Java 里怎么实现？

## A
绑核是限制线程只在指定核上跑（`taskset -c 3 java ...` 或 `sched_setaffinity`）。低延迟系统会：
1. **隔离**出专用核（内核参数 `isolcpus`、`nohz_full`）；
2. 把热线程绑上去；
3. 线程在核上**忙等（busy-spin）**，不阻塞不让出，没有调度延迟，缓存始终热。

Java 标准库没有绑核 API，常用 OpenHFT 的 Java-Thread-Affinity（JNA 调 `sched_setaffinity`）。
