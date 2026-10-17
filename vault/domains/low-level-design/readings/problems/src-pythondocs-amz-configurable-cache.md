---
nodes: [amazon.amz-configurable-cache]
url: https://docs.python.org/3/library/collections.html#collections.OrderedDict
---
# collections — OrderedDict objects（Python 标准库文档）

值得读：官方文档，讲 `OrderedDict` 的 `move_to_end`、`popitem(last=False)` 都是 O(1)，并在页面里直接给出了一个用它实现 LRU 缓存的范例。本题解的 `LruPolicy` 与 `LfuPolicy` 的每个频率桶都建立在它之上；与范例的不同是：范例把值和顺序存在同一个结构里，本题解把「顺序」（策略）和「值」（后端）拆开，因为后端可能是文件。
