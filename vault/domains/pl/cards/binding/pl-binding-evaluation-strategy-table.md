---
id: pl-binding-evaluation-strategy-table
node: binding.evaluation-strategy
type: qa
step: 7
---
## Q
Go、Java、Rust、Python 在惰性序列、延迟计算参数和短路上各用什么工具？它们的选择背后有什么共同逻辑？

## A
| 语言 | 惰性序列 | 延迟计算一个值 | 惰性的性质 |
|---|---|---|---|
| Go | `iter.Seq`（1.23 起）、通道 | 传函数值 | 库层面，范围有限 |
| Java | `Stream`、`Iterator` | `Supplier<T>`、`orElseGet` | 库层面，Stream 一次性 |
| Rust | `Iterator` 适配器链 | 闭包、`unwrap_or_else`、`LazyLock` | 零成本，编译成循环 |
| Python | 生成器、`itertools` | `lambda`、`functools.cache` | 语言内建（`yield`） |

四门语言的共同点：**参数默认严格，惰性是显式、局部、有名字的工具**。读代码时，只要没看到 `Stream`、`yield`、`Supplier`、迭代器适配器或闭包，就可以确信表达式按书写顺序立刻执行。

这背后的逻辑是工程性的。大型程序里最昂贵的错误往往是时序和资源：什么时候发生了 I/O、什么时候占用了内存、什么时候抛了异常。严格求值让这些答案与代码书写顺序一致，评审、调试、性能分析都能沿用同一套直觉。

差异来自各语言的定位：

- Rust 把惰性做成零成本，因为迭代器链被编译器内联成一个手写循环，没有 thunk 对象，也不分配。
- Python 把惰性融进语法（`yield`、生成器表达式），因为它最重视让代码简短。
- Java 把惰性放在库里（`Stream`），反映了它「语言不变，库演进」的保守传统。
- Go 起初完全没有，靠循环和切片表达，直到 1.23 才为迭代器加上标准形式，反映了它「少即是多」的审慎。

趋势：惰性正从学术特性变成各语言标配的显式工具（迭代器、流、协程），而不是默认行为。
