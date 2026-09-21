---
id: threads-creation-cost
node: concurrency.threads
type: qa
source: python-docs
---
## Q
为什么面对大量短任务时，不建议每个任务都 `threading.Thread(...).start()`，而是用线程池？

## A
每次 `start()` 都会向操作系统申请一个真实的系统线程，涉及内核态的线程创建与销毁系统调用，开销明显高于普通函数调用；任务量大、单个任务又很短时，创建/销毁线程的开销可能超过任务本身的执行时间。线程池（如 `ThreadPoolExecutor`）预先建好一组线程并复用，避免了反复创建销毁的成本，也能限制并发线程数量。
