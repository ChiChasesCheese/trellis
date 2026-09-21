%% trellis:begin %%
# 生成器函数与生成器表达式：惰性、O(1) 内存与一次性
*迭代器、生成器与上下文管理器*

理解 `yield` 让函数变成生成器工厂、执行在 `next()` 时才推进、生成器表达式与列表推导的内存差异，以及生成器只能消费一次的坑。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/iteration.iterator-protocol|可迭代对象与迭代器：`__iter__`、`__next__`、`StopIteration`]]

**Unlocks:** [[domains/python/map/iteration.yield-from|`yield from` 与生成器的 `send`/`throw`/`close`]], [[domains/python/map/iteration.itertools|`itertools` 与迭代器组合：`chain`、`groupby`、`islice`、`accumulate`]], [[domains/python/map/iteration.context-managers|上下文管理器：`__enter__`/`__exit__`、`contextlib.contextmanager` 与 `ExitStack`]]

## Readings
- [[cpy-generators-internals|生成器对象怎么把一次函数调用变成可以反复挂起的执行]]
- [[effective-06-comprehensions-generators|Effective Python 3e · 第 6 章 推导式与生成器]]
- [[fluent-17-iterators-generators-coroutines|Fluent Python 2e · 第 17 章 迭代器、生成器与经典协程]]
- [[hpp-05-iterators-generators|High Performance Python 2e · 第 5 章 迭代器与生成器]]
- [[pydocs-functional-howto|函数式编程 HOWTO]]

## Drills
- [[iteration-stream-a-10gb-log|Drill：用生成器管道统计 10 GB 日志的每小时错误数]]

## Cards (6)
1. [[calling-generator-function-does-not-run-body]]
2. [[for-iter-gen-bypasses-dunder-next]]
3. [[generator-is-one-shot-cannot-restart]]
4. [[generator-resumes-in-own-frame-repeatedly]]
5. [[genexp-lazy-vs-listcomp-materialize]]
6. [[yield-value-vs-return-value-extra-state]]
%% trellis:end %%

## Notes
