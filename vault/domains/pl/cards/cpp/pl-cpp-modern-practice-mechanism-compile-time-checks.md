---
id: pl-cpp-modern-practice-mechanism-compile-time-checks
node: cpp.modern-practice
type: qa
step: 6
---
## Q
现代 C++ 的这些小特性怎样把运行时 bug 前移成编译期错误？列出"老写法的 bug → 新写法的编译器反应"。

## A
核心机制是**给编译器更多信息**：你声明意图，编译器核对声明与代码是否一致，不一致就报错。信息越多，能提前拦住的错误越多。

| 老写法的 bug | 新写法 | 编译器的反应（本机真实输出） |
|---|---|---|
| 重写虚函数时参数类型写错，变成了新函数 | `override` | `error: non-virtual member function marked 'override' hides virtual member function` |
| 枚举值隐式转成整数，误传 | `enum class` | `error: cannot initialize a variable of type 'int' with an rvalue of type 'Level'` |
| `double` 悄悄截成 `int` | 花括号初始化 | `error: type 'double' cannot be narrowed to 'int' in initializer list` |
| 忽略了错误码或返回值 | `[[nodiscard]]` | `warning: ignoring return value of function declared with 'nodiscard' attribute` |
| 误派生了不该被继承的类 | `final` | `error: base 'F' is marked 'final'` |

**两个观察**：
1. **这些都是零运行时成本**：全部在编译期完成，生成的机器码不变；
2. **它们的前提是你写了意图**：不写 `override`，编译器没有可核对的东西；不写 `[[nodiscard]]`，忽略返回值不会警告。所以现代 C++ 的清单大多是"**默认要写上**"。

**为什么 C++ 没把它们变成默认**：兼容性。如果 `override` 变成必须写，所有老代码里的重写都会报错；所以只能加新关键字，让新代码主动选择，同时用编译器警告开关（`-Wsuggest-override`、`-Wswitch-enum`）和 clang-tidy（`modernize-use-override`、`modernize-use-nullptr`、`modernize-use-nodiscard`）**自动补齐**。

**另一类机制：用类型代替约定**。`std::optional`、`std::variant`、`std::expected`、`std::span`、`std::string_view`、智能指针，把"可能为空""几选一""借用而不拥有"这些原本写在注释里的约定放进类型。编译器不能证明你用对了，但读代码的人和工具看得见意图。

**局限**：
- 这些检查是**局部的**：编译器只核对声明与使用是否一致，不证明整个程序的内存安全；
- 它们只对你**愿意写**的地方有效；
- 与 Rust 对比：Rust 把不少这类检查（穷尽匹配、`#[must_use]`、不可变默认）做成**默认开启**，不需要靠规范保证。

**自动迁移**：`clang-tidy` 的 `modernize-*` 检查组可以**批量自动改写**老代码（`--fix`），例如加 `override`、把 `NULL` 换成 `nullptr`、把 `typedef` 换成 `using`。这是大型老代码库的现实升级办法。

**要记住的一点**：现代 C++ 的特性大多是"声明意图—编译器核对"的模式；清单的执行靠警告开关和 clang-tidy，不靠记忆。
