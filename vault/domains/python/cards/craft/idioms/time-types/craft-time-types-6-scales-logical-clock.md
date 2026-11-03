---
id: craft-time-types-6-scales-logical-clock
node: craft.idioms.time-types
type: qa
step: 6
---
## Q
**时间类型 · 从 LeetCode 的整数时间戳到分布式里没有统一的钟**｜写法

LeetCode 的 Logger Rate Limiter 把时间戳直接传进来；LLD 的限流器注入单调时钟；到了多机器的分布式系统，「现在几点」还能当作一个统一的答案吗？

## A
**要点。** 不能。单机里一个时钟就够用（LeetCode 里时间是输入，LLD 里时钟是依赖）；多台机器各有各的墙钟，彼此有偏差，且偏差还会变，用它判断「A 事件先于 B 事件」不可靠。分布式系统用**逻辑时钟**（logical clock）排序因果：每个节点维护一个计数器，本地事件加一，发消息时带上计数，收消息时取两者较大值再加一。这样「发送」一定小于「接收」。

```python
# Lamport 逻辑时钟：分布式里没有统一的墙钟，用「先于」关系排序事件
class Node:
    def __init__(self, name: str) -> None:
        self.name, self.c = name, 0

    def tick(self) -> int:                 # 本地事件
        self.c += 1
        return self.c

    def send(self) -> int:                 # 发消息：带上自己的时钟
        return self.tick()

    def recv(self, remote: int) -> int:    # 收消息：取两边较大者再加一
        self.c = max(self.c, remote) + 1
        return self.c

a, b = Node("A"), Node("B")
for _ in range(5):
    a.tick()                               # A 的时钟走得快
m = a.send()                               # A 在 6 发出消息
print("A 发送时的逻辑时间:", m)
print("B 收到前:", b.c, "| 收到后:", b.recv(m), "(一定大于发送时间)")
print("B 之后的本地事件:", b.tick(), "> 发送事件", m)
```

实际输出：

```
A 发送时的逻辑时间: 6
B 收到前: 0 | 收到后: 7 (一定大于发送时间)
B 之后的本地事件: 8 > 发送事件 6
```

**变化。** 墙钟不再用来排序，只用来展示和粗略的过期判断；排序用逻辑时钟或混合逻辑时钟（Hybrid Logical Clock，HLC，墙钟加逻辑计数，既大致接近真实时间又保持因果顺序）。租约这类依赖时长的东西，仍然要靠本地的单调时钟计时，并且为时钟漂移留出余量。

**代价。** Lamport 时钟只保证「因果在前则数值更小」，反过来不成立：数值更小不代表因果在前，无法检测并发。需要判断并发要用向量时钟（vector clock），代价是向量随节点数增长。

**信号。** 需求里有「先发生」「顺序」「过期」，并且发生在多台机器上。
