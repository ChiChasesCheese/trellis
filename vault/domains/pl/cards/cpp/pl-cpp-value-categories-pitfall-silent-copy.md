---
id: pl-cpp-value-categories-pitfall-silent-copy
node: cpp.value-categories
type: qa
step: 10
---
## Q
移动语义的常见陷阱有哪些？为什么 `std::move` 用错时往往不报错，只是悄悄变慢或出现逻辑错误？

## A
`std::move` 是个转换，不是检查；用错了编译器通常不拦。四个典型陷阱：

1. **对 `const` 对象 `std::move`：悄悄拷贝**。
```cpp
const std::string c = a;
std::string b = std::move(c);   // 调用的是拷贝构造函数
```
实测 `c.size()` 仍是 40：没有移动，没有警告。

2. **`return std::move(local)`：阻止 NRVO**。
```cpp
Noisy make_bad() { Noisy n; return std::move(n); }
```
实测多出一次移动：`ctor`、`move`、`dtor`；而 `return n;` 只有 `ctor`。clang 的警告：`moving a local object in a return statement prevents copy elision [-Wpessimizing-move]`。只要开 `-Wall`，就能抓住。

3. **移动之后继续使用**。
```cpp
q.push_back(std::move(s));
println("{}", s.size());   // 实测 0，标准只保证"有效但未指定"
```
这类 bug 在测试里可能一直"正常"：libc++ 的 `string` 移动后总是空串，换一个标准库或换成自定义类型，行为就不同。

4. **移动构造函数没写 `noexcept`：容器退回拷贝**。`vector` 扩容时，若元素的移动构造函数可能抛异常，为了保持强异常安全保证，会选择拷贝。你看不到任何错误，只发现程序比预期慢。

**共同的根因**：C++ 把"这个操作是否发生了移动"留给重载解析，结果完全取决于类型和声明，而代码上看不出来。

**如何防御**：
- `-Wall -Wextra` 抓住 pessimizing/redundant move；
- `clang-tidy` 开 `bugprone-use-after-move`、`performance-move-const-arg`；
- 对关键类型写 `static_assert(std::is_nothrow_move_constructible_v<T>)`，把"移动不抛"变成编译期检查。

**要记住的一点**：C++ 里"我以为这里是移动"和"这里真的是移动"之间没有编译器保证，要靠警告、静态检查和断言去证明。
