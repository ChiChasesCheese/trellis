---
nodes: [problems.components.notification-service]
url: https://docs.python.org/3/library/heapq.html
---
# heapq — Heap queue algorithm（标准库文档）

值得读：延迟重试堆的权威出处，重点是文末 "Priority Queue Implementation Notes" 那一节，它把本题
第 3 关的两个坑直接写成了条目：（1）堆里存元组时，第一个元素相等就会去比较第二个，所以必须有
一个**递增序号**做平局裁决，否则会掉进比较业务对象的 `TypeError`；（2）"如何删除/修改一个已经
入堆的任务"——标准答案是标记为失效而不是从堆里找出来删。本题解的重试堆键是
`(到期时间, 递增序号, 信封)`，就是这一节的直接应用。顺带一提，这一节也解释了为什么本题的优先级
车道**不**用堆：堆天然是严格优先级，低优先级会饿死，而分道加配额才能给出可配置的公平性。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/heapq.html)

## Archived copy
![[src-pythondocs-ttl-cache-clip]]
%% trellis:end %%
