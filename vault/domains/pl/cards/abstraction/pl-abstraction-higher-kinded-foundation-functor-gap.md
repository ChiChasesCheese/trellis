---
id: pl-abstraction-higher-kinded-foundation-functor-gap
node: abstraction.higher-kinded
type: qa
step: 3
---
## Q
Functor 和 Monad 是什么？为什么 Rust、Java、Go、Python 都写不出 `Functor<F>` 这样的接口，试着写会得到什么错误？

## A
**Functor**（函子）是一个很小的约定：一种容器 `F`，提供 `map`，能把函数作用到里面的每个值上，**不改变容器的形状**：`F<A>` 经 `A -> B` 得到 `F<B>`。`Option`、`Vec`、`Result`、`Future` 都满足。

**Monad**（单子）在此基础上多一个操作 `flatMap`（也叫 `and_then`、`bind`）：函数返回的本身就是容器 `A -> F<B>` 时，把结果「压平」成 `F<B>`，而不是 `F<F<B>>`。它刻画的是「一步依赖前一步结果的计算序列」，序列里的每一步可以失败（`Option`、`Result`）、产生多个结果（`Vec`）、需要等待（`Future`）。

它们的价值是：基于这两个约定写出的通用代码（遍历、重试、组合），一份就适用于所有满足约定的容器。

在 Rust 里直接尝试写：

```rust
trait Functor<F<_>> {
    fn map<A, B>(fa: F<A>, f: impl Fn(A) -> B) -> F<B>;
}
```

```console
error: expected one of `,`, `:`, `=`, or `>`, found `<`
```

Java 同理：

```java
interface Functor<F<_>> { <A, B> F<B> map(F<A> fa, Function<A, B> f); }
// error: > expected
```

Go 的泛型声明 `Functor[F[_] any]` 得到 `undefined array length _ or missing type constraint`。Python 的类型检查器 mypy 对 `F[A]`（`F` 是 `TypeVar`）报 `Type variable "F" used with arguments`，运行时 `F[int]` 抛 `TypeError`。

问题都出在同一处：**类型参数的位置只允许放完整的类型，不允许放一个还缺实参的类型构造器**，语法和类型检查器都没有为此设计。

这不是偶然的疏忽：Java、Go 的泛型在设计时就把类型参数的种类固定为 `*`，要支持 HKT，类型检查、推导、擦除、单态化全都要改。

后果：`Optional.map`、`Stream.map`、`CompletableFuture.thenApply` 做的是同一件事，名字甚至不同，库作者无法为它们提供共同的接口，使用者也无法写出对它们通用的函数。
