---
id: bagu-go-channel-map-1-channel-map
node: b.runtime.go-channel-map
type: qa
step: 1
---
## Q
**Go channel · 底层结构、关闭规则与 map 并发**｜追问

面试官：「Go 的 channel 是怎么实现的？对已经关闭的 channel 读写会怎样？map 是并发安全的吗？」

## A
**基本回答。** channel 底层是 `hchan`：环形缓冲区、一把互斥锁、发送和接收两条等待队列（挂着阻塞的 goroutine）。无缓冲要收发双方同时就绪才交接；有缓冲满了发送阻塞、空了接收阻塞。关闭后：nil channel 收发永远阻塞；向已关闭的发送 panic；从已关闭的接收先读完缓冲，再得零值和 `ok=false`；关闭两次 panic，所以只由发送方关闭。`select` 多个 case 同时就绪时随机选一个。map 不是并发安全的：并发写是 `fatal error: concurrent map writes`，不是 panic，`recover` 接不住，进程直接终止；解法是 `sync.RWMutex`、读多写少用 `sync.Map`、分片加锁。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 278">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hchan（容量 4 的 channel）</text>
<rect x="8" y="22" width="324" height="150" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="18" y="32" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">互斥锁 lock</text>
<rect x="130" y="32" width="110" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="185.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">closed 标志</text>
<rect x="18" y="72" width="44" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="40" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="62" y="72" width="44" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="84" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="106" y="72" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="150" y="72" width="44" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">环形缓冲区 buf（已用 2/4）</text>
<rect x="18" y="128" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sendq</text>
<text x="93.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等着发送的 goroutine</text>
<rect x="178" y="128" width="144" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250.0" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">recvq</text>
<text x="250.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等着接收的 goroutine</text>
<text x="10" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对已关闭的 channel：</text>
<text x="10" y="210" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">发送 → panic；再关闭 → panic</text>
<text x="10" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">接收 → 先读完缓冲，再得零值和 ok=false</text>
<text x="10" y="246" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">nil channel 收发 → 永远阻塞</text>
<text x="10" y="268" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只由发送方关闭</text>
</svg>
hchan 里有锁、关闭标志、环形缓冲区（图里已放了 a、b），以及等着发送和等着接收的两条队列；下方是关闭后的行为规则。
**业务场景。** 直播弹幕统计里多个 goroutine 同时 `m[roomID]++`，压测时进程直接崩溃，`defer recover` 也救不了，改成分片加锁后恢复。评论广播给观众连接：每连接一个有缓冲 channel，满了就丢弃或断开，避免慢消费者拖垮广播。
**容易错。**
- **让接收方关闭 channel：** 发送方不知道，继续发就 panic。
- **一概用 channel 同步：** 传递数据所有权、搭流水线用 channel；只保护共享状态用锁，更简单更快。`sync.Mutex` 正常模式新来者可与被唤醒者抢锁，等待超 1ms 转饥饿模式，锁直接交给队首。
