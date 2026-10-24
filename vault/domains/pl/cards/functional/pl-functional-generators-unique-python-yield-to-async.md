---
id: pl-functional-generators-unique-python-yield-to-async
node: functional.generators
type: qa
step: 8
---
## Q
Python 的 `async`/`await` 为什么说是从生成器长出来的？这个演化过程揭示了 Python 怎样的设计风格？

## A
Python 2.5（2006）的 PEP 342 给生成器加上了 `send()`，使生成器可以**接收**值，不只是产出。这让它能充当「协作式任务」：一个调度器反复驱动一批生成器，每个生成器在需要等待（I/O）的地方 `yield` 把控制权交还，调度器稍后再唤醒它。

3.3（2012）的 PEP 380 加入 `yield from`，让生成器可以把子生成器的产出和接收转交过去，这就是**可组合**的协程。asyncio 早期（3.4）正是用 `@asyncio.coroutine` 加 `yield from` 写的。

3.5（2015）的 PEP 492 才把这种用法正式命名成 `async def` 和 `await`，并让它与生成器在类型上区分开。内部机制仍然是同一个：协程对象是一个可暂停的帧，`await` 对应 `yield from`。

这个演化说明 Python 的设计风格：

- **先用一个通用的底层机制**（可暂停的帧），让社区在上面试验出各种用法；
- **用法稳定后再引入专门语法**，并保持底层机制可见；
- 每一步都是向后兼容的增量，而不是推翻重来。

对比 Rust：`async` 是一个有意设计的、编译器生成状态机的特性；Go：协程直接内置在运行时里，没有"演化"这个过程。Python 的路径慢但有机，代价是留下了多套重叠的接口（生成器、`async`、旧式 `@coroutine`）。
