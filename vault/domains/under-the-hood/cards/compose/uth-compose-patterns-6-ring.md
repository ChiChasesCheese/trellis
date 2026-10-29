---
id: uth-compose-patterns-6-ring
node: compose.patterns
type: qa
step: 6
---
## Q
**环形数组 + 序号：定长内存里的队列**｜Linux kfifo · 6.12 / LMAX Disruptor · 4.0

想要一个定长的队列：入队出队都是 O(1)，不搬数据、不分配内存。数组头部出队要整体平移，链表又每个元素单独分配，怎么办？

## A
**背景。** 数组尾部添加是 O(1)，头部删除要把后面的元素全部前移，O(n)。链表没这个问题，但每个节点单独分配内存，对 CPU 缓存不友好。

**结构。** 数组首尾相接成环，再用两个只增不减的序号：`in` 是写入过的总数，`out` 是读走的总数。元素的位置是序号对容量取余。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<text x="14" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">容量 8  out=11  in=14</text>
<rect x="26" y="66" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="62" y="66" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="98" y="66" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="134" y="66" width="34" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="151.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="170" y="66" width="34" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="187.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="206" y="66" width="34" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="223.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="242" y="66" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="259.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="278" y="66" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="295.0" y="84.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<line x1="151.0" y1="40" x2="151.0" y2="64" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="151.0,64.0 148.5,59.0 153.5,59.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="151.0" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">out 11</text>
<line x1="259.0" y1="40" x2="259.0" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="259.0,64.0 256.5,59.0 261.5,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="259.0" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">in 14</text>
<polyline points="295.0,96 295.0,118 43.0,118 43.0,98" fill="none" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="43.0,98.0 45.5,103.0 40.5,103.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">首尾相接 下标 = 序号 &amp; 7</text>
<text x="170" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">个数 = in - out = 3</text>
<text x="170" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">满: in - out == 容量   空: in == out</text>
<text x="170" y="198" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">序号只增不减 不浪费一格</text>
</svg>
```

| 操作 | 做法 | 复杂度 |
|---|---|---|
| 入队 / 出队 | 写或读对应位置，序号加一 | O(1) |
| 个数 | `in - out` | O(1) |

**细节。**

- Linux `kfifo`：容量取 2 的幂，位置是 `序号 & mask`；序号是无符号整数，溢出回绕后相减仍对；单读单写不用锁
- LMAX Disruptor：`sequence & indexMask`，生产者不能领先最慢的消费者超过一整圈
- Java `ArrayBlockingQueue`（OpenJDK 25）、Go 1.24 带缓冲的 channel 存“下标 + 个数”，是同一骨架的另一种写法

**为什么。** 序号只增不减，空和满靠 `in - out` 区分，不用留空位。

**坑。** 只存两个下标、不存个数或序号，队空和队满看起来一模一样。

**例题：** LC 622 设计循环队列

设计循环队列 `MyCircularQueue(k)`：容量为 `k`，`enQueue` 入队成功返回 `True`、队满返回 `False`；`deQueue` 出队；`Front()` 取队首、`Rear()` 取队尾，空则返回 `-1`；`isEmpty()`、`isFull()`。不要使用内置队列库。

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
