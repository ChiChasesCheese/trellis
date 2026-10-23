---
id: hl-javaq-a-q02-layout
node: java-questions.a-speed
type: qa
step: 7
---
## Q
`std::vector<Order>` 和 Java 的 `ArrayList<Order>` 在内存布局上有什么区别？这对速度有多大影响？给出量级数字。

## A
- **C++**：`std::vector<Order>` 是连续内存，遍历是顺序读，缓存友好。
- **Java**：`ArrayList<Order>` 是"指针数组"，每个 `Order` 散落在堆上，遍历要**追指针**（pointer chasing）。
- 实测：1200 万个 long，`long[]` 求和约 **2 ms**，打乱顺序的 `Long[]` 约 **29 ms**，约 10 倍；这是缓存局部性（cache locality）的代价，不是指令数的代价。
- **小对象无头**：C++ 的 `struct {int; long;}` 没有对象头；Java 同样的 record 每个实例有 **12 字节对象头**，`P2(int,int)` 占 24 字节。
- **没有隐式暂停**：C++ 不分配就没有 malloc，没有 GC 线程抢核，没有 safepoint。
- Java 靠 JIT 把部分差距追回，但内存模型是结构性差距。
