---
id: pl-out-java-numbers-char-arith
node: output.java-numbers
type: qa
step: 3
---
## Q
**char 做算术**｜读代码说输出

```java
public class Main { public static void main(String[] x) {
    char c = 'a';
    System.out.println(c + 1);
    System.out.println((char) (c + 1));
    c += 1;
    System.out.println(c);
    System.out.println("" + c + 1);
    System.out.println('a' + 'b' + "c");
    System.out.println("c" + 'a' + 'b');
} }
```

输出什么？

## A
**输出。**
```
98
b
b
b1
195c
cab
```

**为什么。**
- `c + 1`：`char` 参与算术先提升（promote）成 `int`，所以是 98；强转回 `char` 才是 b。
- `c += 1` 的复合赋值自带隐式强转，不用写 cast，`c` 变成 'b'。
- `"" + c + 1` 从左到右，已经是字符串拼接，1 变成文本，得 b1。
- `'a' + 'b' + "c"` 先 97 + 98 = 195，再拼 "c"；`"c" + 'a' + 'b'` 一开始就是字符串，得 cab。

**语言为什么这样设计。**
- `char` 在 JVM 里是 16 位无符号整数，二元运算一律先提升到 `int`（JLS 5.6.2），字节码只需要 `int` 运算指令；`+=` 的隐式窄化（JLS 15.26.2）让 `c += 1` 不必写强转。
- Python 没有 char，`"a" + 1` 直接 TypeError，不会悄悄变成数字；Go 的 `rune` 也是整数，转成文本要显式 `string(r)`。

**怎么写才对。**
```java
String.valueOf(c) + 1          // 先转字符串再拼
(char) (c + 1)                 // 要字符就强转回去
```

**面试里一句话。**
A char promotes to int in arithmetic, and + only becomes string concatenation once a String appears on the left.
