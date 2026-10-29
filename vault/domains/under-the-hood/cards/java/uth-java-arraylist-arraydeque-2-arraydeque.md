---
id: uth-java-arraylist-arraydeque-2-arraydeque
node: java.arraylist-arraydeque
type: qa
step: 2
---
## Q
**ArrayDeque 怎么两端 O(1)**｜Java · OpenJDK 25

`ArrayDeque` 用什么结构做双端队列？数组长度是 2 的幂吗？

## A
**背景。** 队列要从两头进出。`ArrayList` 在头部增删要把后面全部挪一格；链表两头快，但每个元素一个节点，开销大。想要数组的紧凑，又要两头快：让数组首尾相接，头尾各记一个位置。

**结构。** 环形数组（circular array）：`head` 指向队首元素，`tail` 指向下一个空位，下标走到头就绕回 0。例：长 8 的数组，`head = 6`、`tail = 2`，队里的元素在格 6、7、0、1。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">长 8 的环形数组 走到末尾绕回 0</text>
<rect x="26" y="70" width="36" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="44" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<text x="44" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="62" y="70" width="36" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="80" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<text x="80" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="98" y="70" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="116" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="134" y="70" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="152" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="170" y="70" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="188" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="206" y="70" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="224" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="242" y="70" width="36" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<text x="260" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="278" y="70" width="36" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="296" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<text x="296" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<path d="M 296 66 C 296 36 44 36 44 66" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44.0,66.0 41.0,60.0 47.0,60.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">绕回</text>
<line x1="260" y1="158" x2="260" y2="124" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260.0,124.0 263.0,130.0 257.0,130.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="260" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">head</text>
<line x1="116" y1="158" x2="116" y2="124" stroke-width="1.2" stroke="currentColor"/>
<polygon points="116.0,124.0 119.0,130.0 113.0,130.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="116" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">tail</text>
</svg>
```

**细节。**

- `addFirst` 把 `head` 减 1（小于 0 绕到末尾）再写入；`addLast` 写入 `tail` 再加 1；两者相遇就满了，立刻 `grow`（扩容）。
- 长度不是 2 的幂：JDK 8 及以前是，用位与取模；JDK 9 起改用比较判断绕回。
- 初始长 17；长度小于 64 时扩为 `2n+2`，否则加 50%：`17 36 74 111 166 249`。

**为什么。** 环形数组两端都不需要搬动元素，也没有每个节点的对象头和指针。

**例题：** LC 622 设计循环队列

用固定大小的数组实现循环队列 `MyCircularQueue(k)`：`enQueue`、`deQueue`、`Front`、`Rear`、`isEmpty`、`isFull`，队尾越过数组末尾后绕回队首。

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
