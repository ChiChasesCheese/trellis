---
id: pl-cpp-safety-found-hardening
node: cpp.safety
type: qa
step: 3
---
## Q
标准库加固（hardening）是什么？怎样开启，它在越界时的行为和成本是什么？

## A
**加固**：标准库在不改变接口的前提下，给容器和视图的**前置条件**（如 `operator[]` 的下标必须小于 `size()`）加运行时检查，违反时**终止程序**，而不是产生未定义行为。重新编译即可，不用改源码。

**各实现的开关**：
- **libc++（LLVM）**：`-D_LIBCPP_HARDENING_MODE=...`，四档：`NONE`、`FAST`（最小的、低成本的检查，违反时陷入）、`EXTENSIVE`（更多检查）、`DEBUG`（全部检查，带诊断信息）。
- **libstdc++（GCC）**：`-D_GLIBCXX_ASSERTIONS`。
- **MSVC**：Debug 模式下的迭代器检查（`_ITERATOR_DEBUG_LEVEL`）。

**本机实测**，对 `std::vector<int>{1,2,3}` 读 `v[10]`：

| 构建 | 结果 |
|---|---|
| 默认（`-O2`） | 打印 `v[10] = 0`，退出码 0，什么都没发生 |
| `_LIBCPP_HARDENING_MODE_FAST` | 进程陷入终止，退出码 133（SIGTRAP），无输出 |
| `EXTENSIVE` | 同上，退出码 133 |
| `DEBUG` | 断言信息：`libc++ Hardening assertion __n < size() failed: vector[] index out of bounds`，退出码 134 |
| `v.at(10)` | 抛 `std::out_of_range`，未捕获时 `terminating due to uncaught exception` |

**含义**：加固把"静默的未定义行为"变成"确定的崩溃"，崩溃比被利用安全得多。在生产中，崩溃后可以由监控捕获、重启，攻击者拿不到内存读写的原语。

**成本**：检查只是一次比较加一个不太会被执行的分支，libc++ 的设计目标是在 `FAST` 模式下把运行时开销压到很低（常见基准在百分之几以内）；具体数字取决于程序，部署前要在自己的负载上测量。Google 等公司公开报告过在生产环境中开启标准库加固，开销不大，同时发现并修复了大量潜在越界。

**C++26 的变化**：标准正式纳入**加固的标准库实现**（hardened implementation）：前置条件违反时，实现可以选择终止。这意味着"在合规实现里开启加固"有了标准背书，不再是厂商私有选项。

**能抓与不能抓**：
- 能：容器的越界、`front()`/`back()` 在空容器、`optional` 空解引用、`span` 越界；
- 不能：指针算术的越界、生命周期错误（释放后使用、悬垂引用）、数据竞争、C 风格数组。

**对比**：Java、Go、Rust 的数组访问**默认**检查越界，Rust 的 `v[i]` 越界会 panic；C++ 默认不检查，加固是把默认值向这边挪。

**要记住的一点**：生产构建开启标准库加固是性价比最高的一项 C++ 安全措施，应当成为默认配置，但它只解决空间安全。
