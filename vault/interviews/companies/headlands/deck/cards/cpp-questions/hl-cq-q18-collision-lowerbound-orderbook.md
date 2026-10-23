---
id: hl-cq-q18-collision-lowerbound-orderbook
node: cpp-questions.d-containers
type: qa
step: 10
---
## Q
三个追问：`unordered_map` 怎么解决哈希冲突？`map::lower_bound` 的复杂度和含义？订单簿（order book）用什么数据结构？

## A
- **冲突**：分离链接（separate chaining），每个桶是节点链表；负载因子（load factor）控制何时 rehash。
- **`lower_bound`**：O(log n)，返回第一个“不小于”给定 key 的元素。
- **订单簿**：每一边一个按价格为 key 的 `std::map`；价格范围有界时可以用以 tick 为下标的平铺数组；再加一个从订单 id 到其位置的哈希表。
