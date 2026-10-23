---
id: hl-c06-priority-queue-default
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 7
---
## Q
C++ `std::priority_queue` 默认是大顶堆还是小顶堆？怎么声明小顶堆？自定义比较器的方向怎么理解？

## A
- 默认是**大顶堆**（`top()` 是最大值）；Java 的 `PriorityQueue` 默认是小顶堆。
- 小顶堆（Java 的默认行为）：

```cpp
std::priority_queue<int, std::vector<int>, std::greater<int>> minheap;
```
- 自定义比较器的含义是「**谁排在下面**」，与直觉相反：传 `greater` 得小顶堆。
- 带自定义类型：`auto cmp = [](const Trade& a, const Trade& b) { return a.qty*a.px > b.qty*b.px; };` 再 `std::priority_queue<Trade, std::vector<Trade>, decltype(cmp)> pq(cmp);`
