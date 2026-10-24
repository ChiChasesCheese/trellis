---
id: pl-rt-opt-found-inlining-budget
node: runtime.optimizations
type: qa
step: 3
---
## Q
编译器怎样决定一个函数能不能内联（把函数体替换到调用处）？Go 的 `-m`、Java 的 `PrintInlining` 能看到什么，为什么说内联是“优化之母”？

## A
内联本身只省掉调用开销（约几纳秒），**真正的价值是它打开了别的优化**：调用方和被调用方合并后，常量可以传进函数体、重复计算可以消除、小对象可以拆进寄存器、循环可以融合。所以编译器几乎都把内联放在优化流水线的最前面，并用一个**成本模型**防止代码膨胀：函数越大，越不值得。

**Go**：把函数体按语法树节点数记成“成本”，预算 80（一次编译实测）。`go build -gcflags=-m=2` 输出：
```
can inline square with cost 4 as: func(int) int { return x * x }
can inline sum with cost 25 as: func([]int) int { t := 0; for loop; return t }
cannot inline big: function too complex: cost 121 exceeds budget 80
```
循环、小函数能内联；稍微复杂一点就超预算。

**Java**：JIT 有两个阈值，非热点方法超过 35 字节的字节码就不内联，热点方法放宽到 325 字节（`MaxInlineSize` 和 `FreqInlineSize`）。同一个 131 字节的方法，`-XX:+PrintInlining` 先看到 `failed to inline: callee is too large`（编译早期，尚未知道它是热点），后来变成 `inline (hot)`。**阈值用的是运行时测到的热度**，这是 JIT 才有的信息。

**Rust**：LLVM 按成本自动决定，跨 crate（编译单元）的非泛型函数默认不能内联，除非标 `#[inline]` 或开 LTO（链接期优化）。

**Python**：CPython 不内联函数调用。

所以内联的限制就是抽象的上限：函数小到能被内联，“把逻辑拆成小函数”才没有成本；热点函数膨胀过预算，就会悄悄失去一连串后续优化。
