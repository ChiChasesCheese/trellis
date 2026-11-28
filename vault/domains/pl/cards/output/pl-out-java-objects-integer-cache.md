---
id: pl-out-java-objects-integer-cache
node: output.java-objects
type: qa
step: 1
---
## Q
**Integer 缓存**｜读代码说输出

```java
public class Main { public static void main(String[] x) {
    Integer a = 127, b = 127, c = 128, d = 128;
    System.out.println(a == b);
    System.out.println(c == d);
    System.out.println(c.equals(d));
} }
```

输出什么？

## A
**输出。**
```
true
false
true
```

**为什么。**
- `Integer a = 127` 是自动装箱（autoboxing），编译器改写成 `Integer.valueOf(127)`。
- `valueOf` 对 -128 到 127 返回缓存里的同一个对象，所以 `a == b` 比的引用相同；128 每次新建对象，`c == d` 比的是两个不同对象，false。
- 对引用类型，`==` 永远比身份（identity），`equals` 才比值。

**语言为什么这样设计。**
- JLS 5.1.7 规定这个范围内的装箱必须返回同一对象（上限可用 `-XX:AutoBoxCacheMax` 调大），为的是小整数装箱不用反复分配内存。
- 代价是 `==` 的结果取决于数值大小：测试里用 100 通过，线上遇到 1000 就坏。Python 的 `==` 比值、`is` 才比身份，所以同类问题只出现在误用 `is` 的时候。

**怎么写才对。**
```java
c.equals(d)            // 或 Objects.equals(c, d)
c.intValue() == d      // 一边拆箱成 int，按数值比
```

**面试里一句话。**
== on boxed types compares references, and only values from -128 to 127 are cached, so always compare them with equals.
