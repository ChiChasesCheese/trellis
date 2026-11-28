---
id: bagu-lock-watchdog-3-gc-pause
node: a.distributed.lock-watchdog
type: qa
step: 3
---
## Q
**看门狗的盲区 · 长 GC 停顿会怎样**｜必会

面试官：「有了看门狗，是不是就不会出现两个持有者了？持有者发生长时间 GC 停顿会怎样？」

## A
**基本回答。** 不能保证。持有者发生长时间 GC 停顿（stop-the-world，回收器暂停所有线程）或整个进程被挂起时，续期线程也一起停了，锁过期，别人拿到锁；原持有者醒来仍以为自己持有，继续写数据，两个持有者就同时写了。任何基于租约（lease，带期限的授权）的锁都有这个问题。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 290">
<rect x="10" y="6" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持有者 A</text>
<line x1="50" y1="32" x2="50" y2="232" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<rect x="130" y="6" width="80" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 锁</text>
<line x1="170" y1="32" x2="170" y2="232" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<rect x="250" y="6" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 B</text>
<line x1="290" y1="32" x2="290" y2="232" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="54" y="54" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">加锁成功</text>
<line x1="50" y1="60" x2="163" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,60 163,63.2 163,56.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="38" y="80" width="24" height="80" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="68" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">GC 停顿 40 秒</text>
<text x="68" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">续期线程也停</text>
<text x="176" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">t=30 锁过期</text>
<text x="176" y="150" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">B 加锁成功，开始写</text>
<line x1="290" y1="156" x2="177" y2="156" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,156 177,152.8 177,159.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="54" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">A 醒来</text>
<text x="54" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">以为还持锁</text>
<rect x="6" y="240" width="328" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="256.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A、B 先后写入同一份数据</text>
<text x="170" y="271.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">两个持有者</text>
<line x1="290" y1="158" x2="290" y2="233" stroke-width="1.2" stroke="currentColor"/>
<polygon points="290,240 286.8,233 293.2,233" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="50" y1="214" x2="50" y2="233" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="50,240 46.8,233 53.2,233" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
</svg>
A 加锁后被长 GC 整个冻住（粗框），续期线程也一起冻了；锁在 30 秒到期，B 拿到并开始写；A 醒来仍以为自己持锁，也去写，同一份数据就被两个持有者先后写入。
**容易错。**
- **以为有了看门狗就不会有两个持有者：** 进程冻住时续期线程也冻住，锁照样过期。
- **以为「写之前检查一下锁还在」就安全：** 检查和写入之间还有空隙，停顿可以发生在这个空隙。
- **以为只有 GC 才会这样：** 网络分区、虚拟机暂停、时钟跳变同样会让锁失效。
- **以为换成别的租约锁就没事：** 只要靠时间约定，就有这个问题，要靠下游拒绝过期写入。
**业务场景。** 扣款进程一次 Full GC 停了 40 秒，30 秒的锁已过期，另一个请求拿锁完成了扣款；原进程醒来再执行一次，同一笔账被扣了两次。
