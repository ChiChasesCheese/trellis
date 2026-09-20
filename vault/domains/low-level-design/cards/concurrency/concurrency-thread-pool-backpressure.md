---
id: concurrency-thread-pool-backpressure
node: concurrency.patterns
type: qa
step: 4
---
## Q
持续往一个固定大小的 `ThreadPoolExecutor` 里 `submit()` 任务，提交速度远超处理速度，会发生什么？怎么加上背压（backpressure）？

## A
`ThreadPoolExecutor` 的内部任务队列没有容量上限，`submit()` 从不因为"排队太多"而拒绝或阻塞——它会一直接受新任务，队列在内存里无限堆积，延迟越排越长，最终可能把进程内存耗尽，而且这个过程在爆掉之前是"看不见"的，因为每次 `submit()` 都正常返回。

加背压的标准做法是在 `submit()` 前面挡一个有界信号量：

```python
sem = threading.Semaphore(max_workers * 2)

def submit_bounded(pool, fn, *args):
    sem.acquire()
    fut = pool.submit(fn, *args)
    fut.add_done_callback(lambda _: sem.release())
    return fut
```

`sem.acquire()` 在积压任务达到上限时阻塞提交者本身，让生产速度被处理速度自然拖住，而不是让队列无限增长。
