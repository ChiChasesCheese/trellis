---
nodes: [problems.components.ttl-cache]
url: https://docs.python.org/3/library/heapq.html
---
# heapq — Heap queue algorithm（Priority Queue Implementation Notes）

值得读：官方文档末尾那一节把"用堆做优先队列"的两个真实难题讲得比任何面试教程都清楚——
堆无法删除或修改中间元素，所以要把旧条目标成**墓碑**（tombstone）、弹出时跳过；
元组里要塞一个自增序号，让比较永远停在序号上，避免去比较那些只可哈希、不可比较的 key。
本题解的 `ExpiryIndex` 就是这份配方的直接应用。它没有管的那一半，正是本题的考点：
**墓碑什么时候该被压实掉**。文档默认队列规模有限，而一个被反复覆写的热 key 能留下几十万个
死条目，于是"缓存容量有界"这个对外承诺会被一个内部结构悄悄毁掉——所以本题解补上了
"墓碑超过堆长度一半就重建"这条摊还规则，并把 `heap_size` 暴露成可断言的只读属性。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/heapq.html)

## Archived copy
![[src-pythondocs-ttl-cache-clip]]
%% trellis:end %%
