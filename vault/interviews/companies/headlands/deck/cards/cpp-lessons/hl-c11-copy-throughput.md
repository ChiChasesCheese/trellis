---
id: hl-c11-copy-throughput
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 11
---
## Q
拷贝 64 MiB 的 `int`，`std::copy`、`memcpy`、`memmove`、手写 `for` 循环、`vector=` 的吞吐是多少？说明什么？

## A
实测（GB/s，越高越好）：
- `std::copy`：55.6
- `memcpy`：53.8
- `memmove`：52.8
- `for` 循环：56.3
- `vector=`：55.0

结论：它们都落在同一个量级（受**内存带宽**限制）；小块（64 字节）拷贝只需不到 1 ns。差别在**正确性**，而不是速度。
