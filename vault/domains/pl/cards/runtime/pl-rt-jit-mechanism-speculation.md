---
id: pl-rt-jit-mechanism-speculation
node: runtime.jit
type: qa
step: 5
---
## Q
JIT 怎样基于运行时观测做推测优化？请用 Java 虚调用的内联与去优化（deoptimization）说明，调用点见到的类型数怎样影响速度。

## A
JIT 的独特能力是**基于运行时观测的推测优化**。一个接口调用 `shape.area()`，静态地看可能有任意多个实现，AOT 编译器只能做虚表查找（或在能证明时才内联）。HotSpot 在 profile 里发现这个调用点一直只见到一种类型，就生成：

`if (obj.class == A) { 内联 A.area() 的代码 } else { 去优化 }`

虚调用变成一次类型比较加内联体，进而可以继续做常量传播、消除分配等。

实验（Java 25，先只用 1 种实现预热，再改变调用点见到的实现种类，一次测量）：
```java
interface Shape { double area(); }   // records A, B, C, D implement it
static double sum(Shape[] s) { double t = 0; for (Shape x : s) t += x.area(); return t; }
```
| 调用点见到的类型数 | 每次调用耗时 |
|---|---|
| 1 | 0.52 ns |
| 2 | 0.56 ns（双态内联，依然很快） |
| 4 | 1.20 ns（超过阈值，退化为虚表分派） |

用 `-XX:+PrintCompilation` 能看到推测失败的痕迹：
```
Deopt::sum (42 bytes)   made not entrant: uncommon trap
```
即旧代码因“罕见陷阱”被作废，随后重新编译为更通用的版本。

含义：
1. 同样的代码，**调用点的类型多样性**决定速度：热路径上保持单态或双态，多态的虚调用才会被内联。
2. AOT 语言里这类优化需要 PGO（按剖析数据反馈编译）或程序员显式做（Rust 的泛型单态化让编译器看到具体类型，Go 的接口调用不内联，除非能证明类型）。
3. JIT 的“快”建立在可撤销的假设上，所以延迟里会出现偶发的去优化抖动。
