---
id: pl-foundations-design-philosophy-found-java-compat
node: foundations.design-philosophy
type: qa
step: 4
---
## Q
Java 的「向后兼容」具体是什么承诺？一个 API 被弃用（deprecated）后会怎样？

## A
Java 的承诺是：针对旧版本编译或写出的代码，在新版本的 JDK 上应当继续工作，包括已经编译好的 `.class` 文件。为此，语言和标准库极少删除东西，更常见的做法是标记为弃用，并给出替代品。

弃用有两档：`@Deprecated` 表示不建议再用；`@Deprecated(forRemoval = true)` 表示将来会删除，编译器给出更强的警告。即使如此，几乎所有被弃用的 API 都保留了很多年。例如把基本类型包装成对象的构造器 `new Integer(5)` 早已弃用（推荐 `Integer.valueOf`），在 Java 25 里仍可编译运行：

```java
Integer x = new Integer(5);
System.out.println(x);
```

编译时只提示 `Note: Dp.java uses or overrides a deprecated API.`，运行输出 `5`。`Vector`、`Hashtable` 这些 Java 1.0 的类同理，至今还在标准库中。

这个承诺决定了 Java 的节奏：新特性必须能和旧语义共存（所以泛型用了类型擦除（编译后把类型参数擦掉），旧的无参数 `List` 仍然合法），错误的旧设计很难修正。收益是企业可以放心升级 JDK，十几年前的库依然可用；代价是语言里累积了大量遗留物。
