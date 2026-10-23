---
id: hl-cq-q18-script
node: cpp-questions.d-containers
type: qa
step: 11
---
## Q
用英文 60 秒回答：`std::map` vs `std::unordered_map` vs a sorted `vector`: how do they work and when do you use each?

## A
结构：树与哈希表（rehash 失效迭代器不失效引用）→ `operator[]` 会插入 → 百万 key 数字 → 选择（查找用哈希、有序/范围用树如订单簿、小而读多用平铺有序数组）→ 低延迟考虑开放寻址。

- `std::map` is a **red-black tree**: ordered, O(log n), node-based, with stable references. `std::unordered_map` is a **hash table**: average O(1), unordered, and a **rehash invalidates iterators** - but not references to elements, which I verified.
- `operator[]` **inserts** a default value if the key is missing, so for lookups I use `find` or `contains`.
- With a million keys the hash map was about ten times faster than the tree for lookups, and a **sorted vector with binary search** was in between and needs no per-node allocation.
- I'd choose the hash map for pure lookup, the tree when I need ordered iteration or range queries like an order book's price levels, and a flat sorted array for small, read-mostly data.
- For latency-critical lookups I'd consider an open-addressing table, since the standard one allocates per node.
