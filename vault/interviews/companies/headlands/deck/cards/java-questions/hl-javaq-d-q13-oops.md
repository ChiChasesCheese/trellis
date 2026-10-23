---
id: hl-javaq-d-q13-oops
node: java-questions.d-memory
type: qa
step: 12
---
## Q
什么是压缩指针（compressed oops）？堆超过约 32 GB 会怎样？怎么确认它开着？字符串 `"a".repeat(1000)` 和 `"中".repeat(1000)` 各占多少字节？

## A
- **压缩指针**：堆小于约 **32 GB** 时，引用只用 **4 字节**（按 8 字节对齐后左移 3 位寻址）。
- 堆超过阈值，引用变 **8 字节**，同样的数据内存一下涨一截——这就是"堆不要随手设到 32 GB 以上"的由来。
- 确认：`-XX:+PrintFlagsFinal` 显示 `UseCompressedOops = true`，`ObjectAlignmentInBytes = 8`。
- 字符串：`"a".repeat(1000)` = **1040 字节**（`String` 24 + `byte[1000]` 的 1016）；`"中".repeat(1000)` = **2040 字节**（UTF-16：`byte[2000]` 为 2016 + 24）。
