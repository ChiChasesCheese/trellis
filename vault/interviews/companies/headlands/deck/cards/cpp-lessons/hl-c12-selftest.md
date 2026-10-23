---
id: hl-c12-selftest
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 16
---
## Q
自测：为什么说 Rust 和 C++ 速度相近而 Go 不同？Java 比 C++ 强的三点是什么？

## A
- Rust 与 C++ 都无 GC、有值类型、单态化泛型、LLVM 级优化；Go 有 **GC 暂停**和较弱的优化器。
- Java 强的三点：
  1. 运行期 profile 驱动的去虚化/内联；
  2. 逃逸分析消除分配；
  3. 内存安全与生产力（另有快速分配、跨平台、成熟库）。
