---
id: hl-cq-q02-layout-gap
node: cpp-questions.a-why-fast
type: qa
step: 8
---
## Q
`std::vector<Order>` 和 `std::vector<std::unique_ptr<Order>>` 在内存里有什么结构性差别？Java 的 `ArrayList<Order>` 更像哪一个？

## A
```cpp
std::vector<Order> flat(4);                   // 4 个 Order 连续摆放
std::vector<std::unique_ptr<Order>> boxed;    // 4 个指针，Order 散落在堆上
```
- 实测 `sizeof(Order) = 16`，`flat` 相邻元素恰好相距 16 字节，紧挨着；`boxed` 的 3 对相邻元素里 0 对在内存中相邻（只有分配器碰巧时才相邻），因为 `vector` 存的是地址（`sizeof(unique_ptr<Order>) = 8`），不是订单本身。
- Java 的 `ArrayList<Order>` 就是后一种：一个引用数组。
- 后果：遍历前者是**顺序读**；遍历后者每个元素多一次可能的**缓存未命中**（cache miss）。
