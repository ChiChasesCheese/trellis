---
id: amz-configurable-cache-lfu-frequency-buckets
node: amazon.amz-configurable-cache
type: qa
step: 4
tags: [grown]
---
## Q
在可配置缓存里，LFU（最不经常使用，Least Frequently Used）策略怎样让「选受害者」和「访问一次」都是 O(1)？

## A
按访问次数分桶：`freq -> OrderedDict(key)`，再记一个指向最小非空桶的 `min`。victim 就是 `min` 桶里最旧的 key（同频时退化成 LRU）；访问一次是把 key 从 f 桶挪到 f+1 桶，若 f 桶空了且 f==min 则 `min=f+1`。例：容量 2，put a、put b、get a、put c，a 频率 2、b 频率 1，淘汰 b，留下 a 和 c。空桶要立刻删。
