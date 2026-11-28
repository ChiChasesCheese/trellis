---
id: pl-out-java-numbers-divmod
node: output.java-numbers
type: qa
step: 2
---
## Q
**整除与取模**｜读代码说输出

```java
public class Main { public static void main(String[] x) {
    System.out.println(-7 / 2);
    System.out.println(-7 % 2);
    System.out.println(7 % -2);
    System.out.println(Math.floorMod(-7, 2));
    System.out.println(5 / 2 * 2.0);
    System.out.println(5 / 2.0 * 2);
} }
```

输出什么？

## A
**输出。**
```
-3
-1
1
1
4.0
5.0
```

**为什么。**
- 整数除法向零截断（truncate toward zero）：-7/2 是 -3.5，截成 -3。
- `%` 满足 `(a/b)*b + a%b == a`，所以 -7 % 2 = -7 - (-3*2) = -1，符号跟被除数；`7 % -2` 是 1。
- `Math.floorMod(-7, 2)` 向负无穷取整，结果非负，是 1。
- `5 / 2 * 2.0` 从左算：先整数除得 2，再乘 2.0 得 4.0；`5 / 2.0 * 2` 先得 2.5，再得 5.0。

**语言为什么这样设计。**
- 向零截断来自 C：x86 的除法指令本来就这样算，后来的 Java、Go、Rust 都沿用，换来最快的 `/` 和 `%`。
- Python 和 Ruby 选了向下取整（floor），`i % n` 永远落在 0..n-1，环形下标很方便；Java 里同样写法会得到负下标。

**怎么写才对。**
```java
int idx = Math.floorMod(i, n);        // 环形下标
double r = (double) a / b;            // 先转再除
```

**面试里一句话。**
Java integer division truncates toward zero, so % takes the sign of the dividend; use floorMod for wraparound indexes.
