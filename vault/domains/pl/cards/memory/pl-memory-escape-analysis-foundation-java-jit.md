---
id: pl-memory-escape-analysis-foundation-java-jit
node: memory.escape-analysis
type: qa
step: 3
---
## Q
Java 的 JIT 和标量替换（scalar replacement）是什么？它怎样让一个 `new` 出来的对象根本不存在？

## A
Java 先把代码编译成字节码，由 JVM 解释执行；运行中发现某些方法被频繁调用（“热点”），就启动 **JIT**（Just-In-Time，即时编译器，HotSpot 里的高优化版叫 C2），把它编译成优化的机器码。JIT 能做**内联**（inlining）：把被调用的小方法直接展开到调用处，让优化器看到更大的范围。

在内联之后的范围里，JIT 做逃逸分析：如果一个 `new` 出来的对象没有被返回、没有存进堆上的字段或集合、没有传给看不见的代码，就是“不逃逸”。这时 JIT 可以做**标量替换**：不创建对象，把它的字段拆成独立的局部变量，放进寄存器。

```java
record Point(int x, int y) {}
static int sum(int i) { Point p = new Point(i, i + 1); return p.x() + p.y(); }
```

内联到循环里后，`sum` 等价于 `return i + (i + 1)`：`Point` 对象没有分配，没有对象头，也没有 GC。

实测（一亿次调用，`-Xmx64m`）：开启逃逸分析（默认）时 0 次 GC，约 0.04 s；用 `-XX:-DoEscapeAnalysis` 关闭后有 134 次 GC，约 0.21 s。

这是尽力而为的优化：依赖方法被内联、已经预热、对象不被其他代码引用；任何一环不满足，对象就是真实的堆对象。

要记住的一个事实：Java 的逃逸分析在运行期由 JIT 完成，是一个机会性的红利，而不是语言的承诺。
