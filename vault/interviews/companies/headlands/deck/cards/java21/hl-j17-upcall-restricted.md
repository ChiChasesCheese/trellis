---
id: hl-j17-upcall-restricted
node: java21.j17-ffm-api
type: qa
step: 13
---
## Q
什么是 upcall？什么是受限方法（restricted method）？不带 `--enable-native-access` 会怎样？

## A
- **upcall**：C 回调 Java（如 `qsort` 的比较函数），用 `linker.upcallStub(...)`。对比 downcall：Java 调 C。
- **受限方法**：能破坏内存安全的方法（如 `Linker.downcallHandle`，传错签名就崩进程）。
- JDK 21 不带 `--enable-native-access=ALL-UNNAMED` 会打印警告：`WARNING: A restricted method in java.lang.foreign.Linker has been called ... Use --enable-native-access=ALL-UNNAMED to avoid a warning for this module`。
- `invokeExact` 要求调用点的静态类型**精确**匹配（`(long)` 强转、参数是 `MemorySegment`），否则运行时抛 `WrongMethodTypeException`。
