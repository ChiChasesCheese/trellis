---
nodes: [amazon.amz-configurable-cache]
url: https://docs.python.org/3/library/collections.html#collections.OrderedDict
---
# collections — OrderedDict objects（Python 标准库文档）

值得读：官方文档，讲 `OrderedDict` 的 `move_to_end`、`popitem(last=False)` 都是 O(1)，并给出用它实现 LRU 缓存的范例。LRU 策略与 LFU 的每个频率桶都可以建立在它之上；范例把值和顺序存在同一个结构里，而可配置缓存要把「顺序」（策略）和「值」（后端）拆开，因为后端可能是文件。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/collections.html#collections.OrderedDict)

## Archived copy
![[src-pydocs-music-streaming-clip]]
%% trellis:end %%
