---
id: hl-c12-cache-layout
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 4
---
## Q
机制二：为什么值类型和内存布局让 C++ 更快？`vector<Order>` 和 Java 的 `List<Order>` 遍历有何不同？

## A
- 现代 CPU 的瓶颈往往是**内存**而不是算术：一次主存访问约等于几百条指令。CPU 以**缓存行**（通常 64 字节）为单位取数据，并预取顺序访问的数据。
- **C++**：`vector<Order>` 是一整块连续内存，每个元素就是 `Order` 本身。
- **Java**：`List<Order>` 是引用数组，每个 `Order` 是堆上另一个带对象头（约 12–16 字节）的对象，GC 搬动后相邻关系还可能变化。遍历 = **指针追逐**。
- 结构体字段顺序影响 padding；「热字段」和「冷字段」分开（SoA，struct of arrays）能让只访问部分字段的循环少读几倍数据。
