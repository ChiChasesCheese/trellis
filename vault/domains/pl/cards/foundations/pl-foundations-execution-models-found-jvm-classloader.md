---
id: pl-foundations-execution-models-found-jvm-classloader
node: foundations.execution-models
type: qa
step: 2
---
## Q
JVM 上的 `.class` 文件是什么？类加载器（class loader）在程序运行时做什么？

## A
`javac` 把每个 Java 类编译成一个 `.class` 文件。它不是机器码，而是一种与 CPU 无关的二进制格式，包含常量池（字符串、方法名、类型名的表）、字段和方法的描述，以及方法体的字节码（bytecode，一种面向「栈式虚拟机」的指令集）。

JVM 启动时只加载入口类。其余的类按需加载：第一次用到某个类（`new`、调用静态方法）时，类加载器根据类名找到 `.class`（或 JAR 包里的条目），读入、校验字节码是否合法、准备静态变量，然后才执行。后面再用到就直接用已加载的版本。

这带来两个直接后果：一是依赖可以在运行时才解析，所以会遇到 `ClassNotFoundException`、`NoClassDefFoundError` 这类「编译通过，运行时才缺类」的错误；二是类加载器的层次决定谁能看到谁，框架（如应用服务器、插件系统）靠它实现隔离。

实际观察：对一个只打印 `hi` 的程序，用 `java -Xlog:class+load` 记录，会看到约 400 条类加载记录（绝大多数是 JDK 自己的类，来自启动时映射的共享归档），其中属于程序本身的只有 `H` 一个。「hello world」背后是几百个类的加载。
