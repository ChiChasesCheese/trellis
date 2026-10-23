---
id: hft-machine-cache-lines-java-boxed-objects
node: machine.cache-lines
type: qa
step: 3
---
## Q
在 Java 里用 `ArrayList<Long>` 或 `HashMap<Long, Order>` 存订单数据，和用 `long[]` 原始数组相比，缓存上有什么区别？

## A
区别来自内存布局：

- `long[]`：数据本身连续存放，8 个 `long` 刚好占一个 64 字节缓存行，遍历时一次搬运服务 8 个元素，预取器也好用。
- `ArrayList<Long>`：数组里放的是**引用**（指针，通常 4 或 8 字节），每个 `Long` 是堆上单独的对象，对象头加数据约 16 字节，位置由分配器决定、往往分散。读一个元素要先读引用，再跳到对象，是两次依赖的内存访问，很可能各自未命中。
- `HashMap<Long, Order>`：每个条目还有节点对象、`Long` 键对象、`Order` 值对象，一次查找要跳好几处。

后果：同样 O(n) 的遍历，装箱（boxing，把基本类型包进对象）的版本常慢一个数量级，还会产生大量垃圾对象，加重 GC。所以 HFT 的 Java 代码常用原始类型数组和专用的原始类型集合（如 Agrona 的 `Long2ObjectHashMap`）。
