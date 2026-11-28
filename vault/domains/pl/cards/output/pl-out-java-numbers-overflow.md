---
id: pl-out-java-numbers-overflow
node: output.java-numbers
type: qa
step: 1
---
## Q
**整数溢出**｜读代码说输出

```java
public class Main { public static void main(String[] x) {
    int m = Integer.MAX_VALUE, big = 1_000_000;
    System.out.println(m + 1);
    System.out.println(Math.abs(Integer.MIN_VALUE));
    System.out.println(big * big);
    System.out.println((long) big * big);
    System.out.println((int) 3_000_000_000L);
} }
```

输出什么？

## A
**输出。**
```
-2147483648
-2147483648
-727379968
1000000000000
-1294967296
```

**为什么。**
- `int` 是 32 位补码（two's complement）：最大值加 1 回绕（wrap around）到最小值，不报错。
- `Math.abs(MIN_VALUE)`：正数 2147483648 装不下，结果还是它自己，仍是负数。
- `big * big` 在 `int` 里先乘再回绕，10^12 只剩低 32 位；等赋给 `long` 时已经错了，要先 `(long) big` 再乘。`(int) 3_000_000_000L` 同理只留低 32 位。

**语言为什么这样设计。**
- JLS 15.18.2 规定整数溢出静默回绕，不抛异常：结果在所有平台一致，每次加法就是一条 CPU 指令。
- Rust 的 debug 构建会 panic，Python 的整数无限精度，C++ 有符号溢出是未定义行为；Java 选的是「定义好但静默」。

**怎么写才对。**
```java
Math.addExact(m, 1);          // 溢出抛 ArithmeticException
(long) big * big;             // 先拓宽再乘
```

**面试里一句话。**
Java ints wrap silently on overflow; use Math.addExact or widen to long before multiplying.
