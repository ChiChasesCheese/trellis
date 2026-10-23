---
id: hl-cq-cs13-map-unordered
node: cpp-questions.cheatsheet
type: qa
step: 13
---
## Q
一句话背诵：`map` 和 `unordered_map` 的复杂度、`operator[]` 的陷阱、rehash 的影响、100 万键查询耗时。

## A
- `map`：红黑树，有序，O(log n)。`unordered_map`：哈希表，平均 O(1)。
- `operator[]` **会插入**。
- rehash 使迭代器失效，但**不使引用失效**。
- 100 万键查询：`map` **146 ms**，哈希 **13 ms**，排序 `vector` **45 ms**。
