---
id: pl-cpp-modern-practice-found-cpp20-conveniences
node: cpp.modern-practice
type: qa
step: 5
---
## Q
C++20/23 的 `<=>`、指定初始化、`std::format`/`std::print` 各解决了什么老问题？

## A
**1. 三路比较 `<=>`（C++20）**。给一个类型写全套比较（`==`、`!=`、`<`、`<=`、`>`、`>=`）要六个运算符函数，逐个成员比，容易漏、容易不一致。现在只要一行：

```cpp
struct P { int x, y; auto operator<=>(const P&) const = default; };
// P{1,2} < P{1,3} 为 true，P{1,2} == P{1,3} 为 false
```

`= default` 让编译器按成员声明顺序逐个比较，自动生成全部六个运算符。需要自定义时手写 `<=>` 返回 `strong_ordering` 等类型。好处：从源头避免"`==` 和 `<` 不一致"的 bug。

**2. 指定初始化（C++20）**。给聚合类型的成员按名字赋初值：

```cpp
struct Opts { int port = 80; bool tls = false; std::string host = "localhost"; };
Opts o{.port = 443, .tls = true};     // host 保持默认值
```

实测得到 `localhost:443 tls=true`。解决了"一串位置参数不知道是什么意思"的问题，是 Python 关键字参数、Go 结构体字面量的 C++ 版本。要求按**声明顺序**写，不能乱序。

**3. `std::format`（C++20）与 `std::print`（C++23）**。老 C++ 有两种格式化输出：`printf`（类型不安全，格式串与参数对不上就是未定义行为）和 `iostream`（类型安全，但 `<<` 链冗长，格式控制晦涩，运行时开销大）。新方案用 Python 风格的格式串：

```cpp
std::println("{:>8.3f}|{:#x}|{:08b}", 3.14159, 255, 5);
// 输出:    3.142|0xff|00000101
```

格式串在**编译期检查**：参数个数或类型对不上是编译错误（格式串被当作 `consteval` 参数检查）。`std::print` 直接输出到标准流，通常比 `iostream` 快。

**4. 其他**：`std::span`、`concepts`、`ranges`、`std::jthread`、`constexpr` 的扩展，各有自己的机制，这里不展开。

**对比**：Rust 的 `println!("{}", x)` 格式串同样编译期检查（宏实现），`#[derive(PartialOrd, Ord)]` 对应 `<=>` 的 `= default`；Go 的 `fmt.Printf` 是运行时检查（`go vet` 辅助）；Java 的 `String.format` 运行时检查；Python 的 f-string 运行时。

**注意**：这些特性依赖编译器和标准库版本。`std::print` 在本机可用，`<generator>`、`views::enumerate` 则还没有；使用前确认目标平台。

**要记住的一点**：新写法的共同点是**把重复的样板交给编译器生成，把易错的格式交给编译期检查**。
