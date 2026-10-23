---
id: hl-c11-memcpy-overlap-asan
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 7
---
## Q
`char buf[16] = "abcdefghijklmno"; std::memcpy(buf + 1, buf, 8);` 有什么问题？AddressSanitizer 怎么报？

## A
- 目标 `[1,9)` 与源 `[0,8)` **重叠**，`memcpy` 对重叠区域是 **UB**。
- AddressSanitizer 明确检查并报：`memcpy-param-overlap: memory ranges [...) and [...) overlap`。
- 假设不重叠，实现可以更激进（并行、向量化），所以重叠时结果不可预测。
- 修法：改用 `memmove`，或 `std::copy`/`std::copy_backward`。
