---
id: hl-hc05-linkedhashmap-fifo
node: problems.hc05-market-order-book
type: qa
step: 6
---
## Q
同价位的订单队列为什么用 `LinkedHashMap<Long, Node>` 而不是 `ArrayDeque`？再配 `byId` 怎么得到 O(log L) 撤单？

## A
撤单者可能在队伍中间。`ArrayDeque` 入队尾、出队头都是 O(1)，但 `remove(obj)` 要从头线性找，O(队伍长度)（排 10 万张单就扫 10 万次）。

`LinkedHashMap` 是「哈希表 + 双向链表」合体：按 key 找 O(1)；链表按插入顺序串起来，摘节点只改前后邻居指针 O(1)；遍历按插入顺序，队头 = 最先插入的。所以它**既是 Map 又是队列**：`remove(id)`、`firstEntry()`、`pollFirstEntry()`、`putLast(k, v)` 都 O(1)。口述：「我需要先来后到，和按 id O(1) 撤单。ArrayDeque 只有前者，LinkedHashMap 两个都有。」代价是每项多一个 entry 对象。

`putLast` 对已存在的 key 会把它移到链表末尾（「重新排队」）；Java 21 之前要 `remove` 再 `put`。

**`byId`**：`HashMap<Long, Node>`，撤单和改量只带 `id`，没有它得遍历所有价位所有队列 O(n)。节点记着价格和方向。

`cancel(id)` = `byId.get` O(1) + `book.get(price)` O(log L) + `fifo.remove` O(1) + 价位空了从 `TreeMap` 删 O(log L) → **O(log L)**。真 O(1) 要把价位换成数组下标（Part 4）。

C++：`std::map<Price, std::list<Order>>` + `unordered_map<Id, Locator>`，`Locator` 存价位和订单节点的迭代器；`list::erase(iterator)` O(1)；节点式容器的迭代器不会因别的元素增删而失效。
