---
id: concurrency-depth-threads-release-gil
node: concurrency-depth.parallel-scaling
type: qa
step: 4
---
## Q
纯 Python 计算用线程池没有加速，为什么对一批大文件算 SHA-256 的线程池却能加速？worker 数该设多少？

## A
**线程能加速的是释放 GIL 的那部分：大块哈希、文件和网络 I/O**

- **`hashlib` 对大块数据释放 GIL**：文档写明，更新的数据超过 2047 字节时 GIL 被释放，C 代码在这段时间并行跑；读文件等 I/O 也释放；
- **实测（3.11，8 个 8 MB 缓冲区，8 个线程）**：一次 `update` 整块 4.3 倍；换成每次 64 字节的小 `update`，1.09 倍，因为大部分时间在 Python 字节码上持着 GIL；
- **所以块要大**：读文件用 1 MB 的块，不要逐行或逐字节；
- **worker 数跟瓶颈走**：本地固态盘，大概等于核数；机械盘多线程反而互相抢磁头，少开；网络盘或对象存储，瓶颈在服务端，可以开得更多，量一量再定；
- **在途任务要有上限**（示例没有限制，大批量要加）：一次把几十万个文件都 `submit`，所有未完成的 `Future` 都占内存。用信号量限制已提交未完成的数量，或者分批提交；
- **是计算还是等待**：换成进程池前先问，函数里大部分时间是 C 代码在算、还是在等；是前者，线程就够，省掉 pickle 和进程启动。

```python
import hashlib
from concurrent.futures import ThreadPoolExecutor

def file_digest(path, bufsize=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(bufsize):    # 大块：读和哈希都释放 GIL
            h.update(chunk)
    return h.hexdigest()

def digests(paths, workers=8):
    with ThreadPoolExecutor(workers) as ex:
        return dict(zip(paths, ex.map(file_digest, paths)))

print(digests([__file__])[__file__][:8])
```

**知识点：**并行加速与锁竞争（Parallel Speedup & Contention）
