---
id: pl-types-static-dynamic-unique-java-two-types
node: types.static-dynamic
type: qa
step: 7
---
## Q
Java 里 `Object o = "hi";` 之后为什么 `o.length()` 编译不过，尽管 `o` 运行时确实是一个字符串？

## A
Java 里一个引用有两个类型：静态类型（static type）是变量声明时写的类型，编译器只根据它检查；动态类型（dynamic type）是对象在运行时的真实类，由对象头记录。`Object o = "hi"` 中，`o` 的静态类型是 `Object`，动态类型是 `String`。

```java
Object o = "hi";
System.out.println(o.getClass().getSimpleName());   // String
System.out.println(o.length());                     // 编译错误
```

第一行输出 `String`（运行时问对象）。第二行编译失败：

```console
Ob.java:5: error: cannot find symbol
  symbol:   method length()
  location: variable o of type Object
```

编译器只相信静态类型 `Object`，而 `Object` 没有 `length()`。要调用，必须向下转型 `((String) o).length()`，转型会在运行时再核对一次。

这是 Java 独有的双层结构：编译期按声明类型检查，运行期按真实类型分派方法（所以 `o.toString()` 会执行 `String` 的版本）。Python 只有动态类型，没有这种区分；Go 的普通变量只有静态类型，接口变量才同时有静态的接口类型和动态的具体类型，行为与 Java 接近；Rust 默认只有静态类型，用 `dyn Trait`（trait 对象，运行时才确定具体类型）才引入运行时类型。
