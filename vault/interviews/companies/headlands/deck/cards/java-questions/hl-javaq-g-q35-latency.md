---
id: hl-javaq-g-q35-latency
node: java-questions.g-os
type: qa
step: 6
---
## Q
缺页、透明大页（THP）、swap、OOM killer 各怎么影响 Java 服务的延迟或存活？容器被杀而堆正常怎么解释？
Container is OOM-killed but the heap was fine. Why? What is a TLB miss?

## A
- **缺页与低延迟**：堆里新页首次触碰要内核清零，运行中偶发延迟；`-XX:+AlwaysPreTouch`（默认 false）把代价挪到启动期。
- **THP**：减少 TLB 未命中，但内核做页合并时可能造成停顿，是否开启要测。
- **TLB miss**：页表项不在 TLB 缓存里，要走页表遍历；大页减少 miss。
- **swap**：延迟敏感系统一般关掉或用 `mlock` 锁内存，页被换出一次就是毫秒级停顿。
- **OOM killer**：容器里 RSS 超过 cgroup 限制会被内核杀（不是 `OutOfMemoryError`）；所以 `-Xmx` 要小于容器限制并留出堆外 / 线程空间，用 NMT 排查。
- **page cache 对 Java 的意义**：读刚写过的文件很快（31 MB 重读 11 ms）；mmap 直接把 page cache 映射进进程。
