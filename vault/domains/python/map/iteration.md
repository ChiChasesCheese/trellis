%% trellis:begin %%
# 迭代器、生成器与上下文管理器

惰性求值是 Python 处理大数据与流的基本手段：迭代协议、生成器函数、`itertools` 组合，以及 `with` 语句保证资源释放的机制。

## Topics
- [[domains/python/map/iteration.iterator-protocol|可迭代对象与迭代器：`__iter__`、`__next__`、`StopIteration`]]
- [[domains/python/map/iteration.generators|生成器函数与生成器表达式：惰性、O(1) 内存与一次性]]
- [[domains/python/map/iteration.yield-from|`yield from` 与生成器的 `send`/`throw`/`close`]]
- [[domains/python/map/iteration.itertools|`itertools` 与迭代器组合：`chain`、`groupby`、`islice`、`accumulate`]]
- [[domains/python/map/iteration.context-managers|上下文管理器：`__enter__`/`__exit__`、`contextlib.contextmanager` 与 `ExitStack`]]
- [[domains/python/map/iteration.comprehensions|推导式与 `else` 块：可读性边界与作用域]]
- [[domains/python/map/iteration.pattern-matching|结构化模式匹配：`match`/`case`、捕获、守卫与类模式]]
%% trellis:end %%

## Notes
