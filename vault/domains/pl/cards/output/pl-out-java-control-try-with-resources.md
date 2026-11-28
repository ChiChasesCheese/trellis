---
id: pl-out-java-control-try-with-resources
node: output.java-control
type: qa
step: 2
---
## Q
**try-with-resources 的顺序**｜读代码说输出

```java
class R implements AutoCloseable {
    String n;
    R(String n) { this.n = n; System.out.println("open " + n); }
    public void close() { System.out.println("close " + n); }
}
public class Main { public static void main(String[] x) {
    try (R a = new R("A"); R b = new R("B")) {
        System.out.println("body");
        throw new RuntimeException("boom");
    } catch (RuntimeException e) {
        System.out.println("catch " + e.getMessage());
    } finally {
        System.out.println("finally");
    }
} }
```

输出什么？

## A
**输出。**
```
open A
open B
body
close B
close A
catch boom
finally
```

**为什么。**
- 资源按声明顺序打开：先 A 后 B。
- 离开 `try` 块（正常或异常）时，资源按相反顺序关闭：先 B 后 A，像栈一样。
- 关闭发生在 `catch` 和 `finally` 之前，所以 `close A` 先于 `catch boom` 输出。

**语言为什么这样设计。**
- JLS 14.20.3 把它定义成嵌套 `try-finally` 的展开：后打开的先关，因为后面的资源可能依赖前面的。若 `close()` 也抛异常，它作为被抑制异常（suppressed）挂到主异常上，不再把主异常盖掉，这是手写 `finally` 常犯的错。
- Python 的 `with a, b:` 同样反序退出；Go 用 `defer`（后进先出）；Rust 靠 `Drop`，变量按声明反序析构；C++ 的析构顺序也是反序（RAII）。

**怎么写才对。**
```java
try (var in = open(); var out = create()) { … }
// 需要时用 e.getSuppressed() 读 close() 的异常
```

**面试里一句话。**
try-with-resources closes in reverse order, before catch and finally run, and keeps close() failures as suppressed exceptions.
