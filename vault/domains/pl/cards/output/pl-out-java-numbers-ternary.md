---
id: pl-out-java-numbers-ternary
node: output.java-numbers
type: qa
step: 4
---
## Q
**三元运算符的类型**｜读代码说输出

```java
public class Main { public static void main(String[] x) {
    System.out.println(true ? 1 : 2.0);
    Object o = true ? 1 : "s";
    System.out.println(o);
    Integer n = null;
    boolean f = false;
    Integer r2 = f ? Integer.valueOf(1) : n;
    System.out.println(r2);
    try { Integer r = f ? 1 : n; System.out.println(r); }
    catch (NullPointerException e) { System.out.println("NPE"); }
} }
```

输出什么？

## A
**输出。**
```
1.0
1
null
NPE
```

**为什么。**
- `true ? 1 : 2.0`：两个分支都是数值类型，整个表达式按数值提升成 `double`，1 变成 1.0。
- `true ? 1 : "s"`：一个数一个对象，不提升，结果当 `Object`，仍是 1。
- `f ? 1 : n`（`int` 和 `Integer`）也算数值，整个表达式是 `int`，于是对 null 的 `n` 拆箱，NPE。
- `f ? Integer.valueOf(1) : n` 两边都是 `Integer`，不拆箱，得 null。

**语言为什么这样设计。**
- JLS 15.25 按两个操作数的类型决定整个表达式的类型：Java 的每个表达式在编译期都要有一个确定类型，所以必须合并两个分支的类型，规则也因此很多。
- Python 的 `1 if c else 2.0` 运行时选哪个分支就返回哪个值，不合并类型；Kotlin 的 `if` 表达式也不做数值提升。

**怎么写才对。**
```java
cond ? 1.0 : 2.0                      // 两边同类型
Integer r = cond ? Integer.valueOf(1) : n;
```

**面试里一句话。**
A ternary with mixed boxed and primitive operands unboxes, so a null Integer throws NPE and 1 : 2.0 yields 1.0.
