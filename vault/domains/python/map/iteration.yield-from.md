%% trellis:begin %%
# `yield from` 与生成器的 `send`/`throw`/`close`
*迭代器、生成器与上下文管理器*

掌握 `yield from` 如何委托子生成器并透传值与异常、`send()` 让生成器成为经典协程，以及这套机制为何是 async/await 的前身。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/iteration.generators|生成器函数与生成器表达式：惰性、O(1) 内存与一次性]]

**Unlocks:** [[domains/python/map/asyncio.event-loop|事件循环：单线程协作式多任务如何工作]]

## Readings
- [[cpy-generators-internals|生成器对象怎么把一次函数调用变成可以反复挂起的执行]]
- [[effective-06-comprehensions-generators|Effective Python 3e · 第 6 章 推导式与生成器]]
- [[fluent-17-iterators-generators-coroutines|Fluent Python 2e · 第 17 章 迭代器、生成器与经典协程]]
- [[peps-pep342-enhanced-generators|PEP 342：用增强生成器实现协程]]
- [[peps-pep380-yield-from|PEP 380：yield from 委托子生成器语法]]
- [[peps-pep492-async-await|PEP 492：async/await 语法与原生协程]]

## Cards (6)
1. [[await-reuses-yield-from-suspension-chain]]
2. [[for-loop-delegation-leaks-close-chain]]
3. [[generator-close-injects-generatorexit]]
4. [[send-nonnone-on-fresh-generator-typeerror]]
5. [[yield-from-delegates-send-throw-close]]
6. [[yield-from-result-is-stopiteration-value]]
%% trellis:end %%

## Notes
