---
id: pl-abstraction-encapsulation-foundation-java-access-modules
node: abstraction.encapsulation
type: qa
step: 2
---
## Q
Java 有哪几级访问控制？模块系统（JPMS）为什么还要再加一层，反射怎样绕过 `private`？

## A
四级访问修饰符，从严到宽：

- `private`：仅本类；
- 无修饰（包私有，package-private）：同一个包；
- `protected`：同包，加上其他包里的子类；
- `public`：处处可见。

`private` 由编译器和 JVM 共同检查，但在 Java 里是**可以被反射绕开**的：

```java
Field f = Acct.class.getDeclaredField("balance");   // private int balance
f.setAccessible(true);
f.get(acct);     // 100：成功读到私有字段
```

这曾是 Java 生态的暗门：序列化库、ORM、测试框架都靠它，而且很多库偷偷伸手进 JDK 内部（比如 `sun.misc.Unsafe`、`String.value`）。Java 9 引入**模块系统**（JPMS）：模块用 `module-info.java` 声明 `exports` 哪些包。**没有被导出的包，即使里面的类是 `public`，别的模块也访问不到**。Java 16 起（JEP 396，17 去掉了放宽开关）默认强封装 JDK 内部：

```java
Field g = String.class.getDeclaredField("value");
g.setAccessible(true);
// InaccessibleObjectException: module java.base does not
//   "opens java.lang" to unnamed module
```

所以现在 Java 有两层：类层面的 `private`（防同事误改），模块层面的 `exports`（防整个生态依赖内部实现）。后者是为了让 JDK 自己能演进内部结构而不被第三方库钉死。
