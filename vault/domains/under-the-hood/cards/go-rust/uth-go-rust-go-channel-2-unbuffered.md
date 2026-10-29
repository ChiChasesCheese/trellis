---
id: uth-go-rust-go-channel-2-unbuffered
node: go-rust.go-channel
type: qa
step: 2
---
## Q
**无缓冲 channel 的数据停在哪**｜Go · 1.27 运行时

`make(chan int)` 没有缓冲区，发送的值经过谁的手到达接收者？

## A
**背景。** 容量为 0 的 channel 没有地方暂存数据，发送者必须等到接收者出现，两边“碰头”才能传值。

**结构。** 不经过任何缓冲：值在两个 goroutine 的栈（各自的一小块私有内存）之间直接拷贝一次（`sendDirect` / `recvDirect`），再唤醒睡着的一方。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">make(chan int): 没有缓冲, 两边必须碰头</text>
<rect x="10" y="30" width="90" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="55" y="49.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">G1: ch &lt;- 42</text>
<rect x="230" y="30" width="100" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="280" y="49.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">G2: x = &lt;-ch</text>
<line x1="100" y1="45" x2="228" y2="45" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="228,45 222.0,47.7 222.0,42.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="165" y="38" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">栈到栈直接拷贝</text>
<text x="8" y="90" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">接收者先到: 睡在 recvq, 发送者来了直接写进它的变量</text>
<text x="8" y="108" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">发送者先到: 睡在 sendq, 接收者来了直接从它那里取</text>
<text x="8" y="134" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">有缓冲且已满: 接收者取走队首,</text>
<text x="8" y="150" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再让睡着的发送者把值放进刚空的那一格</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">发送返回 = 对方已经收到</text>
</svg>
```

**细节。**

- 谁先到谁排进等待队列：接收者先到就睡在 `recvq` 等值，发送者先到就睡在 `sendq`
- 有缓冲且已满时，接收者取走队首，同时让阻塞的发送者把值放到刚空出的那一格

**为什么。** 不用分配缓冲，也让“发送返回”等于“对方已收到”。

**对应 LeetCode：** 无直接对应的题（并发同步）
