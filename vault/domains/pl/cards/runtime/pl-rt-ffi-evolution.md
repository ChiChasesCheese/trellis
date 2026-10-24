---
id: pl-rt-ffi-evolution
node: runtime.ffi
type: qa
step: 11
---
## Q
FFI 机制这些年有什么变化？Panama / FFM、PyO3、WebAssembly 各代表什么方向？

## A
**背景**：C ABI 是 40 年来事实上的互操作标准。各语言的 FFI 本质上都是“说 C 的语言”。变化在于：**让这件事更安全、更容易、更少样板**。

**Java**：JNI（1997）是为了与旧的原生库兼容而设计的，难用且危险。Project Panama 历时多年，推出 FFM API（JDK 22 正式），同时提供 `jextract` 工具从 C 头文件生成 Java 绑定。目标是让 Java 访问原生库像 Python 一样容易，同时保持内存安全检查（Arena、带边界的 MemorySegment）。受限方法需要显式授权，未来版本计划把“未授权的原生访问”逐步收紧。

**Python**：从手写 C API 与 SWIG，到 Cython、cffi、pybind11，再到 **PyO3**（Rust）。趋势是：用更安全的语言写扩展，库的核心逻辑在 Rust，Python 层很薄。Python 稳定 ABI（`abi3`）和自由线程、子解释器的推进，也要求扩展适配新的运行时模型。

**Rust**：`bindgen`/`cbindgen` 自动化；`cxx` 等库提供 C++ 与 Rust 的安全互操作；在 Linux 内核、Android 等项目里，与 C 共存是核心场景。

**Go**：cgo 基本稳定，性能逐版本改进，但哲学没变：能不用就不用。

**更远的方向**：
1. **WebAssembly 组件模型**：不同语言编译成 Wasm 模块，用统一的接口描述语言（WIT）互相调用，隔离在沙箱中，不共享内存。跨边界的数据要拷贝，但换来安全和语言无关，适合插件系统和边缘计算。
2. **进程外互操作**：gRPC / 管道 / 共享内存，把“语言互操作”变成“服务互操作”，用延迟换隔离。
3. **统一的内存格式**：Apache Arrow 这类列式内存布局，让多个语言零拷贝共享同一块数据（Polars、pandas、DuckDB 之间），把边界成本从“每次调用”降到“一次共享”。

规律：互操作的趋势是**少拷贝、少样板、强隔离**；调用边界越粗，越能容忍它的成本。
