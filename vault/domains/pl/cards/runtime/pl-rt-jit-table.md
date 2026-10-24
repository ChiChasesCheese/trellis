---
id: pl-rt-jit-table
node: runtime.jit
type: qa
step: 6
---
## Q
Java（HotSpot）、Python（CPython、PyPy）、Go、Rust、C++ 在 JIT 与 AOT 上各选了什么？实测收益如何？

## A
| 语言 / 实现 | 选择 | 换来 | 代价 |
|---|---|---|---|
| Java / HotSpot | 解释 + C1 + C2 分层 JIT | 稳态性能接近甚至超过 AOT；按真实 profile 优化 | 预热慢、占内存、延迟不稳定 |
| Python / PyPy | 追踪 JIT | 纯 Python 循环快一个数量级以上 | 与 C 扩展兼容差，启动与内存开销大 |
| Python / CPython | 3.13 起实验性 copy-and-patch JIT，默认关闭 | 保持简单、兼容 C 扩展 | 收益暂时有限，甚至可能变慢 |
| Go、Rust、C++ | 纯 AOT，无 JIT | 启动即全速、无运行时编译开销 | 不能根据运行时 profile 优化（除非 PGO，即用采集到的运行 profile 重新编译） |

实测（一次测量）：纯 Python 双层循环计数 0 到 40 万的素数：
- CPython 3.14 默认：0.33 秒；
- CPython 3.14 开启实验性 JIT（`PYTHON_JIT=1`）：0.51 秒，反而更慢；
- PyPy 3.11：0.02 秒，约快 16 倍。

背后的逻辑：
- JIT 的成败取决于语言能不能提供**稳定的类型信息**与**可预测的热点**。Java 的静态类型和字节码结构清晰，JIT 容易押注；Python 一切是动态对象，PyPy 需要追踪和类型特化才能追上，且无法兼容依赖 C API 内部细节的扩展。
- CPython 选择渐进式：先做低成本的字节码特化（自适应解释器），再试验 copy-and-patch JIT，以兼容性和可维护性为先，所以收益保守。
- Go、Rust 与 C++ 的定位（服务端低延迟、系统编程）更看重启动速度与可预测性，所以放弃 JIT；它们靠静态类型在编译期就能确定大部分信息。C++ 还把“JIT 才有的信息”变成了构建流程的一环：Clang/GCC 的 PGO 和 LTO，先跑一遍采集 profile，再重新编译。C++ 标准不涉及运行时编译，这符合它“没有强制运行时”的定位。
