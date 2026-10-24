---
id: pl-functional-closures-foundation-java-effectively-final
node: functional.closures
type: qa
step: 2
---
## Q
Java 为什么要求 lambda 捕获的局部变量是 effectively final？想累加状态时怎么办？

## A
Java 的 lambda 捕获的是变量的**值**：创建 lambda 时把值复制进 lambda 对象。局部变量存在栈上，方法返回就销毁，lambda 可能活得更久（比如传给另一个线程），所以不可能引用原变量；复制是唯一安全的做法。

于是规则出现了：被捕获的局部变量必须是 `final` 或 **effectively final**（虽然没写 `final`，但整个作用域内从未被重新赋值）。否则复制出去的值与原变量会不一致，产生迷惑：

```java
int n = 0;
Runnable r = () -> n++;
// error: local variables referenced from a lambda expression
//        must be final or effectively final
```

Java 选择**编译期拒绝**，而不是静默产生两份不同步的状态。

需要累加状态时，把可变性放进**对象**里（引用本身是 final 的，对象内容可变）：

```java
var n = new AtomicInteger();
Runnable r = () -> n.incrementAndGet();      // 线程安全
int[] box = {0};
Runnable r2 = () -> box[0]++;                // 单线程的小技巧
```

前者在多线程下安全，后者只适合单线程。

更好的做法是改写风格：不要在 lambda 里修改外部状态，而是让 lambda 返回结果，由 `reduce`、`collect`、`sum` 之类的操作汇总。限制看似麻烦，实际在推动你写没有副作用的函数式代码，这也是 Java 设计者的有意引导。
