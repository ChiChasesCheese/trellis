---
id: pl-eco-modules-intro-java
node: ecosystem.modules
type: qa
step: 3
---
## Q
Java 的 package、类路径（classpath）和 JPMS 模块（Java Platform Module System）分别是什么？为什么需要在 package 之上再加一层模块？

## A
**package**：类的命名空间，用反向域名约定（`com.company.app`），同时也是 `package-private`（默认可见性）的作用范围。`public` 的类对所有代码可见，没有「只对某些包公开」的办法。

**类路径**：运行时告诉 JVM 去哪些 JAR 里找类的一个扁平列表。所有 JAR 的类混在一起，**同名类先找到谁用谁**，没有强边界：任何代码都能访问任何库里任何 `public` 的类，包括库作者本意只是内部实现的类。这带来「JAR 地狱」：缺失依赖要到运行时才报错，版本冲突悄悄选了一个。

**JPMS 模块（Java 9）**：在 package 之上加一层。模块用 `module-info.java` 声明：

```java
module lib { exports com.lib.api; }      // only this package is public
module app { requires lib; }
```

规则：只有被 `exports` 的 package 对其他模块可见；依赖必须用 `requires` 声明。在编译期强制：`app` 试图导入 `com.lib.internal.Impl`，真实报错是 `package com.lib.internal is not visible (package ... is declared in module lib, which does not export it)`。

**模块的价值**：
1. **强封装**：库作者能真正隐藏实现，不再被别人依赖内部类。
2. **可靠配置**：启动时检查依赖是否齐全、有没有同一个包出现在两个模块里。
3. **JDK 自己被模块化**：`java.base`、`java.sql` 等，可以用 `jlink` 裁剪出只含需要模块的小运行时。

**要记住的一点**：JPMS 解决的是类路径的无边界问题，但大部分应用代码仍然跑在类路径上，真正强制使用它的是 JDK 自己。
