---
id: hl-cq-q31-detect-avoid
node: cpp-questions.g-concurrency
type: qa
step: 20
---
## Q
怎么发现代码里有伪共享？有哪些具体的避免办法？

## A
**检测**：
- 症状：“加线程反而变慢”、多线程吞吐不随核数增长。
- Linux 上用 `perf c2c` 或 `perf stat` 看缓存未命中。
- 代码审查时找：数组里按线程下标分槽、相邻的原子变量、紧挨着放的生产者 / 消费者索引。

**避免**：
- `alignas(64)`（或 `std::hardware_destructive_interference_size`）；
- 每线程私有累加器，最后合并；
- 把只读数据和被写数据分开放（SPSC 队列的 `head` 和 `tail` 分开放）；
- 代价是内存，所以只给热的、有竞争的变量加填充。
