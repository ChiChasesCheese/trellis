---
id: hl-cq-q18-map-vs-unordered
node: cpp-questions.d-containers
type: qa
step: 7
---
## Q
面试题：`std::map`、`std::unordered_map` 和排序 `vector` 怎么实现？各在什么时候用？
`std::map` vs `std::unordered_map` vs a sorted `vector`: how do they work and when do you use each?

## A
- **`map`**：红黑树，有序，O(log n)，节点式，引用稳定。
- **`unordered_map`**：哈希表，平均 O(1)，无序；rehash 使**迭代器**失效，但**不使指向元素的引用 / 指针失效**。
- **排序 `vector` + 二分**：小数据或读多写少时常常最快，没有逐节点分配。
- 选择：纯查找用哈希表；要有序遍历或范围查询（比如订单簿的价格档位）用树；追求延迟时考虑开放寻址哈希表，因为标准的 `unordered_map` 每个节点单独分配。
