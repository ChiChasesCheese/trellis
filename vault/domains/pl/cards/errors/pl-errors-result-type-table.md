---
id: pl-errors-result-type-table
node: errors.result-type
type: qa
step: 6
---
## Q
「值可能缺失或操作可能失败」这件事，C++、Go、Java、Rust、Python 各用什么表达？强制性、组合性和成本有什么差别？

## A
| 语言 | 选择 | 换来 | 代价 |
|---|---|---|---|
| C++ | 缺失用 `std::optional<T>`（C++17），失败用 `std::expected<T, E>`（C++23），带 `transform`、`and_then`、`or_else` 组合器；没有 `?`，早返回要手写；也有异常与错误码 | 标准库提供，值型、无堆分配；成功失败互斥，可用组合器串联 | 访问 `*r`、`->` 时不检查状态，错取是未定义行为（标准不规定后果）；没有 `?` 糖，样板比 Rust 多；与异常、错误码并存，没有统一风格 |
| Go | `(T, error)` 加零值；缺失用零值或 `ok` 布尔 | 简单，无泛型机制也行 | 不强制检查；失败时的 `T` 是零值，容易误用；难以链式组合 |
| Java | 缺失用 `Optional<T>` 或 `null`；失败用异常 | `Optional` 提供组合器 | `Optional` 只是约定，参数和字段里不鼓励，`null` 仍然存在 |
| Rust | `Option<T>`、`Result<T, E>`，加 `?` | 编译器强制处理；成功失败互斥；组合器与 `?` 好用 | 要设计错误类型，学习泛型与 trait 转换 |
| Python | 缺失用 `None`；失败用异常 | 最简单 | `None` 可以流到任何地方，错误出现在远处（`AttributeError`） |

逻辑：这是在「强制性」和「简单性」之间的取舍。Rust 用类型把两者都拿到：简单性来自 `?` 和组合器，强制性来自枚举；代价是类型系统更复杂，初学者要花时间。Java 的 `Optional` 是一个折中，只作为返回值类型使用，无法根除 `null`。Go 与 Python 选择了最小语言机制，把正确性交给程序员和测试。C++ 属于晚到的跟随者：`optional` 和 `expected` 是 2017 和 2023 年才加进标准的，晚于 Rust 的 `Result` 近十年，而且作为库而不是语言特性加入，所以没有 `?`、没有穷尽的 `match`，强制性弱于 Rust；这是 C++ 一贯的方式——不改核心语言，用库补。
作为参照，`expected` 的本机用法：`parse("12").transform([](int n) { return n * 2; }).value_or(-1)` 得到 `24`，`parse("12x")` 失败时带着 `E`（一条错误字符串），`sizeof(std::expected<int, int>)` 是 8 字节。

与受检异常的比较很有启发：`Result` 实质上是「受检异常的函数式版本」——失败也出现在签名里，调用者必须处理；但因为它是普通类型，可以放进集合、作为参数传递、被泛型组合，`Stream.map` 与受检异常无法兼容的问题在 `Result` 上并不存在。
