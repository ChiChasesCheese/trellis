---
id: pl-abstraction-interfaces-traits-foundation-java-interface-default
node: abstraction.interfaces-traits
type: qa
step: 2
---
## Q
Java 的接口和 `default` 方法是什么？为什么 Java 8 要允许接口带实现，这又带来了什么新冲突？

## A
Java 接口是一份「方法签名清单」，类用 `implements` 显式声明遵守它，一个类可以实现多个接口。接口原先只有签名，没有任何实现。

问题出在**接口演进**：要给已发布的 `Collection` 增加 `stream()`，所有第三方实现类都会因为缺这个方法而编译失败。Java 8（2014）的解法是 `default` 方法：接口里直接给出默认实现，旧类无需改动。

```java
interface Greeter {
    String name();
    default String greet() { return "hello " + name(); }
}
record En(String name) implements Greeter {}
new En("ann").greet();   // "hello ann"
```

代价是菱形问题以小规模回来了：一个类同时实现两个带同名 `default` 方法的接口，编译器无法选择，直接报错：

```java
interface A { default String hi() { return "A"; } }
interface B { default String hi() { return "B"; } }
class C implements A, B { }
// error: types A and B are incompatible;
//   class C inherits unrelated defaults for hi() from types A and B
```

规则是类自己覆写该方法消除歧义（可以用 `A.super.hi()` 指定调用谁）。接口因此仍然没有字段，只带行为，这是它与抽象类的根本区别。
