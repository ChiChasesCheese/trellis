# C++ 速查表 · 20 条要脱口而出的事实

一页，面试前一小时过一遍。每条的数字都来自 `demos/` 里的程序（`./build_demos.sh`）。

1. **为什么快**：提前编译成原生码 + 没有强制运行时（无 GC、默认不查边界）+ 优化器看得见整个翻译单元所以能内联。`std::sort` 500 万 `int` 81 ms，`qsort` 303 ms（比较函数是否内联）。性能是"可以做到"，不是"自动得到"。
2. **和别的编译语言比**：差别在编译后还剩多少运行时工作和布局控制权。Java/Go 有 GC，Java 除原始类型都是堆对象+引用；`vector<Order>` 连续，`ArrayList<Order>` 是指针数组。对 Rust：同一个 LLVM 后端，差别是生态，不是机器码。
3. **编译模型**：预处理 → 编译（每个 `.cpp` 独立）→ 汇编 → 链接。`#include <iostream>` 展开成 84,248 行。声明可重复，定义只能一次（ODR）；头文件里的函数要 `inline`；模板定义放头文件。声明了没定义 = 链接错误。
4. **虚函数**：每对象一个 vptr（`int` 的类 4 字节 → 加 virtual 变 16 字节）；调用是间接的、不能内联；基类要有 **virtual 析构**，否则 `delete` 基类指针是 UB（派生析构不运行）。热路径用 CRTP / `final` / `variant`。
5. **缓存**：一次读 64 字节缓存行。400 万 `int`：`vector` 0.2 ms，`list` 4.4 ms，节点乱序的链表 28 ms；只用一个字段时 SoA 比 AoS 快约 10 倍。
6. **标准版本**：**11** 移动语义/`auto`/lambda/智能指针/线程+原子/`constexpr`；**14** 泛型 lambda/`make_unique`；**17** `optional`/`variant`/`string_view`/结构化绑定/`if constexpr`/保证的复制省略；**20** concepts/ranges/coroutines/modules/`span`/`<=>`/`jthread`/`format`；**23** `expected`/`print`/deducing this。
7. **`malloc` vs `new`**：`malloc` 给未初始化字节，`NULL` 表示失败，`free`；`new` = `operator new` + **构造函数**，失败抛 `bad_alloc`，`delete` 先析构；`new[]` 配 `delete[]`，不能混用；可重载；placement new 在已有内存上构造。
8. **智能指针**：`unique_ptr` 8 字节、只能移动、默认选它；`shared_ptr` 16 字节、原子引用计数（控制块线程安全，被指对象不是），`make_shared` 1 次分配（`shared_ptr(new T)` 是 2 次）；`weak_ptr` 打破循环引用，否则析构不运行。
9. **移动**：`std::move` 只是转型；对 `const` 对象会退化成拷贝；移动构造要 `noexcept`（否则 `vector` 扩容时 7 次拷贝而不是 7 次移动）；`return local;` 不要写 `std::move`；C++17 返回临时对象保证不拷贝。
10. **`std::copy` vs `memcpy` vs `memmove`**：`memcpy` 复制字节、重叠是 UB、仅限 trivially copyable；`memmove` 允许重叠；`std::copy` 类型感知，对 `int` 数组就编译成一次 `memmove`。`std::pair<int,int>` 不是 trivially copyable。类型双关用 `std::bit_cast`。
11. **布局**：成员按对齐加填充，大的放前面（同样四个字段 24 → 16 字节）；`alignas(64)` 让对象独占一条缓存行；`sizeof(空类)` = 1。
12. **`vector`**：翻倍扩容（1 2 4 … 128）；扩容使**所有**迭代器/指针/引用失效；`erase` 使被删位置及之后失效；先 `reserve`（1000 次 `push_back`：11 次分配 → 1 次）。
13. **`map` / `unordered_map`**：红黑树有序 O(log n) / 哈希表平均 O(1)；`operator[]` **会插入**；rehash 使迭代器失效但不使引用失效；100 万键查询：`map` 146 ms，哈希 13 ms，排序 vector 45 ms。
14. **删除元素**：`remove_if` 只前移不缩容（size 仍是 6），要接 `erase`；循环里 `it = c.erase(it)`；C++20 `std::erase_if`；顺序无关用 swap-and-pop。
15. **模板 vs 泛型**：模板按类型实例化、无装箱、错误在实例化处；concepts 把错误挪到调用处（"constraints not satisfied … because 't.price()' would be invalid"）。**完美转发**：`T&&` 是转发引用，要 `std::forward<T>`；`emplace_back` 就地构造（0 次移动 vs `push_back` 1 次）。
16. **未定义行为**：有符号溢出、越界、悬空、未初始化、移位 ≥ 位宽、数据竞争、缺 `return`。例：`x + 1 > x` 在 `INT_MAX` 上 `-O0` 得 0，`-O2` 得 1。无符号溢出有定义（回绕）。
17. **Sanitizer**：`-g -fsanitize=address,undefined`（ASan：越界/UAF；UBSan：溢出/移位/未对齐），`-fsanitize=thread`（数据竞争，不能和 ASan 同开）。读报告：错误类型 → 第一栈帧 → allocated/freed by。libc++ 加固：`-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG`。
18. **位运算**：置位 `r | (1u<<b)`，清位 `r & ~(1u<<b)`，翻转 `^`，测试 `(r>>b)&1`；`x & (x-1)` 清最低位，`x & -x` 取最低位；`std::popcount/rotl/countr_zero`。坑：移位 ≥ 位宽是 UB；`~uint8_t(0x0F)` 是 `int` −16；有符号右移是算术的；`==` 优先级高于 `&`；掩码写 `1u`。
19. **并发**：`cv.wait(lk, pred)` 必须带谓词（虚假唤醒）；多锁用 `scoped_lock`；release/acquire 发布数据；`relaxed` 只给计数器；**`volatile` 不是原子**（4 线程 × 50 万次丢更新：1,995,942 / 2,000,000）；数据竞争是 UB；伪共享：相邻计数器 404 ms，隔 64 字节 30 ms。
20. **系统与低延迟**：线程共享地址空间，进程不共享（fork 写时复制）；映射 512 MB 零缺页，碰过每页才有 32,768 次缺页。IPC：pipe / socketpair / TCP / **共享内存**（`shm_open`+`ftruncate`+`mmap`，只放 POD+无锁原子，不放指针）。`condition_variable` 往返 2.4 µs，自旋 82 ns。SPSC 环形队列缓存对方索引：72 → 2 ns/项。异常：不抛≈零成本，一次抛出 3–4 µs。随机分支 47 ms，排序后 8 ms，无分支 6 ms。

**编译命令**：`clang++ -std=c++20 -O2 -Wall -Wextra -fsanitize=address,undefined x.cpp`（测速时去掉 sanitizer；C++23 用 `-std=c++23`）。**现场口诀**：问语言 → 最小骨架先跑通 → 小步编译 → 读第一个错误 → 先说测试用例和复杂度 → `size_t` 下溢、整数溢出、迭代器失效三件事每次检查。
