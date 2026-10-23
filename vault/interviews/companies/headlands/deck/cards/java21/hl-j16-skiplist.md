---
id: hl-j16-skiplist
node: java21.j16-concurrency-primitives
type: qa
step: 22
---
## Q
跳表（skip list）是什么？为什么并发的有序 Map 选跳表而不是平衡树？

## A
在有序链表之上叠几层「快车道」链表，每层是下一层的随机抽样，查找从最高层出发跳过大段，期望 **O(log n)**。

比平衡树的好处：**插入/删除只改局部指针，容易做成无锁（CAS）**，并发版本不需要全局锁；平衡树的旋转要改多处，并发难做。

`ConcurrentSkipListMap`（Java 6）就是基于跳表的线程安全 `NavigableMap`，订单簿的天然选择：key = 价格，按价格有序取最优档，多线程挂单。
