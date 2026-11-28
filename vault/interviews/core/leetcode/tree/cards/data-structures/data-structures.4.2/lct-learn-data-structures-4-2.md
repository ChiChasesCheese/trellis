---
id: lct-learn-data-structures-4-2
node: data-structures.4.2
type: qa
step: 1
---
## Q
**常用数据结构 › 队列 › 设计**｜学习卡

套路是什么？

## A
**一句话。** 设计队列就是选底层结构并守住不变量：循环队列用定长数组 + 队首下标 `head` + 元素个数 `size`，下标一律对容量取模；用栈实现队列用两个栈，输出栈空了才整体倒入。

下图：容量 6、`head = 4`、`size = 3` 的循环队列；队尾写入位置由 `head + size` 取模得到。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="50" y="50" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="70.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="90" y="50" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="130" y="50" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="50" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="210" y="50" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="230.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="250" y="50" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="270.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<text x="70.0" y="96" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="110.0" y="96" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="150.0" y="96" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="190.0" y="96" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="230.0" y="96" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="270.0" y="96" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<line x1="230.0" y1="20" x2="230.0" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="230.0,48.0 227.0,41.7 233.0,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="230.0" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">head = 4</text>
<line x1="110.0" y1="20" x2="110.0" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="110.0,48.0 107.0,41.7 113.0,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="110.0" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">(head + size) % 6 = 1</text>
<path d="M 270 82 Q 170 135 70 82" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="70.0,82.0 76.3,85.1 71.6,88.8" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">size = 3：a b c，下标取模后绕回 0</text>
</svg>

```python
class MyCircularQueue:
    def __init__(self, k):
        self.a = [0] * k
        self.head = self.size = 0    # 队首下标、元素个数

    def enQueue(self, v):
        if self.size == len(self.a):
            return False
        self.a[(self.head + self.size) % len(self.a)] = v
        self.size += 1
        return True

    def deQueue(self):
        if self.size == 0:
            return False
        self.head = (self.head + 1) % len(self.a)
        self.size -= 1
        return True                  # 队首元素是 a[head]
```

**要点。**
- 为什么对？：队尾下标恒为 `(head + size) % k`，用 `size` 区分空和满，不需要浪费一格；所有操作 `O(1)`。
- LC 232 怎么改？：`inbox` 只压入，`outbox` 只弹出；`outbox` 为空时才把 `inbox` 全倒进去，每个元素最多搬一次，均摊 `O(1)`。

**易错点。**
- 只用 `head` 和 `tail` 判空满：两者相等时分不清空还是满，要么多留一格，要么另记 `size`。
- 232 在 `outbox` 非空时倒栈：会打乱顺序，新元素跑到旧元素前面。
- 忘了取模：`head + 1` 到末尾要回到 `0`。

**对应题目。** LC 622 设计循环队列、LC 232 用栈实现队列
