---
id: uth-go-rust-go-channel-1-hchan
node: go-rust.go-channel
type: qa
step: 1
---
## Q
**channel 底下是什么**｜Go · 1.27 运行时

`make(chan int, 3)` 之后，数据和等待者各存在哪里？

## A
**背景。** 两个 goroutine（Go 的轻量线程）要传数据，又不想自己加锁。channel 就是一个自带锁的队列：发送者放进去，接收者取出来；队列满了发送者睡眠等待，空了接收者睡眠等待。例：`make(chan int, 3)` 能存 3 个，第 4 次发送就得等。

**结构。** 一个 `hchan` 结构：一把锁、一个环形缓冲区（数组首尾相接，用两个下标分别记读、写位置），外加接收和发送两条等待队列。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">make(chan int, 3): 环形缓冲, 容量 3</text>
<rect x="30" y="28" width="44" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="52" y="46.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<text x="52" y="72" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="80" y="28" width="44" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="102" y="46.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<text x="102" y="72" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="130" y="28" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="152" y="72" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="8" y="46" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">buf</text>
<text x="52" y="88" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑ recvx</text>
<text x="152" y="88" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑ sendx</text>
<text x="190" y="46" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下标到头就绕回 0</text>
<text x="8" y="114" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">一把锁保护所有字段; qcount = 2, dataqsiz = 3</text>
<rect x="10" y="128" width="150" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="85" y="146.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">recvq: 等数据的接收者</text>
<rect x="176" y="128" width="150" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="251" y="146.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sendq: 等空位的发送者</text>
<text x="10" y="176" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缓冲有数据: 接收者直接取走; 没数据: 挂进 recvq 睡眠</text>
<text x="10" y="192" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缓冲满了: 发送者挂进 sendq 睡眠</text>
</svg>
```

**细节。**

- 环形缓冲：`buf`、`qcount`（已有个数）、`dataqsiz`（容量）、`sendx` / `recvx`（写、读下标）
- `recvq` / `sendq` 是阻塞中的 goroutine 链表
- 发送顺序：先看有没有等待的接收者，有就直接交给它；其次缓冲有空位就入队；都不行就挂到 `sendq` 睡眠

**为什么。** 所有字段由同一把互斥锁保护，实现简单；缓冲区加两个下标，入队出队都是 O(1)。

**例题：** LC 622 设计循环队列（同类：LC 641 设计循环双端队列）

用固定长度的数组实现循环队列（环形缓冲）：`enQueue`、`deQueue`、`Front`、`Rear`、`isEmpty`、`isFull`，队尾越过数组末尾就绕回开头。例：容量 3，入队 1、2、3 后再入队返回 `false`，出队一个再入队 4 成功。

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
