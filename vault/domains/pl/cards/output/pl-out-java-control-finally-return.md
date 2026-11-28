---
id: pl-out-java-control-finally-return
node: output.java-control
type: qa
step: 1
---
## Q
**finally 里的 return**｜读代码说输出

```java
public class Main {
    static int a() { try { return 1; } finally { return 2; } }
    static int b() { int x = 0; try { return x; } finally { x = 5; } }
    static int c() { try { throw new RuntimeException("t"); } finally { return 3; } }
    public static void main(String[] args) {
        System.out.println(a());
        System.out.println(b());
        System.out.println(c());
    }
}
```

输出什么？

## A
**输出。**
```
2
0
3
```

**为什么。**
- `a()`：`try` 里的 `return 1` 先记下返回值，再执行 `finally`；`finally` 里的 `return 2` 把它覆盖，结果 2。
- `b()`：`return x` 在进入 `finally` 前就把值 0 拷出来了，`finally` 里改 `x` 不影响已保存的返回值，仍是 0。
- `c()`：异常正在传播，`finally` 里的 `return` 把它吞掉，返回 3，没人看到 `RuntimeException`。

**语言为什么这样设计。**
- JLS 14.20.2 规定 `finally` 总会执行；如果它自己突然结束（`return`、`throw`），原来的返回值或异常就被丢弃。这保证清理代码一定运行，也让这种写法很危险。
- Python 的 `finally` 有同样行为，3.14 起对 `finally` 里的 `return` 发出 SyntaxWarning（PEP 765）；javac 加 `-Xlint:finally` 也会警告。

**怎么写才对。**
```java
try { … } finally { cleanup(); }   // finally 只做清理，不 return、不 throw
```

**面试里一句话。**
A return or throw inside finally overrides whatever the try block was returning or throwing.
