---
id: pl-out-java-objects-boxed-equals
node: output.java-objects
type: qa
step: 4
---
## Q
**Long 与 Integer**｜读代码说输出

```java
public class Main { public static void main(String[] x) {
    Integer i = 1000;
    int j = 1000;
    Long l = 1000L;
    System.out.println(i == j);
    System.out.println(l.equals(1000));
    System.out.println(l.equals(1000L));
    System.out.println(l == 1000);
} }
```

输出什么？

## A
**输出。**
```
true
false
true
true
```

**为什么。**
- `i == j` 一边是 `int`，另一边自动拆箱（unboxing）成 `int` 再比数值，所以超过缓存范围也是 true。
- `l.equals(1000)`：`1000` 是 `int`，要装箱成 `Integer` 才能传给 `equals(Object)`；`Long.equals` 要求参数也是 `Long`，类型不同直接 false。
- `l.equals(1000L)` 装箱成 `Long`，true；`l == 1000` 又拆箱比数值，true。

**语言为什么这样设计。**
- `equals` 的约定包含「类型相同」，所以 `Long` 与 `Integer` 即使数值相同也不相等，保证对称和传递；`==` 走数值提升（JLS 5.6.2、5.1.8），混用基本类型和包装类型也能比。
- Python 里 `1000 == 1000.0` 就是 True，只有一种数值相等；Kotlin 干脆在编译期拒绝 `Int == Long`。

**怎么写才对。**
```java
l.equals(1000L)        // 类型对齐
Objects.equals(l, 1000L)
```

**面试里一句话。**
Boxed equals checks the type first, so Long.equals(Integer) is false even for the same number.
