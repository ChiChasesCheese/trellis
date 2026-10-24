---
id: pl-types-strong-weak-found-implicit-conversion
node: types.strong-weak
type: qa
step: 2
---
## Q
什么是隐式类型转换（implicit conversion）？在 Java 里什么时候会发生？

## A
隐式转换指编译器或运行时在你没有明确写转换的情况下，自动把一种类型的值变成另一种，让表达式得以成立。

Java 里有两种最常见：

- 数值加宽（widening）：窄类型赋给或参与运算于宽类型时自动转换，`int` 到 `long` 到 `float` 到 `double`。
- 字符串拼接：`+` 的一侧是 `String` 时，另一侧的任何值都被自动转成文字。

```java
int i = 7;
long l = i;            // 加宽，自动
double d = l;          // 自动
String s = "n=" + i;   // + 把 int 变成文字
System.out.println(l + " " + d + " " + s);
```

实际输出 `7 7.0 n=7`。

隐式转换的利弊是同一件事：它省掉了样板，但转换点从代码里消失了。读者看不出这里发生了类型变化，也看不出是否丢失信息（`int` 转 `float` 就可能丢精度）。不同语言对这件事的态度，是「强类型」与「弱类型」的区别：隐式转换越多，越「弱」。
