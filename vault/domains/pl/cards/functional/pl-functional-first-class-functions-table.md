---
id: pl-functional-first-class-functions-table
node: functional.first-class-functions
type: qa
step: 7
---
## Q
Go、Java、Rust、Python 的函数值在类型表示与性能上有什么区别？

## A
| 语言 | 函数的类型 | 买到 | 付出 |
|---|---|---|---|
| Go | 结构化的 `func(A) B` | 写法简单，不用声明接口 | 通过函数值的调用难内联 |
| Java | lambda 落在具名的函数式接口上 | 与已有接口和类库兼容 | 没有函数类型，受检异常不相容 |
| Rust | 每个闭包独特类型 + `Fn` trait | 泛型时零成本，可内联 | 异构存放需装箱，类型签名冗长 |
| Python | 动态对象，`Callable` 仅注解 | 最灵活，任何可调用都行 | `lambda` 只能一个表达式，调用慢 |

规律：越强调**静态性能**的语言，函数的类型越具体（Rust 连每个闭包都有独立类型）；越强调**兼容与简单**的语言，函数越像普通对象（Java 的接口、Python 的动态对象）。

Java 在 2014 年才有 lambda，必须与 1995 年起积累的类库兼容，于是选择「lambda 是函数式接口的实例」，旧的 `Comparator`、`Runnable` 一夜之间都能用 lambda。Go 从一开始就设计了函数类型，保持简洁。Rust 要在不牺牲性能的前提下提供函数式风格，因此泛型加独特类型。Python 的函数是语言最早的特性之一，作为动态对象，写法最自由。
