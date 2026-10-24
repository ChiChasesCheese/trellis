---
id: pl-abstraction-higher-kinded-principle
node: abstraction.higher-kinded
type: qa
step: 1
---
## Q
`Option`、`List`、`Future` 都有 `map`，能不能只写一份对「任意这类容器」都成立的代码？这要求语言有什么能力，设计空间是什么？

## A
泛型让你对**类型**抽象：`fn first<T>(xs: &[T]) -> &T` 对任何元素类型 `T` 成立。但很多代码想抽象的是**容器本身**：「给我任意一种能装东西的结构 `F`，我对里面的元素逐个变换，返回同一种结构」。这里 `F` 不是 `i32` 这样的普通类型，而是 `Option`、`Vec`、`Future` 这样**还缺一个类型实参**的东西（类型构造器，type constructor）。能对它们抽象的能力，叫**高阶类型**（higher-kinded types，HKT）。

写出来的抽象大致是：

```text
trait Functor<F>  where F is "something<_>":
    map : F<A> -> (A -> B) -> F<B>
```

有了它，`map` 的使用方（比如「对每个元素加 1」）只写一遍，就对 `Option`、`Vec`、`Result`、`Future` 全部适用，也就是对「效果」做抽象：可能为空、可能出错、可能异步、可能有多个，都是容器的不同种类。Haskell 的 `Functor`、`Applicative`、`Monad` 就是这类抽象，整套函数式库建立在它之上。

设计空间有四种做法：

1. **完整支持 HKT**：Haskell、Scala。表达力最强，抽象最彻底。
2. **不支持，每个容器各写一份**：Java、Go、Python 的现状。`Optional.map`、`Stream.map` 各写各的，互不相关。
3. **部分补偿**：C++ 的模板模板参数可以对 `vector`、`optional` 这类类型构造器本身做参数，但没有契约检查，错误在实例化时才出现；Rust 的关联类型（GAT）能编码出 `Functor`，但笨重；语言还把 `?` 运算符做成对 `Option` 和 `Result` 都适用的特例。
4. **用别的机制替代**：Java/Kotlin/Go 用协程、虚拟线程把异步写成同步风格，Rust 用 `async` 关键字，各自把「效果」做成语法。

取舍的轴是**表达力对复杂度**：HKT 带来强大的统一，也带来难懂的类型签名、难读的错误信息，团队需要学习 `Monad` 这一套术语。Go、Java、Rust、Python 的设计者在不同时间都选择了不加；C++ 因为模板是实例化时检查的，模板模板参数几乎是顺带得到的，所以它没有做这个选择，也没有为此付出 HKT 的类型检查成本。
