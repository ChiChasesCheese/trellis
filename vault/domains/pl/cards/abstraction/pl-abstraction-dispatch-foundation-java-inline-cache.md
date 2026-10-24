---
id: pl-abstraction-dispatch-foundation-java-inline-cache
node: abstraction.dispatch
type: qa
step: 3
---
## Q
Java 的 JIT 怎样让接口调用接近静态调用？内联缓存（inline cache）与 monomorphic、bimorphic、megamorphic 是什么意思？

## A
JVM 先解释执行字节码，并记录每个调用点（call site）**实际见过哪些类型的对象**；热点代码再交给 JIT 编译器优化。基于这份统计，JIT 做**推测性优化**：

- **monomorphic**（单态）：一个调用点只见过一种类型。JIT 在那里放一个类型检查（guard），命中则直接内联该类型的方法体，没命中则去优化回退。
- **bimorphic**（双态）：见过两种类型，放两个检查，各自内联。
- **megamorphic**（多态，三种及以上）：JIT 放弃内联，走普通的虚表 / 接口表调用。

另有一招**类层次分析**（class hierarchy analysis）：如果当前已加载的类里，某个接口只有一个实现，JIT 就直接把调用当成静态的；将来加载了第二个实现，则让已编译的代码失效（deoptimization）并重新编译。

```java
Shape s = shapes[i];   // 数组里全是 Circle：monomorphic，内联
s.area();              // 数组里混了 Circle/Rect/Tri：megamorphic，不内联
```

这套机制的哲学是：**写代码时用最灵活的抽象，把赌注押在运行期的真实分布上**，赌输了才付代价。因此 Java 里「接口调用慢」大多是误解，除非调用点真的见到了太多种类型。
