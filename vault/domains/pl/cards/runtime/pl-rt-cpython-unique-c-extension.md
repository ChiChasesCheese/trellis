---
id: pl-rt-cpython-unique-c-extension
node: runtime.cpython-internals
type: qa
step: 6
---
## Q
为什么 Python 写的程序在科学计算里并不慢？C 扩展为什么快，它又给 Python 带来了什么束缚？

## A
同样是对 2000 万个整数求和（本机一次测量）：

| 写法 | 每个元素的耗时 |
|---|---|
| Python `for` 循环 `s += i`（函数内） | 约 12.4 ns |
| 内置 `sum(range(N))` | 约 4.0 ns |
| 内置 `sum(list)` | 约 2.0 ns |
| NumPy `x.sum()`（连续的 int64 数组） | 约 0.32 ns |

快的原因逐层递进：
1. **内置 `sum`** 是 C 写的：循环在 C 里，不再有字节码分派，但元素仍是 Python 对象。
2. **NumPy** 把数据存成**连续的原生数组**（每个元素 8 字节，没有对象头），内核是编译好的 C，能向量化（SIMD）、缓存友好，一次调用处理整个数组。从“每个元素一个对象”变成“一块内存”，是数量级的差距（比 Python 循环快约 40 倍）。

这就是 Python 的**胶水语言**哲学：高层逻辑写 Python，热点下沉到 C/C++/Rust 内核（NumPy、PyTorch、pandas、cryptography）。Python 因此在数据科学与机器学习中成为主流，慢的部分不在热路径上。

**代价**：C API 暴露了解释器的内部细节（对象头布局、引用计数、GIL 的存在），大量扩展直接依赖。这使 CPython 难以改变自身：换内存管理、去掉 GIL、引入移动式 GC 或激进的 JIT，都会破坏这些扩展。所以 PyPy 兼容性有限，GIL 去除也花了二十年。

教训：生态一旦绑定到了实现细节，实现就被生态“冻结”。稳定的 ABI（Java 的 JNI 抽象了对象布局，Rust 的 C ABI 只导出函数）与庞大的生态之间有长期的张力。
