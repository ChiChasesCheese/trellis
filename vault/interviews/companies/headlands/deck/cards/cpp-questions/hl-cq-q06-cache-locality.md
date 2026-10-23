---
id: hl-cq-q06-cache-locality
node: cpp-questions.a-why-fast
type: qa
step: 31
---
## Q
面试题：为什么 `std::vector` 扫描比 `std::list` 快 20 倍，明明两者都是 O(n)？什么是缓存局部性？
Why can a `std::vector` scan beat a `std::list` scan by 20x even though both are O(n)? What is cache locality?

## A
一句话：Big-O 不计内存访问成本。
- CPU 一次读一整条**缓存行**（cache line，通常 **64 字节**），顺序访问时后面的数据已经在缓存里，硬件还会**预取**（prefetch）。
- 链表节点散落在堆上，每个节点都可能是一次**缓存未命中**，单次约 **100 ns** 级别，比一次加法慢两个数量级。
- 所以延迟敏感代码默认用连续容器，并让热数据紧凑。
