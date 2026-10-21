# C++ 教科书（给每天写 Java、C++ 生疏的工程师）

16 课，每课独立成篇：先讲 Java 里怎么做，再从零讲 C++，配可运行的例子（代码与输出都在课里）、坑、面试官接着会问什么（含答案要点）、自测（答案折叠）。目标是资深（senior）水平的 C++ 电话面 / CoderPad。

## 课程目录

| 课 | 主题 | 面试里怎么出现 |
|---|---|---|
| [C01](C01_value_lifetime_raii.md) | 值语义、对象生命周期、RAII（对比 Java GC） | 「RAII 是什么」「栈和堆」 |
| [C02](C02_references_pointers_const.md) | 引用 vs 指针 vs `const`，`string_view`/`span` | 「引用和指针的区别」「const 的位置」 |
| [C03](C03_smart_pointers.md) | `unique_ptr`、`shared_ptr`（控制块、开销）、`weak_ptr`、何时用裸指针 | **原题：smart pointers** |
| [C04](C04_move_semantics.md) | 移动语义、右值引用、Rule of 0/3/5、复制省略 | 「`std::move` 做了什么」 |
| [C05](C05_stl_containers.md) | STL 容器的复杂度、内存布局、**迭代器失效**、`unordered_map` 桶、`string` SSO | 「vector 扩容」「哪些操作使迭代器失效」 |
| [C06](C06_algorithms_lambdas_ranges.md) | 算法、lambda、ranges | 编程题里每天都用 |
| [C07](C07_templates_constexpr_concepts.md) | 模板、`constexpr`、concepts | 「模板 vs Java 泛型」 |
| [C08](C08_cxx11_14_17_20_tour.md) | **C++11/14/17/20 每个版本加了什么、为什么** | **原题：Differences between C++ 11, 14, 17, 20** |
| [C09](C09_undefined_behaviour_sanitizers.md) | **未定义行为清单**与 sanitizer | 「什么是 UB」 |
| [C10](C10_new_malloc_allocators.md) | `new`/`delete` vs `malloc`/`free`、placement new、分配器、内存池 | **原题：malloc vs new** |
| [C11](C11_copy_vs_memcpy.md) | `std::copy` vs `memcpy`/`memmove`，平凡可拷贝，编译器生成什么 | **原题：std::copy vs memcpy** |
| [C12](C12_why_cpp_is_fast.md) | **为什么 C++ 快**（及 Java 赢在哪里） | **原题：为什么 C++ 比别的语言快 / 比别的编译型语言也快** |
| [C13](C13_memory_model_atomics.md) | 内存模型、`atomic`、`memory_order`、无锁 SPSC、伪共享 | 「lock-free」「共享内存」 |
| [C14](C14_threads_mutex_cv_jthread.md) | 线程、`mutex`、`condition_variable`、`jthread` | 「实现一个线程安全队列」 |
| [C15](C15_io_performance_coding_rounds.md) | 编程题 I/O 与性能：`sync_with_stdio`、`getline`、`from_chars` | live coding 读输入 |
| [C16](C16_coderpad_survival.md) | CoderPad 生存：单文件骨架、自测、读编译错误、陷阱 | live coding 全程 |

## 怎么读

* 建议顺序：**C01 → C02 → C03 → C04**（所有权与生命周期，其余都建立在上面）→ **C05 → C06**（容器与算法，写题必需）→ **C07 → C08**（模板与版本巡礼）→ **C09 → C10 → C11 → C12**（底层与性能，高频原题）→ **C13 → C14**（并发）→ **C15 → C16**（实战）。
* 每课末尾的「面试官接着会问」先盖住答案自己口述，再对照要点；带英文引号的「口述版」可以直接背成自己的话。
* 例子全部可编译运行。目录 `examples/C01 … C16/` 下是 73 个独立的 `.cpp`；`examples/build_all.sh` 一次性编译并运行全部（默认 `clang++ -std=c++20 -O2 -Wall -Wextra -fsanitize=address,undefined`），输出在 `examples/out/`。名字以 `_ub` 结尾的例子是**故意**触发未定义行为、由 sanitizer 报告的；文件名含 `_bad` 的例子是故意编译失败、用来练习读报错。

```bash
cd study/20-cpp/examples
./build_all.sh          # 全部
./build_all.sh C05      # 只跑某一课
```

## 六天计划（到 10/26 周一 12:00 PT）

每天约 3–4 小时：读课 1.5–2 小时 + 把例子改一改再跑 1 小时 + 口述自测 30 分钟。**优先级按原题出现频率排**：C12、C08、C03、C10、C11 是被明确问过的题，其余是支撑。

| 日 | 内容 | 当天产出 |
|---|---|---|
| 10/21 周三 | C01、C02、C03 | 能用 60 秒讲清 RAII；能说出三种智能指针的所有权和 `shared_ptr` 的控制块；默写 `unique_ptr` 工厂 + `weak_ptr` 打破环 |
| 10/22 周四 | C04、C05、C06 | 能解释 `std::move` 和 Rule of 5；背下迭代器失效表；用 `priority_queue` 写 top-k |
| 10/23 周五 | C07、C08、C09 | **C08 合上书，在纸上写出 11/14/17/20 各 5 个特性和"为什么"**；说出 6 种 UB 并指出 sanitizer |
| 10/24 周六 | C10、C11、C12 | 三道原题各口述 2 分钟（`malloc` vs `new`、`copy` vs `memcpy`、为什么 C++ 快 + Java 赢在哪） |
| 10/25 周日 | C13、C14、C15、C16 | 默写阻塞队列和 SPSC 环形缓冲；在单个文件里限时 25 分钟做一道题（用 C16 骨架 + `CHECK` 自测） |
| 10/26 周一上午 | 只复习：C16 骨架、C08 表、C12 口述版、C05 失效表；开机前把编译错误那一节过一遍 | 不学新东西；确认编辑器的 `-std` 版本 |

## 面试当天的 C++ 小抄

1. 先问需求、边界、数据规模；说方案与复杂度，再写代码。
2. 默认 `std::vector` / `unordered_map` / `std::string`；参数 `const T&` 或 `string_view`；所有权 `unique_ptr`；不写 `new`/`delete`。
3. 倒序循环用 `for (size_t i = n; i-- > 0;)`；中点 `lo + (hi - lo) / 2`；金额用整数。
4. 写完用 `CHECK` 跑 3–5 个边界用例，说出你在测什么。
5. 被问到「为什么」：先给**机制**（布局、内联、无 GC、RAII），再诚实说取舍。
