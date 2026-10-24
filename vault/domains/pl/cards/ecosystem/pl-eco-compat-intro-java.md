---
id: pl-eco-compat-intro-java
node: ecosystem.compatibility
type: qa
step: 2
---
## Q
Java 的向后兼容承诺具体指什么？源码兼容、二进制兼容、`--release` 与弃用移除（`forRemoval`）怎样配合，一个例子里发生了什么？

## A
**两层兼容**：
- **二进制兼容**：旧版本编译出的 `.class` 文件，在新版 JVM 上仍然能运行。你不必重新编译。
- **源码兼容**：旧源码在新编译器上仍然能编译。

Java 对前者承诺极强：一个为 Java 8 编译的程序，在 Java 25 上直接运行。

```java
// javac --release 8 Old.java   (compile for the Java 8 platform)
// java Old   ->   compiled for 8, runs on 25.0.4.1
```

真实输出：`compiled for 8, runs on 25.0.4.1`（编译器同时警告 8 已经过时）。

**`--release N`**：编译时指定目标版本，编译器会检查你只用了那个版本存在的 API，避免“用新 JDK 编译，但在旧 JVM 上缺方法”。

**怎样移除不好的东西**：Java 不直接删，而是分两步：先用 `@Deprecated` 标记（不推荐使用），确定要删时加 `forRemoval = true`（下个版本可能删除），编译器会给出“removal”警告。例如 `new Integer(5)` 构造函数。最典型的是 `Thread.stop()`：早已弃用，在较新的 JDK 上调用，真实结果是抛出 `java.lang.UnsupportedOperationException`，而不是停止线程。方法还在，但行为被替换成明确失败。

**新增的做法**：用预览特性（preview features）和孵化模块试验新语法，成熟后才稳定；模块系统（JPMS）对 JDK 内部 API 的封装是少数实质性的破坏，用 `--add-opens` 提供迁移通道。

**要记住的一点**：Java 的原则是“旧程序不应因 JDK 升级而无法运行”，所以它几乎不删，只让错误的东西变得无用或明确失败。
