---
id: uth-kafka-timing-wheel-1-hierarchical-wheel
node: kafka.timing-wheel
type: qa
step: 1
---
## Q
**分层时间轮：让超时便宜**｜Kafka · 4.0

broker 里同时挂着成千上万个带超时的请求（等副本确认的生产请求、等够数据的 fetch 请求）。怎么让“登记一个超时”和“取消一个超时”都很便宜？

## A
**背景。** 每个请求都要设一个“到点还没完成就算超时”的闹钟，其中绝大多数在到点前就完成并取消了。最直接的办法，是把所有闹钟放进一个按到期时间排序的堆（优先队列），但登记和取消每次都要 O(log n)，n 是闹钟个数。

**结构。** 时间轮（timing wheel）像一个钟面：一圈若干格，每格代表一小段时间，同一段时间到期的任务串在这一格的链表里。登记 = 算出格子编号、挂上链表，O(1)；取消 = 从链表摘掉，O(1)。默认每格 1 ms、共 20 格；一圈放不下的任务交给上一层，上一层每格的跨度正好是下一层的整圈（20 ms、400 ms、8 s……），像里程表进位。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 144">
<text x="60" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第 2 层: 每格 20 ms</text>
<rect x="60" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="73" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="86" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="99" y="22" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="112" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="125" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="138" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="151" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="164" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="177" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="190" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="203" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="216" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="229" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="242" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="255" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="268" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="281" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="294" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="307" y="22" width="13" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="99" y1="44" x2="60" y2="94" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="112" y1="44" x2="320" y2="94" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="138" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">格到期后任务落进下层</text>
<rect x="60" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="73" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="86" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="99" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="112" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="125" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="138" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="151" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="164" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="177" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="190" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="203" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="216" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="229" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="242" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="255" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="268" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="281" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="294" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="307" y="96" width="13" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="60" y="136" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第 1 层: 每格 1 ms, 共 20 格</text>
</svg>
```

**细节。**

- 格子 = `(expiration / tickMs) % wheelSize`，最多经过 m 层。
- 高层的格到期时，任务重新插入更细的层。

**为什么。** 堆的登记和取消都是 O(log n)；超时请求大多到期前就完成并取消，时间轮让这条最常见的路径最便宜。

**例题：** LC 622 设计循环队列

用固定长度的数组实现先进先出的循环队列，队尾接回队首，出队腾出的位置可以重复使用。`MyCircularQueue(k)` 容量为 `k`；`enQueue` 队满返回 `False`，`deQueue` 队空返回 `False`，`Front` / `Rear` 队空返回 `-1`。例：容量 `3`，入队 `1, 2, 3` 成功，再入队 `4` 返回 `False`，`Rear()` 得 `3`；出队一次后再入队 `4` 成功。

```python
class MyCircularQueue:
    def __init__(self, k: int) -> None:
        self.buf = [0] * k
        self.cap = k
        self.head = 0                           # 队首下标
        self.size = 0                           # 元素个数：用 size 区分空和满，不浪费一格

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.buf[(self.head + self.size) % self.cap] = value
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.buf[self.head]

    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.buf[(self.head + self.size - 1) % self.cap]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.cap
```
