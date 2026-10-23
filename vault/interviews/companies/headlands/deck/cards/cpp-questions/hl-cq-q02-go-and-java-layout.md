---
id: hl-cq-q02-go-and-java-layout
node: cpp-questions.a-why-fast
type: qa
step: 10
---
## Q
追问：Go 在性能上处于什么位置？在 Java 里怎样拿到连续的内存布局？
Where does Go sit? How do you get contiguous layout in Java?

## A
- **Go**：启动快、并发好，但有 GC 和边界检查；峰值吞吐和尾延迟通常落后于 C++。
- **Java 要连续布局**：用原始类型数组、并行数组（parallel arrays），或堆外缓冲区（off-heap buffer）；都是手动的，写起来别扭。
- 补充：Java 靠 JIT 能拿回一部分优化（静态编译器做不到的运行期优化），值类型也在路上，但目前布局仍是结构性差距。
