---
id: uth-python-asyncio-3-blocking
node: python.asyncio
type: qa
step: 3
---
## Q
**协程里 time.sleep 会怎样**｜Python · CPython 3.14

一个协程里调用了 `time.sleep(0.5)`，同时另一个协程只 `await asyncio.sleep(0.1)`，后者什么时候醒来？

## A
**背景。** 事件循环只有一个线程，一轮里先后执行各个回调。回调里调用 `time.sleep` 会让整个线程停住，不是只让这一个协程停住，别的回调一个也轮不到。

**结构。** 回调不返回，就进不了下一轮；到期的定时器要等下一轮才被取出。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<line x1="30" y1="150" x2="320" y2="150" stroke-width="1.2" stroke="currentColor"/>
<polygon points="320.0,150.0 314.0,153.0 314.0,147.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="40" y="70" width="116" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="98" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">time.sleep(0.5)</text>
<line x1="40" y1="144" x2="40" y2="156" stroke-width="1.2" stroke="currentColor"/>
<text x="40" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<line x1="63.2" y1="44" x2="63.2" y2="150" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="63.2" y="36" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">本应醒来 0.1 s</text>
<line x1="156" y1="98" x2="156" y2="144" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="156" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.5 s</text>
<line x1="160.64" y1="112" x2="160.64" y2="148" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="160.6,148.0 157.6,142.0 163.6,142.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="168.64" y="125" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">实际 0.52 s 才醒</text>
</svg>
```

**细节。**

- 实测后者 0.52 秒才醒，不是 0.1 秒。
- 回调里 `call_soon` 的新回调也要等下一轮：实测顺序 `a, b, c`。
- 调试模式下，超过 `slow_callback_duration`（默认 0.1 秒）的回调会打警告。

**为什么。** 协作式调度（回调自己主动交出控制权，没人强行打断）切换开销极小；代价是任何阻塞调用都拖住全部任务。

**坑。** 阻塞或 CPU 密集的工作用 `asyncio.to_thread` 或进程池。

**对应 LeetCode：** 无直接对应的题
