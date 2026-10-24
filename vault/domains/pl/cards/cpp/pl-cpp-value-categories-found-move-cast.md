---
id: pl-cpp-value-categories-found-move-cast
node: cpp.value-categories
type: qa
step: 3
---
## Q
`std::move` 到底做了什么？为什么说它不移动任何东西？对 `const` 对象调用它会发生什么？

## A
`std::move(x)` **只是一个类型转换**：把表达式 `x` 转成右值引用（将亡值）。它不修改 `x`、不调用任何构造函数。真正的“移动”发生在接收这个右值的**移动构造函数或移动赋值**里。所以更准确的读法是“`x` 已允许被偷”，而不是“现在移动 `x`”。

**用一次实测看清**（libc++）：

```cpp
const std::string c = a;
std::string b = std::move(c);   // c 仍是 40 个字符
std::string d = std::move(a);   // a 变空，d 拿走了同一块缓冲区
std::vector<int> v(1000, 1);
auto w = std::move(v);          // w.data() == 原 v.data()，v.size() == 0
```

输出：`after const move: c.size=40 (copied)`，`after real move: a.size=0 d.data same buffer=true`，`vector moved: buffer stolen=true v.size=0`。

**对 `const` 对象**：`std::move(c)` 得到 `const std::string&&`。移动构造函数要写入源对象（把指针置空），不能接收 `const`，所以匹配的是拷贝构造函数 `const std::string&`。结果是**悄悄拷贝**，没有报错，也没有警告。

**被移动之后对象的状态**：标准库类型保证处于“**有效但未指定**”（valid but unspecified）状态——可以析构、可以被赋新值，但内容不确定。`std::string` 在 libc++ 里恰好变成空串，但标准不承诺；`std::unique_ptr` 则明确规定变成空指针。

**要记住的一点**：移动是**非破坏性**的：被移动的对象仍然存在，它的析构函数仍会运行。这与 Rust 不同，后者编译器会禁止再使用被移动的变量。
