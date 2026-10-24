---
id: pl-trends-effects-foundation-java-checked
node: trends.effects
type: qa
step: 2
---
## Q
为什么说 Java 的受检异常是一种早期的效应系统？它在哪里遇到了「效应多态」的困难，lambda 和 `Stream` 为什么用不了它？

## A
Java 方法签名里的 `throws IOException` 就是在类型里记录一个效应：「这个方法可能因 I/O 失败」。编译器强制检查：调用者要么处理，要么也声明 `throws`，效应沿着调用链向上传递。这正是效应系统的基本形态：效应出现在签名里，被调用者继承。

它在 Java 8 引入 lambda 和 `Stream` 后暴露了最大的缺陷：**高阶函数无法对效应通用**。`Stream.map` 接收的是 `Function<T, R>`，而 `Function.apply` 没有声明 `throws`，所以传进去的函数不能抛受检异常：

```java
List<String> out = ps.stream().map(p -> Files.readString(p)).toList();
```

```console
error: unreported exception IOException; must be caught or declared to be thrown
```

理想的签名应当是「`map` 会抛出传入函数抛出的任何异常」，即对异常**多态**。Java 的泛型能写 `<E extends Exception> R apply(T t) throws E`，但只适用于单一异常类型，对多个异常、对 `Stream` 这类链式 API 都无法工作，所以标准库没有这样做。

后果是常见的绕路：

- 在 lambda 里 `try/catch`，包装成 `RuntimeException`（如 `UncheckedIOException`）再抛出，把受检异常**变成**非受检异常，效应信息在类型里消失；
- 写一个自己的 `ThrowingFunction<T, R, E extends Exception>` 接口，每个方法重载一遍。

结果是：受检异常被许多现代 Java 库和 Kotlin、Scala 等后继语言放弃。C#、Python、Go 从一开始就没有采用同样的设计。

教训不是「效应不该写进类型」，而是：**只给单一效应开专门通道，不提供对效应的抽象，效应一多就会被组合性打败**。这也是代数效应和 Koka 的效应多态要解决的问题：`map` 的类型写成 `map : (list<a>, a -> e b) -> e list<b>`，`e` 就是传入函数的效应，原样传出。

Rust 吸取了这个教训，用 `Result<T, E>` 这个普通的值来表达可失败，而不是函数签名上的特殊子句；`?` 与 `map`、`collect::<Result<_, _>>()` 组合，不需要效应多态。
