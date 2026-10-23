---
id: hl-c05-map-orderbook
node: cpp-lessons.c05-stl-containers
type: qa
step: 17
---
## Q
订单簿一侧用什么容器？买盘和卖盘怎么声明才能让最优价 `begin()` 取到？`lower_bound` 返回什么？

## A
`std::map<price, qty>`：红黑树，有序，O(log n)，每个元素一个堆节点。
```cpp
std::map<long, long, std::greater<long>> bids;  // 降序：begin() 是最高买价
std::map<long, long> asks;                      // 升序：begin() 是最低卖价
bids[10010] += 100;
```
- 最优价是 `begin()`，O(1) 取；`rbegin()` 是最大 key。
- `lower_bound(k)` 返回第一个**不在 k 之前**的元素（按该容器排序）：买盘 `lower_bound(10006)` 得到 10005（降序中第一个 ≤ 10006）。
- 按迭代器删除 `asks.erase(it)` 摊销 O(1)。
- 实测：买盘 10010×125 为最优，卖盘 10020×40 为最优。
