---
id: pl-out-java-init-lazy-static
node: output.java-init
type: qa
step: 4
---
## Q
**类什么时候初始化**｜读代码说输出

```java
class K {
    static final int MAX = 10;
    static final Integer BOX = 20;
    static int n = 30;
    static { System.out.println("K init"); }
}
public class Main { public static void main(String[] x) {
    System.out.println(K.MAX);
    System.out.println(K.BOX);
    System.out.println(K.n);
} }
```

输出什么？

## A
**输出。**
```
10
K init
20
30
```

**为什么。**
- 类在第一次主动使用时才初始化：`new`、调用静态方法、读写非常量的静态字段。
- `MAX` 是 `static final int` 且用常量初始化，属于编译期常量，javac 把 10 直接内联到使用处，不会触发 `K` 的初始化。
- `BOX` 是 `static final`，但 `Integer` 对象不是常量，读它触发初始化：先执行静态块打印 `K init`，再得到 20；之后读 `n` 时类已初始化，直接 30。

**语言为什么这样设计。**
- JLS 12.4.1 规定初始化时机。常量内联让 `switch` 的 case 和注解值可以使用常量，也避免循环依赖，代价是改了常量后，用到它的类必须重新编译，否则还是旧值。
- Python 的 import 立即执行模块顶层代码；Go 的 `init()` 在程序启动时按依赖顺序执行，都不是懒加载。

**怎么写才对。**
```java
class Holder { static final Service S = new Service(); }   // holder idiom：首次用 Holder.S 才创建
```

**面试里一句话。**
A class initializes on first active use, and reading a compile-time constant does not count as use.
