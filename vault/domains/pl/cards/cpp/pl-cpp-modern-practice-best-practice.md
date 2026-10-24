---
id: pl-cpp-modern-practice-best-practice
node: cpp.modern-practice
type: qa
step: 9
---
## Q
一份新 C++ 项目的"现代写法"检查清单是什么？每条为什么比老写法好？

## A
**资源与所有权**
1. 不用裸 `new`/`delete`：`std::make_unique`、容器、值语义。原因：RAII 保证释放，消灭泄漏与重复释放；
2. 类遵循零法则；需要手写资源管理时五个特殊成员函数一起写；
3. 所有权在签名里表达：`unique_ptr` 传所有权，引用/`span`/`string_view` 表示借用。

**类型与初始化**
4. 局部变量就地初始化，初始化用 `{}`：拒绝窄化，避免未初始化变量；
5. `auto` 用在类型显而易见或冗长时；需要引用写 `auto&`/`const auto&`；
6. `enum class` 代替 `enum`；`nullptr` 代替 `NULL`/`0`；`using` 代替 `typedef`；`constexpr` 代替宏常量；
7. 默认 `const`：变量、成员函数、参数。能 `constexpr` 就 `constexpr`。

**接口意图**
8. 重写虚函数一律写 `override`，叶子类写 `final`；基类虚析构；
9. 单参数构造函数默认 `explicit`；
10. 返回错误或资源的函数标 `[[nodiscard]]`；移动操作、析构、`swap` 标 `noexcept`；
11. 用 `= default` 和 `= delete` 声明特殊成员函数的意图。

**数据与算法**
12. 范围 for、标准算法、ranges 代替手写下标循环；
13. 参数：只读用 `const T&`，小类型按值；字符串只读用 `std::string_view`，连续数据用 `std::span`；
14. "可能没有"用 `std::optional`，"几选一"用 `std::variant`，"成功或错误"用 `std::expected`；
15. 结构化绑定拆 `pair`/`tuple`/结构体；
16. 输出用 `std::print`/`std::format`，不用 `printf` 和 `<<` 链。

**语言特性**
17. 模板接口用 concepts 约束；类型分支用 `if constexpr`；
18. 比较运算符用 `<=> = default`；聚合初始化用指定初始化；
19. 线程用 `std::jthread`，锁用 `std::scoped_lock`。

**工程**
20. 开 `-Wall -Wextra`，CI 里 sanitizer；`clang-tidy` 配 `modernize-*`、`cppcoreguidelines-*`、`bugprone-*`；
21. 用 `clang-format` 统一格式；
22. 构建在多个编译器上测试。

**什么时候打破**：兼容旧编译器或旧接口（C 库、旧 API）时，在边界处转换，内部保持现代写法；极热路径上经过测量证明的特殊优化，局部使用并写注释。

**怎么落地**：不要靠评审记住 22 条；用 clang-tidy 把能自动检查的变成 CI 失败，剩下的写进评审清单。

**为什么**：每一条对应一类 bug 或一处样板；清单的价值是让"正确的写法"成为习惯，而不是争论风格。
