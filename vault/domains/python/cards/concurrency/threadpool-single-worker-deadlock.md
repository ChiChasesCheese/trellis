---
id: threadpool-single-worker-deadlock
node: concurrency.executors
type: qa
source: python-docs
---
## Q
为什么 `ThreadPoolExecutor(max_workers=1)` 里，一个已提交的任务在自己内部又 `executor.submit(...)` 并调用 `.result()` 等待新任务的结果，会造成死锁？

## A
整个执行器只有一个工作线程。这个唯一的线程正在执行外层任务，外层任务里 `.result()` 会阻塞等待新提交的内层任务完成；但内层任务同样要排队等这个唯一的工作线程空闲下来才能被执行——而工作线程永远不会空闲，因为它正阻塞在 `.result()` 上。两者互相等待，谁都无法推进，本质是「单线程池里任务等待另一个任务的结果」这种自依赖导致的死锁，扩大 `max_workers` 或避免任务间相互等待可以规避。
