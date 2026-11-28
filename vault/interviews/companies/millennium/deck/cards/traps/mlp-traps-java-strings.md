---
id: mlp-traps-java-strings
node: traps.java-output
type: qa
step: 1
---
## Q
**字符串 ==、Integer 缓存、整数溢出**｜语言陷阱与读代码

下面的 Java 代码输出什么？

```java
String a = "hi", b = "hi";
String c = new String("hi");
String d = "h" + "i";
String e = "h"; String f = e + "i";
System.out.println((a == b) + " " + (a == c) + " " + (a == d) + " " + (a == f) + " " + a.equals(c));
Integer x = 127, y = 127, p = 128, q = 128;
System.out.println((x == y) + " " + (p == q) + " " + p.equals(q));
long big = 1_000_000 * 3_000;
int m = Integer.MAX_VALUE;
System.out.println(big + " " + (m + 1) + " " + Math.abs(Integer.MIN_VALUE));
```

## A
**输出。**
```
true false true false true
true false true
-1294967296 -2147483648 -2147483648
```

- **`a == b` 为 true：** 字符串字面量放在常量池（string pool），相同内容共用一个对象。
- **`a == c` 为 false：** `new String` 总是新建对象；`==` 比较的是引用（是不是同一个对象），不是内容。
- **`a == d` 为 true：** `"h" + "i"` 是编译期常量，编译时合并成 `"hi"`；**`a == f` 为 false：** `e` 是变量，拼接发生在运行时，产生新对象。
- **Integer 缓存：** 装箱时 -128 到 127 复用同一批对象，所以 127 的 `==` 为 true，128 为 false；比较内容永远用 `equals`。
- **溢出：** `1_000_000 * 3_000` 先按 `int` 算，3×10⁹ 超过 2147483647 回绕成负数，再赋给 `long`；要写 `1_000_000L * 3_000`。`MAX_VALUE + 1` 回绕为最小值，`Math.abs(MIN_VALUE)` 没有对应的正数，仍是负数。
- **记住：** 比较对象内容用 `equals`；运算在赋值前就按操作数的类型完成；Java 的整数溢出不报错。

**英文答法。**
- "`==` compares **references**; I'd use `equals` for content."
- "The multiplication happens in **int** and overflows before it's widened to long."
