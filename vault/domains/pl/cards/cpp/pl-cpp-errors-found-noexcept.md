---
id: pl-cpp-errors-found-noexcept
node: cpp.errors
type: qa
step: 4
---
## Q
`noexcept` 是什么？为什么没有 `noexcept` 的移动构造函数会让 `std::vector` 退回拷贝，违反 `noexcept` 又会怎样？

## A
**`noexcept`**：函数声明"我不会抛出异常"。它做两件事：
1. **给编译器和库信息**：知道调用不会展开，可以省去清理路径、做更激进的优化，库可以据此选择更快的算法。
2. **是一个承诺，违反则终止**：`noexcept` 函数如果真的抛出异常并且逃出函数，运行时直接调用 `std::terminate`，外层的 `catch` 没有机会运行。

**最重要的应用：移动构造函数**。`std::vector::push_back` 在容量不足时要把旧元素搬到新缓冲区。标准要求**强异常保证**（失败后状态回到操作之前）：搬到一半失败，原 vector 必须保持不变。如果元素的移动构造函数可能抛出，已搬走一半的旧元素就无法恢复，所以 `vector` 的策略是：

- 移动构造函数是 `noexcept` → **移动**；
- 否则（且有可用的拷贝构造函数）→ **拷贝**，因为拷贝失败不会破坏源对象。

**本机实测**：往 vector 里 `emplace_back` 1000 个元素，扩容时：

```
move is noexcept:   copies=0     moves=1023
move not noexcept:  copies=1023  moves=0
```

对一个含 `std::string` 与 `std::vector<int>` 的结构体，把移动构造函数从 `= default` 的 `noexcept` 版本换成手写的、没有写 `noexcept` 的版本，插入 10 万个元素重复 20 次，耗时从约 60 ms 升到约 140 ms，慢约 2.3 倍（一次测量）。没有任何报错或警告，只是悄悄变慢。

**因此的规则**：
1. 自己写移动构造函数和移动赋值，几乎总是加 `noexcept`（移动一般只是交换指针，不可能失败）。
2. 能用 `= default` 的就用 `= default`，编译器会自己推导 `noexcept`。
3. 对关键类型加 `static_assert(std::is_nothrow_move_constructible_v<T>)`。
4. 析构函数默认就是 `noexcept` 的，不要改它。
5. 不要把 `noexcept` 加在可能抛出的函数上"为了优化"：失败会直接终止进程。

**对比**：Rust 没有这个问题，因为 Rust 的移动是按位复制，不会失败，也不执行用户代码。

**要记住的一点**：`noexcept` 在 C++ 里不是可选的装饰，它是移动语义能否真正生效的开关。
