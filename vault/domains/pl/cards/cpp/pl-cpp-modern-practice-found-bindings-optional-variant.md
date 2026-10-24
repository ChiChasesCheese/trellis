---
id: pl-cpp-modern-practice-found-bindings-optional-variant
node: cpp.modern-practice
type: qa
step: 4
---
## Q
结构化绑定（structured bindings）、`std::optional` 和 `std::variant` 是什么？它们取代了哪些老写法，与 Rust 的 `Option`、`enum` 有什么差别？

## A
**结构化绑定（C++17）**：一次把一个复合值拆成几个命名变量。

```cpp
for (const auto& [key, value] : m) std::print("{}={} ", key, value);   // m 是 map
// 老写法: for (auto& p : m) { p.first ... p.second ... }
```

适用于 `pair`、`tuple`、`std::array`、简单结构体。好处：名字有意义（`key` 比 `p.first` 清楚），不容易把 `first`/`second` 弄反。

**`std::optional<T>`（C++17）**："可能没有值"的类型。以前的做法是用魔法值（`-1`、`nullptr`）或"返回 `bool` + 输出参数"。`optional` 把"没有"放进类型里：`std::optional<int> o;`，`o.value_or(-1)` 提供默认值，`if (o)` 检查。本机实测 `value_or(-1)` 得 `-1`。成本是多一个"是否有值"的标志位和对齐填充，没有堆分配。

**`std::variant<A, B, ...>`（C++17）**："这几个类型之一"的类型，也叫和类型（sum type）、带标签联合体（tagged union）。以前用 `union` + 手写标签，容易搞错当前是哪个。用 `std::visit` 对当前持有的类型分派：

```cpp
std::variant<int, std::string> var = std::string("hi");
std::visit([](const auto& v) { std::println("variant holds {}", v); }, var);
```

实测输出 `variant holds hi`。

**和 Rust 对比**：Rust 的 `Option<T>`、`enum`（带数据的枚举）、`match` 是同一思想的**语言级**版本：
1. **穷尽性检查**：`match` 漏掉一个分支是编译错误；C++ 的 `std::visit` 用一个泛型 lambda 时，编译器不强制你为每个类型写不同的行为；用重载集合（`overloaded` 技巧）时，漏掉一个类型会编译失败，但要自己搭这个辅助类型；
2. **语法**：Rust 的模式匹配直接写 `Some(x) => ...`；C++ 要写 `std::visit` 或 `std::get_if`，更啰嗦；C++26 之后的模式匹配提案（`inspect`）还在讨论；
3. **空值安全**：Rust 里没有空指针，`Option` 是唯一的"可能没有"；C++ 有 `nullptr`、`optional`、裸指针多种表示，需要约定；
4. **成本**：两者都是栈上的带标签联合体，没有额外开销。

**什么时候用**：
- 查找可能失败、"可选参数"：`optional`（预期失败且需要原因时用 `expected`）；
- 一个值是几种固定类型之一（AST 节点、消息类型、状态机状态）：`variant`，替代继承层次（更适合"封闭集合"）；
- `unique_ptr<Base>` 的虚函数多态适合"开放集合"（调用者可以增加新类型）。

**要记住的一点**：把"没有值""几选一"这类语义写进类型，调用者就不能忘记处理；这是现代 C++ 向 Rust 的 `Option`/`enum` 靠拢的方向，但缺少模式匹配的语法支持。
