---
id: hft-java-at-hft-interop-bugs
node: java-at-hft.interop
type: qa
step: 5
---
## Q
在 Java 与 C++ 混合的系统里，跨语言边界最常见的 bug 有哪些？怎么预防？

## A
常见 bug：
- **字节序、对齐、填充不一致**：C++ 的 `struct` 编译器可能自动插入 padding，Java 一侧的偏移是手算的，读错字段；
- **内存序不一致**：一边用 relaxed 或 plain，另一边按 release/acquire 假设，看到写了一半的数据；
- **生命周期**：Java 的 GC 可能移动或回收对象，而 C++ 持有它的指针；双方都以为对方会释放内存；
- **崩溃传播**：C++ 的段错误会让整个 JVM 进程死掉，Java 异常也不能穿过 C++ 栈；
- **版本漂移**：schema 改了，有一边没重新编译。

预防办法：用 schema 生成代码；常量放在共享的定义里；写跨语言契约测试：同一组测试字节，两边解码结果必须相等。
