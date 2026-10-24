---
id: pl-functional-first-class-functions-table
node: functional.first-class-functions
type: qa
step: 7
---
## Q
Go、Java、Rust、Python、C++ 的函数值在类型表示与性能上有什么区别？

## A
| 语言 | 函数的类型 | 买到 | 付出 |
|---|---|---|---|
| Go | 结构化的 `func(A) B` | 写法简单，不用声明接口 | 通过函数值的调用难内联 |
| Java | lambda 落在具名的函数式接口上 | 与已有接口和类库兼容 | 没有函数类型，受检异常不相容 |
| Rust | 每个闭包独特类型 + `Fn` trait | 泛型时零成本，可内联 | 异构存放需装箱，类型签名冗长 |
| Python | 动态对象，`Callable` 仅注解 | 最灵活，任何可调用都行 | `lambda` 只能一个表达式，调用慢 |
| C++ | 每个 lambda 是编译器生成的独特匿名类；要统一类型时用 `std::function`（类型擦除的包装器）或函数指针 | 作为模板参数传入时零成本、可内联 | `std::function` 有间接调用，大闭包要堆分配；类型名写不出来，只能用 `auto` 或模板 |

规律：越强调**静态性能**的语言，函数的类型越具体（Rust 连每个闭包都有独立类型）；越强调**兼容与简单**的语言，函数越像普通对象（Java 的接口、Python 的动态对象）。

Java 在 2014 年才有 lambda，必须与 1995 年起积累的类库兼容，于是选择「lambda 是函数式接口的实例」，旧的 `Comparator`、`Runnable` 一夜之间都能用 lambda。Go 从一开始就设计了函数类型，保持简洁。Rust 要在不牺牲性能的前提下提供函数式风格，因此泛型加独特类型。Python 的函数是语言最早的特性之一，作为动态对象，写法最自由。

C++ 是 Rust 这条路的前辈：C++11（2011）起每个 lambda 就是独立的类型，抽象由模板在编译期展开，所以「不用的不付费」成立；需要运行期统一类型时才付 `std::function` 的间接调用与可能的堆分配。与 Rust 的差别是没有 `Fn`/`FnMut`/`FnOnce` 这层约束，函数能否被并发调用、能否改状态都靠约定。
