---
id: pl-foundations-language-vs-implementation-unique-java-tck
node: foundations.language-vs-implementation
type: qa
step: 6
---
## Q
Java 为什么能同时拥有多个互相兼容的虚拟机实现（HotSpot、OpenJ9、GraalVM），而 Python、Rust 甚至 C++ 做不到同样程度？

## A
Java 把「语言」和「机器」都写成了独立的规范：JLS 规定源代码怎么解释，JVMS 规定 `.class` 字节码文件的格式和每条指令的语义，再加一套规模很大的 TCK 兼容性测试。一个厂商只要实现 JVMS 并通过 TCK，就能名正言顺地叫 Java 实现。

这样做的后果有三条：

- 竞争：Eclipse OpenJ9 追求低内存，GraalVM 追求多语言和原生镜像，HotSpot 追求稳态峰值，用户可以在不改代码的前提下换虚拟机。
- 语言多样性：因为 JVMS 独立于 Java 语言，Kotlin、Scala、Clojure 等语言只要生成合规的字节码就能在任何 JVM 上运行。
- 治理成本：规范要长期向后兼容，每个新特性都要走 JEP 流程并更新规范和测试。

C++ 介于两者之间：有 ISO 标准和 GCC、Clang、MSVC 多个实现，但标准只规定源码的含义，没有统一的二进制格式，也没有 TCK 这样的官方认证；换编译器必须从源码重新编译，各家的 ABI（二进制接口约定）和标准库也不互通。
Python 的情形相反：它的 C 扩展接口暴露了 CPython 的内部结构（对象布局、引用计数），NumPy 这类扩展直接依赖这些细节，别的实现要兼容就得模拟，速度和完整度都打折扣。Rust 则是单一参考实现，语言怎么变由 `rustc` 说了算，靠 edition 机制保持兼容。
