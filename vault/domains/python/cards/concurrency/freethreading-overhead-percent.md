---
id: freethreading-overhead-percent
node: concurrency.free-threading
type: qa
source: python-docs
---
## Q
3.13 起可选的自由线程（free-threading，PEP 703）构建关闭了 GIL，它对单线程程序的性能有什么影响？

## A
自由线程构建执行 Python 代码时比默认（GIL 开启）构建多出额外开销，具体幅度依工作负载和硬件而定：在 pyperformance 基准套件上，平均开销从 macOS aarch64 上约 1% 到 x86-64 Linux 上约 8% 不等。这个开销主要来自把 GIL 提供的免费互斥换成了偏向引用计数（biased reference counting）等更细粒度的同步机制，是「关闭 GIL 换多核并行」的单线程代价。
