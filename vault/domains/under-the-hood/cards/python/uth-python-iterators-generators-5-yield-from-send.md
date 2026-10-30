---
id: uth-python-iterators-generators-5-yield-from-send
node: python.iterators-generators
type: qa
step: 5
---
## Q
**yield from、send 与 await：同一套挂起机制**｜Python · CPython 3.14

`yield from` 比手写 `for x in sub: yield x` 多做了什么？`async def` 里的 `await` 跟生成器是什么关系？

## A
**背景。** 有了生成器，自然想把一个生成器的输出接到另一个后面，比如递归遍历树、拼接流水线。手写 `for x in sub: yield x` 能用，但不能把调用方 `send` 进来的值转交给子生成器，也拿不到子生成器的返回值。

**结构。** `yield from sub` 把 `sub` 吐出的值原样转交给外层调用方，把 `send()` 送进来的值和异常转交给 `sub`；`sub` 里的 `return v` 成为这个表达式的值（它藏在 `StopIteration.value` 里）。

```python
def outer():
    r = yield from inner()   # inner 里 return "r"，所以 r == "r"
    yield 3
```

**细节。**

- 实测 `await x` 和 `yield from s` 都编译成 `SEND` 加 `YIELD_VALUE` 的循环；协程对象（`async def` 调用的结果）和生成器共用「冻结的栈帧」这套机制。
- asyncio 的 `Task` 每走一步就是调一次 `coro.send(None)`：协程跑到 `await` 一个没完成的 `Future`，就把它一路交还给事件循环；`Future` 完成后，事件循环再 `send` 一次，协程从原处继续。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="80" y="10" width="180" height="30" rx="3"/>
<rect x="80" y="78" width="180" height="30" rx="3"/>
<line x1="200" y1="78" x2="200" y2="40"/>
<line x1="200" y1="146" x2="200" y2="108"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="80" y="146" width="180" height="40" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="140" y1="40" x2="140" y2="78"/>
<line x1="140" y1="108" x2="140" y2="146"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="200.0,40.0 203.0,46.0 197.0,46.0"/>
<polygon points="200.0,108.0 203.0,114.0 197.0,114.0"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="140.0,78.0 137.0,72.0 143.0,72.0"/>
<polygon points="140.0,146.0 137.0,140.0 143.0,140.0"/>
</g>
<g fill="currentColor">
<text x="170" y="29">事件循环 (event loop)</text>
<text x="170" y="97">Task.__step</text>
<text x="170" y="164">协程: 冻结的栈帧</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="170" y="180" font-size="11">停在 await fut 处</text>
<text x="208" y="62" text-anchor="start" font-size="11">再排队</text>
<text x="208" y="130" text-anchor="start" font-size="11">await 的 fut</text>
<text x="170" y="208" font-size="11">fut 完成后, 循环再 send 一次</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="132" y="62" text-anchor="end" font-size="11">run</text>
<text x="132" y="130" text-anchor="end" font-size="11">send(None)</text>
</g>
</g>
</svg>
```

**为什么。** 协程挂起时，栈帧和局部变量都还在，所以事件循环不需要为每个等待的任务开一个线程。

**对应 LeetCode：** 无直接对应的题
