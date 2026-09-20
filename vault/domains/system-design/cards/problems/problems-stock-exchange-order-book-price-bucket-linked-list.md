---
id: problems-stock-exchange-order-book-price-bucket-linked-list
node: problems.commerce.stock-exchange
type: qa
step: 2
tags: [grown]
---
## Q
In a matching engine's order book, why is a price bucket (array or hash table indexed by price) with a doubly-linked list of orders per bucket a better data structure than a balanced tree (e.g. red-black tree) keyed by price, given a microsecond-level latency budget per order?

## A
Prices are discrete (bounded by a minimum tick size), so they can be indexed directly in O(1) via an array or hash table instead of requiring O(log N) tree traversal and rebalancing. Within a price bucket, orders sit in a linked list ordered by arrival time, which preserves price-time priority automatically: adding an order is an O(1) tail insert, cancelling is an O(1) removal (the order holds a pointer to its own list node), and matching just pops from the head of the best-price bucket. A tree's O(log N) operations carry constant-factor overhead from pointer rebalancing and comparisons that, while individually small, accumulate to matter at a microsecond budget, and a tree still needs separate bookkeeping for time priority within equal prices.

## Q zh
在撮合引擎的订单簿（order book）中，为什么在每单订单延迟预算是微秒级的前提下，用按价格索引的价位桶（数组或哈希表）+ 每个价位一条双向链表，会比用一棵按价格排序的平衡树（如红黑树）更合适？

## A zh
价格是离散的（受最小报价单位 tick size 限制），所以可以用数组或哈希表直接 O(1) 索引，而不需要 O(log N) 的树遍历和重平衡。价位桶内部，订单按到达时间排成一条链表，天然维持价格-时间优先级：新增订单是 O(1) 的链表尾部插入，撤单是 O(1) 的移除（订单本身持有指向自己链表节点的指针），撮合只需要从最优价位桶的表头弹出。树的 O(log N) 操作带有指针重平衡和比较带来的常数开销，单次看似很小，但在微秒级预算下会累积成不可忽视的延迟，而且树还需要额外维护同一价位内的时间优先级。
