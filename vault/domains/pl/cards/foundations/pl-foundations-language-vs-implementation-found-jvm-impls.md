---
id: pl-foundations-language-vs-implementation-found-jvm-impls
node: foundations.language-vs-implementation
type: qa
step: 3
---
## Q
HotSpot、GraalVM、OpenJ9 和 OpenJDK、Temurin 这些名字分别是什么？为什么同一个 `.class` 文件可以在它们上面运行？

## A
先分清三层概念：

- 规范：JLS 规定 Java 源代码的含义；JVMS 规定 `.class` 文件格式和每条字节码指令的行为。它们是文字合同。
- 虚拟机实现：按 JVMS 写出来的程序。HotSpot 是 OpenJDK 自带的默认实现，以高性能的 JIT 编译器（C1、C2）和成熟的垃圾回收器著称；OpenJ9 是 Eclipse 基金会的另一个实现，目标是更低的内存占用和更快的启动；GraalVM 带有用 Java 写的 JIT 编译器，还能把 Java 程序提前编译成不依赖 JVM 的原生可执行文件。
- 发行版（distribution）：OpenJDK 是开源项目的源代码，Temurin、Corretto、Zulu 等是不同厂商把同一份源代码构建、测试、打包后发布的二进制，彼此可替换。

可以互换的原因是：`.class` 文件的格式和语义完全由 JVMS 规定，任何通过兼容性测试套件（TCK）的虚拟机都必须按同样的方式执行它。所以同一个 `app.jar` 可以不改一行代码，分别用 HotSpot 和 OpenJ9 运行，行为相同，只是速度、内存、启动时间不同。

本机的实际情况：`java -version` 的输出是 `OpenJDK 64-Bit Server VM Temurin-25...`，即 HotSpot 实现，Temurin 发行版。判断 Java 的某个行为是语言规定的，还是某个虚拟机的特性，就看规范有没有承诺。
