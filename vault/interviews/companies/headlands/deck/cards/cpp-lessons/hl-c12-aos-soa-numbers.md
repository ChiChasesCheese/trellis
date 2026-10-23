---
id: hl-c12-aos-soa-numbers
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 5
---
## Q
400 万订单按 `px*qty` 求和：`vector<Order>`、`vector<unique_ptr<Order>>`（乱序）、SoA 各每订单多少纳秒？只汇总 `qty` 一列呢？说明什么？

## A
每订单纳秒：
- `vector<Order>`：0.335
- `vector<unique_ptr<Order>>`（内存顺序被打乱，Java 风格）：2.744
- struct of arrays（只读 px、qty 两列）：0.144
- 只汇总 `qty`：`vector<Order>` 0.271，SoA 0.072

读法：连续 `vector` 比指针数组快约 **9 倍**；SoA 只读需要的列，再快一倍多；只汇总一列时 SoA 又快约 3 倍（整条缓存行都是有用数据，还能向量化）。字段顺序也影响大小：`Order` 32 字节，字段顺序不当的 `OrderBad` 变 40 字节。
