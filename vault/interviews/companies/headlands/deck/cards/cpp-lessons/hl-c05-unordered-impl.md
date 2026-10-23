---
id: hl-c05-unordered-impl
node: cpp-lessons.c05-stl-containers
type: qa
step: 13
---
## Q
面试问：`std::unordered_map` 怎么实现？负载因子和 rehash 是什么？什么时候最坏？
Interview question: How is `std::unordered_map` implemented, and when does it degrade?

## A
- 标准库实现是**链式哈希**：桶数组，哈希值取模选桶，桶里是链表；每个元素是单独分配的**节点**，所以引用稳定。
- **负载因子**（load factor）= 元素数 / 桶数，超过 `max_load_factor`（默认 1.0）就 **rehash**：桶数约翻倍并取素数，所有元素重新分桶，**迭代器失效**，元素地址不变。
- 实测 rehash 点：1→2、3→5、6→11 … 10 万元素时桶数 102877，负载因子 0.97。
- 平均 O(1)，**最坏 O(n)**（哈希碰撞）；缓存不友好（节点分配），热路径常换成开放寻址哈希表。
- 遍历顺序不确定，不要依赖。
