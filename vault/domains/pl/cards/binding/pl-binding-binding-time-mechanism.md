---
id: pl-binding-binding-time-mechanism
node: binding.binding-time
type: qa
step: 5
---
## Q
Java 和 Python 在语言层面是晚绑定的，运行时系统怎样用「猜测 + 守卫」把热点路径变回早绑定？

## A
晚绑定的成本来自「每次都要查」。实现者发现：**同一个调用点在实际运行中绝大多数时候看到同一种类型**，于是做推测（speculation）：先假设它不变，直接走快速路径，再放一个**守卫**（guard）检查假设是否仍成立，不成立就退回慢路径。

**Java（HotSpot JIT）**：在解释执行阶段统计每个虚调用点见过的接收者类型。如果只见过一种，JIT 就把调用替换为该类的实现，并且内联。下面这段代码里，`s.area()` 的调用点只见过 `Sq`：

```text
$ java -XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining Hot
@ 13  Hot$Sq::area (2 bytes)   inline (hot)
      TypeProfile (16260/16260 counts) = Hot$Sq
```

守卫失败时（后来出现了 `Ci`），JIT 会作废这段优化代码，回到解释器重新来过，这叫**去优化**（deoptimization）。同样的道理，如果整个程序里 `Shape` 只有一个已加载的实现类，虚调用可以直接当作静态调用。

**Python（3.11 起的自适应解释器）**：字节码在执行若干次后，会被原地改写成**特化**版本。读 `p.x` 的指令在热身后变成：

```python
dis.dis(get, adaptive=True)   # get(p) returns p.x
# LOAD_ATTR_INSTANCE_VALUE (x)   instead of generic LOAD_ATTR
```

这条指令内部检查对象的类版本，一致就直接按固定偏移读属性，不再逐层查字典，不一致就退回通用版本。

两者思路相同：语言保留了晚绑定的全部语义（猴子补丁、新子类随时可以出现），运行时只在「没有人动过」的前提下走捷径。

提前编译的 C++ 没有运行时可推测，只能在构建期做同类的事：给类或函数标 `final`、开链接时优化（LTO，链接阶段跨文件再优化）看到全部子类，或用 PGO（用一次采样运行的数据指导编译）把常见的虚调用目标先猜出来；一旦编译完成，假设就固定了。
差别在于预算：JIT 会花编译时间做到内联，Python 的特化只省掉查表，所以热点循环里 Java 往往快一个数量级。
