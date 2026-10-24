---
id: pl-functional-first-class-functions-foundation-java-lambda
node: functional.first-class-functions
type: qa
step: 2
---
## Q
Java 的 lambda 和函数式接口是什么？为什么 lambda 里不能随便抛受检异常？

## A
Java 没有「函数类型」。它的做法是：**函数式接口**（functional interface）——只有一个抽象方法的接口，如 `Function<T, R>`（`R apply(T)`）、`Runnable`（`void run()`）、`Predicate<T>`。lambda 表达式只是为这类接口创建实例的简写，目标接口由上下文决定：

```java
Function<String, Integer> f = String::length;     // 方法引用
Runnable r = () -> System.out.println("hi");
```

lambda 不是匿名内部类的语法糖：编译器生成的是 `invokedynamic` 指令，运行期才由 `LambdaMetafactory` 生成实现类（实测 `f.getClass()` 不是匿名类，名字形如 `Main$$Lambda/0x...`）。没有捕获变量的 lambda 通常复用同一个实例，开销很小。

lambda 受目标接口方法签名约束。`Function.apply` 没有声明 `throws`，所以 lambda 体里不能抛受检异常：

```java
List.of("a.txt").forEach(s -> Files.readString(Path.of(s)));
// error: unreported exception IOException; must be caught or declared to be thrown
```

要么在 lambda 里 `try/catch` 包成 `RuntimeException`，要么自定义一个允许抛异常的函数式接口。这是 Java 受检异常机制与函数式 API 不相容的典型摩擦（流式 API 的各个 `map`、`forEach` 都不允许受检异常）。因此函数式风格在 Java 里常配合「把异常包成非受检」的做法。
