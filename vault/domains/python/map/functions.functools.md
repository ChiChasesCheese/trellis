%% trellis:begin %%
# `functools`：`lru_cache`、`partial`、`singledispatch`、`cached_property`
*函数、闭包与装饰器*

掌握标准库提供的函数工具及其陷阱：`lru_cache` 要求参数可哈希且可能泄漏内存、`partial` 固定参数、`singledispatch` 按第一个参数类型分派。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/functions.decorators|装饰器：`@` 语法糖、`functools.wraps` 与执行时机]]

## Readings
- [[fluent-09-decorators-closures|Fluent Python 2e · 第 9 章 装饰器与闭包]]
- [[pydocs-functional-howto|函数式编程 HOWTO]]
- [[pydocs-functools-module|functools 模块：高阶函数工具箱]]

## Drills
- [[functions-write-retry-decorator-live|Drill：现场写一个 `@retry(times, exceptions, backoff)` 装饰器]]
- [[memory-debug-the-growing-worker|Drill：长驻 worker 的 RSS 每小时涨 200 MB，怎么定位]]

## Cards (6)
1. [[cached-property-vs-property]]
2. [[functools-partial-freezes-args]]
3. [[lru-cache-memory-leak-risk]]
4. [[lru-cache-requires-hashable-args]]
5. [[reduce-vs-for-loop-readability]]
6. [[singledispatch-dispatches-on-first-arg-type]]
%% trellis:end %%

## Notes
