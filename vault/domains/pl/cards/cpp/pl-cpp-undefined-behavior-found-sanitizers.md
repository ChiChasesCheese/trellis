---
id: pl-cpp-undefined-behavior-found-sanitizers
node: cpp.undefined-behavior
type: qa
step: 4
---
## Q
Sanitizer（运行时检查器）是什么？ASan、UBSan、TSan 各自抓哪类问题，怎样用，成本多大？

## A
**Sanitizer**：编译时往程序里插入检查代码、运行时拦截内存分配的工具，把"静默的 UB"变成"带栈追踪的明确报错"。由 Clang/GCC 内置，加编译选项即可，不需要改源码。

| 选项 | 抓什么 |
|---|---|
| `-fsanitize=address`（ASan） | 越界、释放后使用、重复释放、栈上悬垂 |
| `-fsanitize=undefined`（UBSan） | 有符号溢出、移位越界、空指针、对齐、类型转换违规 |
| `-fsanitize=thread`（TSan） | 数据竞争 |
| `-fsanitize=memory`（MSan） | 读取未初始化内存（Linux 上） |

**实测输出**：

```cpp
v.push_back(4);       // vector 扩容，p 指向旧缓冲区
println("{}", *p);    // ASan: heap-use-after-free on address 0x602000000910 ... READ of size 4
```
```
d1.cpp:3:49: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
d7.cpp:5:47: runtime error: shift exponent 32 is too large for 32-bit type 'int'
```

**原理（ASan）**：为每 8 字节堆/栈内存维护一个"影子字节"，记录哪些可访问；每次读写前先查影子；分配块两侧放"红区"，释放后的块进入隔离区。因此能抓到越过边界和使用已释放内存。

**成本**：量级上，ASan 使 CPU 变慢约 2 倍、内存增加数倍；UBSan 开销较小；TSan 约 5 到 15 倍。所以**不进生产**，进 CI 的测试构建和模糊测试。

**局限**：只检查**实际执行到的路径**，代码没覆盖到就看不见；所以要配合高覆盖的测试和 fuzzing（用随机输入逼出路径）。ASan 与 TSan 不能同时开。

**要记住的一点**：sanitizer 是 C++ 里"把 UB 变成测试失败"的主要手段，没有它的 C++ 项目基本是在盲飞。
