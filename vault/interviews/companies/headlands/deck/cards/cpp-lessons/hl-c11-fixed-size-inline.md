---
id: hl-c11-fixed-size-inline
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 10
---
## Q
`std::memcpy(out, a, 16 * sizeof(int))`（大小编译期已知）和 `memcpy(out, a, n * sizeof(int))`（运行期大小）分别会被编译成什么？

## A
- **大小编译期已知**（64 字节）：不调用库函数，内联成几条宽向量加载/存储（arm64 上 `ldp q0,q1` / `stp q2,q3`，一次搬 32 字节）。实测 64 字节拷贝约 0.76 ns。
- **运行期大小**：同样变成对库的调用。
- 手写 `for` 循环：若编译器无法排除重叠，会生成向量化循环外加一个运行期重叠检查。
