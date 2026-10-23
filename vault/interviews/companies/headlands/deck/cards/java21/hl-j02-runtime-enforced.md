---
id: hl-j02-runtime-enforced
node: java21.j02-sealed
type: qa
step: 11
---
## Q
有人说"`sealed` 只是编译器检查，运行时没用"。怎么反驳？写出两个运行时可观察到的证据，并说明怎么复现 JVM 拒绝。

## A
证据一：class 文件有 **`PermittedSubclasses` 属性**，反射可读：
```java
Result.class.isSealed();                  // true
Result.class.getPermittedSubclasses();    // [Ok, Err]
```
证据二：绕过 `javac`，让不在名单里的子类被加载，JVM 抛 `java.lang.IncompatibleClassChangeError: class Y cannot implement sealed interface S`。

复现：先编译 `S permits X, Y`，再把 `S` 改成 `permits X` 单独重编译、保留旧的 `Y.class`，运行 `new Y()` 即得该异常。所以 `sealed` 是 **JVM 强制的规则**，不是君子协定。
