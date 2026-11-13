---
id: li-compiler-kernels-kernel-perf-measure
node: compiler.kernels
type: qa
step: 4
---
## Q
怎样正确地测量一个 GPU 内核的耗时？为什么用 Python 的 `time.time()` 包住调用会测错？`triton.testing.do_bench` 做了哪些处理？

## A
**为什么 `time.time()` 测不准：** 内核（GPU 上执行的函数）的启动是**异步**的：CPU 发出启动命令后立即返回，GPU 稍后才执行。

```python
t0 = time.time(); out = my_kernel(x); t1 = time.time()   # 只测到了"发出命令"的时间
```

测到的可能只有十几微秒，和内核真正的执行时间无关。

**正确做法的要点：**
- **同步：** 计时前后调用 `torch.cuda.synchronize()`，等 GPU 真正做完。
- **用 GPU 事件计时：** `torch.cuda.Event(enable_timing=True)` 在 GPU 的时间线上打点，比 CPU 计时更精确，不包含 CPU 的调度抖动。
- **预热：** 第一次调用可能触发编译、自动调优、显存分配，不应计入。
- **多次重复取统计值：** 单次几十微秒的内核受抖动影响大，重复几十到几百次，取中位数或分位数。
- **清空 L2 缓存：** 连续重复调用时，输入数据已经在 L2 缓存（GPU 片上 50 MB 量级的缓存）里，测出来比真实场景快。每次调用前写一块大内存把缓存冲掉。

**`triton.testing.do_bench` 已经做了这些：**

```python
from triton.testing import do_bench
ms = do_bench(lambda: my_kernel(x), warmup=25, rep=100)   # 返回毫秒
bytes_moved = 3 * x.numel() * x.element_size()
print(f"{ms:.3f} ms, {bytes_moved / ms / 1e6:.1f} GB/s")
```

它会先预热、估算单次耗时、决定重复次数、每次调用前清空 L2，并用 GPU 事件计时。

**把耗时转换成有意义的数：**
- 受带宽限制的内核：实际带宽 = 读写字节数 ÷ 耗时，和显存峰值带宽比较。
- 受算力限制的内核：实际算力 = 运算次数 ÷ 耗时，和峰值算力比较。

**稳定测量环境：** 固定 GPU 时钟（`nvidia-smi -lgc`），避免降频；机器上不运行其他任务；记录驱动和库版本。

**在推理语境下：** 单个内核测得快，不代表整步快。还要用 Nsight Systems 看整步的时间线，确认内核之间没有大段空隙。
