---
nodes: [problems.components.ttl-cache]
url: https://github.com/anomaly2104/cache-low-level-system-design
tags: [no-archive]
---
# anomaly2104/cache-low-level-system-design — Cache low level design

值得读：`prasadgujar/low-level-design-primer` 为"设计缓存"这道题指向的参考实现，Java。
它把 `Storage`（存储）和 `EvictionPolicy`（淘汰规则）拆成两个包，这条接缝和本题解一致，
可以看它怎么组织类与异常（`StorageFullException` / `NotFoundException`）。
分歧很大：它**完全没有存活时间（TTL）**，因而没有注入时钟、没有到期索引，
也就碰不到本题真正的难点——"一条再也没人读的数据谁去收尸"；
它用 `CacheFactory` 组装对象，在 Python 里这是一个函数的事；
`Storage` 接口上的 `getSize()` 这类 getter，Python 里应当是 `@property` 或 `__len__`。
仓库无 LICENSE 文件，故只链接不摘录。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/anomaly2104/cache-low-level-system-design)
%% trellis:end %%
