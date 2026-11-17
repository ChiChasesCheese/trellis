---
id: concurrency-depth-chunking
node: concurrency-depth.parallel-scaling
type: qa
step: 2
---
## Q
用 `ProcessPoolExecutor.map` 对 40 万个数各算一次平方，为什么比一个循环慢几千倍？任务应该切成多大？

## A
**每个任务要比一次进程间通信贵得多，所以分块**

- **实测（3.11，8 个进程，40 万个整数求平方和）**：顺序循环 0.006 s；`map(f, data)`（默认 `chunksize=1`）19.2 s；`chunksize=5000` 0.039 s；手工切 8 块、每块一次调用 0.004 s；
- **原因**：每个任务要序列化（pickle）参数、经管道发给 worker、再把结果传回。单个任务的计算只有几百纳秒，通信是它的几万倍；
- **经验值**：一个任务的计算至少几毫秒；块数取 worker 数的 2–4 倍，既让每个 worker 有活，又能吸收快慢不均；
- **块太大**：块数少于 worker 数，有人闲着；一个块特别慢，别人等它（尾巴效应）；
- **工作函数必须在模块顶层**（能被 pickle），参数和返回值也要能 pickle；macOS 和 Windows 用 spawn 启动，入口要放在 `if __name__ == "__main__"` 里；
- **进程之间不共享内存**：块是拷贝过去的，大数据用 `multiprocessing.shared_memory` 或让每个进程自己读文件。

```python
from concurrent.futures import ProcessPoolExecutor

def chunk_sum(chunk):
    return sum(x * x for x in chunk)

def parallel_sum_squares(data, workers=8):
    size = -(-len(data) // (workers * 4))          # 向上取整：约 4 倍 worker 数的块
    parts = [data[i:i + size] for i in range(0, len(data), size)]
    with ProcessPoolExecutor(workers) as ex:
        return sum(ex.map(chunk_sum, parts))

if __name__ == "__main__":
    print(parallel_sum_squares(list(range(1000))))   # 332833500
```

**知识点：**并行加速与锁竞争（Parallel Speedup & Contention）
