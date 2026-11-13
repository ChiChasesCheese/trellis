---
id: li-compiler-kernels-what-is-kernel
node: compiler.kernels
type: qa
step: 1
---
## Q
GPU 上的"内核"（kernel）是什么？它是怎样被启动和并行执行的？用 Triton 写一个向量加法内核说明。

## A
**内核：** 在加速器上执行的一个函数。主机（CPU）上的程序发出"用多少个并行实例运行这个函数"的命令，GPU 上成千上万个线程同时执行同一段代码，各自处理数据的不同部分。

**启动结构：**
- **网格（grid）：** 一次启动的所有线程块（block）。
- **线程块：** 被分配到某一个 SM（流式多处理器，GPU 里的"大核"）上执行，块内的线程可以共享一块片上内存。
- 每个实例通过自己的编号（第几个块、块内第几个线程）算出该处理哪部分数据。

**Triton：** 用 Python 写 GPU 内核的语言和编译器，以"块"为单位编程，不必管理单个线程。PyTorch 的 `torch.compile` 默认后端就生成 Triton 内核。

```python
import triton
import triton.language as tl

@triton.jit
def add_kernel(x_ptr, y_ptr, out_ptr, n, BLOCK: tl.constexpr):
    pid = tl.program_id(0)                         # 第几个块
    offs = pid * BLOCK + tl.arange(0, BLOCK)       # 本块负责的下标
    mask = offs < n                                # 最后一块可能越界
    x = tl.load(x_ptr + offs, mask=mask)
    y = tl.load(y_ptr + offs, mask=mask)
    tl.store(out_ptr + offs, x + y, mask=mask)

def add(x, y):
    out = torch.empty_like(x)
    grid = (triton.cdiv(x.numel(), 1024),)         # 需要多少个块
    add_kernel[grid](x, y, out, x.numel(), BLOCK=1024)
    return out
```

**要点：**
- **`mask` 处理边界：** 数据长度不是 1,024 的倍数时，最后一块有一部分下标越界，必须屏蔽，否则读写到不属于自己的内存。忘了屏蔽是内核最常见的错误之一，只在长度不整除时出现。
- **启动是异步的：** CPU 发出启动命令后立即返回，GPU 稍后执行。内核里的错误可能在之后的某个同步点才报出来。
- **性能：** 向量加法每个元素读 2 个数、写 1 个数、算 1 次加法，完全受显存带宽限制。好的实现应接近显存峰值带宽，可以用 `triton.testing.do_bench` 测时间，再换算成实际带宽。
