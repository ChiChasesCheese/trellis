---
id: threadpool-max-workers-default
node: concurrency.executors
type: qa
source: python-docs
---
## Q
`ThreadPoolExecutor` 不显式传 `max_workers` 时的默认线程数是多少（3.8+）？为什么这样设计？

## A
默认是 `min(32, os.cpu_count() + 4)`（3.13 起用 `os.process_cpu_count()`）。设计理由：`ThreadPoolExecutor` 主要用于重叠 I/O 等待，而不是 CPU 计算，所以工作线程数理应比 CPU 核数更多，公式里的 `+4` 保证即使在 1 核机器上也至少有约 5 个线程可用于 I/O 密集任务；同时封顶 32，避免在核数很多的机器上隐式创建过多线程占用资源。
