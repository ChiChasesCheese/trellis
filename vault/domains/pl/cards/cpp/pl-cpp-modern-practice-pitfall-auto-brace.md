---
id: pl-cpp-modern-practice-pitfall-auto-brace
node: cpp.modern-practice
type: qa
step: 10
---
## Q
现代写法本身有哪些陷阱？`auto` 悄悄拷贝、`vector<bool>` 的代理类型、花括号选错构造函数，各会怎样？

## A
**陷阱一：`auto` 丢掉引用，悄悄拷贝**。本机实测：

```cpp
auto x  = ws[0];    // 打印 "copy"：拷贝了元素
auto& y = ws[0];    // 没有拷贝
for (auto s : v)        { /* 每次迭代拷贝一个字符串 */ }
for (const auto& s : v) { /* 引用，不拷贝 */ }
```

遍历 3 个各含 1000 字符的 `std::string`，`for (auto s : v)` 每个元素分配并拷贝 1000 字节；`const auto&` 则不拷贝。两者结果相同，所以没有任何测试会失败，只是慢。**规则**：`for` 里默认写 `const auto&`，要修改写 `auto&`，只有元素是小的标量时才按值。`clang-tidy` 的 `performance-for-range-copy`、`performance-unnecessary-copy-initialization` 能抓。

**陷阱二：`auto` 与代理类型**。`std::vector<bool>` 的 `operator[]` 返回的是代理对象，不是 `bool`：

```cpp
std::vector<bool> vb{true, false};
auto b0 = vb[0];     // sizeof(b0) 本机实测为 16，不是 1
```

`b0` 保存着一个指向 `vb` 内部位的引用，`vb` 修改或销毁后继续用就是悬垂。表达式模板库（Eigen）也有同类问题：`auto` 保存了未求值的表达式，引用了已销毁的临时矩阵。**规则**：怀疑返回的是代理类型时，显式写出目标类型，如 `bool b0 = vb[0];`。

**陷阱三：花括号选中 `initializer_list` 构造函数**。`std::vector<int> b{3, 1}` 是两个元素 3 和 1，而 `std::vector<int> a(3, 1)` 是三个值为 1 的元素，实测 `b.size()==2`、`a.size()==3`。给类型新增一个 `initializer_list` 构造函数，会悄悄改变已有的 `{...}` 调用的含义。**规则**：想用"数量 + 值"的构造函数时用圆括号。

**陷阱四：`auto x = {1}`**：推导成 `std::initializer_list<int>` 而不是 `int`（`auto x{1}` 在 C++17 起是 `int`）。

**陷阱五：最令人烦恼的解析**：`T t();` 声明了一个函数而不是对象，clang 警告 `empty parentheses interpreted as a function declaration [-Wvexing-parse]`。

**陷阱六：过度使用 `auto`** 让读者看不出类型。`auto result = compute();` 没有信息，`const std::vector<Order> orders = ...` 更好。

**共同的根因**：这些特性的行为依赖推导规则，规则细，**行为改变不会改变代码的结果，只改变成本或寿命**，所以测试发现不了。

**如何防御**：打开 `-Wall -Wextra` 与 clang-tidy 的 `performance-*`；对热点代码用基准测试；代码评审时对每个 `auto` 问："这里是拷贝还是引用？"

**要记住的一点**：现代写法让代码更短，也把更多的规则放进了推导过程里；"短"并不等于"没有细节"。
