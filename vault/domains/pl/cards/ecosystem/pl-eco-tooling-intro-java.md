---
id: pl-eco-tooling-intro-java
node: ecosystem.tooling
type: qa
step: 4
---
## Q
Java 的工具链为什么由多家工具拼成？JUnit、格式化器、Checkstyle、SpotBugs 和 Error Prone 各是什么？

## A
**事实**：JDK 只提供编译器 `javac`、运行时和少数工具（`jshell`、`javadoc`、`jfr`），**没有官方的格式化器、测试框架、统一的静态检查器**。这些都是社区和厂商生态。

**常见的组合**：
- **JUnit**（目前是 JUnit 5，又称 Jupiter）：事实标准的测试框架，用 `@Test` 注解标记测试方法，配合 Mockito（模拟对象）和 AssertJ（断言库）。运行通常通过 Maven 或 Gradle。
- **格式化器**：`google-java-format`、Spotless（Maven/Gradle 插件，把格式化接入构建）、IDE 内置格式化。没有唯一标准，每个团队选一个。
- **Checkstyle**：基于规则检查代码规范（命名、长度、Javadoc）。
- **SpotBugs**：分析**字节码**找 bug 模式（空指针、资源泄漏）。
- **Error Prone**：Google 的 `javac` 插件，在编译时发现常见错误，比如把 `Integer` 用 `==` 比较、忽略返回值。
- **IDE**（IntelliJ IDEA、Eclipse）：自带大量检查与重构，是 Java 开发体验的重要部分。

**为什么是多家**：Java 诞生时语言团队专注于语言和 JVM，把工具留给生态；生态因此极其丰富、可定制，也意味着每个项目都在做选择和配置，不同项目的风格和检查口径不同。企业里常由平台团队统一一套配置（parent POM），再通过 CI 强制。

**要记住的一点**：Java 的工具是“选择多、配置多、功能强”；要点是在项目里用构建插件（Spotless、Checkstyle）把它们接进 `mvn verify`，否则它们只存在于某些人的 IDE 里。
