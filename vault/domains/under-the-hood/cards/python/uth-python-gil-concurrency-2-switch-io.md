---
id: uth-python-gil-concurrency-2-switch-io
node: python.gil-concurrency
type: qa
step: 2
---
## Q
**GIL 什么时候换人、什么时候放手**｜Python · CPython 3.14

多线程做 CPU 计算不会变快，为什么多线程下载却能？线程之间多久切换一次？

## A
**背景。** 一把大锁同一时刻只有一个线程能拿。如果拿着不放，别的线程永远没机会；如果每条指令都换人，切换的开销会爆炸。

**结构。** 想要 GIL 的线程先等一段时间：默认 5 毫秒（`sys.getswitchinterval()` 返回 `0.005`）。超时了还没拿到，就给持有者挂一个「请放手」的标记。持有者只在固定的检查点看这个标记：函数入口、循环往回跳（`JUMP_BACKWARD`）、调用返回之后，并不是每条指令都看。另外，阻塞调用（读写 socket 和文件、`time.sleep`）进去之前，线程会主动放手，返回后再去抢。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="156" y="40" width="100" height="28" rx="3" stroke-dasharray="4,3"/>
<rect x="56" y="100" width="100" height="28" rx="3" stroke-dasharray="4,3"/>
<rect x="256" y="100" width="74" height="28" rx="3" stroke-dasharray="4,3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="56" y="40" width="100" height="28" rx="3"/>
<rect x="256" y="40" width="74" height="28" rx="3"/>
<rect x="156" y="100" width="100" height="28" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="156" y1="24" x2="156" y2="150"/>
</g>
<g fill="currentColor">
<text x="106" y="58">运行</text>
<text x="293" y="58">运行</text>
<text x="106" y="118">等 GIL</text>
<text x="206" y="118">运行</text>
<text x="293" y="118">等 GIL</text>
<text x="156" y="184" font-size="11">有实心块的线程才持有 GIL</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="30" y="54">线程 1</text>
<text x="30" y="114">线程 2</text>
<text x="206" y="58">等 I/O</text>
<text x="156" y="166" font-size="11">线程 1 等 5ms 或进入 I/O</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="156" y="16" font-size="11">放手</text>
</g>
</g>
</svg>
```

**细节。**

- CPU 密集：几个线程轮流用 GIL，总时间不会缩短，还多了切换的开销。
- I/O 密集：一个线程在等网络时不占 GIL，别的线程照常运行，所以多线程下载仍然有效。
- 做压缩、哈希的 C 扩展，也常在计算期间放手。

**为什么。** 先等 5 毫秒再要求放手，避免无谓的频繁切换；在 I/O 前主动放手，等待的时间就能让给别人。

**对应 LeetCode：** 无直接对应的题
