---
id: pl-types-type-conversions-found-java-cast
node: types.type-conversions
type: qa
step: 3
---
## Q
Java 里的强制转换 `(T) x` 和 `instanceof` 模式匹配分别做什么？对象转型失败时发生什么？

## A
Java 的 `(T) x` 有两种完全不同的含义，取决于类型：

- 数值类型之间：直接改变表示，可能截断（`(byte) 200` 得 -56）。不检查，不抛异常。
- 引用类型之间的向下转型（downcast）：声称一个 `Object` 引用实际指向 `T` 的实例。JVM 在运行时检查对象的真实类，不符就抛 `ClassCastException`。

`instanceof` 模式匹配（Java 16）把「判断」和「转型」合成一步，条件为真时才引入绑定变量：

```java
Object o = 42;
if (o instanceof Integer n && n > 40) System.out.println("int " + (n + 1));
Object p = "text";
try { Integer bad = (Integer) p; }
catch (ClassCastException e) { System.out.println("CCE"); }
```

实际输出：`int 43`，然后 `CCE`。第一个条件里 `n` 只在判断为真时才存在，不可能漏检查；第二个强制转换在运行时失败。

旧写法 `if (o instanceof Integer) { Integer n = (Integer) o; ... }` 要写两遍类型，且两次必须一致，写错就是运行时异常。所以资深写法几乎总是用模式匹配版本。
