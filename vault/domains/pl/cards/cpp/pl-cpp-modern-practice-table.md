---
id: pl-cpp-modern-practice-table
node: cpp.modern-practice
type: qa
step: 7
---
## Q
在"默认不可变、空值、和类型、字符串格式化"这几件日常事上，C++、Rust、Go、Java、Python 的默认做法各是什么？C++ 现代写法追上了哪些，没追上哪些？

## A
| 语言 | 变量默认 | 空值 | 和类型（几选一） | 格式化 |
|---|---|---|---|---|
| C++ | 可变，要主动写 `const` | `nullptr`、`optional`、裸指针并存 | `variant` + `visit`，无模式匹配 | `std::format`，编译期检查 |
| Rust | **不可变**，要写 `mut` | 无空指针，`Option<T>` | `enum` + `match`，穷尽检查 | `format!`，编译期检查 |
| Go | 可变 | `nil`（指针、接口、map 等） | 无；接口 + 类型断言 | `fmt.Printf`，运行时 |
| Java | 可变，`final` 可选 | `null`，`Optional` 可选 | `sealed`（17）+ `switch` 模式匹配（21） | `String.format`，运行时 |
| Python | 可变 | `None` | 无；类型注解 `Union` 仅提示 | f-string，运行时 |

**逻辑**：这张表展示 C++ 现代写法的真实位置——它在**能力**上追上了其他语言（有 `optional`、有 `variant`、有编译期格式化），在**默认值**上没追上（可变、无穷尽匹配、需要主动写意图）。

这是兼容性的直接后果：Rust 的默认值是"安全的做法"，C++ 的默认值是"1980 年代的做法"，新特性只能作为**可选的新写法**加进去。

**这带来的实际差异**：
1. 同样一份"几选一"的数据，Rust 里漏处理一个分支是编译错误，C++ 里要靠 `visit` 加重载集合，团队没有约定时可能漏；
2. Rust 里忘记写 `mut` 是编译错误，C++ 里忘记写 `const` 只是少了一次检查机会；
3. C++ 的空值有三种表示（指针、`optional`、哨兵值），每个库选一种，混用时要转换。

**Java 17 之后的追赶**：`sealed` 类（Java 17）+ `switch` 模式匹配（Java 21），已经在"和类型 + 穷尽检查"上接近 Rust；C++ 的模式匹配提案尚未进入标准。

**实用结论**：在 C++ 团队里，用**规范 + 静态检查**补默认值：规定"能 `const` 就 `const`"（用 `clang-tidy` 的 `misc-const-correctness` 强制）、规定"所有 `variant` 用带穷尽检查的访问器"、规定"一个项目里只用一种空值表示"。

**要记住的一点**：C++ 的现代化是"能力追平、默认不改"；差距体现在你必须主动写的那一部分。
