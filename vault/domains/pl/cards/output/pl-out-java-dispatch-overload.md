---
id: pl-out-java-dispatch-overload
node: output.java-dispatch
type: qa
step: 1
---
## Q
**重载看静态类型**｜读代码说输出

```java
public class Main {
    static void f(Object o) { System.out.println("Object"); }
    static void f(String s) { System.out.println("String"); }
    public static void main(String[] x) {
        Object o = "s";
        f(o);
        f("s");
        f(null);
        f((Object) "s");
    }
}
```

输出什么？

## A
**输出。**
```
Object
String
String
Object
```

**为什么。**
- 重载解析（overload resolution）发生在编译期，只看参数的静态类型（声明类型）：`o` 声明为 `Object`，选 `f(Object)`，尽管它实际指向 String。
- `f("s")` 与 `f(null)`：两个方法都适用，编译器选更具体的 `f(String)`。
- `(Object) "s"` 把静态类型改回 `Object`。

```mermaid
%%{init: {"flowchart": {"wrappingWidth": 320}, "themeVariables": {"fontSize": "18px"}}}%%
flowchart LR
A["编译期：静态类型"] --> B["选定签名 f(Object)"] --> C["运行期：只看接收者"]
```

**语言为什么这样设计。**
- JLS 15.12.2 把「选哪个签名」放在编译期，运行期只对接收者（点号前的对象）做虚分派（virtual dispatch）：这是单分派（single dispatch），实现简单，调用快，还能静态检查方法是否存在。
- Common Lisp 的 CLOS 和 Julia 是多重分派（multiple dispatch），参数的实际类型也参与选择；Java 要用访问者模式（visitor）去模拟。

**怎么写才对。**
```java
switch (o) {                       // Java 21 模式匹配，按实际类型分支
    case String s -> f(s);
    default -> f(o);
}
```

**面试里一句话。**
Overloads are chosen at compile time from static types, overrides at run time from the receiver's actual class.
