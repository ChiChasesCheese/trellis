---
id: uth-storage-buffer-pool-3-ring-buffer
node: storage.buffer-pool
type: qa
step: 3
---
## Q
**大表扫描只用一个小环形缓冲**｜PostgreSQL · 17 / 18

PostgreSQL 顺序扫描一张比缓冲池还大的表，会不会把池里的热数据冲掉？

## A
**背景。** 和 InnoDB 一样，大表的顺序扫描读进来的页大多只用一次，不该挤掉热页。

**结构。** 不会。大表的顺序扫描改用一个小的环形缓冲（ring buffer）：只在这几个缓冲区里循环复用，淘汰也在环内完成，不碰共享缓冲区里的热页。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<rect x="8" y="12" width="110" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="28.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大表顺序扫描</text>
<line x1="118" y1="26" x2="184.633" y2="59.3167" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190,62 183.3,62.0 186.0,56.6" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<rect x="8" y="74" width="150" height="48" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="83" y="95" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">shared_buffers</text>
<text x="83" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">热页不被挤走</text>
<rect x="192" y="52" width="30" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="228" y="52" width="30" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="264" y="52" width="30" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="300" y="52" width="30" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<path d="M321 50 Q256 14 207 48" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="205,52 206,42 214,47" stroke="currentColor" stroke-width="1.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="262" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">256 KB 环形缓冲</text>
<text x="262" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只在环内复用</text>
</svg>
```

**细节。**

- 触发条件：表大于 `shared_buffers` 的 1/4（`NBuffers / 4`）。
- 环大小：顺序扫描 256 KB（17 及之前；18 起再加上异步 I/O 并发所需的空间），`VACUUM`（清理死数据的维护任务）2 MB，批量写入（如 `COPY`）16 MB。

**为什么。** 比 InnoDB 的中点 LRU 更直接：扫描页干脆不进全局的淘汰池。

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
