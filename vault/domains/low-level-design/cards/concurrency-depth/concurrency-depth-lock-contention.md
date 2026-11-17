---
id: concurrency-depth-lock-contention
node: concurrency-depth.parallel-scaling
type: qa
step: 3
---
## Q
8 个线程各算一段，结果累加进共享变量。锁罩住整个任务、锁只罩住累加、每个元素都抢一次锁，三种写法的加速比差多少？

## A
**锁里只放合并：计算在锁外，累加先在本地**

- **实测（3.14t free-threaded，8 个线程，8 个任务各约 0.07 s 的纯 Python 计算）**：顺序 0.54 s；锁罩住整个任务 0.54 s（1.0 倍，等于串行）；只在累加时拿锁 0.12 s（4.5 倍）；
- **粒度太细**：每个线程做 20 万次 `total += 1`，每次都拿锁，0.15 s；每个线程先在局部变量里累加、最后拿一次锁合并，0.01 s，相差 15 倍：锁竞争的代价主要是线程互相等待和切换；
- **3.11 上的线程池**：三种写法都约 0.5 s，因为 GIL 本来就让纯 Python 计算串行，加不加这些锁都没有并行可言；这两个对比在有 GIL 的构建上看不出来；
- **规则**：持锁时间尽量短，持锁次数尽量少；每个 worker 先在本地算好，最后一次合并（这也是封闭的做法）；
- **量出来锁仍然是瓶颈时**：把一把锁拆成按 key 分片的几把，或把共享累加换成每个线程一个槽、最后求和。

```python
import threading

total, lock = 0, threading.Lock()

def worker(items):
    global total
    local = 0
    for x in items:
        local += x * x            # 计算和累加都在本地，不碰锁
    with lock:                    # 一次合并，持锁时间极短
        total += local

ts = [threading.Thread(target=worker, args=(range(i, 1000, 4),)) for i in range(4)]
[t.start() for t in ts]; [t.join() for t in ts]
print(total)                      # 332833500
```

**知识点：**并行加速与锁竞争（Parallel Speedup & Contention）
