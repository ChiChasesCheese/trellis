---
id: pl-meta-codegen-intro-java-processor
node: metaprogramming.code-generation
type: qa
step: 3
---
## Q
Java 的注解处理器（annotation processor）是什么？它在编译的哪一步运行，能做什么、不能做什么？

## A
**是什么**：注解处理器是一个实现了 `javax.annotation.processing.Processor` 的普通 Java 类，被 `javac` 在编译时加载并调用。编译器把源码解析成元素模型（类、方法、字段的结构化描述）交给它，它读取被某个注解标记的元素，并通过 `Filer` 写出新的源文件。

**心智模型**：编译器的插件。编译分「轮次」：第一轮把你的源码给处理器，处理器生成的新源文件进入第二轮继续被处理，直到没有新文件为止，然后才进入真正的生成字节码阶段。

**场景**：给类打 `@Gen` 标记，处理器为每个被标记的类生成一个配套的 `XxxInfo` 类：

```java
@Gen public class Order {}
// javac -processor Proc ...   prints: [round] generating OrderInfo
// Main calls OrderInfo.name()  ->  Order
```

真实输出：编译时打印 `[round] generating OrderInfo`，生成的源文件在 `-s` 指定的目录里，运行 `Main` 得到 `Order`。`Main` 调用了一个没人手写过的类，它在编译时才诞生。

**边界**：标准的注解处理器只能**新增**文件，不能修改已有的类。想给已有类增加方法的 Lombok 之所以特殊，是因为它绕过公开接口，直接修改编译器内部的语法树，这也是它在 JDK 升级时容易出兼容问题的原因。

**要记住的一点**：Dagger（依赖注入）、MapStruct（对象映射）、AutoValue 都是这种机制：在编译期生成普通 Java 源码，运行时没有反射。
