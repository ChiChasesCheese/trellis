%% trellis:begin %%
# 可迭代对象与迭代器：`__iter__`、`__next__`、`StopIteration`
*迭代器、生成器与上下文管理器*

区分 iterable（能产生迭代器）与 iterator（有状态、一次性），理解 `for` 循环的展开方式，以及为什么迭代器耗尽后要重新获取。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.dunder-protocols|特殊方法与语言协议：`__repr__`、`__len__`、`__getitem__`、`__call__`]]

**Unlocks:** [[domains/python/map/iteration.generators|生成器函数与生成器表达式：惰性、O(1) 内存与一次性]]

## Readings
- [[effective-03-loops-iterators|Effective Python 3e · 第 3 章 循环与迭代器]]
- [[fluent-17-iterators-generators-coroutines|Fluent Python 2e · 第 17 章 迭代器、生成器与经典协程]]
- [[pydocs-functional-howto|函数式编程 HOWTO]]

## Drills
- [[iteration-stream-a-10gb-log|Drill：用生成器管道统计 10 GB 日志的每小时错误数]]

## Cards (6)
1. [[dict-iter-keys-vs-values-items]]
2. [[for-loop-iter-next-desugar]]
3. [[infinite-iterator-max-min-in-hangs]]
4. [[iterator-exhausted-must-reiter]]
5. [[iterator-protocol-next-stopiteration]]
6. [[unpacking-requires-exact-count]]
%% trellis:end %%

## Notes
