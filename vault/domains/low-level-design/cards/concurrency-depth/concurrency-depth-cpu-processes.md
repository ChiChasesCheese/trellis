---
id: concurrency-depth-cpu-processes
node: concurrency-depth.selection
type: qa
step: 2
---
## Q
批量处理图片的变换是纯 Python 代码，用线程池为什么没有加速？换成进程池要注意什么？

## A
**纯 Python 计算用进程池；任务要能 pickle，要够大**

- **线程池没用**：实测（3.11，8 个 800 万次循环的任务，12 核机器）线程池 2、4、8 个都是 0.98–1.01 倍，GIL 一次只让一个线程跑字节码；
- **进程池有用**：同样的任务 2、4、8 个进程是 1.99、3.52、5.54 倍，每个进程有自己的解释器和 GIL；
- **函数和参数要能 pickle**：`lambda`、嵌套函数、带锁的对象都不行，`ex.map(lambda ...)` 抛 `PicklingError`；函数要写在模块顶层；
- **启动有成本**：8 个进程启动加 8 个空任务约 0.07 s，线程池不到 1 ms；任务本身不到几十毫秒就别用进程池；
- **数据要拷贝**：大图片、大数组来回传输的开销可能比计算还大；传路径让 worker 自己读，或用 `multiprocessing.shared_memory`；
- **例外**：函数里的主要工作在释放 GIL 的 C 库里（`hashlib`、`zlib`、`numpy` 的大数组运算），线程就够，不用付进程的代价；3.14t（free-threaded）上纯 Python 的线程池 8 线程也有 4.3 倍。

```python
from concurrent.futures import ProcessPoolExecutor

def heavy(n):                      # 模块顶层的函数才能被 pickle
    return sum(i * i for i in range(n))

if __name__ == "__main__":        # spawn 启动方式要求入口有这个保护
    with ProcessPoolExecutor(4) as ex:
        print(list(ex.map(heavy, [10, 100, 1000])))   # [285, 328350, 332833500]
        try:
            list(ex.map(lambda n: n, [1]))            # lambda 不能 pickle
        except Exception as e:
            print(type(e).__name__)                   # PicklingError
```

**知识点：**线程、进程与协程的选择（Choosing a Model）
