---
id: performance-mem-bound-inflight
node: performance.memory
type: qa
step: 4
---
## Q
图片处理服务用线程池，一次把一万张图全部 `submit` 进去，内存还是被撑爆了，哪怕 `max_workers` 只有 4。为什么？预算怎么估、怎么限住？

## A
**内存取决于“在途”的数量，不是线程数：要限制已提交未完成的任务**

- **池的队列是无界的**：`submit` 立刻返回，任务和它携带的数据都排在队列里；一万张图的原始字节全在内存；
- **解码后的体积远大于文件**：一张 8000 × 6000 的 RGB 图，解码后是 8000 × 6000 × 3 = 144,000,000 字节；
- **预算要算解码后的峰值**：峰值 ≈ 在途个数 × 单个最大体积；上限 4 个在途、每个 144 MB，就是约 576 MB；
- **提交处加信号量**：`acquire` 之后才 `submit`，任务完成的回调里 `release`；满了就让生产者等；
- **生产里要量的是**：解码缓冲、输出缓冲、结果表、整个进程的 RSS（驻留内存）峰值，而不是只数输入文件大小。

```python
import threading, concurrent.futures as cf

def run_all(items, work, workers=2):
    slots = threading.BoundedSemaphore(workers * 2)   # 已提交未完成的上限
    with cf.ThreadPoolExecutor(workers) as ex:
        futs = []
        for it in items:
            slots.acquire()                           # 满了就在这里等
            f = ex.submit(work, it)
            f.add_done_callback(lambda _: slots.release())
            futs.append(f)
    return [f.result() for f in futs]

print(run_all(range(6), lambda i: i * i))   # [0, 1, 4, 9, 16, 25]
```

**知识点：**减少分配（Reducing Allocation）
