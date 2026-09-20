---
nodes: [problems.marketplaces.stock-brokerage]
url: https://docs.python.org/3/library/bisect.html
---
# Python 文档：bisect —— Array bisection algorithm

值得读：订单簿的活跃价位需要"一直有序、能取端点、能按值删"，标准库里没有 `SortedDict`，
`bisect` 加一条普通 `list` 就是那个替代品。文档里有两句话直接决定了本题解的复杂度论证：
其一，查找是 O(log n) 但 `insort` 的**插入**是 O(n)，因为要搬内存——所以"开一个新价位"付的是
O(价位数)，而不是 O(log 订单数)；其二，文档明确建议把 `bisect` 用在"搜索多、插入少"的场景，
订单簿恰好如此（价位数几十到几百，订单数几万）。配套要读的是
[`stdtypes` 里关于 `dict` 的那一句](https://docs.python.org/3/library/stdtypes.html#dict)：
"Dictionaries preserve insertion order" 是**语言保证**，本题解每个价位内的 FIFO 就建立在
这句话上，而 `dict` 的按键删除是 O(1)，这正是它比 `deque` 更适合当撤单频繁的队列的理由；
以及 [`heapq` 的 Priority Queue Implementation Notes](https://docs.python.org/3/library/heapq.html)，
它自己讨论了堆无法删除任意元素、只能标记为已删除，以及由此堆积的垃圾——那是订单簿否决堆的依据。
