---
nodes: [problems.components.thread-pool]
url: https://docs.python.org/3/library/queue.html
---
# queue — A synchronized queue class

值得读：`PriorityQueue` 的官方文档——它只保证"每次取出最小的那个"，排序依据完全由塞
进去的对象自己的比较逻辑决定，文档本身没有提醒"包着非纯数据的对象时必须让不可比较的
字段退出比较"，这正是本题解决策三里 `field(compare=False)` 那个陷阱的来源，读这份文档
时要自己补上这一课。
